import tkinter as tk
import numpy as np
from util.app_config import settings
from PIL import Image, ImageTk


class Sidebar(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # add controller
        self.controller = controller

        # set sidebar dimensions
        self.config(height=settings.get_sidebar_height(), width=settings.get_sidebar_width())

        self.create_window()

    def slider_control(self, label_text, command, min, max):
        """Create a slider with a label"""
        # Create a container to hold the label and slider
        frame = tk.Frame(self)
        frame.pack(pady=5, padx=10, fill="x")

        # create label
        label = tk.Label(frame, text=label_text)
        label.pack(side="left", padx=(10, 20))

        # create horizontal slider
        slider = tk.Scale(
            frame, from_=min, to=max, orient=tk.HORIZONTAL, command=command
        )
        slider.pack(side="left", fill="x")
        return slider

    def noise_frame(self):
        # create a PIL Image object from the NumPy array
        image_array = np.random.randint(low=255, size=(100, 100), dtype=np.uint8)

        # MUST BE SAVED UNDER SELF OTHERWISE PYTHON WILL DELETE IN GARBAGE COLLECTION
        # DONT WORRY, THIS IS WORKING AS INTENDED https://bugs.python.org/issue632323
        self.photo_image = ImageTk.PhotoImage(Image.fromarray(image_array))

        # create a label widget with the PhotoImage
        image_label = tk.Label(self, image=self.photo_image, width=100, height=100)
        image_label.pack(side="bottom")

    def create_window(self):
        """Create the main window"""

        # add buttons and sliders to UI
        x_val = self.slider_control("x", command=self.controller.set_x, min=0, max=5)
        y_val = self.slider_control("y", command=self.controller.set_y, min=0, max=5)
        z_val = self.slider_control("z", command=self.controller.set_z, min=0, max=5)

        # updates value when the slider is adjusted
        x_val.set(self.controller.get_x())
        y_val.set(self.controller.get_y())
        z_val.set(self.controller.get_z())


        max_angle = self.slider_control("Max angle", command=self.controller.set_max_angle, min=0, max=90)
        max_angle.set(self.controller.get_max_angle())

        max_angle = self.slider_control("Foliage density", command=self.controller.set_foliage_density, min=0, max=90)
        max_angle.set(self.controller.get_foliage_density())
        # z_val.set(self.controller.get_z())
        # TODO: add export button
        button_frame = tk.Frame(self)
        button_frame.pack()
        # add export functionality
        file_label = tk.Button(
            button_frame, text="Export mesh", # command=self.open_file_explorer
        )
        file_label.pack(side="left", pady=10)
