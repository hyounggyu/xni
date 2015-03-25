# -*- coding: utf-8 -*-

import sys

from IPython.parallel import Client

try:
    rc = Client()
    lv = rc.load_balanced_view()
except FileNotFoundError:
    sys.exit("Could not find IPython worker processes")

from PyQt4 import QtGui
import pyqtgraph as pg
import numpy as np
import h5py

from .tifffile import *
from ..align import correlation


def swap(im):
    if im.ndim == 2:
        return np.swapaxes(im, 0, 1)
    elif im.ndim == 3:
        return np.swapaxes(im, 1, 2)
    else:
        return None


@lv.parallel()
def recon_image(im):
    from skimage.transform import iradon
    return iradon(im, circle=True)


class Dataset:

    def __init__(self, filename):
        self.fd = h5py.File(filename,'r')
        self.name = self.fd['/'].attrs['name'].decode()
        self.origin = self.fd['original'][:]
        self.image = self.origin

    def recon(self):
        self.result = recon_image.map([self.image[:,i,:].T for i in range(self.image.shape[1])])
        return self.result

    def show(self, parent=None):
        win = QtGui.QMainWindow(parent)
        imv = pg.ImageView()
        imv.setImage(swap(self.image))
        win.setCentralWidget(imv)
        win.setWindowTitle('pyqtgraph example: ImageView')
        win.show()

    def update(self):
        self.image = np.array(self.result.get())

# shift(im, (dy, dx)
# dy, dx = correlation.ccorr2d(ref, trans)
