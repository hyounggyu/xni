import numpy as np

from ..calc.corr import corr1d, corr2d
from ..util import fromiter

def valign(data, _map=map):
    '''
    data: 3d volume data (0:2pi, top:bottom, left:right)
    '''
    map_obj = _map(corr2d, data, data[1:])
    res = fromiter(map_obj, dtype=data.dtype)
    res = np.cumsum(res.T[0])
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
