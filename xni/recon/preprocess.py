import numpy as np


def normalize(bg, im):
    return np.log(im / bg)
