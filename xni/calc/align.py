import numpy as np

from ..calc.corr import corr1d, corr2d
from ..util import fromiter

def valign(data, _map=map):
    '''
    data: 3d volume data (0:2pi, top:bottom, left:right)
    '''
    d = np.sum(data, axis=2) # axis 2 is left-right
    map_obj = _map(corr1d, d, d[1:])
    res = fromiter(map_obj, dtype=data.dtype)
    res = np.cumsum(res)
    res = -1.0 * np.insert(res, 0, 0)
    return res


def rot_center(data):
    '''
    data: 0...2pi
    return
    move position
    '''
    yt, xt = corr2d(data[0], np.fliplr(data[-1]))
    return xt
