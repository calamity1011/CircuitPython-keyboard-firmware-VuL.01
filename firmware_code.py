# firmware_code.py

import board
import digitalio
import displayio
import busio
import terminalio
from adafruit_display_text.label import Label
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.hid import HIDService
from keyboard_library import KeyboardManager, LAYER_LEFT, LAYER_RIGHT, LAYER_CENTER
import time

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
    if layout == "left":
        return LAYER_LEFT
    elif layout == "right":
        return LAYER_RIGHT
    elif layout == "center":
        return LAYER_CENTER

# Load configuration from file
config_data = load_configuration()

# If configuration exists, use it, otherwise use default values
if config_data:
    input_pins = config_data.get("input_pins", [board.D1, board.D2, board.D3, board.D4, board.D5, board.D6])
    output_pins = config_data.get("output_pins", [board.D7, board.D8, board.D9, board.D10, board.D11])
    spi_pins = config_data.get("spi_pins", [board.D12, board.D13, board.D14, board.D15])
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

# Initialize KeyboardManager
keyboard_manager = KeyboardManager()

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
                key_state = 1
                # Handle multitap (if key was pressed before)
                if hasattr(button, "last_state") and button.last_state == 0:
                    key_state = 2
                button.last_state = button.value
                key = i if i in custom_layout else None
                if key:
                    # Process key using KeyboardManager
                    keyboard_manager.process_key(key, custom_layout, key_state)

        # Update and display characters on the SPI display
        display_text = ''.join([str(custom_layout[i]) if i in custom_layout else ' ' for i in range(30)])
        text_area = Label(terminalio.FONT, text=display_text, color=0xFFFFFF)
        display_group.pop()
        display_group.append(text_area)
        board.DISPLAY.refresh_soon()
        board.DISPLAY.wait_for_frame()

    time.sleep(0.1)
