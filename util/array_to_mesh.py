import numpy as np
from pathlib import Path
from PIL import Image
from trimesh import Trimesh, proximity, transformations, visual, smoothing, ray
from trimesh.exchange import load
import copy


def rotate_mesh(mesh, rotation_angle, rotation_axis):
    """Define the rotation angle in radians and the rotation axis (e.g., [0, 1, 0] for y-axis)"""

    # Create a rotation matrix using trimesh's transformations module
    rotation_matrix = transformations.rotation_matrix(rotation_angle, rotation_axis)

    # Apply the rotation matrix to the mesh's vertices
    mesh.vertices = transformations.transform_points(mesh.vertices, rotation_matrix)


def scale_mesh(mesh, factor):
    mesh.vertices *= factor


def translate_mesh(mesh, translation):
    matrix = transformations.translation_matrix(translation)
    mesh.vertices = transformations.transform_points(mesh.vertices, matrix)


def max_angle(points):
    "TODO: FIX"
    # Initialize a variable to store the maximum angle
    max_angle = 0.0

    # Iterate through each point
    num_points = len(points)
    for i in range(num_points):
        # Get the current point and its neighbors
        current_point = points[i]
        next_point = points[(i + 1) % num_points]  # Wrap around to the first point

        # Calculate vectors from the current point to its neighbors
        vector1 = next_point - current_point
        vector2 = points[(i + 2) % num_points] - current_point  # Second neighbor

        # Calculate the dot product and magnitudes of the vectors
        dot_product = np.dot(vector1, vector2)
        magnitude1 = np.linalg.norm(vector1)
        magnitude2 = np.linalg.norm(vector2)

        # Calculate the angle between the vectors using the dot product formula
        angle_rad = np.arccos(dot_product / (magnitude1 * magnitude2))
        angle_deg = np.degrees(angle_rad)

        # Update the maximum angle if needed
        if angle_deg > max_angle:
            max_angle = angle_deg

def create_vertices(noise_map, resolution=50, width=10, height=10):
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
    # max_angle(Z)
    vertices = np.vstack((X.flatten(), Y.flatten(), Z)).T
    # max_angle(vertices)
    return vertices


def create_faces(resolution=50):
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
            # This creates two new faces using the four vertices we calculated
            # aka triangulation
            faces.extend([[p1, p2, p3], [p1, p3, p4]])

    return faces


def create_ground_mesh(
    noise_map, resolution=50, width=10, height=10
):
    """
    Create a trimesh from the vertices and faces
    `noise_map` -- a 2D array of equal dimensions e.g. if rows=10 then columns=10
    `resolution` -- determines the level of detail and complexity of the resulting mesh
    `width` -- width of mesh. (default=10)
    `height` -- height of mesh (default=10)
    `obstacle_count` -- count of obstacles on resulting mesh (default=0)
    """
    vertices = create_vertices(noise_map, resolution, width, height)
    faces = create_faces(resolution)
    terrain_mesh = Trimesh(vertices=vertices, faces=faces)
    smoothing.filter_humphrey(terrain_mesh)

    return terrain_mesh


def displace_mesh(mesh, displacement, scale, rotation_axis, rotation_angle):
    rotate_mesh(mesh, rotation_angle, rotation_axis)
    scale_mesh(mesh, scale)
    translate_mesh(mesh, displacement)


