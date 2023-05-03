import numpy as np
from noise import pnoise2
import trimesh


def create_perlin_mesh():
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
    return mesh
