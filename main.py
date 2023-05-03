from controllers.terrain_generator import TerrainGeneratorController
from models.terrain_generator import TerrainGeneratorModel
from views.base_view import BaseView
import numpy as np
from noise import pnoise2

import pyglet
import trimesh

# from pcg_gazebo.simulation import create_object, SimulationModel, World


def show_3d_model():
    # Define the size and resolution of the plane
    width = 10
    height = 10
    resolution = 50

    # Define the Perlin noise parameters
    scale = 10  # Controls the frequency of the noise
    octaves = 2  # Controls the level of detail in the noise
    persistence = 0.8  # Controls the roughness of the noise

    # Generate the Perlin noise map
    noise_map = np.zeros((resolution, resolution))
    for i in range(resolution):
        for j in range(resolution):
            noise_map[i][j] = pnoise2(
                i / scale, j / scale, octaves=octaves, persistence=persistence
            )

    # Create the grid of vertices
    x = np.linspace(-width / 2, width / 2, resolution)
    y = np.linspace(-height / 2, height / 2, resolution)
    X, Y = np.meshgrid(x, y)
    Z = noise_map.flatten()  # Use the Perlin noise map to displace the vertices
    vertices = np.vstack((X.flatten(), Y.flatten(), Z)).T

    # Create the list of faces
    faces = []
    for i in range(resolution - 1):
        for j in range(resolution - 1):
            p1 = i * resolution + j
            p2 = i * resolution + j + 1
            p3 = (i + 1) * resolution + j + 1
            p4 = (i + 1) * resolution + j
            faces.extend([[p1, p2, p3], [p1, p3, p4]])

    # Create the mesh
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
    mesh.show()


def main():
    # window = pyglet.window.Window(width=800, height=600, caption="Pyglet Window")
    # side_panel = pyglet.layout.SidePanel(width=200, height=600)
    # viewport = pyglet.layout.Viewport(width=600, height=600)
    # layout.add(side_panel)
    # layout.add(viewport)


    window = pyglet.window.Window()
    # pyglet.layout

    # label = pyglet.text.Label("Hello world")
    # model = SimulationModel("box")
    # Create box link
    # model.add_cuboid_link(
    #     "box",
    #     mass=0.1,
    #     size=[1, 1, 1],
    # )
    # scene = model.create_scene()
    # world = World("test")
    # scene: trimesh.Scene = world.create_scene()

    # scene.show()

    # batch = pyglet.graphics.Batch()

    # for mesh in scene.geometry:
    #     vertices = mesh.vertices.reshape((-1,))
    #     indices = mesh.faces.reshape((-1,))
    #     colors = mesh.visual.vertex_colors.reshape((-1,))
    #     pyglet_mesh = batch.add_indexed(
    #         len(vertices) // 3,
    #         pyglet.gl.GL_TRIANGLES,
    #         None,
    #         indices,
    #         ("v3f", vertices),
    #         ("c3B", colors),
    #     )

    @window.event
    def on_draw():
        window.clear()
        # batch.draw()
        # label.draw()

    @window.event
    def on_close():
        pyglet.app.exit()

    pyglet.app.run()
    # Create Model, View, and Controller
    # model = TerrainGeneratorModel()
    # controller = TerrainGeneratorController(model)
    # view = BaseView(controller)
    # controller.set_view(view)
    # view.mainloop()

    # start trimesh app
    # show_3d_model()


if __name__ == "__main__":
    main()
