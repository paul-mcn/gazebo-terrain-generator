import tkinter as tk
from pcg_gazebo.simulation import create_object, SimulationModel, World
from util.app_config import settings
from trimesh import Scene
from trimesh.transformations import rotation_matrix
import trimesh
from util.mesh_creator import create_perlin_mesh

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
        model = self.create_model()
        world.add_model(model.name, model)

        mesh = create_perlin_mesh()
        world.add_model("plane2", mesh)
        scene = world.create_scene()


        # scene: Scene = model.create_scene()
        # define a rotation matrix around the y-axis
        # theta = 45.0
        # R = rotation_matrix(theta, [0, 1, 0])

        # compute the center of the bounding box of the scene
        # min_coord, max_coord = scene.bounds()
        # center = (min_coord + max_coord) / 2
        # scene.apply_transform(R)

        # Rotate your mesh
        # mesh = scene.rotate([1, 0, 0], angle=45)
        # world.add_include
        # for model in world.models:
        #     print(type(model))
        #     for face in model.mesh.faces:
        #         vertices = model.mesh.vertices[face]
        #         coords = [(v[0], v[1]) for v in vertices]
        #         self.canvas.create_polygon(coords, fill='white', outline='black')
        for mesh in scene.geometry.values():
            vertices = mesh.vertices
            for edge in mesh.edges:
                start = vertices[edge[0]][:2] * scale + 400
                end = vertices[edge[1]][:2] * scale + 400
                self.canvas.create_line(
                    start[0], start[1], end[0], end[1], fill="black"
                )

        # scene.show()
        # self.canvas.create_polygon([150, 34, 432, 234], fill="green", outline="yellow")

    def create_preview_window(self):
        """Creates a preview window of the 3D mesh"""
        # model = self.create_model()
        # scene = model.create_scene()
        world = World(self.model_name)
        scene = world.create_scene()
        scene.show()
