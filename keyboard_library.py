# keyboard_library.py
import board
import digitalio
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
import time

class KeyboardManager:
    def __init__(self):
        self.keyboard = Keyboard()

    def process_key(self, key, layer, key_state):
        if key in layer:
            key_value = layer[key]
            if isinstance(key_value, str):
                # Key is a character
                self.keyboard.press(Keycode[key_value])
                time.sleep(0.1)
                self.keyboard.release_all()
            elif callable(key_value):
                # Key has a custom function (multitap)
                key_value(self.keyboard, key_state)

def handle_multitap_a(keyboard, key_state):
    if key_state == 1:
        # First tap: Send 'a'
        keyboard.press(Keycode.A)
        time.sleep(0.1)
        keyboard.release_all()
    elif key_state == 2:
        # Second tap: Send 'b'
        keyboard.press(Keycode.B)
        time.sleep(0.1)
        keyboard.release_all()

# Add more multitap functions as needed

# Example layers
LAYER_LEFT = {
    0: 'A',
    1: 'B',
    2: 'C',
    3: 'D',
    4: 'E',
    5: 'F',
    # Add more keys as needed
}

LAYER_RIGHT = {
    0: '5',
    1: '6',
    2: '7',
    3: '8',
    4: '9',
    5: '0',
    # Add more keys as needed
}

LAYER_CENTER = {
    0: '!',
    1: '@',
    2: '#',
    3: '$',
    4: '%',
    5: '^',
    # Add more keys as needed
}

# Add more layers as needed

# Initialize KeyboardManager with the default configuration file
keyboard_manager = KeyboardManager()

