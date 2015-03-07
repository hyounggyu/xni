import os

from IPython.parallel import Client

try:
    rc = Client()
except:
    pass

from PyQt4 import QtGui

import pyqtgraph as pg

import numpy as np

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

    def show(self, parent):
        win = QtGui.QMainWindow(parent)
        imv = pg.ImageView()
        imv.setImage(np.swapaxes(self.origin, 1, 2))
        win.setCentralWidget(imv)
        win.setWindowTitle('pyqtgraph example: ImageView')
        win.show()

# shift(im, (dy, dx)
# dy, dx = correlation.ccorr2d(ref, trans)

# class ViewWindow(QtGui.QMainWindow):
#
#     def __init__(self, parent=None):
#         super(ViewWindow, self).__init__(parent)
#         self.data = Dataset()
#         self.initUI()
#
#     def initUI(self):
#         # centralWidget = QtGui.QWidget(self)
#         imv = pg.ImageView()
#         imv.setImage(np.swapaxes(self.data.origin*10., 1, 2))
#         self.setCentralWidget(imv)
#
#         # win = pg.GraphicsLayoutWidget()
#         # view = win.addViewBox()
#         # view.setAspectLocked(True)
#         # img = pg.ImageItem(border='w')
#         # view.addItem(img)
#         # view.setRange(QtCore.QRectF(0, 0, 600, 600))
#         # img.setImage(np.swapaxes(self.data.origin[0],0,1))
#         # self.setCentralWidget(win)
