from IPython.parallel import Client

rc = Client()

import os

import h5py

from scipy.ndimage.interpolation import shift

from skimage.transform import iradon

from ..io.tifffile import *
from ..align import correlation


PATH='/Users/hgkim/Data/workspaces/XrayNanoImaging/ipython/sample'

class Dataset:

    def __init__(self):
        self.hf = h5py.File(os.path.join(PATH,'tm181x400x400.h5'),'r')
        self.origin = self.hf['original'][:]
        # self.hf = h5py.File(os.path.join(PATH,'phantom3d.h5'),'r')
        # self.origin = self.hf['Dataset1'][:]


# shift(im, (dy, dx)
# dy, dx = correlation.ccorr2d(ref, trans)
