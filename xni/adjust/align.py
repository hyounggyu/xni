import numpy as np
from scipy.ndimage.interpolation import shift as ndshift

from ..util import fromiter
from ..calc.corr import corr1d


def shift(data, pos, _map=map):
    map_obj = _map(ndshift, data, pos)
    return fromiter(map_obj)


def rot_axis(data, axis=2, data_shift=False, _map=map):
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
