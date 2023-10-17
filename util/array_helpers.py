import numpy as np

def normalise_array(array):
    min = np.min(array)
    return (array - min) / (np.max(array) - min)
