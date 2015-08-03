import numpy as np
from scipy.ndimage.interpolation import shift as ndshift

from ..util import fromiter, isvector


def absceil(val):
    if np.abs(np.around(val)-val) < np.finfo(type(val)).eps:
        val = np.around(val)
    return np.sign(val)*np.ceil(np.abs(val))


def crop_index(pos):
    if isvector(pos):
        if len(pos.shape) > 1:
            raise TypeError('1d array')
        pos_max = absceil(max(pos))
        pos_min = absceil(min(pos))
    else:
        pos_max = pos_min = absceil(pos)

    if pos_max*pos_min < 0:
        return np.index_exp[pos_max:pos_min]

    if pos_max >= 0:
        return np.index_exp[pos_max:]
    else:
        return np.index_exp[:pos_min]


def shift2d(data, vt=None, ht=None, crop=True, _map=map):
    '''
    vt: float or sequence
    ht: float or sequence
    '''
    if vt is None and ht is None:
        raise ValueError('At least 1 position value')
    if vt is None:
        vt = 0.0
    if ht is None:
        ht = 0.0

    if type(vt) is type(ht): # vectors or scalars
        pass
    elif isvector(vt): # vt is a vector, ht is a value
        ht_val = ht
        ht = np.empty(vt.shape, dtype=vt.dtype)
        ht.fill(ht_val)
    else: # vt is a value, ht is a vector
        vt_val = vt
        vt = np.empty(ht.shape, dtype=ht.dtype)
        vt.fill(vt_val)

    pos = np.vstack((vt, ht)).T
    map_obj = _map(ndshift, data, pos)
    result = fromiter(map_obj)

    if crop:
        return result[np.index_exp[:]+crop_index(vt)+crop_index(ht)]
    else:
        return result
