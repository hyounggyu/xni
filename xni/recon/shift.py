import numpy as np
from scipy.ndimage.interpolation import shift


def shift_image(im, dx, dy):
    return shift(im, (dy, dx))

def vertical_align(a, v, start, end, dy_max):
    """
    dy_max: -dy_max <= dy <= dy_max
    """
    corr = np.correlate(a[start-dy_max:end+dy_max], v[start:end])
    dy = np.argmax(corr) - dy_max
    return dy

def vertical_align2(a, v, start, end, dy_max):
    sqsum = [np.sum(np.square(a[start:end] - v[start + i:end + i])) for i in range(-dy_max, dy_max+1)]
    dy = np.argmin(sqsum) - dy_max
    return dy
