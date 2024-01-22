# CircuitPython-keyboard-firmware-VuL.01:
a simple 3 parts keyboard firmware and displayIO GUI for customize the input/output pin, display SPI, and keyboard layout.

# Firmware Code (firmware_code.py)

Configuration Loading:
The firmware can load configuration settings from a file (config.txt) on startup.

Display Setup:
Initializes an SPI display for each keyboard part.

Button and Output Setup:
Sets up digital input buttons and output pins for each keyboard part.

Custom Layouts:
Defines custom keyboard layouts for the left, right, and center parts.

Bluetooth Connectivity:
Initializes Bluetooth and provides an HID service for keyboard emulation.

Dynamic Layout Switching:
The firmware dynamically switches between left, right, and center layouts based on user configuration.

Button Handling:
Monitors button presses on each part and simulates key presses according to the selected layout.

SPI Display Update:
Updates and displays characters on the SPI display based on the key presses.

# GUI Code (gui_code.py)

Pin and Layout Selection:
Provides a GUI for selecting input pins, output pins, SPI pins, and keyboard layout.

Dynamic Pin Selection:
Dynamically displays and allows the user to select pins for input, output, and SPI connections.

Layout Selection:
Allows the user to choose between predefined keyboard layouts for each part.

Configuration Saving:
Enables the user to save the selected configuration to a file (config.txt).

Visual Feedback:
Displays a visual representation of the selected pins and layout on the screen.

# Interaction Between Firmware and GUI:

Configuration File:
The GUI saves the selected configuration to a file (config.txt), which the firmware loads on startup.

Dynamic Adjustment:
The firmware dynamically adjusts its behavior based on the loaded configuration.
The GUI and firmware are separate scripts, promoting modularity and ease of maintenance.

Important Note:
Code Organization:
The firmware and GUI codes are separate and should be run independently. 
The GUI code generates a configuration file (config.txt) that the firmware reads at startup.

# Keyboard_library.py 
 library contains a KeyboardManager class that has a process_key method to handle key processing with layers and multitap support. 
It also includes example multitap functions (handle_multitap_a) and predefined layers (LAYER_LEFT, LAYER_RIGHT, LAYER_CENTER). 
You can customize and extend these layers and multitap functions based on your needs.

Feel free to adapt and modify the code as needed for your specific requirements and hardware configurations.
