import numpy as np


def average(imgs):
    if len(imgs.shape) == 3:
        img = np.average(imgs, axis=0)
    elif len(imgs.shape) == 2:
        img = imgs
    else:
        raise TypeError('2d or 3d')
    return img
