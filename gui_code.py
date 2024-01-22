# gui_code.py

import board
import displayio
import terminalio
from adafruit_display_shapes.rect import Rect
from adafruit_display_text.label import Label
from adafruit_displayio_layout.widgets.button import Button

# Define available pins
input_pins = [board.D1, board.D2, board.D3, board.D4, board.D5, board.D6]
output_pins = [board.D7, board.D8, board.D9, board.D10, board.D11]
spi_pins = [board.D12, board.D13, board.D14, board.D15]

# Define layouts
layouts = ["left", "right", "center"]

# Initialize display
display = board.DISPLAY
display.auto_brightness = True

# Create a group for display elements
group = displayio.Group()

# Create a background rectangle
background = Rect(0, 0, display.width, display.height, fill=0xFFFFFF)
group.append(background)

# Create a title label
label_title = Label(terminalio.FONT, text="Keyboard Configuration", color=0x000000)
label_title.x = (display.width - label_title.bounding_box[2]) // 2
label_title.y = 20
group.append(label_title)

# Create labels and buttons for input pins
label_input = Label(terminalio.FONT, text="Select Input Pins", color=0x000000)
label_input.x = 20
label_input.y = 60
group.append(label_input)

buttons_input = []
for i, pin in enumerate(input_pins):
    button = Button(
        x=20,
        y=100 + i * 40,
        width=140,
        height=30,
        label=f"{pin}",
        style=Button.ROUNDRECT,
        fill_color=0x00FF00,
        label_font=terminalio.FONT,
        label_color=0x000000,
    )
    buttons_input.append(button)
    group.append(button)

# Create labels and buttons for output pins
label_output = Label(terminalio.FONT, text="Select Output Pins", color=0x000000)
label_output.x = 20
label_output.y = 300
group.append(label_output)

buttons_output = []
for i, pin in enumerate(output_pins):
    button = Button(
        x=20,
        y=340 + i * 40,
        width=140,
        height=30,
        label=f"{pin}",
        style=Button.ROUNDRECT,
        fill_color=0xFF0000,
        label_font=terminalio.FONT,
        label_color=0x000000,
    )
    buttons_output.append(button)
    group.append(button)

# Create labels and buttons for SPI pins
label_spi = Label(terminalio.FONT, text="Select SPI Pins", color=0x000000)
label_spi.x = 20
label_spi.y = 540
group.append(label_spi)

buttons_spi = []
for i, pin in enumerate(spi_pins):
    button = Button(
        x=20,
        y=580 + i * 40,
        width=140,
        height=30,
        label=f"{pin}",
        style=Button.ROUNDRECT,
        fill_color=0x0000FF,
        label_font=terminalio.FONT,
        label_color=0x000000,
    )
    buttons_spi.append(button)
    group.append(button)

# Create labels and buttons for layouts
label_layout = Label(terminalio.FONT, text="Select Keyboard Layout", color=0x000000)
label_layout.x = 20
label_layout.y = 780
group.append(label_layout)

buttons_layout = []
for i, layout in enumerate(layouts):
    button = Button(
        x=20,
        y=820 + i * 40,
        width=140,
        height=30,
        label=layout,
        style=Button.ROUNDRECT,
        fill_color=0xFFFF00,
        label_font=terminalio.FONT,
        label_color=0x000000,
    )
    buttons_layout.append(button)
    group.append(button)

# Create a button for saving configuration
button_save = Button(
    x=20,
    y=1000,
    width=140,
    height=30,
    label="Save Configuration",
    style=Button.ROUNDRECT,
    fill_color=0xFFA500,
    label_font=terminalio.FONT,
    label_color=0x000000,
)
group.append(button_save)

# Show the group on the display
display.show(group)

# Wait for button presses to select pins and layout
selected_input_pins = []
selected_output_pins = []
selected_spi_pins = []
selected_layout = None

while not selected_input_pins or not selected_output_pins or not selected_spi_pins or selected_layout is None:
    for i, button in enumerate(buttons_input):
        if button.selected:
            selected_input_pins.append(input_pins[i])

    for i, button in enumerate(buttons_output):
        if button.selected:
            selected_output_pins.append(output_pins[i])

    for i, button in enumerate(buttons_spi):
        if button.selected:
            selected_spi_pins.append(spi_pins[i])

    for i, button in enumerate(buttons_layout):
        if button.selected:
            selected_layout = layouts[i]

    if button_save.selected:
        # Save configuration to file
        config_data = {
            "input_pins": selected_input_pins
