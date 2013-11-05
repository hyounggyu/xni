# -*- coding: utf-8 -*-
"""
    xni.marker
    ~~~~~~~~~~

    :copyright: (c) 2013 by Hyounggyu Kim.
    :license: GPL, see LICENSE for more details.
"""

import sys, os, json
from functools import partial

import numpy as np

import matplotlib
matplotlib.use('Qt4Agg')
matplotlib.rcParams['backend.qt4']='PySide'
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from skimage import data, transform, util

from PySide import QtGui, QtCore

class MainWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.img = util.img_as_float(data.imread('sample.tif'))
        self.orig_img = self.img.copy()
        # is 8 bit or 16 bit?
        self.imax = int(self.img.max()*50)/50. # 0.02 씩 
        self.imin = int(self.img.min()*50)/50. # 0.02 씩
        self.scale = 1.
        self.width, self.height = self.img.shape
        self.xmin = 0
        self.ymax = self.height
        self.pressedPosition = (0,0)
        self.initUI()

    def initUI(self):
        self.fig = plt.figure()
        canvas = FigureCanvas(self.fig)
        canvas.setFixedSize(700,700)
        canvas.mpl_connect('button_press_event', self.figOnPress)
        canvas.mpl_connect('button_release_event', self.figOnRelease)
        canvas.mpl_connect('scroll_event', self.figOnScroll)

        iminEdit = QtGui.QLineEdit(str(self.imin))
        imaxEdit = QtGui.QLineEdit(str(self.imax))

        iminSld = QtGui.QSlider(self)
        iminSld.setOrientation(QtCore.Qt.Horizontal)
        iminSld.setRange(0, 50) # test range
        iminSld.setSliderPosition(int(self.imin*50)) # float to int
        iminSld.valueChanged[int].connect(partial(self.updateIntensity, 'IMIN', iminEdit))

        imaxSld = QtGui.QSlider(self)
        imaxSld.setOrientation(QtCore.Qt.Horizontal)
        imaxSld.setRange(0, 50) # test range
        imaxSld.setSliderPosition(int(self.imax*50)) # float to int
        imaxSld.valueChanged[int].connect(partial(self.updateIntensity, 'IMAX', imaxEdit))

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(iminEdit)
        vbox.addWidget(iminSld)
        vbox.addWidget(imaxEdit)
        vbox.addWidget(imaxSld)

        centralWidget = QtGui.QWidget(self)
        hbox = QtGui.QHBoxLayout(centralWidget)
        hbox.addWidget(canvas)
        hbox.addLayout(vbox)
        self.setCentralWidget(centralWidget)

        self.resize(1000,800)

        self.updateView()

    def updateIntensity(self, tag, widget, value):
        value = value / 50. # test range
        if tag == 'IMAX':
            self.imax = value
        elif tag == 'IMIN':
            self.imin = value
        widget.setText(str(value))
        self.updateView()

    def updateScale(self):
        self.img = transform.rescale(self.orig_img, self.scale)
        updateView()

    def updateView(self):
        self.fig.figimage(self.img[:self.ymax,self.xmin:], cmap=plt.gray(), vmin=self.imin, vmax=self.imax)
        self.fig.canvas.draw()

    def msgBox(self, msg):
        msgbox = QtGui.QMessageBox()
        msgbox.setText(msg)
        msgbox.exec_()

    def figOnPress(self, event):
        self.pressedPosition = (int(event.x), int(event.y)) # why y is float?

    def figOnRelease(self, event):
        posx, posy = (int(event.x), int(event.y))
        oldposx, oldposy = self.pressedPosition
        dx = oldposx - posx
        dy = oldposy - posy        
        self.xmin = self.xmin + dx
        self.ymax = self.ymax - dy
        self.updateView()

    def figOnScroll(self, event):
        pass

class App(QtGui.QApplication):
    def __init__(self, *argv):
        QtGui.QApplication.__init__(self, *argv)
        self.main = MainWindow()
        self.lastWindowClosed.connect(self.bye)
        self.main.show()
        self.main.activateWindow()
        self.main.raise_()

    def bye(self):
        self.exit(0)

if __name__ == '__main__':
    global app
    app = App(sys.argv)
    sys.exit(app.exec_())
