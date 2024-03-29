from pathlib import Path
import shutil
from pcg_gazebo.parsers.sdf import create_sdf_element
from pcg_gazebo.simulation import World
from models.terrain_generator import TerrainGeneratorModel
from util.sdf_creator import (
    create_grass_sdf,
    create_ground_sdf,
    create_rock_sdf,
    create_tree_sdf,
)
import numpy as np
import yaml
from util.terrain_defaults import settings


def emit_value_change(func):
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        self.generate_procedural_array()
        if self.on_value_change:
            self.on_value_change()
        return result

    return wrapper


class TerrainGeneratorController:
    """docstring for Controller."""

    def __init__(self, model):
        super(TerrainGeneratorController, self).__init__()
        self.model: TerrainGeneratorModel = model
        self.view = None
        self.callback = None
        self.on_value_change = None
        self.load_generator_settings("Default.yml")
        # make sure these dirs exist
        model_path = Path(Path.cwd(), "assets", "setting-presets")
        model_path.mkdir(exist_ok=True)

    @emit_value_change
    def set_width(self, value):
        self.model.set_width(value)

    @emit_value_change
    def set_depth(self, value):
        self.model.set_depth(value)

    @emit_value_change
    def set_height_multiplier(self, value):
        self.model.set_height_multiplier(value)

    @emit_value_change
    def set_noise_type(self, value):
        self.model.set_noise_type(value)

    @emit_value_change
    def set_noise_options(self, options):
        self.model.set_noise_options(options)

    @emit_value_change
    def set_max_angle(self, value):
        self.model.set_max_angle(value)

    @emit_value_change
    def set_tree_density(self, value):
        self.model.set_tree_density(value)

    @emit_value_change
    def set_rock_density(self, value):
        self.model.set_rock_density(value)

    @emit_value_change
    def set_total_obstacles(self, value):
        self.model.set_total_obstacles(value)

    @emit_value_change
    def set_total_grass(self, value):
        self.model.set_total_grass(value)

    @emit_value_change
    def set_resolution(self, value):
        self.model.set_resolution(value)

    @emit_value_change
    def set_scale(self, value):
        self.model.set_scale(value)

    def set_view(self, view):
        self.view = view

    def set_on_value_change(self, callback):
        self.on_value_change = callback

    def get_depth(self):
        return self.model.get_depth()

    def get_width(self):
        return self.model.get_width()

    def get_height_multiplier(self):
        return self.model._height_multiplier

    def get_noise_type(self):
        return self.model._noise_type

    def get_noise_types(self):
        return [
            "Cellular",
            "Cubic",
            "CubicFractal",
            "Perlin",
            "PerlinFractal",
            "Simplex",
            "SimplexFractal",
            "Value",
            "ValueFractal",
            "WhiteNoise",
        ]

    def get_noise_options(self):
        return self.model.get_noise_options()

    def get_noise_option(self, key):
        return self.model.get_noise_option(key)

    def get_noise_dropdown_options(self, key):
        table = {
            "cellular_return_type": [
                "CellValue",
                "Distance",
                "Distance2",
                "Distance2Add",
                "Distance2Sub",
                "Distance2Mul",
                "Distance2Div",
                "NoiseLookup",
                "Distance2Cave",
            ],
            "cellular_distance_function": ["Euclidean", "Manhattan", "Natural"],
            "fractal_type": ["FBM", "RigidMulti", "Billow"],
            "perturb_type": [
                "Gradient",
                "GradientFractal",
                "GradientFractal_Normalise",
                "Gradient_Normalise",
                "NoPerturb",
                "Normalise",
            ],
        }

        return table.get(key)

    def get_resolution(self):
        return self.model.get_resolution()

    def get_scale(self):
        return self.model.get_scale()

    def get_max_angle(self):
        return self.model.get_max_angle()

    def get_total_obstacles(self):
        return self.model.get_total_obstacles()

    def get_total_grass(self):
        return self.model.get_total_grass()

    def get_tree_density(self):
        return self.model.get_tree_density()

    def get_rock_density(self):
        return self.model.get_rock_density()

    def get_procedural_array(self):
        return self.model.get_procedural_array()

    def load_generator_settings(self, filename):
        filepath = filename if ".yml" in filename else f"{filename}.yml"
        try:
            with open(f"./assets/setting-presets/{filepath}", "r") as stream:
                try:
                    yml_settings = yaml.safe_load(stream)
                    # we use get here because the yml setting may not exist
                    # whereas the default setting will always exist
                    get_setting = lambda x: yml_settings.get(x) or settings[x]
                    self.set_depth(get_setting("depth"))
                    self.set_width(get_setting("width"))
                    self.set_height_multiplier(get_setting("height_multiplier"))
                    self.set_resolution(get_setting("resolution"))
                    self.set_scale(get_setting("scale"))
                    self.set_max_angle(get_setting("max_angle"))
                    self.set_noise_type(get_setting("noise_type"))
                    self.set_noise_options(get_setting("noise_options"))
                    self.set_tree_density(get_setting("tree_density"))
                    self.set_rock_density(get_setting("rock_density"))
                    self.set_total_obstacles(get_setting("total_obstacles"))
                except yaml.YAMLError as exc:
                    print("Error: Could not load yml file")
                    print(exc)

        except FileNotFoundError:
            print("file not found error")
            self.save_generator_settings("Default")

    def save_generator_settings(self, filename):
        data = {
            "depth": self.get_depth(),
            "width": self.get_width(),
            "resolution": self.get_resolution(),
            "scale": self.get_scale(),
            "noise_options": self.get_noise_options(),
            "noise_type": self.get_noise_type(),
            "max_angle": self.get_max_angle(),
            "tree_density": self.get_tree_density(),
            "rock_density": self.get_rock_density(),
            "total_obstacles": self.get_total_obstacles(),
        }
        filepath = f"./assets/setting-presets/{filename}.yml"
        with open(filepath, "w") as f:
            yaml.dump(data, f, default_flow_style=False)
            print(f"Saved settings in {filepath}")

    def export_collision_objects(self):
        """
        Collision objects are contained within the repo. They are copied from ./assets/meshes to ~/.gazebo/models
        """
        assets_dir = Path(Path.cwd(), "assets", "meshes")
        model_dir = Path(Path.home(), ".gazebo", "models")
        shutil.copytree(assets_dir, model_dir, dirs_exist_ok=True)

    def export_world(self, custom_name=None):
        noise_type = self.model.get_noise_type().lower().replace(" ", "-")
        model_folder = custom_name or f"{noise_type}_terrain_mesh"
        model_path = Path(Path.home(), ".gazebo", "models", model_folder)
        model_path.mkdir(exist_ok=True)
        ground_mesh = self.model.get_mesh()
        if ground_mesh is None:
            return print("Erorr: mesh does not exist")

        # mesh mush be exported first so the path exists
        ground_mesh.export(f"{model_path}/model.obj")
        # create a link to the exported mesh
        ground_mesh_uri = f"model://{model_folder}/model.obj"
        ground_mesh = create_ground_sdf(
            ground_mesh_uri,
            "ground_mesh",
            [0, 0, 0, 0, 0, 0],
            "Gazebo/Grass",
            [1, 1, 1],
        )
        self.model.update_mesh()
        obstacles = self.model.get_obstacles()
        world = World()
        world = world.to_sdf(with_default_sun=True)
        world.children["model"] = [ground_mesh]
        for i, grass_mesh in enumerate(obstacles):
            x, y, z = grass_mesh.metadata["displacement"]
            model = None
            if grass_mesh.metadata["name"] == "rock":
                roll, pitch, yaw = np.random.rand(3)
                model = create_rock_sdf(
                    "model://rock/meshes/Rock1.dae",
                    [
                        "model://rock/materials/scripts/",
                        "model://rock/materials/textures/",
                    ],
                    f"Rock_{i}",
                    [x, y, z, roll, pitch, yaw],
                    "Rock",
                    [0.2, 0.2, 0.2],
                )
            else:
                # only used for "yaw" so trees rotate on up axis
                model_pose = [x, y, z, 0, 0, np.random.random_sample()]
                model = create_tree_sdf(
                    "model://oak_tree/meshes/oak_tree.dae",
                    [
                        "model://oak_tree/materials/scripts/",
                        "model://oak_tree/materials/textures/",
                    ],
                    f"Tree_{i}",
                    model_pose,
                    ["OakTree/Branch", "OakTree/Bark"],
                    [0.4, 0.4, 0.4],
                )
            world.children["model"].append(model)
        grass = self.model.get_grass()
        for i, grass_mesh in enumerate(grass):
            x, y, z = grass_mesh.metadata["displacement"]
            model_pose = [x, y, z, np.random.random_sample(), 0, 0]
            model = create_grass_sdf(
                "model://grass_blade/meshes/model.dae",
                f"Grass_{i}",
                model_pose,
                "Gazebo/Green",
                [0.1, 0.1, 0.1],
            )
            world.children["model"].append(model)
        sdf = create_sdf_element("sdf")
        sdf.children["world"] = world
        world_name = custom_name or f"{noise_type}_generated_world.world"
        world_name = world_name if ".world" in world_name else f"{world_name}.world"
        sdf.export_xml(f"./worlds/{world_name}")
        print("world exported")

    def preview_mesh(self):
        self.model.preview_mesh()

    def generate_procedural_array(self):
        self.model.generate_procedural_array()
