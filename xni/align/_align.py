import numpy as np
from scipy.ndimage.interpolation import shift as ndshift

from .correlation import corr1d


def shift(data, pos, lview=None):
    if lview == None:
        map_obj = map(ndshift, data, pos)
    else:
       lview.block = True
       map_obj = lview.map(ndshift, data, pos)

    res = np.array(list(map_obj))

    return res


def align_rot_axis(data, axis=2, data_shift=False, lview=None):
    '''
    data: 3d volume data
    axis: sum axis
    '''
    d = np.sum(data, axis=axis)

    if lview == None:
        map_obj = map(corr1d, d, d[1:])
    else:
        lview.block = True
        map_obj = lview.map(corr1d, d, d[1:])

    res = np.fromiter(map_obj, np.double)
    res = np.insert(np.cumsum(res), 0, 0)

    return res
