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
from skimage import io, transform, util, exposure

from OpenGL import GL

from PySide import QtGui, QtCore, QtOpenGL

FIGURE_WIDTH = 700
FIGURE_HEIGHT = 700
SLIDER_NORMALIZED_END = 50

class GLWidget(QtOpenGL.QGLWidget):
    def __init__(self, ix, iy, image, parent=None):
        QtOpenGL.QGLWidget.__init__(self, parent)

        self.ix, self.iy, self.image = (ix, iy, image)
        self.xTrans, self.yTrans = (0, 0)

        self.lastPos = QtCore.QPoint()

    def minimumSizeHint(self):
        return QtCore.QSize(50, 50)

    def sizeHint(self):
        return QtCore.QSize(400, 400)

    def setXTranslation(self, position):
        if position != self.xTrans:
            self.xTrans = position
            self.emit(QtCore.SIGNAL("xTranslationChanged(int)"), position)
            self.updateGL()

    def setYTranslation(self, position):
        if position != self.yTrans:
            self.yTrans = position
            self.emit(QtCore.SIGNAL("yTranslationChanged(int)"), position)
            self.updateGL()

    def loadTexture(self, image):
        GL.glTexSubImage2D(GL.GL_TEXTURE_2D, 0, 0, 0, self.ix, self.iy, GL.GL_RGB, GL.GL_UNSIGNED_SHORT, image)
        self.updateGL()

    def initializeGL(self):
        # 아래 코드 테스트 할 것
        GL.glEnable(GL.GL_TEXTURE_2D)
        GL.glBindTexture(GL.GL_TEXTURE_2D, GL.glGenTextures(1))
        GL.glPixelStorei(GL.GL_UNPACK_ALIGNMENT, 4) # word-alignment
        GL.glTexParameter(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_REPEAT) # 무슨 뜻?
        GL.glTexParameter(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_REPEAT) # 무슨 뜻?
        GL.glTexParameter(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_NEAREST)
        GL.glTexParameter(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_NEAREST)
        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGB16, self.ix, self.iy, 0, GL.GL_RGB, GL.GL_UNSIGNED_SHORT, self.image)

    def paintGL(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glLoadIdentity()
        #GL.glColor(2.0, 2.0, 2.0)
        GL.glTranslate(self.xTrans, self.yTrans, 0.0)
        GL.glScale(2.0, 2.0, 1.0)
        GL.glBegin(GL.GL_QUADS)
        GL.glTexCoord(0.0, 0.0)
        GL.glVertex  (0.0, 0.0)
        GL.glTexCoord(1.0, 0.0)
        GL.glVertex  (1.0, 0.0)
        GL.glTexCoord(1.0, 1.0)
        GL.glVertex  (1.0, 1.0)
        GL.glTexCoord(0.0, 1.0)
        GL.glVertex  (0.0, 1.0)
        GL.glEnd()

    def resizeGL(self, width, height):
        side = min(width, height)
        GL.glViewport((width - side) / 2, (height - side) / 2, side, side)

        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GL.glOrtho(0.0, 1.0, 0.0, 1.0, 0.0, 1.0)
        GL.glMatrixMode(GL.GL_MODELVIEW)

    def mousePressEvent(self, event):
        self.lastPos = QtCore.QPoint(event.pos())

    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        #if event.buttons() & QtCore.Qt.LeftButton:
        self.setXTranslation(self.xTrans + dx/100.)
        self.setYTranslation(self.yTrans + dy/100.)

        self.lastPos = QtCore.QPoint(event.pos())

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

        imageSld = QtGui.QSlider(self)
        imageSld.setOrientation(QtCore.Qt.Horizontal)
        imageSld.setRange(0, 20)
        imageSld.setSliderPosition(0)
        imageSld.valueChanged[int].connect(self.changeIndex)

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

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(imageSld)
        #vbox.addWidget(scaleComboBox)
        vbox.addWidget(iminEdit)
        vbox.addWidget(iminSld)
        vbox.addWidget(imaxEdit)
        vbox.addWidget(imaxSld)

        centralWidget = QtGui.QWidget(self)
        hbox = QtGui.QHBoxLayout(centralWidget)
        hbox.addWidget(self.glWidget)
        hbox.addLayout(vbox)
        self.setCentralWidget(centralWidget)

        self.resize(1000,800)

    def loadImages(self):
        self.imgs = io.ImageCollection('sample/sample*.tif')
        im = self.imgs[0]
        self.iy, self.ix = im.shape
        self.image = np.dstack((im, im, im)).flatten().tostring()

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
        #imin = util.dtype.dtype_range[im.dtype][0] * self.imin
        #imax = util.dtype.dtype_range[im.dtype][1] * self.imin
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
