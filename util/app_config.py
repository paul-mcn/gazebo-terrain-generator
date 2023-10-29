# This is a the config file for the app settings.
# This is cleaner as it can just be imported if needed rather than populating the global variable space with uneeded info.
# Also faster than waiting a few ms before calling winfo_height() for information we already know.
# I'm sure there is a better way to do this but im use to js/html/css worflow.


class AppConfig:
    def __init__(self):
        # app/root settings
        self.app_width = 1280
        self.app_height = 720

        # sidebar settings
        self.sidebar_width = int(self.app_width * 0.2)  # make 20% of the app width
        self.sidebar_height = int(self.app_height)

        # viewport settings
        self.viewport_width = int(self.app_width - self.sidebar_width)
        self.viewport_height = int(self.app_height)
        self.viewport_bg_color = "#5c5c5c"

        # color settings
        self.background = "#d9d9d9"
        self.text_enabled = "black"
        self.text_disabed = "#969696"
        
        # yml config
        self.default_yml_config = "Default.yml"

    def get_app_width(self):
        return self.app_width

    def get_app_height(self):
        return self.app_height

    def get_sidebar_width(self):
        return self.sidebar_width

    def get_sidebar_height(self):
        return self.sidebar_height

    def get_viewport_width(self):
        return self.viewport_width

    def get_viewport_height(self):
        return self.viewport_height

    def get_viewport_bg_color(self):
        return self.viewport_bg_color

    def get_default_setting_name(self):
        return self.default_yml_config

    def get_background(self):
        return self.background

    def get_enabled_text_color(self):
        return self.text_enabled

    def get_disabled_text_color(self):
        return self.text_disabed


settings = AppConfig()
