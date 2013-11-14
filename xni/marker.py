# -*- coding: utf-8 -*-
"""
    xni.marker
    ~~~~~~~~~~

    :copyright: (c) 2013 by Hyounggyu Kim.
    :license: GPL, see LICENSE for more details.
"""

import sys
import math
from functools import partial

import numpy as np
from skimage import io, transform, util, exposure

from OpenGL import GL
from PySide import QtGui, QtCore, QtOpenGL

FIGURE_WIDTH = 700
FIGURE_HEIGHT = 700
SLIDER_NORMALIZED_END = 50

class Communicate(QtCore.QObject):

    xmarkerChanged = QtCore.Signal(int)
    ymarkerChanged = QtCore.Signal(int)

class GLWidget(QtOpenGL.QGLWidget):
    def __init__(self, ix, iy, image, parent=None):
        QtOpenGL.QGLWidget.__init__(self, parent)

        self.signal = Communicate()

        self.ix, self.iy, self.image = (ix, iy, image)
        self.normix, self.normiy = (1.0, float(ix)/float(iy))
        self.ortho = 1.0
        self.scale = 1.0
        self.xTrans = 0.0
        self.yTrans = 0.0

        self.lastPos = QtCore.QPoint()

    def setTranslation(self, dx, dy):
        self.xTrans = self.normalizeTranslation(self.normix*self.scale, self.xTrans+dx) # normix to normimwidth
        self.yTrans = self.normalizeTranslation(self.normiy*self.scale, self.yTrans+dy)
        self.updateGL()

    def setScale(self, normx, normy, delta):
        oldscale = self.scale
        newscale = self.scale + delta
        if newscale > 1.0:
            self.xTrans = normx - newscale*(normx-self.xTrans)/oldscale
            self.yTrans = normy - newscale*(normy-self.yTrans)/oldscale
            self.xTrans = self.normalizeTranslation(self.normix*newscale, self.xTrans) # normix to normimwidth
            self.yTrans = self.normalizeTranslation(self.normiy*newscale, self.yTrans)
        else:
            newscale = 1.0
            self.xTrans, self.yTrans = (0, 0)
        self.scale = newscale
        self.updateGL()

    def getImagePosition(self, normx, normy):
    	ix = self.ix * (normx - self.xTrans) / self.scale
    	iy = self.iy * (normy - self.yTrans) / self.scale
    	return ix, iy

    def loadTexture(self, image):
        GL.glTexSubImage2D(GL.GL_TEXTURE_2D, 0, 0, 0, self.ix, self.iy, GL.GL_RGB, GL.GL_UNSIGNED_SHORT, image)
        self.updateGL()

    def initializeGL(self):
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)

        GL.glBindTexture(GL.GL_TEXTURE_2D, GL.glGenTextures(1))
        GL.glPixelStorei(GL.GL_UNPACK_ALIGNMENT, 4) # word-alignment
        GL.glTexParameter(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_REPEAT) # 무슨 뜻?
        GL.glTexParameter(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_REPEAT) # 무슨 뜻?
        GL.glTexParameter(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_NEAREST)
        GL.glTexParameter(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_NEAREST)
        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGB16, self.ix, self.iy, 0, GL.GL_RGB, GL.GL_UNSIGNED_SHORT, self.image)

    def paintGL(self):
        #GL.glClearColor(0.0, 0.0, 1.0, 1.0) # background color
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glLoadIdentity()
        GL.glTranslate(self.xTrans, self.yTrans, 0.0)
        GL.glScale(self.scale, self.scale, 1.0)

        GL.glEnable(GL.GL_BLEND)

        GL.glEnable(GL.GL_TEXTURE_2D)
        GL.glBegin(GL.GL_QUADS)
        GL.glColor(1.0, 1.0, 1.0, 1.0)
        #GL.glTexCoord(        0.0,         0.0)  # texture coordinate?
        #GL.glVertex  (        0.0,         0.0)
        #GL.glTexCoord(        1.0,         0.0)  # texture coordinate?
        #GL.glVertex  (self.normix,         0.0)
        #GL.glTexCoord(        1.0,         1.0)  # texture coordinate?
        #GL.glVertex  (self.normix, self.normiy)
        #GL.glTexCoord(        0.0,         1.0)  # texture coordinate?
        #GL.glVertex  (        0.0, self.normiy)
        GL.glTexCoord(0.0, 1.0)  # texture coordinate?
        GL.glVertex  (0.0, 0.0)
        GL.glTexCoord(1.0, 1.0)  # texture coordinate?
        GL.glVertex  (1.0, 0.0)
        GL.glTexCoord(1.0, 0.0)  # texture coordinate?
        GL.glVertex  (1.0, 1.0)
        GL.glTexCoord(0.0, 0.0)  # texture coordinate?
        GL.glVertex  (0.0, 1.0)
        GL.glEnd()
        GL.glDisable(GL.GL_TEXTURE_2D)

        GL.glEnable(GL.GL_POINT_SMOOTH)
        GL.glPointSize(100*self.scale)
        GL.glBegin(GL.GL_POINTS)
        GL.glColor(0.7, 0.5, 0.2, 0.5)
        GL.glVertex(0.5, 0.5)
        GL.glEnd()

        GL.glDisable(GL.GL_BLEND)

    def resizeGL(self, width, height):
        side = min(width, height)
        GL.glViewport((width - side) / 2, (height - side) / 2, side, side)

        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GL.glOrtho(0.0, 1.0, 0.0, 1.0, 0.0, 1.0)
        GL.glMatrixMode(GL.GL_MODELVIEW)

    def mousePressEvent(self, event):
        self.lastPos = QtCore.QPoint(event.pos())

        normx = float(event.x()) / self.size().width()
        normy = 1. - (float(event.y()) / self.size().height())
        imgx, imgy = self.getImagePosition(normx, normy)

        self.signal.xmarkerChanged.emit(imgx)
        self.signal.ymarkerChanged.emit(imgy)

    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        #if event.buttons() & QtCore.Qt.LeftButton:
        self.setTranslation(dx/200., dy/200.) # translation speed is 1/200.

        self.lastPos = QtCore.QPoint(event.pos())

    def wheelEvent(self, event):
        normx = float(event.x()) / self.size().width()
        normy = 1. - (float(event.y()) / self.size().height())
        delta = event.delta() / 200. # scale speed
        self.setScale(normx, normy, delta)

    def normalizeTranslation(self, imsize, new):
        transmin = -imsize + self.ortho
        transmax = 0.0
        if new > transmax:
            new = transmax
        elif new < transmin:
            new = transmin
        return new

class MainWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.idx = 0
        self.imin, self.imax = (0, 1)

        self.loadImages()
        self.initUI()

    def initUI(self):
        self.glWidget = GLWidget(self.ix, self.iy, self.image)
        self.glWidget.setFixedSize(FIGURE_WIDTH, FIGURE_HEIGHT)
        self.glWidget.signal.xmarkerChanged.connect(self.xmarkerChanged)
        self.glWidget.signal.ymarkerChanged.connect(self.ymarkerChanged)

        imageSld = QtGui.QSlider(self)
        imageSld.setOrientation(QtCore.Qt.Horizontal)
        imageSld.setRange(0, 20)
        imageSld.setSliderPosition(0)
        imageSld.valueChanged[int].connect(self.changeIndex)

        xmarkerLabel     = QtGui.QLabel('x')
        ymarkerLabel     = QtGui.QLabel('y')
        self.xmarkerEdit = QtGui.QLineEdit('0')
        self.ymarkerEdit = QtGui.QLineEdit('0')

        iminEdit = QtGui.QLineEdit(str(self.imin))
        imaxEdit = QtGui.QLineEdit(str(self.imax))

        iminSld = QtGui.QSlider(self)
        iminSld.setOrientation(QtCore.Qt.Horizontal)
        iminSld.setRange(0, SLIDER_NORMALIZED_END)
        iminSld.setSliderPosition(int(self.imin*SLIDER_NORMALIZED_END))
        iminSld.valueChanged[int].connect(partial(self.changeIntensity, 'IMIN', iminEdit))

        imaxSld = QtGui.QSlider(self)
        imaxSld.setOrientation(QtCore.Qt.Horizontal)
        imaxSld.setRange(0, SLIDER_NORMALIZED_END)
        imaxSld.setSliderPosition(int(self.imax*SLIDER_NORMALIZED_END))
        imaxSld.valueChanged[int].connect(partial(self.changeIntensity, 'IMAX', imaxEdit))

        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(xmarkerLabel)
        hbox1.addWidget(self.xmarkerEdit)
        hbox1.addWidget(ymarkerLabel)
        hbox1.addWidget(self.ymarkerEdit)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(imageSld)
        vbox.addLayout(hbox1)
        vbox.addWidget(iminEdit)
        vbox.addWidget(iminSld)
        vbox.addWidget(imaxEdit)
        vbox.addWidget(imaxSld)

        centralWidget = QtGui.QWidget(self)
        hbox = QtGui.QHBoxLayout(centralWidget)
        hbox.addWidget(self.glWidget)
        hbox.addLayout(vbox)
        self.setCentralWidget(centralWidget)

        #self.resize(1000,800)

    def loadImages(self):
        self.imgs = io.ImageCollection('sample/sample*.tif')
        im = self.imgs[0]
        self.iy, self.ix = im.shape
        self.image = np.dstack((im, im, im)).flatten().tostring()

    def xmarkerChanged(self, pos):
        self.xmarkerEdit.setText(str(pos))

    def ymarkerChanged(self, pos):
        self.ymarkerEdit.setText(str(pos))

    def changeIndex(self, idx):
        self.idx = idx
        self.drawImage()

    def changeIntensity(self, tag, widget, value):
        value = value / float(SLIDER_NORMALIZED_END)
        if tag == 'IMAX':
            self.imax = value
        elif tag == 'IMIN':
            self.imin = value
        self.drawImage()

    def drawImage(self):
        im = self.imgs[self.idx]
        #imin = util.dtype.dtype_range[im.dtype][0] * self.imin # KeyError uint16
        #imax = util.dtype.dtype_range[im.dtype][1] * self.imin # KeyError uint16
        imin = self.imin * (256*256-1)
        imax = self.imax * (256*256-1)
        im = exposure.rescale_intensity(im, (imin, imax))
        self.glWidget.loadTexture(np.dstack((im, im, im)).flatten().tostring())

    def msgBox(self, msg):
        msgbox = QtGui.QMessageBox()
        msgbox.setText(msg)
        msgbox.exec_()

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
