import numpy as np

from ._util import isvector

def absceil(val):
    if np.abs(np.around(val)-val) < np.finfo(type(val)).eps:
        val = np.around(val)
    return np.sign(val)*np.ceil(np.abs(val))


def crop_index(pos):
    if isvector(pos):
        if len(pos.shape) > 1:
            raise TypeError('1d array')
        pos_max = absceil(pos.max())
        pos_min = absceil(pos.min())
    else:
        pos_max = pos_min = absceil(pos)

    if pos_max*pos_min < 0:
        return np.index_exp[pos_max:pos_min]

    if pos_max >= 0:
        return np.index_exp[pos_max:]
    else:
        return np.index_exp[:pos_min]
