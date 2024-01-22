# firmware_code.py
import time
from keyboard_library import KeyboardManager
from keyboard_gui import KeyboardGUI

class KeyboardFirmware:
    def __init__(self):
        self.keyboard_manager = KeyboardManager()
        self.keyboard_gui = KeyboardGUI(self.keyboard_manager)

    def run(self):
        while True:
            # Process keyboard actions based on layout
            self.keyboard_manager.process_key(0, {}, 1)

            # Update GUI
            self.keyboard_gui.update()

            time.sleep(0.1)

# Run the firmware
if __name__ == "__main__":
    firmware = KeyboardFirmware()
    firmware.run()
