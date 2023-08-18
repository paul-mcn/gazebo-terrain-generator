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

    def slider_control(self, frame, label_text, command, min, max, **args):
        """Create a slider with a label"""
        # Create a container to hold the label and slider
        slider_frame = tk.Frame(frame)
        slider_frame.pack(pady=5, padx=10)

        # create label
        label = tk.Label(slider_frame, text=label_text)
        label.pack(padx=(10, 20), side="left")

        # create horizontal slider
        slider = tk.Scale(
            slider_frame,
            from_=min,
            to=max,
            orient=tk.HORIZONTAL,
            command=command,
            **args,
        )
        slider.pack(fill="x")
        return slider

    def procedural_array_to_image(self):
        image_array = self.controller.get_procedural_array()

        if image_array is None:
            return ImageTk.PhotoImage(np.array([]))
        shifted_array = image_array + np.abs(np.min(image_array))
        img = Image.fromarray(shifted_array * 100).resize((300, 300))
        return ImageTk.PhotoImage(img)

    def noise_frame(self, image_array):
        # MUST BE SAVED UNDER "SELF" OTHERWISE PYTHON WILL DELETE IN GARBAGE COLLECTION
        # DONT WORRY, THIS IS WORKING AS INTENDED https://bugs.python.org/issue632323
        self.photo_image = image_array

        # create a label widget with the PhotoImage
        image_label = tk.Label(self, image=self.photo_image, width=300, height=300)
        image_label.pack(padx=20, pady=20)
        return image_label

    def on_value_change(self):
        self.photo_image = self.procedural_array_to_image()
        self.image_label.configure(image=self.photo_image, width=300, height=300)

    def create_inputs(self):
        """Create the main window"""

        slider_frame = tk.Frame(self)
        slider_frame.pack(fill="y", side="left")
        # add buttons and sliders to UI
        width_val = self.slider_control(
            slider_frame, "Width", command=self.controller.set_width, min=1, max=100
        )
        height_val = self.slider_control(
            slider_frame, "Height", command=self.controller.set_height, min=1, max=100
        )
        resolution_val = self.slider_control(
            slider_frame,
            "Resolution",
            command=self.controller.set_resolution,
            min=2,
            max=200,
        )
        scale_val = self.slider_control(
            slider_frame, "Scale", command=self.controller.set_scale, min=1, max=100
        )
        octaves_val = self.slider_control(
            slider_frame, "Octaves", command=self.controller.set_octaves, min=1, max=25
        )
        persistence_val = self.slider_control(
            slider_frame,
            "Persistence",
            command=self.controller.set_persistence,
            min=0,
            max=1,
            resolution=0.1,
        )
        max_angle = self.slider_control(
            slider_frame,
            "Max angle",
            command=self.controller.set_max_angle,
            min=0,
            max=90,
        )
        tree_val = self.slider_control(
            slider_frame,
            "Tree density",
            command=self.controller.set_tree_density,
            min=0,
            max=90,
        )
        total_obstacles = self.slider_control(
            slider_frame,
            "Total obstacles",
            command=self.controller.set_tree_density,
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
        tree_val.set(self.controller.get_tree_density())
        total_obstacles.set(self.controller.get_total_obstacles())

        image_array = self.procedural_array_to_image()
        self.image_label = self.noise_frame(image_array)

        # update procedurally generated image when values change
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
