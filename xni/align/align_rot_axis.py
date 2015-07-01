import numpy as np

from .correlation import corr1d


def align_rot_axis(data, axis=2, lview=None):
    '''
    data: 3d volume data
    axis: sum axis
    '''

    d = np.sum(data, axis=axis)
    map_obj = map(corr1d, d, d[1:])
    res = np.array(list(map_obj))
    res = np.insert(np.cumsum(res), 0, 0)

    return res
