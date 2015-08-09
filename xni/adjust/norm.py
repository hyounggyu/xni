import numpy as np
from scipy.ndimage.interpolation import shift as ndshift

from ..calc.image import average
from ..util import fromiter


def norm(data, bg, dk=None, beam_power=None, beam_center=None, _map=map):
    map_obj = None
    _bg = average(bg)

    if dk is not None:
        _dk = average(dk)
        _bg = _bg - _dk
        map_obj = _map(lambda im: np.subtract(im, _dk), map_obj or data)

    if beam_power is not None:
        map_obj = _map(np.subtract, map_obj or data, beam_power)

    if beam_center is not None:
        _norm = lambda im, pos: im / ndshift(_bg, pos, cval=1.0)
        map_obj = _map(_norm, map_obj or data, beam_center)
    else:
        _norm = lambda im: im / _bg
        map_obj = _map(_norm, map_obj or data)

    return fromiter(map_obj, dtype=data.dtype)
