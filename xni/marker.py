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

FIGURE_WIDTH = 700
FIGURE_HEIGHT = 700
SLIDER_NORMALIZED_END = 50

class MainWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.img = util.img_as_float(data.imread('sample.tif'))
        self.orig_img = self.img.copy()
        self.imax = int(self.img.max()*SLIDER_NORMALIZED_END)/float(SLIDER_NORMALIZED_END) 
        self.imin = int(self.img.min()*SLIDER_NORMALIZED_END)/float(SLIDER_NORMALIZED_END)
        self.scale = 1.
        self.width, self.height = self.img.shape
        self.xstart, self.xend = (0, FIGURE_WIDTH)
        self.ystart, self.yend = (0, FIGURE_HEIGHT)
        self.pressedPosition = (0,0)
        self.initUI()

    def initUI(self):
        self.fig = plt.figure()
        canvas = FigureCanvas(self.fig)
        canvas.setFixedSize(FIGURE_WIDTH, FIGURE_HEIGHT)
        canvas.mpl_connect('button_press_event', self.figOnPress)
        canvas.mpl_connect('button_release_event', self.figOnRelease)
        canvas.mpl_connect('scroll_event', self.figOnScroll)

        iminEdit = QtGui.QLineEdit(str(self.imin))
        imaxEdit = QtGui.QLineEdit(str(self.imax))

        iminSld = QtGui.QSlider(self)
        iminSld.setOrientation(QtCore.Qt.Horizontal)
        iminSld.setRange(0, SLIDER_NORMALIZED_END)
        iminSld.setSliderPosition(int(self.imin*SLIDER_NORMALIZED_END))
        iminSld.valueChanged[int].connect(partial(self.updateIntensity, 'IMIN', iminEdit))

        imaxSld = QtGui.QSlider(self)
        imaxSld.setOrientation(QtCore.Qt.Horizontal)
        imaxSld.setRange(0, SLIDER_NORMALIZED_END)
        imaxSld.setSliderPosition(int(self.imax*SLIDER_NORMALIZED_END))
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

        self.figDraw()

    def updateIntensity(self, tag, widget, value):
        value = value / float(SLIDER_NORMALIZED_END)
        if tag == 'IMAX':
            self.imax = value
        elif tag == 'IMIN':
            self.imin = value
        widget.setText(str(value))
        self.figDraw()

    def updateScale(self):
        self.img = transform.rescale(self.orig_img, self.scale)
        self.figDraw()

    def msgBox(self, msg):
        msgbox = QtGui.QMessageBox()
        msgbox.setText(msg)
        msgbox.exec_()

    def figDraw(self):
        self.fig.figimage(self.img[self.ystart:self.yend,self.xstart:self.xend], cmap=plt.gray(), vmin=self.imin, vmax=self.imax)
        self.fig.canvas.draw()

    def figOnPress(self, event):
        self.pressedPosition = (int(event.x), int(event.y)) # why y is float?

    def figOnRelease(self, event):
        posx, posy = (int(event.x), int(event.y))
        oldposx, oldposy = self.pressedPosition
        dx = oldposx - posx
        dy = oldposy - posy        
        self.xstart = self.xstart + dx
        self.yend = self.yend - dy
        self.figDraw()

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
