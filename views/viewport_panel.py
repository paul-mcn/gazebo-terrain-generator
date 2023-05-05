import tkinter as tk
from pcg_gazebo.simulation import SimulationModel, World
from util.app_config import settings
from util.mesh_creator import create_perlin_mesh
from pcg_gazebo.parsers.sdf import create_sdf_element, Include
from pathlib import Path

class Viewport(tk.Frame):
    """Displays the 3D render of the mesh"""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.model_name = "generated_world1"
        self.parent = parent
        self.canvas = tk.Canvas(
            self,
            height=settings.get_viewport_height(),
            width=settings.get_viewport_width(),
            highlightthickness=1,
            highlightbackground="grey",
            bg=settings.get_viewport_bg_color(),
        )
        self.canvas.pack(fill="both", expand=True)

        # wait until the widget has been displayed before setting height & width, otherwise incorrect height is calculated
        self.draw_scene()

    def create_model(self):
        """Create 3D mesh"""
        model = SimulationModel(self.model_name)
        # Create box link
        model.add_cuboid_link(
            "box",
            mass=0.1,
            size=[
                self.controller.get_x(),
                self.controller.get_y(),
                self.controller.get_z(),
            ],
            pose=[0, 0, 0, 4, 5, 6],
        )
        # new_polygons = [
        #     [(0, 0, 0), (1, 0, 0), (1, 1, 0)],  # Triangle 1
        #     [(0, 0, 0), (1, 1, 0), (0, 1, 0)]   # Triangle 2
        # ]
        # model.add_geometry(new_polygons)
        return model

    def draw_scene(self, scale=250):
        # Draw the edges of the meshes in the scene on the canvas
        self.canvas.delete("all")
        world = World(self.model_name)
        # model = self.create_model()
        # world.add_model(model.name, model)

        # Create model path for gazebo
        # model_dir = "/home/paul/repos/gazebo-terrain-generator/worlds"

        # Create model folder
        folder_name = "ground_mesh"
        model_name = "model.obj"
        model_path = Path(Path.home(), ".gazebo", "models", folder_name)
        model_path.mkdir(exist_ok=True)

        mesh = create_perlin_mesh()
        mesh.export(f"{model_path}/{model_name}")

        mesh = create_sdf_element("mesh")
        mesh.uri = f"model://{folder_name}/{model_name}" # type: ignore (ignore linting for pyright lsp)

        geometry = create_sdf_element("geometry")
        geometry.mesh = mesh # type: ignore

        collision = create_sdf_element("collision")
        collision.children["geometry"] = geometry # type: ignore

        options = [
{
            ""
                }

                ]
        visual = create_sdf_element("visual")
        if visual:
            visual.children["geometry"] = geometry  
            # print(visual.to_xml_as_str())

        link = create_sdf_element("link")
        if link:
            link.children["collision"] = collision
            link.children["visual"] = visual

        model = create_sdf_element("model")
        if model:
            model.name = "ground_mesh1"  # type: ignore
            model.pose = [0, 0, 0, 0, 0, 0] # type: ignore
            model.static = True # type: ignore
            model.children["link"] = link  

        sdf = create_sdf_element("sdf")
        if sdf:
            sdf.children["model"] = model
            sdf.export_xml(f"{model_path}/model.sdf") # type: ignore

        include = Include()
        include.uri = f"model://{folder_name}"
        world.add_include(include)
        world.to_sdf()
        print(world)
        # world.add_model("model", model)

        world.export_to_file(output_dir="./worlds", filename="generated_world.world")
        # print(world.to_sdf())

        # mesh.export(file_type="sdf")
        
        # world.add_model("plane2", mesh)
        # scene = world.create_scene()

    def create_preview_window(self):
        """Creates a preview window of the 3D mesh"""
        # model = self.create_model()
        # scene = model.create_scene()
        world = World(self.model_name)
        scene = world.create_scene()
        scene.show()
