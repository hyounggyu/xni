# -*- coding: utf-8 -*-

from PyQt4 import QtGui

import pyqtgraph as pg

import numpy as np


class ViewWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(ViewWindow, self).__init__(parent)
        self.initUI()

    def initUI(self):
        #centralWidget = QtGui.QWidget(self)
        imv = pg.ImageView()
        img = pg.gaussianFilter(np.random.normal(size=(200, 200)), (5, 5)) * 20 + 100
        img = img[np.newaxis,:,:]
        decay = np.exp(-np.linspace(0,0.3,100))[:,np.newaxis,np.newaxis]
        data = np.random.normal(size=(100, 200, 200))
        data += img * decay
        data += 2

        sig = np.zeros(data.shape[0])
        sig[30:] += np.exp(-np.linspace(1,10, 70))
        sig[40:] += np.exp(-np.linspace(1,10, 60))
        sig[70:] += np.exp(-np.linspace(1,10, 30))

        sig = sig[:,np.newaxis,np.newaxis] * 3
        data[:,50:60,50:60] += sig

        imv.setImage(data, xvals=np.linspace(1., 3., data.shape[0]))

        self.setCentralWidget(imv)
