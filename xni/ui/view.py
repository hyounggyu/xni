# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

import pyqtgraph as pg

import numpy as np

from ..dataset.dataset import Dataset


class ViewWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(ViewWindow, self).__init__(parent)
        self.data = Dataset()
        self.initUI()

    def initUI(self):
        # centralWidget = QtGui.QWidget(self)
        imv = pg.ImageView()
        imv.setImage(np.swapaxes(self.data.origin*10., 1, 2))
        self.setCentralWidget(imv)

        # win = pg.GraphicsLayoutWidget()
        # view = win.addViewBox()
        # view.setAspectLocked(True)
        # img = pg.ImageItem(border='w')
        # view.addItem(img)
        # view.setRange(QtCore.QRectF(0, 0, 600, 600))
        # img.setImage(np.swapaxes(self.data.origin[0],0,1))
        # self.setCentralWidget(win)
