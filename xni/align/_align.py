import numpy as np
from scipy.ndimage.interpolation import shift as ndshift

from ..._shared import fromiter
from .corr import corr1d


def shift(data, pos, _map=map):
    map_obj = _map(ndshift, data, pos)
    return fromiter(map_obj)


def align_rot_axis(data, axis=2, data_shift=False, lview=None):
    '''
    data: 3d volume data
    axis: sum axis
    '''
    d = np.sum(data, axis=axis)
    map_obj = _map(corr1d, d, d[1:])
    res = np.fromiter(map_obj, np.double)
    res = np.cumsum(res)
    res = np.insert(res, 0, 0)
    return res
