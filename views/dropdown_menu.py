import tkinter as tk


class Dropdown(tk.Frame):
    def __init__(self, parent, default, values, command=lambda: print):
        tk.Frame.__init__(self, parent)

        self.default = default
        self.values = values
        self.command = command

        self.selected_value = tk.StringVar(parent, default)
        self.option_menu = tk.OptionMenu(
            parent,
            self.selected_value,
            *values,
        )
        self.option_menu.pack(fill="x")
        self.selected_value.trace_add(
            "write", callback=lambda *_: self.command(self.selected_value.get())
        )

    def update_options(self, new_options=[]):
        # Clear the existing menu
        self.option_menu["menu"].delete(0, "end")

        # Add the new options to the menu
        for option in new_options:
            self.option_menu["menu"].add_command(
                label=option, command=tk._setit(self.selected_value, option)
            )
    
    def set(self, value):
        print(f"value={value}")
        self.selected_value.set(value)

    def get_value(self):
        return self.selected_value.get()
