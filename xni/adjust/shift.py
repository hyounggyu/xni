import numpy as np
from scipy.ndimage.interpolation import shift as ndshift

from ..util import fromiter, isvector, crop_index


def shift_all(data, vt=0.0, ht=0.0, crop=True, _map=map):
    '''
    vt: float or sequence
    ht: float or sequence
    '''
    if not isvector(vt):
        vt_val = vt
        vt = np.empty(data.shape[0], dtype=data.dtype)
        vt.fill(vt_val)

    if not isvector(ht):
        ht_val = ht
        ht = np.empty(data.shape[0], dtype=data.dtype)
        ht.fill(ht_val)

    pos = np.vstack((vt, ht)).T
    map_obj = _map(ndshift, data, pos)
    result = fromiter(map_obj)

    if crop:
        return result[np.index_exp[:]+crop_index(vt)+crop_index(ht)]
    else:
        return result
