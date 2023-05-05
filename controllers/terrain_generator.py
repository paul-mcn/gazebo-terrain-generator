from pathlib import Path
from pcg_gazebo.parsers.sdf_config import Author, Model, SDF, Version

from pcg_gazebo.simulation.link import create_sdf_config_element
from models.terrain_generator import TerrainGeneratorModel
from util.sdf_creator import (
    create_model_sdf_elements,
    create_sdf_tree,
)
from pcg_gazebo.parsers.sdf import Include
from pcg_gazebo.simulation import Link
from util.sdf_creator import create_sdf_tree


class TerrainGeneratorController:
    """docstring for Controller."""

    def __init__(self, model):
        super(TerrainGeneratorController, self).__init__()
        self.model: TerrainGeneratorModel = model
        self.view = None

    def set_width(self, value):
        self.model.set_width(int(value))

    def set_height(self, value):
        self.model.set_height(int(value))

    def set_z(self, value):
        self.model.set_z(int(value))

    def set_max_angle(self, value):
        self.model.set_max_angle(int(value))

    def set_foliage_density(self, value):
        self.model.set_foliage_density(int(value))

    def set_resolution(self, value):
        self.model.set_resolution(int(value))

    def set_scale(self, value):
        self.model.set_scale(int(value))

    def set_octaves(self, value):
        self.model.set_octaves(int(value))

    def set_persistence(self, value):
        self.model.set_persistence(float(value))

    def set_view(self, view):
        self.view = view

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

    def get_foliage_density(self):
        return self.model.get_foliage_density()

    def export_mesh(self, model_folder="ground_mesh", model_name="model.obj"):
        model_path = Path(Path.home(), ".gazebo", "models", model_folder)
        model_path.mkdir(exist_ok=True)

        mesh = self.model.get_mesh()
        if mesh is None:
            return print("Erorr: mesh does not exist")

        mesh.export(f"{model_path}/{model_name}")

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
