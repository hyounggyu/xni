import numpy as np
from scipy.ndimage.interpolation import shift

from .correlation import corr1d


def align_rot_axis(data, axis=2, data_shift=False, lview=None, block=True):
    '''
    data: 3d volume data
    axis: sum axis
    '''

    d = np.sum(data, axis=axis)
    if lview == None:
        map_obj = map(corr1d, d, d[1:])
    else:
        lview.block = block
        map_obj = lview.map(corr1d, d, d[1:])
    res = np.array(list(map_obj))
    res = np.insert(np.cumsum(res), 0, 0)

    if data_shift:
        shifted = np.zeros(data.shape, data.dtype)
        tmp_img = np.zeros(data.shape[1:], data.dtype)
        for i in range(data.shape[0]):
            shift(data[i], (res[i], 0.0), output=tmp_img)
            shifted[i,:] = tmp_img[:]
        return shifted, res
    else:
        return res
