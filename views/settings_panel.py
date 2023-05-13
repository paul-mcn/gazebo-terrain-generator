import tkinter as tk
import numpy as np
from controllers.terrain_generator import TerrainGeneratorController
from util.app_config import settings
from PIL import Image, ImageTk


class SettingsPanel(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # add controller
        self.controller: TerrainGeneratorController = controller

        # set sidebar dimensions
        self.config(
            height=settings.get_sidebar_height(), width=settings.get_sidebar_width()
        )

        self.create_inputs()

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

    def procedural_array_to_image(self):
        image_array = self.controller.get_procedural_array()

        if image_array is None:
            return np.array([])
        shifted_array = image_array + np.abs(np.min(image_array))
        img = Image.fromarray(shifted_array * 100).resize((300, 300))
        return ImageTk.PhotoImage(img)

    def noise_frame(self, image_array):
        # create a PIL Image object from the NumPy array
        # image_array = np.random.randint(low=255, size=(100, 100), dtype=np.uint8)

        # MUST BE SAVED UNDER "SELF" OTHERWISE PYTHON WILL DELETE IN GARBAGE COLLECTION
        # DONT WORRY, THIS IS WORKING AS INTENDED https://bugs.python.org/issue632323
        self.photo_image = image_array

        # create a label widget with the PhotoImage
        image_label = tk.Label(self, image=self.photo_image, width=300, height=300)
        image_label.pack(side="right")
        return image_label

    def on_value_change(self):
        self.photo_image = self.procedural_array_to_image()
        self.image_label.configure(image=self.photo_image, width=300, height=300) # pylint: disable=all


    def create_inputs(self):
        """Create the main window"""

        # add buttons and sliders to UI
        width_val = self.slider_control(
            "width", command=self.controller.set_width, min=0, max=100
        )
        height_val = self.slider_control(
            "height", command=self.controller.set_height, min=0, max=100
        )
        resolution_val = self.slider_control(
            "resolution", command=self.controller.set_resolution, min=0, max=200
        )
        scale_val = self.slider_control(
            "scale", command=self.controller.set_scale, min=0, max=100
        )
        octaves_val = self.slider_control(
            "octaves", command=self.controller.set_octaves, min=0, max=100
        )
        persistence_val = self.slider_control(
            "persistence", command=self.controller.set_persistence, min=0, max=1
        )
        max_angle = self.slider_control(
            "Max angle", command=self.controller.set_max_angle, min=0, max=90
        )
        foliage_val = self.slider_control(
            "Foliage density",
            command=self.controller.set_foliage_density,
            min=0,
            max=90,
        )

        # updates value when the slider is adjusted
        width_val.set(self.controller.get_width())
        height_val.set(self.controller.get_height())
        resolution_val.set(self.controller.get_resolution())
        scale_val.set(self.controller.get_scale())
        octaves_val.set(self.controller.get_octaves())
        persistence_val.set(self.controller.get_persistence())
        max_angle.set(self.controller.get_max_angle())
        foliage_val.set(self.controller.get_foliage_density())

        image_array = self.procedural_array_to_image()
        self.image_label = self.noise_frame(image_array)

        
        # update noise image when values are changed
        self.controller.set_on_value_change(self.on_value_change)

        button_frame = tk.Frame(self)
        button_frame.pack()
        # add export functionality
        export_btn = tk.Button(
            button_frame, text="Export mesh", command=self.export_mesh
        )
        export_btn.pack(side="left", pady=10)

        preview_btn = tk.Button(
            button_frame, text="Preview mesh", command=self.preview_mesh
        )
        preview_btn.pack(side="left", pady=10)

    def export_mesh(self):
        self.controller.export_mesh()

    def preview_mesh(self):
        self.controller.preview_mesh()

