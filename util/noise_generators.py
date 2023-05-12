import numpy as np
from noise import pnoise2


def perlin_noise(resolution=50, scale=10, octaves=2, persistence=0.8):
    """
    Creates a Perlin noise numpy array
    `resolution` -- resolution of mesh (default=50)
    `scale` -- Controls the frequency of the noise (default=10)
    `octaves` -- Controls the level of detail in the noise (default=2)
    `persistence` -- Controls the roughness of the noise, should be between 0 and 1 (default=0.8)

    returns -- (vertices, faces)
    """

    # Generate the Perlin noise map
    noise_map = np.zeros((resolution, resolution))
    for i in range(resolution):
        for j in range(resolution):
            noise_map[i][j] = pnoise2(
                i / scale, j / scale, octaves=octaves, persistence=persistence
            )

    return noise_map
