import numpy as np

from ._util import isvector

def absceil(val):
    if np.abs(np.around(val)-val) < np.finfo(type(val)).eps:
        val = np.around(val)
    return np.sign(val)*np.ceil(np.abs(val))


def crop_index(pos):
    '''
    pos: value or values
    '''
    if isvector(pos):
        pos_max = absceil(max(pos))
        pos_min = absceil(min(pos))
    else:
        pos_max = pos_min = absceil(pos)

    if pos_max*pos_min < 0: # pos_max > 0 and pos_min < 0
        return np.index_exp[pos_max:pos_min]

    if pos_max >= 0: # pos_max >= 0 and pos_min >= 0
        return np.index_exp[pos_max:]
    else: # pos_max < 0 and pos_min < 0
        return np.index_exp[:pos_min]
