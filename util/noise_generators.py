import numpy as np
from noise import pnoise2
import pyfastnoisesimd as fns


def perlin_noise(resolution=48, scale=10, octaves=2, persistence=0.8):
    # return perlin_noise_old(resolution, scale, octaves, persistence)
    return perlin_noise_new(resolution, scale, octaves, persistence)


def perlin_noise_old(resolution=48, scale=10, octaves=2, persistence=0.8):
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


def perlin_noise_new(resolution=48, scale=10, octaves=2, frequency=0.1):
    """
    Creates a Perlin noise numpy array
    `resolution` -- resolution of mesh (default=50)
    `scale` -- Controls the frequency of the noise (default=10)
    `octaves` -- Controls the level of detail in the noise (default=2)
    `persistence` -- Controls the roughness of the noise, should be between 0 and 1 (default=0.8)

    returns -- (vertices, faces)
    """

    perlin = fns.Noise(0)
    perlin.frequency = frequency
    perlin.noiseType = fns.NoiseType.Perlin
    perlin.fractal.octaves = octaves
    perlin.fractal.lacunarity = 2.1
    # perlin.
    # perlin.fractal.gain = 0.45
    # perlin.perturb.perturbType = fns.PerturbType.NoPerturb
    array = perlin.genAsGrid([resolution, resolution, resolution])
    return array[:, :, 1]
