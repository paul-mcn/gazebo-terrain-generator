import tkinter as tk


class LoadingBar(tk.Frame):
    def __init__(self, parent, label_text):
        tk.Frame.__init__(self, parent)

        # self.default = default
        # Create a container to hold the label and slider
        self.container_frame = tk.Frame(parent)
        self.container_frame.pack(pady=5, padx=10)

        # create label
        self.label = tk.Label(self.container_frame, text=self.format_text(label_text))
        self.label.pack(padx=(10, 20))

    def format_text(self, value):
        if value and len(value) > 0:
            return f"Status: {value}"
        return value

    def set(self, value):
        self.label.config(text=self.format_text(value))
