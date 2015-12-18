import numpy as np
from scipy.ndimage.interpolation import shift as ndshift

from xni.core.util import fromiter, isvector

from .crop import crop_index


def shift2d(data, t=0.0):
    '''
    t: float or sequence
    '''
    ret = None
    if isvector(t):
        map_obj = map(ndshift, data, t)
        ret = fromiter(map_obj)
    else:
        ret = ndshift(data, (0.0, t))

    return ret


def shift3d(data, vt=0.0, ht=0.0, crop=True, _map=map):
    '''
    Shift 2-D all images

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
    ret = fromiter(map_obj)

    if crop:
        return ret[np.index_exp[:]+crop_index(vt)+crop_index(ht)]
    else:
        return ret
