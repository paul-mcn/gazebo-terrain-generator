import tkinter as tk
import numpy as np
from controllers.terrain_generator import TerrainGeneratorController
from util.app_config import settings
from PIL import Image, ImageTk
import glob
import re
import os


class SettingsPanel(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # add controller
        self.controller: TerrainGeneratorController = controller

        # set sidebar dimensions
        self.config(
            height=settings.get_sidebar_height(), width=settings.get_sidebar_width()
        )
        self.slider_frame = tk.Frame(self)
        self.slider_frame.pack(fill="y", side="left")

        self.dropdown = self.create_dropdown(
            self.slider_frame, command=self.on_change_dropdown
        )
        self.inputs = self.create_inputs()
        image_array = self.procedural_array_to_image()
        self.image_label = self.noise_frame(image_array)

        # update procedurally generated image when values change
        self.controller.set_on_value_change(self.on_value_change)
        self.create_buttons()

    def slider_control(self, frame, label_text, command, min, max, **args):
        """Create a slider with a label"""
        # Create a container to hold the label and slider
        container_frame = tk.Frame(frame)
        container_frame.pack(pady=5, padx=10)

        # create label
        label = tk.Label(container_frame, text=label_text)
        label.pack(padx=(10, 20), side="left")

        # create horizontal slider
        slider = tk.Scale(
            container_frame,
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
            return ImageTk.PhotoImage(np.array([]))  # type: ignore
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
        # update image in viewport
        self.photo_image = self.procedural_array_to_image()
        self.image_label.configure(image=self.photo_image, width=300, height=300)

    def center_window(self, window):
        window.update_idletasks()  # Ensure the window has its correct size
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        window_width = window.winfo_width()
        window_height = window.winfo_height()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def create_modal(self, command):
        modal = tk.Toplevel()
        modal.geometry("400x100")
        self.center_window(modal)
        modal.wm_title("Save preset")

        label = tk.Label(modal, text="Preset name:")

        textvariable = tk.StringVar()
        input = tk.Entry(modal, textvariable=textvariable)

        label.pack(padx=5)
        input.pack()

        def on_click():
            input_value = textvariable.get()
            # Define a regular expression pattern for allowed characters in filenames
            allowed_chars_pattern = r"[a-zA-Z0-9_\-\. ]+"

            # Use the regular expression to filter out disallowed characters
            cleaned_value = "".join(re.findall(allowed_chars_pattern, input_value))

            # Update the entry widget with the cleaned value
            input.delete(0, tk.END)
            input.insert(0, cleaned_value)

            command(f"{cleaned_value}.yml")
            modal.destroy()

        btn = tk.Button(modal, text="Okay", command=on_click)
        btn.pack(side="bottom")

    def get_setting_presets(self):
        preset_values = []
        for filepath in glob.glob("./assets/setting-presets/*.yml"):
            filename = os.path.basename(filepath)
            preset_values.append(filename)

        return preset_values

    def update_dropdown(self, selected_value):
        # Get new options from ./assets/setting-presets/*.yml
        new_options = self.get_setting_presets()

        # Clear the existing menu
        self.dropdown["menu"].delete(0, "end")

        # Add the new options to the menu
        for option in new_options:
            self.dropdown["menu"].add_command(
                label=option, command=tk._setit(self.dropdown_selected, option)
            )

        self.dropdown_selected.set(selected_value)

    def create_dropdown(self, root, command):
        preset_values = self.get_setting_presets()

        dropdown_selected_val = tk.StringVar(root, "Default.yml")
        option_menu = tk.OptionMenu(
            root,
            dropdown_selected_val,
            *preset_values,
        )
        dropdown_selected_val.trace_add(
            "write", callback=lambda *_: command(dropdown_selected_val.get())
        )
        option_menu.pack(fill="x")
        self.dropdown_selected = dropdown_selected_val
        return option_menu

    def on_click_save_settings(self):
        def on_submit(filename):
            self.controller.save_generator_settings(filename)
            self.update_dropdown(filename)

        self.create_modal(on_submit)

    def create_buttons(self):
        button_frame = tk.Frame(self)
        button_frame.pack()
        # add export functionality
        export_btn = tk.Button(
            button_frame, text="Export world", command=self.export_world
        )
        export_btn.pack(side="left", pady=10)

        preview_btn = tk.Button(
            button_frame, text="Preview mesh", command=self.preview_mesh
        )
        preview_btn.pack(side="left", pady=10)

        save_btn = tk.Button(
            button_frame,
            text="Save settings",
            command=self.on_click_save_settings,
        )
        save_btn.pack(side="left", pady=10)

        return [export_btn, preview_btn, save_btn]

    def update_input_values(self):
        for input in self.inputs:
            input["widget"].set(input["getter"]())

    def on_change_dropdown(self, value):
        self.controller.load_generator_settings(value)
        self.update_input_values()

    def create_inputs(self):
        """
        Responsible for creating all the ui inputs

        It also creates buttons such as the save/export buttons, however, those arent returned.

        @returns inputs
        """

        terrain_surface_frame = tk.LabelFrame(self.slider_frame, text="Terrain Surface")
        obstacles_frame = tk.LabelFrame(self.slider_frame, text="Obstacles")
        misc_frame = tk.LabelFrame(self.slider_frame, text="Misc")

        terrain_surface_frame.pack(fill="x")
        obstacles_frame.pack(fill="x")
        misc_frame.pack(fill="x")

        input_params = [
            {
                "root": terrain_surface_frame,  # the parent frame
                "label": "Width",
                "command": self.controller.set_width,  # the handler for the input
                "getter": self.controller.get_width,  # the value from the input
                "min": 1,
                "max": 200,
            },
            {
                "root": terrain_surface_frame,
                "label": "Height",
                "command": self.controller.set_height,
                "getter": self.controller.get_height,
                "min": 1,
                "max": 200,
            },
            {
                "root": terrain_surface_frame,
                "label": "Resolution",
                "command": self.controller.set_resolution,
                "getter": self.controller.get_resolution,
                "min": 2,
                "max": 200,
            },
            {
                "root": terrain_surface_frame,
                "label": "Scale",
                "command": self.controller.set_scale,
                "getter": self.controller.get_scale,
                "min": 1,
                "max": 100,
            },
            {
                "root": terrain_surface_frame,
                "label": "Octaves",
                "command": self.controller.set_octaves,
                "getter": self.controller.get_octaves,
                "min": 1,
                "max": 25,
            },
            {
                "root": terrain_surface_frame,
                "label": "Persistence",
                "command": self.controller.set_persistence,
                "getter": self.controller.get_persistence,
                "min": 0,
                "max": 1,
                "resolution": 0.1,
            },
            {
                "root": terrain_surface_frame,
                "label": "Max angle",
                "command": self.controller.set_max_angle,
                "getter": self.controller.get_max_angle,
                "min": 0,
                "max": 90,
            },
            {
                "root": obstacles_frame,
                "label": "Tree density %",
                "command": self.controller.set_tree_density,
                "getter": self.controller.get_tree_density,
                "min": 0,
                "max": 100,
            },
            {
                "root": obstacles_frame,
                "label": "Rock density %",
                "command": self.controller.set_rock_density,
                "getter": self.controller.get_rock_density,
                "min": 0,
                "max": 100,
            },
            {
                "root": obstacles_frame,
                "label": "Total",
                "command": self.controller.set_total_obstacles,
                "getter": self.controller.get_total_obstacles,
                "min": 0,
                "max": 90,
            },
            {
                "root": misc_frame,
                "label": "Grass",
                "command": self.controller.set_total_grass,
                "getter": self.controller.get_total_grass,
                "min": 0,
                "max": 1000,
            },
        ]

        inputs = []
        for input in input_params:
            # add buttons and sliders to UI
            widget = self.slider_control(
                frame=input["root"],
                label_text=input["label"],
                command=input["command"],
                min=input["min"],
                max=input["max"],
                resolution=input.get("resolution") or 1,
            )

            # updates value when the slider is adjusted
            widget.set(input["getter"]())
            input["widget"] = widget
            inputs.append(input)

        return inputs

    def export_world(self):
        self.controller.export_collision_objects()
        self.controller.export_world()

    def preview_mesh(self):
        self.controller.preview_mesh()
