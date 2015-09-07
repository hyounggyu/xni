import numpy as np
from scipy.ndimage.interpolation import shift as ndshift

from ..util import fromiter, crop_index


def set_normfunc(bg, dk=None):
    '''
    bg: 2d
    dk: 2d
    '''
    def normfunc(im, bp=None, bc=None):
        '''
        im: 2d image
        bp: beam power value
        bc: beam center
        '''
        _im = im
        _bg = bg
        _dk = dk

        if dk is not None:
            _im = _im - _dk
            _bg = _bg - _dk
        if bp is not None:
            _im = _im - bp
        if bc is not None:
            _bg = ndshift(_bg, bc, mode='constant', cval=1.0)
        res = (_im / _bg)
        return res
    return normfunc


def norm_all(data, bg, dk=None, beam_power=None, beam_center=None, crop=True, _map=map):
    '''
    data: 3d
    bg: 2d
    dk: 2d
    beam_power: sequence of intensity values
    beam_center: sequence of [(yt0, xt0), (yt1, xt1) ...]
    '''
    data.flags.writeable = False
    bg.flags.writeable = False
    if dk is not None:
        dk.flags.writeable = False

    normfunc = set_normfunc(bg, dk=dk)
    bp = [None]*data.shape[0] if beam_power is None else beam_power
    bc = [None]*data.shape[0] if beam_center is None else beam_center
    map_obj = _map(normfunc, data, bp, bc)
    res = fromiter(map_obj, dtype=data.dtype)

    if beam_center is not None and crop:
        return res[np.index_exp[:]+crop_index(bc.T[0])+crop_index(bc.T[1])]
    else:
        return res
