import numpy as np

from xni.core.util import fromiter

from .corr import corr1d, corr2d


def valign(data, _map=map):
    '''
    data: 3d volume data (0:2pi, top:bottom, left:right)
    '''
    map_obj = _map(corr2d, data, data[1:])
    res = fromiter(map_obj, dtype=data.dtype)
    res = np.cumsum(res.T[0])
    res = -1.0 * np.insert(res, 0, 0)
    return res


def valign2(data, _map=map):
    '''
    intensity sum
    '''
    d = np.sum(np.abs(data), axis=2) # axis 2 is left-right
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
