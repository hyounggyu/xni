# -*- coding: utf-8 -*-

import sys

from IPython.parallel import Client

try:
    rc = Client()
    lv = rc.load_balanced_view()
except FileNotFoundError:
    sys.exit("Could not find IPython worker processes")


import numpy as np
import h5py

from ..align import correlation


@lv.parallel()
def recon_image(im):
    from skimage.transform import iradon
    return iradon(im, circle=True)


class Dataset:

    name = None
    origin = None
    recon = None
    nslice = None

    def __init__(self, filename):
        self.fd = h5py.File(filename,'r')
        self.name = self.fd['/'].attrs['name'].decode()
        self.origin = self.fd['original'][:]
        self.nslice = self.origin.shape[1]

    def recon_async(self):
        self.result = recon_image.map([self.origin[:,i,:].T for i in range(self.origin.shape[1])])
        return self.result

    def recon_sync(self, slice_number):
        self.result = recon_image.map([self.origin[:,slice_number,:].T])
        self.result.wait()
        self.recon = self.result.get()[0]

    def update(self):
        self.image = np.array(self.result.get())


# shift(im, (dy, dx)
# dy, dx = correlation.ccorr2d(ref, trans)
