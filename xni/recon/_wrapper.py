import numpy as np
from skimage.transform import iradon

from ..util import fromiter

def generate_sinogram(data, index_exp):
    sg = data[ np.index_exp[:] + index_exp + np.index_exp[:] ] # data is always 3d volume
    if len(sg.shape) == 3: # suppose that sg is 2d image or 3d volume
        sg = np.swapaxes(sg, 0, 1)
    return sg

def recon(data, index_exp, method='fbp', _map=map):
    sg = generate_sinogram(data, index_exp)
    if len(sg.shape) == 3:
        mapobj = _map(lambda s: iradon(s.T, circle=True), sg)
        res = fromiter(mapobj)
    else:
        res = iradon(sg.T, circle=True)
    return res
