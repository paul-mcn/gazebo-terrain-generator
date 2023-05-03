from tkinter import filedialog

# from matplotlib import pyplot as plt
import os
import numpy as np

from PIL import Image, ImageTk

# import xml.etree.ElementTree as ElementTree
# import xml.dom.minidom as MD
# from xml.etree.ElementTree import Element, Comment
# from xml.dom.minidom import parseString
import xml

class TerrainGeneratorModel():
    """Creates window object for terrain generator"""

    def __init__(self):
        super().__init__()
        # coordinates
        self.x = 1  # width (red)
        self.y = 1  # depth (green)
        self.z = 1  # height (blue)

        self.max_angle = 45
        self.foliage_density = 1

        # set default export path to $HOME
        self.export_path = os.path.expanduser("~")
 
    def set_x(self, value):
        self.x = float(value)

    def set_y(self, value):
        self.y = float(value)

    def set_z(self, value):
        self.z = float(value)

    def set_max_angle(self, value):
        self.max_angle = value

    def set_foliage_density(self, value):
        self.foliage_density = value

    def image_window(self, shape):
        # Add image to label using Array
        img = Image.fromarray(shape)
        img_tk = ImageTk.PhotoImage(img)
        # img_label = tk.Label(self.frame, image=img_tk)
        # return img_label

    def open_file_explorer(self):
        """open file explorer and save file to chosen path"""
        dir = filedialog.askdirectory()
        print(dir)
        # model = self.create_model()
        # model.to_gazebo_model(dir)


