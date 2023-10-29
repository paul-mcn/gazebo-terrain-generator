import tkinter as tk
from util.app_config import settings


class SliderControl(tk.Frame):
    def __init__(self, parent, label_text, command, **args):
        tk.Frame.__init__(self, parent)

        # self.default = default
        # Create a container to hold the label and slider
        self.container_frame = tk.Frame(parent)
        self.container_frame.pack(pady=5, padx=10)
        self.command = command

        # create label
        self.label = tk.Label(
            self.container_frame, text=label_text, anchor="w", width=20
        )
        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(
            self.container_frame,
            textvariable=self.entry_var,
            width=5,
        )
        self.entry.bind("<Return>", self.on_entry_change)
        self.entry.bind("<FocusOut>", self.on_entry_change)

        # create horizontal slider
        self.slider = tk.Scale(
            self.container_frame,
            orient=tk.HORIZONTAL,
            command=self.on_slider_change,
            showvalue=False,
            **args,
        )
        self.label.pack(padx=(10, 20), side="left")
        self.entry.pack(padx=(10), side="left")
        self.slider.pack(fill="x", side="left")

    def set(self, value):
        self.slider.set(value)
        self.entry_var.set(value)

    def on_slider_change(self, value):
        self.command(value)
        self.entry_var.set(value)

    def on_entry_change(self, *_):
        self.command(self.entry_var.get())
        self.slider.set(self.entry_var.get())

    def set_enabled(self, should_enable):
        if should_enable:
            self.label.configure(foreground=settings.get_enabled_text_color())
            self.slider.configure(
                foreground=settings.get_enabled_text_color(), state="normal"
            )
            self.entry.configure(
                foreground=settings.get_enabled_text_color(), state="normal"
            )
        else:
            self.label.configure(foreground=settings.get_disabled_text_color())
            self.slider.configure(
                foreground=settings.get_disabled_text_color(), state="disabled"
            )
            self.entry.configure(
                foreground=settings.get_disabled_text_color(), state="disabled"
            )
