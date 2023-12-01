import numpy as np
import pyfastnoisesimd as fns


def custom_noise(
    resolution=48,
    noise_type="Perlin",
    fractal_octaves=2,
    fractal_gain=0.5,
    fractal_lacunarity=2,
    frequency=0.1,
    fractal_type="FBM",
    perturb_type="NoPerturb",
    perturb_amp=1,
    perturb_frequency=0.5,
    perturb_gain=0.5,
    perturb_octaves=3,
    perturb_lacunarity=2.0,
    perturb_normalise_length=1.0,
    cellular_return_type="Distance",
    cellular_distance_function="Euclidean",
    cellular_jitter=0.45,
    cellular_lookup_frequency=0.2,
):
    noise = fns.Noise(0)
    noise.frequency = frequency
    noise.noiseType = fns.NoiseType[noise_type]
    noise.fractal.fractalType = fns.FractalType[fractal_type]
    noise.fractal.octaves = fractal_octaves
    noise.fractal.gain = fractal_gain
    noise.fractal.lacunarity = fractal_lacunarity
    if perturb_type != "NoPerturb":
        noise.perturb.perturbType = fns.PerturbType[perturb_type]
        noise.perturb.octaves = perturb_octaves
        noise.perturb.lacunarity = perturb_lacunarity
        noise.perturb.normaliseLength = perturb_normalise_length
        noise.perturb.frequency = perturb_frequency
        noise.perturb.gain = perturb_gain
        noise.perturb.amp = perturb_amp
    if cellular_return_type != "Distance":
        noise.cell.jitter = cellular_jitter
        noise.cell.distanceFunc = fns.CellularDistanceFunction[
            cellular_distance_function
        ]
        noise.cell.returnType = fns.CellularReturnType[cellular_return_type]
        noise.cell.lookupFrequency = cellular_lookup_frequency
        noise.cell.noiseLookupType = fns.NoiseType[noise_type]

    array = noise.genAsGrid([resolution, resolution, resolution])
    sliced_array = array[:, :, 1]  # we just want the y axis
    offset_array = sliced_array + abs(sliced_array.min())  # remove negative values

    return offset_array
