# from tkinter import filedialog
# import os
from pcg_gazebo.simulation import World
from util.noise_generators import custom_noise
from util.generate_mesh import create_grass, create_ground_mesh, create_obstacles
import numpy as np
from trimesh import scene


class TerrainGeneratorModel:
    """Creates window object for terrain generator"""

    def __init__(self):
        super().__init__()
        # settings for mesh
        self._width = 10
        self._height = 10
        self._z = 10  # not currently used
        self._resolution = 48
        self._scale = 10
        self._max_angle = 90
        self._tree_density = 1
        self._rock_density = 1
        self._total_obstacles = 1
        self._mesh_rgba = np.array([0, 128, 0, 1])  # the color the mesh will be
        self._obstacle_items = []
        self._total_grass = 100
        self._grass_items = []
        self._noise_type = "Perlin"
        self._noise_options = {
            "fractal_octaves": 2,
            "fractal_gain": 0.5,
            "fractal_lacunarity": 2,
            "frequency": 0.1,
            "fractal_type": "FBM",
            "perturb_type": "NoPerturb",
            "perturb_amp": 1,
            "perturb_frequency": 0.5,
            "perturb_gain": 0.5,
            "perturb_octaves": 3,
            "perturb_lacunarity": 2.0,
            "perturb_normalise_length": 1.0,
            "cellular_return_type": "Distance",
            "cellular_distance_function": "Euclidean",
            "cellular_jitter": 0.45,
            "cellular_lookup_frequency": 0.2,
        }

        # Numpy procedural array
        self._procedural_array = None
        self.generate_procedural_array()

        # Mesh
        self._mesh = None
        self._generate_mesh()
        self._world = World("world1")

    def set_width(self, value):
        self._width = max(int(value), 1)

    def set_height(self, value):
        self._height = max(int(value), 1)

    def set_z(self, value):
        self._z = int(value)

    def set_noise_type(self, value):
        self._noise_type = str(value)

    def set_noise_options(self, options):
        if type(options) is tuple:
            self._noise_options[options[0]] = options[1]
        elif isinstance(options, dict):
            for option in options.keys():
                var_type = type(self._noise_options[option])
                self._noise_options[option] = var_type(options[option])
        else:
            for option, value in options:
                self._noise_options[option] = value

    def set_resolution(self, value):
        self._resolution = int(value)

    def set_scale(self, value):
        self._scale = int(value)

    def set_max_angle(self, value):
        self._max_angle = int(value)

    def set_tree_density(self, value):
        self._tree_density = float(value)

    def set_rock_density(self, value):
        self._rock_density = float(value)

    def set_total_obstacles(self, value):
        self._total_obstacles = int(value)

    def set_total_grass(self, value):
        self._total_grass = int(value)

    def update_mesh(self):
        self.generate_procedural_array()
        self._generate_mesh()

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    def get_noise_type(self):
        return self._noise_type

    def get_noise_options(self):
        return self._noise_options

    def get_noise_option(self, key):
        return self._noise_options.get(key)

    def get_resolution(self):
        return self._resolution

    def get_scale(self):
        return self._scale

    def get_mesh(self):
        return self._mesh

    def get_world(self):
        return self._world

    def get_max_angle(self):
        return self._max_angle

    def get_tree_density(self):
        return self._tree_density

    def get_rock_density(self):
        return self._rock_density

    def get_total_obstacles(self):
        return self._total_obstacles

    def get_obstacles(self):
        return self._obstacle_items

    def get_total_grass(self):
        return self._total_grass

    def get_grass(self):
        return self._grass_items

    def get_mesh_color(self, normalise=False):
        if normalise:
            # just normalise the red, green and blue channels, not the alpha
            rgb = self._mesh_rgba[:3] / 255
            return np.append(rgb, self._mesh_rgba[-1])
        return self._mesh_rgba

    def get_procedural_array(self):
        return self._procedural_array

    def preview_mesh(self):
        # reset the mesh
        self.update_mesh()
        if self._mesh:
            world = scene.scene.Scene(self._mesh)
            for geo in self._obstacle_items:
                world.add_geometry(geo)
            for geo in self._grass_items:
                world.add_geometry(geo)
            world.show()

    def generate_procedural_array(self):
        self._procedural_array = custom_noise(
            resolution=self._resolution,
            noise_type=self._noise_type,
            **self._noise_options
        )

    def get_obstacle_count(self):
        """
        Returns the count of obstacles based on obstacle type
        @returns [rock_count, tree_count]
        """
        normalised_percentage = self._rock_density + self._tree_density
        if normalised_percentage == 0:
            return [0, 0]
        rock_count = np.rint(
            self._total_obstacles * self._rock_density / normalised_percentage
        ).astype(int)
        tree_count = np.rint(
            self._total_obstacles * self._tree_density / normalised_percentage
        ).astype(int)
        return [rock_count, tree_count]

    def _generate_mesh(self):
        """
        Generates a trimesh using a noise_map, width, height and resolution.
        `self._generate_procedural_array` needs to be called first.
        """
        mesh = create_ground_mesh(
            noise_map=self._procedural_array,
            resolution=self._resolution,
            width=self._width,
            height=self._height,
            max_angle=self._max_angle,
        )
        self._mesh = mesh
        if self._total_obstacles > 0:
            rock_count, tree_count = self.get_obstacle_count()
            # center displacement
            x_displacement = [-self._width // 2, self._width // 2]
            y_displacement = [-self._height // 2, self._height // 2]
            self._obstacle_items = create_obstacles(
                rock_count, tree_count, x_displacement, y_displacement, mesh
            )
            self._grass_items = create_grass(
                self._total_grass, x_displacement, y_displacement, mesh
            )

    # TODO: implement custom paths
    # def open_file_explorer(self):
    #     """open file explorer and save file to chosen path"""
    #     dir = filedialog.askdirectory()
    #     print(dir)
    # model = self.create_model()
    # model.to_gazebo_model(dir)
