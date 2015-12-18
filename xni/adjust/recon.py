import numpy as np
from skimage.transform import iradon

from xni.core.util import fromiter

from .shift import shift2d


def recon2d(sinogram, cr=0.0, method='fbp'):
    if cr is not 0.0:
        sg = shift2d(sinogram, t=cr)
    else:
        sg = sinogram
    return iradon(sg.T, circle=True)


def recon3d(sinograms, method='fbp', _map=map):
    mapobj = _map(lambda sg: iradon(sg.T, circle=True), sinograms)
    return fromiter(mapobj)
