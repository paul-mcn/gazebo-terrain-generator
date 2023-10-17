import numpy as np
from pathlib import Path
from PIL import Image
from trimesh import Trimesh, proximity, transformations, visual, smoothing
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


def calc_run(x0, x1, y0, y1):
    return np.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)


def test_angle(points, angle_threshold, resolution):
    print("test angle------")
    # Calculate the threshold in radians
    angle_threshold_radians = np.radians(angle_threshold)
    # max_height = 0

    max_angle = float(0)

    # Iterate through each point
    for i in range(len(points) - 1 - resolution):
        x0, y0, z0 = points[i]

        # calculate slope between itself and 3 neighbouring points
        for x, y, z in [
            points[i + 1],
            points[i + resolution],
            points[i + resolution + 1],
        ]:
            run = calc_run(x0, x, y0, y)
            rise = z - z0

            # Calculate the angle of the point in radians
            point_angle = np.arctan(abs(rise) / abs(run))

            # Check if the point and neighbouring point angle is within the threshold
            if abs(point_angle) > angle_threshold_radians:
                angle = np.degrees(point_angle)
                if angle > max_angle:
                    max_angle = angle
                    max_angle_z = abs(run * np.tan(angle_threshold_radians))
                    print(
                        f"max_angle_z={np.round(max_angle_z, 4)}"
                        + f" rise={np.round(abs(rise), 4)}"
                        + f" max_angle={np.round(angle, 4)}"
                        + f" is_rise_greater={abs(rise) > max_angle_z}"
                        + f" x0={np.round(x0, 4)} y0={np.round(y0, 4)} z0={np.round(z0, 4)}"
                        + f" x={np.round(x, 4)} y={np.round(y, 4)} z={np.round(z, 4)}"
                        + f" scale_factor={np.round(max_angle_z + abs(z0), 4)} / {np.round(abs(rise) + abs(z0), 4)}"
                    )

    print("max angle:")
    print(max_angle)


def clamp_angle(points, angle_threshold, resolution):
    # Calculate the threshold in radians
    angle_threshold_radians = np.radians(angle_threshold)

    max_angle = float(0)
    scale_factor = 1

    # Iterate through each point
    for i in range(len(points) - 1 - resolution):
        x0, y0, z0 = points[i]

        # calculate slope between itself and 3 neighbouring points
        for x, y, z in [
            points[i + 1],
            points[i + resolution],
            points[i + resolution + 1],
        ]:
            run = calc_run(x0, x, y0, y)
            rise = z - z0

            # Calculate the angle of the point in radians
            point_angle = np.arctan(abs(rise) / abs(run))

            # Check if the point and neighbouring point angle is within the threshold
            if abs(point_angle) > angle_threshold_radians:
                angle = np.degrees(point_angle)
                if angle > max_angle:
                    max_angle = angle
                    max_angle_z = abs(run * np.tan(angle_threshold_radians))
                    scale_factor = max_angle_z / abs(rise)

    return points * [1, 1, scale_factor]


def create_vertices(noise_map, resolution=48, width=10, height=10):
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


def create_faces(resolution=48):
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


def create_ground_mesh(noise_map, resolution=48, width=10, height=10, max_angle=90):
    """
    Create a trimesh from the vertices and faces
    `noise_map` -- a 2D array of equal dimensions e.g. if rows=10 then columns=10
    `resolution` -- determines the level of detail and complexity of the resulting mesh
    `width` -- width of mesh. (default=10)
    `height` -- height of mesh (default=10)
    `obstacle_count` -- count of obstacles on resulting mesh (default=0)
    """
    vertices = create_vertices(noise_map, resolution, width, height)
    clamped_vertices = clamp_angle(vertices, max_angle, resolution)
    faces = create_faces(resolution)
    terrain_mesh = Trimesh(vertices=clamped_vertices, faces=faces)
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
    rock_mesh.metadata["name"] = "rock"  # type: ignore
    texture_path = Path(
        Path.cwd(), "assets/meshes/rock/materials/textures/rock-diffuse.png"
    )
    material = visual.material.SimpleMaterial(image=Image.open(texture_path))
    rock_mesh.visual.material = material  # type: ignore
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


def create_grass(count, x_displacement, y_displacement, ground_mesh):
    grass_mesh_path = Path(Path.cwd(), "assets/meshes/grass_blade/meshes/model.dae")
    grass_mesh = load.load(grass_mesh_path, force="mesh")
    rotation_axis = [[1, -0.5, 1], [1, 1, 1]]
    return create_displaced_meshes(
        grass_mesh,
        count,
        x_displacement,
        y_displacement,
        [0.05, 0.07],
        rotation_axis,
        rotation_angle_range=[np.pi, np.pi * 2],
        ground_mesh=ground_mesh,
    )


def create_obstacles(
    rock_count, tree_count, x_displacement, y_displacement, ground_mesh
):
    rocks = create_rock_obstacles(
        rock_count, x_displacement, y_displacement, ground_mesh
    )
    trees = create_tree_obstacles(
        tree_count, x_displacement, y_displacement, ground_mesh
    )

    return rocks + trees
