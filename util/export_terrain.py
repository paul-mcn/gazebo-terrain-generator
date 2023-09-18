from pcg_gazebo.parsers.sdf import Include
from pcg_gazebo.parsers.sdf_config import Author, Model, SDF, Version
from pathlib import Path

from util.sdf_creator import create_model_sdf_elements, create_sdf_tree


def export_ground_mesh(mesh, mesh_name="ground_mesh1", color=(0.5, 0.5, 0.5, 1)):
    model_name = "model.obj"
    model_path = Path(Path.home(), ".gazebo", "models", mesh_name)
    model_path.mkdir(exist_ok=True)

    if mesh is None:
        return print("Erorr: Could not export as mesh does not exist")

    # mesh mush be exported first so the path exists
    mesh.export(f"{model_path}/{model_name}")
    # create a link to the exported mesh
    uri = f"model://{mesh_name}/{model_name}"
    rgba_color = color
    sdf_elements = create_model_sdf_elements(uri, rgba_color)
    model_sdf = create_sdf_tree(sdf_elements)
    if model_sdf:
        model_sdf.export_xml(f"{model_path}/model.sdf")
        print(f"Successfully exported {model_name} to {model_path}")

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


def export_world(path, ground_mesh_name, world, obstacles=[]):
    """
    1. click on "Export"
    2. export meshes
        - ground mesh
        - tree
        - rocks

    3. export world
        - ref ground mesh
        - ref tree
        - ref rocks

        world:
        <include>
            <uri>model://ground_mesh</uri>
            <pose frame="">0 0 0 0 -0 0</pose>
            <name>ground_mesh</name>
            <static>1</static>
        </include>
        <include>
            <uri>model://ground_plane</uri>
        </include>
        <include>
            <uri>model://sun</uri>
        </include>
    """
    include = Include()
    include.uri = f"model://{ground_mesh_name}"
    world.add_include(include)
    world.to_sdf()

    world_name = "generated_world.world"
    world.export_to_file(output_dir="./worlds", filename=world_name)
    print(
        f"Successfully exported {world_name} to {Path('./worlds').resolve()}\nYou can now safely close the application."
    )
