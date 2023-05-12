import numpy as np
from scipy.spatial import Delaunay
from trimesh import Trimesh

def create_vertices(noise_map, resolution, width=10, height=10):
    """
    create verticies using a noise map
    `noise_map` -- a 2D array of equal dimensions e.g. if rows=10 then columns=10
    `resolution` -- the resolution variable is used in conjunction with the width and height 
    variables to create a regular grid of points using np.meshgrid() function. 
    The total number of vertices in the mesh will be resolution squared.
    `width` -- width of mesh. (default=10)
    `height` -- height of mesh (default=10)
    """
    # Create the grid of vertices
    x = np.linspace(-width / 2, width / 2, resolution)
    y = np.linspace(-height / 2, height / 2, resolution)
    X, Y = np.meshgrid(x, y)
    Z = noise_map.flatten()  # Use the Perlin noise map to displace the vertices
    vertices = np.vstack((X.flatten(), Y.flatten(), Z)).T
    return vertices


def create_faces(resolution):
    """ 
    Creates faces
    `resolution` -- the resolution needed for the mesh
    """
    # Create the list of faces
    faces = []
    # The -1 is used here because we want to create quads (4 vertices per face),
    # and the last row and column of vertices will not be used for creating faces
    for i in range(resolution - 1): 
        # Again, the -1 is used because we want to create quads. 
        for j in range(resolution - 1):
            # This calculates the index of the first vertex of the current quad 
            # using the formula i * resolution + j.
            # Since each row contains resolution vertices, 
            # we multiply i by resolution to get the start index of the current row,
            # and then add j to get the index of the current vertex within that row.
            p1 = i * resolution + j
            p2 = i * resolution + j + 1
            p3 = (i + 1) * resolution + j + 1
            p4 = (i + 1) * resolution + j
            faces.extend([[p1, p2, p3], [p1, p3, p4]])

    return faces

def create_mesh(noise_map, resolution, width, height):
    """
    Create a trimesh from the vertices and faces
    `noise_map` -- a 2D array of equal dimensions e.g. if rows=10 then columns=10
    `resolution` -- determines the level of detail and complexity of the resulting mesh
    `width` -- width of mesh. (default=10)
    `height` -- height of mesh (default=10)
    """
    vertices = create_vertices(noise_map, resolution, width, height)
    faces = create_faces(resolution)

    # Create the mesh
    mesh = Trimesh(vertices=vertices, faces=faces)
    return mesh

