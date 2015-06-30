import numpy as np

from .correlation import corr1d


def align_rot_axis(data, axis=1, lview=None):
    '''
    data: 3d volume data
    axis: sum axis
    '''

    d = np.sum(data, axis)
    res = np.zeros(d.shape[0], dtype=np.double)

    res = map(corr1d, d, d[1:])

    return res
