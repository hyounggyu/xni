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
        pw = pg.PlotWidget(name='Plot1')
        pw.plot(np.random.normal(size=100), pen=(255,0,0))

        self.setCentralWidget(pw)
