import numpy as np

from ..util import fromiter


def beam(data, index, _map=map):
    '''
    return normalised data, average
    '''
    if np.prod(data[np.index_exp[:] + index].shape) == 0:
        raise ValueError('Cannot average. array shape')
    # slice_obj must be tuple
    map_obj = map(np.average, data[np.index_exp[:] + index])
    iavg = fromiter(map_obj, dtype=data.dtype) # intensity average of each image
    iavg = iavg - np.average(iavg) # distance from all average

    return iavg


def avg_imgs(imgs):
    if len(imgs.shape) == 3:
        img = np.average(imgs, axis=0)
    elif len(imgs.shape) == 2:
        img = imgs
    else:
        raise TypeError('2d or 3d')
    return img


def norm(data, bg, dk=None, beam_power=None, _map=map):
    map_obj = None
    _bg = avg_imgs(bg)

    if dk is None:
        f = lambda im: im / _bg
    else:
        _dk = avg_imgs(dk)
        f = lambda im: (im - _dk) / (_bg - _dk)

    if beam_power is not None:
        map_obj = _map(np.subtract, data, beam_power)

    map_obj = _map(f, map_obj or data)
    return fromiter(map_obj, dtype=data.dtype)
