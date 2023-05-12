# from tkinter import filedialog
# import os
from pcg_gazebo.simulation import World
from util.noise_generators import perlin_noise
from util.array_to_mesh import create_mesh


class TerrainGeneratorModel:
    """Creates window object for terrain generator"""

    def __init__(self):
        super().__init__()
        # settings for mesh
        self._width = 10
        self._height = 10
        self._z = 10  # not currently used
        self._resolution = 50
        self._scale = 10
        self._octaves = 2
        self._persistence = 0.8
        self._max_angle = 45  # not currently used
        self._foliage_density = 1  # not currently used

        # Numpy procedural array
        self._procedural_array = None
        self._generate_procedural_array()

        # Mesh
        self._mesh = None
        self._generate_mesh()
        self._world = World("world1")

    def set_width(self, value):
        self._width = int(value)

    def set_height(self, value):
        self._height = int(value)

    def set_z(self, value):
        self._z = int(value)

    def set_resolution(self, value):
        self._resolution = int(value)

    def set_scale(self, value):
        self._scale = int(value)

    def set_octaves(self, value):
        self._octaves = value

    def set_persistence(self, value):
        self._persistence = value

    def set_max_angle(self, value):
        self._max_angle = value

    def set_foliage_density(self, value):
        self._foliage_density = value

    def _update_mesh(self):
        self._generate_procedural_array()
        self._generate_mesh()

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    def get_resolution(self):
        return self._resolution

    def get_scale(self):
        return self._scale

    def get_octaves(self):
        return self._octaves

    def get_persistence(self):
        return self._persistence

    def get_mesh(self):
        return self._mesh

    def get_world(self):
        return self._world

    def get_max_angle(self):
        return self._max_angle

    def get_foliage_density(self):
        return self._foliage_density

    def preview_mesh(self):
        # reset the mesh
        self._generate_mesh()
        if self._mesh:
            self._mesh.show()

    def _generate_procedural_array(self):
        self._procedural_array = perlin_noise(
            resolution=self._resolution,
            scale=self._scale,
            octaves=self._octaves,
            persistence=self._persistence,
        )

    def _generate_mesh(self):
        """
        Generates a trimesh using a noise_map, width, height and resolution.
        `self._generate_procedural_array` needs to be called first.
        """
        mesh = create_mesh(
            noise_map=self._procedural_array,
            width=self._width,
            height=self._height,
            resolution=self._resolution,
        )
        self._mesh = mesh

    # TODO: implement custom paths
    # def open_file_explorer(self):
    #     """open file explorer and save file to chosen path"""
    #     dir = filedialog.askdirectory()
    #     print(dir)
    # model = self.create_model()
    # model.to_gazebo_model(dir)
