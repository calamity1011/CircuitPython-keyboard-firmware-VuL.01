# gui_code.py

import displayio
from adafruit_display_shapes.rect import Rect
from adafruit_display_text.label import Label
from adafruit_displayio_layout.layouts.grid_layout import GridLayout
from adafruit_display_widget_button import Button
import time
from keyboard_library import KeyboardManager

class KeyboardGUI:
    def __init__(self, keyboard_manager):
        self.keyboard_manager = keyboard_manager
        self.grid = self.create_gui()

    def create_gui(self):
        grid = GridLayout(x=0, y=0, width=display.width, height=display.height, cell_size=(80, 40), grid_size=(3, 2))

        left_layout_button = Button(x=0, y=0, width=80, height=40, style=Button.ROUNDRECT, fill_color=0x00FF00, outline_color=0x000000, name="left_layout", label="Left")
        left_layout_button.on_press = self.set_left_layout

        right_layout_button = Button(x=80, y=0, width=80, height=40, style=Button.ROUNDRECT, fill_color=0x00FF00, outline_color=0x000000, name="right_layout", label="Right")
        right_layout_button.on_press = self.set_right_layout

        center_layout_button = Button(x=160, y=0, width=80, height=40, style=Button.ROUNDRECT, fill_color=0x00FF00, outline_color=0x000000, name="center_layout", label="Center")
        center_layout_button.on_press = self.set_center_layout

        grid.add_content(left_layout_button, grid_cell=(0, 0))
        grid.add_content(right_layout_button, grid_cell=(1, 0))
        grid.add_content(center_layout_button, grid_cell=(2, 0))

        return grid

    def set_left_layout(self, button):
        self.keyboard_manager.keyboard_layout = "left"

    def set_right_layout(self, button):
        self.keyboard_manager.keyboard_layout = "right"

    def set_center_layout(self, button):
        self.keyboard_manager.keyboard_layout = "center"

    def update(self):
        display.show(self.grid)
        time.sleep(0.1)
