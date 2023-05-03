import tkinter as tk
from util.app_config import settings

# The application's panels
from views.viewport_panel import Viewport
from views.sidebar_panel import Sidebar


class BaseView(tk.Tk):
    """
    The `BaseView` contains all panels (Viewport, Sidebar, etc...),
    and each panel is defined in a separate file.
    You can add additional files for additional panels/views as needed.

    Additionally, it sets the title and minsize among other things.
    """

    def __init__(self, controller):
        super().__init__()

        # App configurations
        self.title("Terrain Generator")
        self.minsize(settings.get_app_width(), settings.get_app_height())

        # frame to hold all the panels, without it, weird things happen... man
        self.frame = tk.Frame(self)
        self.frame.pack(fill="both", expand=True)
        
        # Panels
        self.sidebar = Sidebar(self.frame, controller)
        self.viewport = Viewport(self.frame, controller)

        self.sidebar.pack(side="left", fill="both", expand=True)
        self.viewport.pack(side="left", fill="both", expand=True)

        # Shortcuts
        self.bind("<KeyPress>", lambda x: self.quit_app(x))

    def quit_app(self, key):
        """Quit the app on "q" keypress"""

        if key.char == "q":
            self.destroy()

