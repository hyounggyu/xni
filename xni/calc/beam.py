import numpy as np

from ..util import fromiter

from .corr import corr2d


def power(data, index, _map=map):
    '''
    data:
    index: index_exp. 2d. empty.

    return normalised data
    '''
    # index must be tuple
    if np.prod(data[np.index_exp[:] + index].shape) == 0:
        raise ValueError('Cannot average. array shape')
    map_obj = map(np.average, data[np.index_exp[:] + index])
    iavg = fromiter(map_obj, dtype=data.dtype) # intensity average of each image
    iavg = iavg - np.average(iavg) # distance from all average
    return iavg


def center(data, bg, _map=map):
    if len(bg.shape) == 3:
        _bg = np.average(bg, axis=0)
    elif len(bg.shape) == 2:
        _bg = bg
    else:
        raise TypeError('background should be 2d or 3d array')

    map_obj = _map(lambda im: corr2d(_bg, im), data)
    return fromiter(map_obj, dtype=data.dtype)
