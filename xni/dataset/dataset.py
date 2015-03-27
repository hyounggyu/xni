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
    origin_data = None
    recon_data = None
    max_slice_num = None

    def __init__(self, filename):
        self.fd = h5py.File(filename,'r')
        self.name = self.fd['/'].attrs['name'].decode() # byte array to string
        self.origin_data = self.fd['original'][:]
        self.max_slice_num = self.origin_data.shape[1]

    def recon(self, start=0, end=0, step=1, block=False):
        # if end >= start:
        #   raise
        # if end == start, it returns empty list
        self.async_result = recon_image.map([self.origin_data[:,i,:].T for i in range(start, end, step)])
        if block is True:
            self.async_result.wait()
        return self.async_result

    def update_recon_result(self):
        self.recon_data = np.array(self.async_result.get())


# shift(im, (dy, dx)
# dy, dx = correlation.ccorr2d(ref, trans)