def create_displaced_meshes(
    mesh,
    count,
    x_range,
    y_range,
    scale_range,
    rotation_axis_range,
    rotation_angle_range,
    ground_mesh,
):
    mesh_array = []
    for _ in range(count):
        x_min, x_max = x_range
        x = np.random.uniform(x_min, x_max)
        y_min, y_max = y_range
        y = np.random.uniform(y_min, y_max)
        closest, _, _ = proximity.closest_point(ground_mesh, [np.array([x, y, 0])])
        z = closest[0][2]
        scale_min, scale_max = scale_range
        scale = np.random.uniform(scale_min, scale_max)
        rotation_axis_min, rotation_axis_max = rotation_axis_range
        rotation_axis = np.random.uniform(rotation_axis_min, rotation_axis_max)
        rotation_angle_min, rotation_angle_max = rotation_angle_range
        rotation_angle = np.random.uniform(rotation_angle_min, rotation_angle_max)
        dup_mesh = copy.deepcopy(mesh)
        dup_mesh.metadata["displacement"] = [
            x,
            y,
            z,
        ]  # quick and dirty way to save mesh position for export
        displace_mesh(dup_mesh, [x, y, z], scale, rotation_axis, rotation_angle)
        mesh_array.append(dup_mesh)
    return mesh_array


def create_rock_obstacles(count, x_displacement, y_displacement, ground_mesh):
    """
    loads, generates and randomly displaces rock meshes

    :param count int: number of rock meshes to generate
    :param x_displacement float: amount of space rock mesh can displace
    :param y_displacement float: amount of space rock mesh can displace
    :param ground_mesh Trimesh: mesh that rock obstacles will be projected onto (the z_displacement)
    """
    if count == 0:
        return []

    mesh_path = Path(Path.cwd(), "assets/meshes/rock/meshes/Rock1.dae")
    rock_mesh = load.load(mesh_path, force="mesh")
    rock_mesh.metadata["name"] = "rock"
    texture_path = Path(
        Path.cwd(), "assets/meshes/rock/materials/textures/rock-diffuse.png"
    )
    material = visual.material.SimpleMaterial(image=Image.open(texture_path))
    rock_mesh.visual.material = material
    rotation_angle = [0, np.pi * 2]
    rotation_axis = [[-0.5, -0.5, -0.5], [0.5, 0.5, 0.5]]
    rocks = create_displaced_meshes(
        rock_mesh,
        count,
        x_displacement,
        y_displacement,
        [0.2, 0.3],
        rotation_axis,
        rotation_angle,
        ground_mesh,
    )
    return rocks


def create_tree_obstacles(count, x_displacement, y_displacement, ground_mesh):
    if count == 0:
        return []
    tree_mesh_path = Path(Path.cwd(), "assets/meshes/oak_tree/meshes/oak_tree.dae")
    # leaves_mesh_path = Path(Path.cwd(), "assets/meshes/tree_8/crown8.obj")
    tree_mesh = load.load(tree_mesh_path, force="mesh")
    # leaves_mesh = load.load(leaves_mesh_path, force="mesh")
    tree_mesh.metadata["name"] = "tree"

    texture_path = Path(Path.cwd(), "assets/meshes/tree_8/JA02_Bark01_dif_su.png")
    # Create a material
    texture = visual.TextureVisuals(image=texture_path)
    # trimesh.visual.material.pack # <== look into this more
    tree_mesh.visual.texture = texture

    rotation_angle = [0, np.pi * 2]
    rotation_axis = [[-0.5, -0.5, 1], [1, 1, 1]]

    # Combine the individual box meshes into a single mesh
    return create_displaced_meshes(
        tree_mesh,
        count,
        x_displacement,
        y_displacement,
        [0.2, 0.3],
        rotation_axis,
        rotation_angle,
        ground_mesh,
    )


def create_obstacles(
    rock_count, tree_count, x_displacement, y_displacement, ground_mesh
):
    # box_meshes = []
    # for _ in range(count):
    #     bias = np.array([height, width, 0.2])  # bias in x y or z direction
    #     translation = np.random.rand(3) * bias - bias / 2  # Generate random translation
    #     transform = transformations.translation_matrix(translation)
    #     c = creation.cylinder(radius=0.1, height=np.random.rand(1), transform=transform)
    #     box_meshes.append(c)
    #
    # return box_meshes
    rocks = create_rock_obstacles(
        rock_count, x_displacement, y_displacement, ground_mesh
    )
    trees = create_tree_obstacles(
        tree_count, x_displacement, y_displacement, ground_mesh
    )

    return rocks + trees
