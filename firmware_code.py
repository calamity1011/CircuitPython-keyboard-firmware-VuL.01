# firmware_code.py

import board
import digitalio
import displayio
import busio
import terminalio
from adafruit_display_text.label import Label
import time
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.hid import HIDService
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# Function to load configuration from file
def load_configuration():
    try:
        with open("config.txt", "r") as config_file:
            config_data = eval(config_file.read())
            return config_data
    except FileNotFoundError:
        return None

# Function to initialize display
def setup_display():
    spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
    display_pins = board.D12, board.D13, board.D14, board.D15
    display_group = displayio.Group(max_size=10)
    display = displayio.TileGrid(terminalio.FONT, pixel_shader=terminalio.COLOR, x=0, y=0)
    display_group.append(display)
    board.DISPLAY.show(display_group)
    return display_group, display

# Function to setup buttons
def setup_buttons(button_pins):
    buttons = [digitalio.DigitalInOut(pin) for pin in button_pins]
    for button in buttons:
        button.direction = digitalio.Direction.INPUT
        button.pull = digitalio.Pull.UP
    return buttons

# Function to setup outputs
def setup_outputs(output_pins):
    outputs = [digitalio.DigitalInOut(pin) for pin in output_pins]
    for output in outputs:
        output.direction = digitalio.Direction.OUTPUT
    return outputs

# Function to get custom layout based on configuration
def get_custom_layout(layout):
    # Implement your custom layout logic here
    # Example: Alphanumeric layout for each part
    if layout == "left":
        custom_layout = {
            0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F',
            6: 'G', 7: 'H', 8: 'I', 9: 'J', 10: 'K', 11: 'L',
            12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R',
            18: 'S', 19: 'T', 20: 'U', 21: 'V', 22: 'W', 23: 'X',
            24: 'Y', 25: 'Z', 26: '1', 27: '2', 28: '3', 29: '4',
        }
    elif layout == "right":
        custom_layout = {
            0: '5', 1: '6', 2: '7', 3: '8', 4: '9', 5: '0',
            6: Keycode.ENTER, 7: Keycode.SPACE, 8: Keycode.LEFT_ARROW, 9: Keycode.RIGHT_ARROW,
            10: Keycode.UP_ARROW, 11: Keycode.DOWN_ARROW, 12: Keycode.BACKSPACE, 13: Keycode.TAB,
            14: Keycode.SHIFT, 15: Keycode.CTRL, 16: Keycode.ALT, 17: Keycode.GUI,
            18: Keycode.F1, 19: Keycode.F2, 20: Keycode.F3, 21: Keycode.F4, 22: Keycode.F5,
            23: Keycode.F6, 24: Keycode.F7, 25: Keycode.F8, 26: Keycode.F9, 27: Keycode.F10,
            28: Keycode.F11, 29: Keycode.F12,
        }
    elif layout == "center":
        custom_layout = {
            0: '!', 1: '@', 2: '#', 3: '$', 4: '%', 5: '^',
            6: '&', 7: '*', 8: '(', 9: ')', 10: '_', 11: '+',
            12: '{', 13: '}', 14: '[', 15: ']', 16: '|', 17: '\\',
            18: ':', 19: ';', 20: '"', 21: '\'', 22: '<', 23: '>',
            24: ',', 25: '.', 26: '/', 27: '?', 28: '`', 29: '~',
        }
    return custom_layout

# Load configuration from file
config_data = load_configuration()

# If configuration exists, use it, otherwise use default values
if config_data:
    input_pins = config_data.get("input_pins", [board.D1, board.D2, board.D3, board.D4, board.D5, board.D6])
    output_pins = config_data.get("output_pins", [board.D7, board.D8, board.D9, board.D10, board.D11])
    spi_pins = config_data.get("spi_pins", [board.D12, board.D13, board.D14, board.D15])
# Define keyboard section
    keyboard_layout = config_data.get("layout", "left")
else:
    input_pins = [board.D1, board.D2, board.D3, board.D4, board.D5, board.D6]
    output_pins = [board.D7, board.D8, board.D9, board.D10, board.D11]
    spi_pins = [board.D12, board.D13, board.D14, board.D15]
    keyboard_layout = "left"

# Initialize Bluetooth
ble = BLERadio()
hid = HIDService(ble)
advertisement = ProvideServicesAdvertisement(hid)

# Initialize displays
display_group, display = setup_display()

# Initialize buttons and outputs
buttons = setup_buttons(input_pins)
outputs = setup_outputs(output_pins)

while True:
    # Get custom layout for the specified part
    custom_layout = get_custom_layout(keyboard_layout)

    # Check for Bluetooth connection
    ble.start_advertising(advertisement)
    while not ble.connected:
        pass

    ble.stop_advertising()

    while ble.connected:
        # Check button presses and use custom layout
        for i, button in enumerate(buttons):
            if not button.value:
                key = custom_layout[i] if i in custom_layout else None
                if key:
                    # Simulate key press based on custom layout
                    if isinstance(key, str):
                        Keyboard.press(Keycode[key])
                    else:
                        Keyboard.press(key)
                    time.sleep(0.1)
                    Keyboard.release_all()

        # Update and display characters on the SPI display
        display_text = ''.join([str(custom_layout[i]) if i in custom_layout else ' ' for i in range(30)])
        text_area = Label(terminalio.FONT, text=display_text, color=0xFFFFFF)
        display_group.pop()
        display_group.append(text_area)
        board.DISPLAY.refresh_soon()
        board.DISPLAY.wait_for_frame()

    time.sleep(0.1)
