import time
import tkinter as tk
import numpy as np
from controllers.terrain_generator import TerrainGeneratorController
from util.app_config import settings
from PIL import Image, ImageTk
import glob
import re
import os
import collections

from util.array_helpers import normalise_array
from views.dropdown_menu import Dropdown
from views.slider_control import SliderControl


class SettingsPanel(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # add controller
        self.controller: TerrainGeneratorController = controller

        # set sidebar dimensions
        self.config(
            height=settings.get_sidebar_height(), width=settings.get_sidebar_width()
        )
        self.left_sidebar_frame = tk.Frame(self)
        self.main_frame = tk.Frame(self)
        self.right_sidebar_frame = tk.Frame(self)
        self.left_sidebar_frame.pack(fill="both", side="left")
        self.main_frame.pack(fill="both", side="left", expand=True)
        self.right_sidebar_frame.pack(fill="both", side="left")
        self.inputs = self.create_inputs()
        image_array = self.procedural_array_to_image()
        self.image_label = self.noise_frame(image_array)

        # update procedurally generated image when values change
        self.controller.set_on_value_change(self.on_value_change)
        self.create_buttons()
        self.on_noise_type_change(self.controller.get_noise_type())
        self.on_peturb_type_change(self.controller.get_noise_option("perturb_type"))

    def procedural_array_to_image(self):
        procedural_array = self.controller.get_procedural_array()

        if procedural_array is None:
            return ImageTk.PhotoImage(np.array([]))  # type: ignore
        # make array values range from 0 to 255
        rgb_array = normalise_array(procedural_array) * 255
        img = Image.fromarray(rgb_array).resize((300, 300))
        return ImageTk.PhotoImage(img)

    def noise_frame(self, image_array):
        # MUST BE SAVED UNDER "SELF" OTHERWISE PYTHON WILL DELETE IN GARBAGE COLLECTION
        # DONT WORRY, THIS IS WORKING AS INTENDED https://bugs.python.org/issue632323
        self.photo_image = image_array

        # create a label widget with the PhotoImage
        image_label = tk.Label(
            self.main_frame, image=self.photo_image, width=300, height=300
        )
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

            command(cleaned_value)
            modal.destroy()

        btn = tk.Button(modal, text="Okay", command=on_click)
        btn.pack(side="bottom")

    def get_setting_presets(self):
        preset_values = []
        for filepath in glob.glob("./assets/setting-presets/*.yml"):
            filename = os.path.basename(filepath)
            preset_values.append(filename)

        return preset_values

    def on_click_save_settings(self):
        def on_submit(filename):
            self.controller.save_generator_settings(filename)
            dropdown = self.get_inputs_by_ids("dropdown-presets")["widget"]  # type: ignore
            new_options = self.get_setting_presets()
            dropdown.update_options(new_options)
            dropdown.set(filename)

        self.create_modal(on_submit)

    def create_buttons(self):
        button_frame = tk.Frame(self.main_frame)
        button_frame.pack()
        # add export functionality
        export_btn = tk.Button(
            button_frame, text="Export world", command=self.export_world
        )
        export_btn.pack(side="left", pady=10)

        preview_btn = tk.Button(
            button_frame, text="Preview mesh", command=self.controller.preview_mesh
        )
        preview_btn.pack(side="left", pady=10)

        save_btn = tk.Button(
            button_frame,
            text="Save settings",
            command=self.on_click_save_settings,
        )
        save_btn.pack(side="left", pady=10)

        return [export_btn, preview_btn, save_btn]

    def get_inputs_by_ids(self, ids):
        """
        Get an input using a `str` or multiple using an array of `str`.

        :param ids str or str[]: string or array of strings
        """
        if isinstance(ids, str):
            for input in self.inputs:
                if input.get("id") == ids:
                    return input
        inputs = []
        for input in self.inputs:
            if input.get("id") in ids:
                inputs.append(input)
        return inputs

    def update_input_values(self):
        """
        Updates all of the inputs related to changing the terrain
        """
        for input in self.inputs:
            if input.get("getter"):
                input.get("widget").set(input["getter"]())

    def on_change_load_settings_dropdown(self, value):
        self.controller.load_generator_settings(value)
        self.update_input_values()

    def on_noise_type_change(self, noise_type):
        self.controller.set_noise_type(noise_type)
        noise_pattern = "fractal"
        self.disable_inputs_by_option(
            noise_pattern, re.search(noise_pattern, noise_type, re.IGNORECASE)
        )

    def on_peturb_type_change(self, perturb_type):
        self.controller.set_noise_options(("perturb_type", perturb_type))
        noise_pattern = "perturb"
        self.disable_inputs_by_option(
            noise_pattern, not re.search(noise_pattern, perturb_type, re.IGNORECASE)
        )

    def on_cell_return_type_change(self, cell_return_type):
        self.controller.set_noise_options(("cellular_return_type", cell_return_type))
        # noise_pattern = "cellular"
        # self.disable_inputs_by_option(
        #     noise_pattern, cell_return_type == "Distance"
        # )  # "Distance" is the default setting

    def disable_inputs_by_option(self, noise_pattern, should_enable):
        noise_options = self.controller.get_noise_options()
        fractal_input_ids = []
        # find all the inputs related to the "noise_pattern"
        # for e.g. if noise_pattern == "fractal" => get all the fractal related inputs
        for option in noise_options.keys():
            # if option is fractal and selected dropdown item is fractal
            if re.search(noise_pattern, option, re.IGNORECASE):
                fractal_input_ids.append(option)

        # toggle the text color of inputs based on the dropdown menu's selected item
        for option in self.get_inputs_by_ids(fractal_input_ids) or []:
            option.get("widget").set_enabled(should_enable)

    def create_noise_inputs(self, frame):
        noise_options = self.controller.get_noise_options()
        inputs = []
        for option in noise_options.keys():
            getter = lambda option=option: self.controller.get_noise_option(option)
            command = lambda value, option=option: self.controller.set_noise_options(
                (option, value)
            )
            if isinstance(noise_options[option], (int, float)):
                input = collections.defaultdict(dict)
                input = {
                    "id": option,
                    "getter": getter,
                    "input_creator": SliderControl,
                    "input_args": {
                        "command": command,
                        "parent": frame,
                        "label_text": option.replace("_", " ").capitalize(),
                    },
                }
                if type(noise_options[option]) == int:
                    input["input_args"]["from_"] = 1
                    input["input_args"]["to"] = 10
                elif type(noise_options[option]) == float:
                    input["input_args"]["from_"] = 0.01
                    input["input_args"]["resolution"] = 0.01
                    input["input_args"]["to"] = 3
                inputs.append(input)

            elif type(noise_options[option]) == str:
                noise_option = self.controller.get_noise_option(option)
                dropdown_values = self.controller.get_noise_dropdown_options(option)
                input_commands = {
                    "noise_type": lambda value: self.on_noise_type_change(value),
                    "perturb_type": lambda value: self.on_peturb_type_change(value),
                    "cellular_return_type": lambda value: self.on_cell_return_type_change(
                        value
                    ),
                }

                input = {
                    # "id": noise_option,
                    "getter": getter,
                    "input_creator": Dropdown,
                    "input_args": {
                        "command": input_commands.get(option) or command,
                        "parent": frame,
                        "default": noise_option,
                        "values": dropdown_values,
                    },
                }
                inputs.append(input)

        return inputs

    def create_inputs(self):
        """
        Responsible for creating all the ui inputs

        It also creates buttons such as the save/export buttons, however, those arent returned.

        @returns inputs
        """

        generator_settings_frame = tk.LabelFrame(
            self.left_sidebar_frame, text="Generator Settings"
        )
        terrain_surface_frame = tk.LabelFrame(
            self.left_sidebar_frame, text="Terrain Surface"
        )
        noise_frame = tk.LabelFrame(self.left_sidebar_frame, text="Noise")
        noise_dropdown_frame = tk.Frame(noise_frame)
        noise_input_frame = tk.Frame(noise_frame)
        obstacles_frame = tk.LabelFrame(self.right_sidebar_frame, text="Obstacles")
        misc_frame = tk.LabelFrame(self.right_sidebar_frame, text="Misc")

        generator_settings_frame.pack(fill="x")
        terrain_surface_frame.pack(fill="x")
        noise_frame.pack(fill="x")
        noise_dropdown_frame.pack(fill="x")
        noise_input_frame.pack(fill="x")
        obstacles_frame.pack(fill="x")
        misc_frame.pack(fill="x")

        input_params = [
            {
                "id": "dropdown-presets",
                "input_creator": Dropdown,
                "input_args": {
                    "command": self.on_change_load_settings_dropdown,
                    "parent": generator_settings_frame,
                    "default": "Default.yml",
                    "values": self.get_setting_presets(),
                },
            },
            {
                "getter": self.controller.get_width,  # the value from the input
                "input_creator": SliderControl,
                "input_args": {
                    "command": self.controller.set_width,  # the handler for the input
                    "parent": terrain_surface_frame,  # the parent frame
                    "label_text": "Width (m)",
                    "from_": 1,
                    "to": 200,
                },
            },
            {
                "getter": self.controller.get_depth,
                "input_creator": SliderControl,
                "input_args": {
                    "command": self.controller.set_depth,
                    "parent": terrain_surface_frame,
                    "label_text": "Depth (m)",
                    "from_": 1,
                    "to": 200,
                },
            },
            {
                "getter": self.controller.get_height_multiplier,
                "input_creator": SliderControl,
                "input_args": {
                    "command": self.controller.set_height_multiplier,
                    "parent": terrain_surface_frame,
                    "label_text": "Height multiplier",
                    "from_": 0,
                    "to": 10,
                    "resolution": 0.01,
                },
            },
            {
                "getter": self.controller.get_resolution,
                "input_creator": SliderControl,
                "input_args": {
                    "command": self.controller.set_resolution,
                    "parent": terrain_surface_frame,
                    "label_text": "Resolution",
                    "from_": 4,
                    "to": 200,
                    "resolution": 4,  # Resolution must be a multiple of 4
                },
            },
            {
                "getter": self.controller.get_max_angle,
                "input_creator": SliderControl,
                "input_args": {
                    "command": self.controller.set_max_angle,
                    "parent": terrain_surface_frame,
                    "label_text": "Max angle (degrees)",
                    "from_": 0,
                    "to": 90,
                },
            },
            {
                "id": "dropdown-noise",
                "getter": self.controller.get_noise_type,
                "input_creator": Dropdown,
                "input_args": {
                    "command": self.on_noise_type_change,
                    "parent": noise_dropdown_frame,
                    "default": self.controller.get_noise_type(),
                    "values": self.controller.get_noise_types(),
                },
            },
            # {
            #     "getter": self.controller.get_scale,
            #     "input_creator": SliderControl,
            #     "input_args": {
            #         "command": self.controller.set_scale,
            #         "parent": noise_frame,
            #         "label_text": "Scale",
            #         "from_": 1,
            #         "to": 100,
            #     },
            # },
            {
                "getter": self.controller.get_tree_density,
                "input_creator": SliderControl,
                "input_args": {
                    "command": self.controller.set_tree_density,
                    "parent": obstacles_frame,
                    "label_text": "Tree density %",
                    "from_": 0,
                    "to": 100,
                },
            },
            {
                "getter": self.controller.get_rock_density,
                "input_creator": SliderControl,
                "input_args": {
                    "command": self.controller.set_rock_density,
                    "parent": obstacles_frame,
                    "label_text": "Rock density %",
                    "from_": 0,
                    "to": 100,
                },
            },
            {
                "getter": self.controller.get_total_obstacles,
                "input_creator": SliderControl,
                "input_args": {
                    "command": self.controller.set_total_obstacles,
                    "parent": obstacles_frame,
                    "label_text": "Total",
                    "from_": 0,
                    "to": 90,
                },
            },
            {
                "getter": self.controller.get_total_grass,
                "input_creator": SliderControl,
                "input_args": {
                    "parent": misc_frame,
                    "label_text": "Grass",
                    "command": self.controller.set_total_grass,
                    "from_": 0,
                    "to": 1000,
                },
            },
        ]

        input_params += self.create_noise_inputs(noise_input_frame)

        inputs = []
        for input in input_params:
            # add buttons and sliders to UI
            widget = input["input_creator"](**input["input_args"])
            # updates value when the slider is adjusted
            if input.get("getter"):
                widget.set(input["getter"]())
            input["widget"] = widget
            inputs.append(input)

        return inputs

    def export_world(self):
        self.controller.export_collision_objects()
        self.controller.export_world("noise_rocky")
