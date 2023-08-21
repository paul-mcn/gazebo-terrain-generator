from pathlib import Path
from pcg_gazebo.parsers.sdf_config import Author, Model, SDF, Version

# from pcg_gazebo.simulation.link import create_sdf_config_element
from models.terrain_generator import TerrainGeneratorModel
from util.sdf_creator import (
    create_model_sdf_elements,
    create_sdf_tree,
)
from pcg_gazebo.parsers.sdf import Include
from util.sdf_creator import create_sdf_tree


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

    @emit_value_change
    def set_width(self, value):
        self.model.set_width(value)

    @emit_value_change
    def set_height(self, value):
        self.model.set_height(value)

    @emit_value_change
    def set_z(self, value):
        self.model.set_z(value)

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
    def set_resolution(self, value):
        self.model.set_resolution(value)

    @emit_value_change
    def set_scale(self, value):
        self.model.set_scale(value)

    @emit_value_change
    def set_octaves(self, value):
        self.model.set_octaves(value)

    @emit_value_change
    def set_persistence(self, value):
        self.model.set_persistence(value)

    def set_view(self, view):
        self.view = view

    def set_on_value_change(self, callback):
        self.on_value_change = callback

    def get_height(self):
        return self.model.get_height()

    def get_width(self):
        return self.model.get_width()

    def get_z(self):
        return self.model._z

    def get_resolution(self):
        return self.model.get_resolution()

    def get_scale(self):
        return self.model.get_scale()

    def get_octaves(self):
        return self.model.get_octaves()

    def get_persistence(self):
        return self.model.get_persistence()

    def get_max_angle(self):
        return self.model.get_max_angle()

    def get_total_obstacles(self):
        return self.model.get_total_obstacles()

    def get_tree_density(self):
        return self.model.get_tree_density()

    def get_rock_density(self):
        return self.model.get_rock_density()

    def get_procedural_array(self):
        return self.model.get_procedural_array()

    def export_mesh(self, model_folder="ground_mesh", model_name="model.obj"):
        model_path = Path(Path.home(), ".gazebo", "models", model_folder)
        model_path.mkdir(exist_ok=True)
        
        # TODO: generate collisions for mesh.
        # Maybe the best way to do this is to create a separate trimesh then combine it with the model trimesh on export
        # This is because: for the max_angle function, it must only iterate over the world object, and not the obstacles
        # All collisions height will have to update after the model is udpated
        
        mesh = self.model.get_mesh()
        if mesh is None:
            return print("Erorr: mesh does not exist")

        # mesh mush be exported first so the path exists
        mesh.export(f"{model_path}/{model_name}")
        # create a link to the exported mesh
        uri = f"model://{model_folder}/{model_name}"
        sdf_elements = create_model_sdf_elements(uri)
        model_sdf = create_sdf_tree(sdf_elements)
        if model_sdf:
            model_sdf.export_xml(f"{model_path}/model.sdf")

        author = Author()
        author.email = "me@my.email"
        author.name = "My Name"
        sdf = SDF()
        version = Version()
        version.value = "1.0"
        model = Model()
        model.children["sdf"] = sdf
        model.children["version"] = version
        model.children["auhtor"] = author
        model.export_xml(f"{model_path}/model.config")
        include = Include()
        include.uri = f"model://{model_folder}"
        world = self.model.get_world()
        world.add_include(include)
        world.to_sdf()

        world.export_to_file(output_dir="./worlds", filename="generated_world.world")

    def preview_mesh(self):
        self.model.preview_mesh()

    def generate_procedural_array(self):
        self.model.generate_procedural_array()
