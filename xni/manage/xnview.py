# -*- coding: utf-8 -*-

from functools import partial

import numpy as np

from OpenGL import GL
from PyQt4 import QtGui, QtCore, QtOpenGL

from skimage import io, data_dir

class Communicate(QtCore.QObject):

    xMarkerChanged = QtCore.pyqtSignal(int)
    yMarkerChanged = QtCore.pyqtSignal(int)


class GLWidget(QtOpenGL.QGLWidget):

    def __init__(self, img, parent=None):
        QtOpenGL.QGLWidget.__init__(self, parent)

        self.signal = Communicate()
        self.lastPos = QtCore.QPoint()

        self.reloadTexture = False
        # self.img, self.imgWidth, self.imgHeight, self.xMarker, self.yMarker
        #self.setImage(img, marker)
        self.setImage(img)

        self.imgScale = 1.0
        self.xTrans   = 0.0
        self.yTrans   = 0.0
        self.normImgWidth = 1.0  # related with glOrtho
        self.normImgHeight = 1.0 # related with glOrtho

    def initializeGL(self):
        # Initialize blend
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        # Initialize texture
        GL.glBindTexture(GL.GL_TEXTURE_2D, GL.glGenTextures(1))
        GL.glPixelStorei(GL.GL_UNPACK_ALIGNMENT, 4) # word-alignment
        GL.glTexParameter(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_REPEAT) # 무슨 뜻?
        GL.glTexParameter(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_REPEAT) # 무슨 뜻?
        GL.glTexParameter(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_NEAREST)
        GL.glTexParameter(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_NEAREST)
        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGB16, self.imgWidth, self.imgHeight, 0, GL.GL_RGB, GL.GL_UNSIGNED_SHORT, self.img)
        self.reloadTexture = True

    def paintGL(self):
        GL.glClearColor(0.0, 0.0, 1.0, 1.0) # background color
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glLoadIdentity()
        GL.glTranslate(self.xTrans, self.yTrans, 0.0)
        GL.glScale(self.imgScale, self.imgScale, 1.0)

        GL.glEnable(GL.GL_BLEND)

        GL.glEnable(GL.GL_TEXTURE_2D)
        GL.glBegin(GL.GL_QUADS)
        GL.glColor(1.0, 1.0, 1.0, 1.0) # white
        GL.glTexCoord(0.0, 1.0)
        GL.glVertex  (0.0, 0.0)
        GL.glTexCoord(1.0, 1.0)
        GL.glVertex  (1.0, 0.0)
        GL.glTexCoord(1.0, 0.0)
        GL.glVertex  (1.0, 1.0)
        GL.glTexCoord(0.0, 0.0)
        GL.glVertex  (0.0, 1.0)
        GL.glEnd()
        GL.glDisable(GL.GL_TEXTURE_2D)

        #if self.xMarker != None and self.yMarker != None:
        #    GL.glEnable(GL.GL_POINT_SMOOTH) # point shape
        #    GL.glPointSize(10*self.imgScale) # point size
        #    GL.glBegin(GL.GL_POINTS)
        #    GL.glColor(0.7, 0.5, 0.2, 0.5) # point color
        #    GL.glVertex(self.xMarker, self.yMarker)
        #    GL.glEnd()

        GL.glDisable(GL.GL_BLEND)

    def resizeGL(self, width, height):
        side = min(width, height)
        GL.glViewport((width - side) / 2, (height - side) / 2, side, side)

        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GL.glOrtho(0.0, 1.0, 0.0, 1.0, 0.0, 1.0)
        GL.glMatrixMode(GL.GL_MODELVIEW)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.lastPos = QtCore.QPoint(event.pos())
            self.pressedPos = QtCore.QPoint(event.pos())

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            dx = event.x() - self.pressedPos.x()
            dy = event.y() - self.pressedPos.y()
            if dx == 0 and dy == 0:
                self.setMarker(event.x(), event.y())

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            dx = event.x() - self.lastPos.x()
            dy = event.y() - self.lastPos.y()
            if dx != 0 or dy != 0:
                self.lastPos = QtCore.QPoint(event.pos())
                self.setTranslation(dx/200., dy/200.) # translation speed is 1/200.

    def wheelEvent(self, event):
        self.setScale(event.x(), event.y(), event.delta()/200.) # zoom speed is 1/200.

    def setImage(self, img):
        self.img = np.dstack((img, img, img)).flatten().tostring()
        self.imgHeight, self.imgWidth = img.shape
        #self.xMarker, self.yMarker = marker
        #if self.xMarker != None and self.yMarker != None:
        #    self.xMarker /= float(self.imgWidth)
        #    self.yMarker /= float(self.imgHeight)
        if self.reloadTexture == True:
            GL.glTexSubImage2D(GL.GL_TEXTURE_2D, 0, 0, 0, self.imgWidth, self.imgHeight, GL.GL_RGB, GL.GL_UNSIGNED_SHORT, self.img)
            self.updateGL()

#    def setMarker(self, posx, posy):
        #normposx, normposy = self.normalizeMousePosition(posx, posy)
        #self.xMarker = (normposx - self.xTrans) / self.imgScale
        #self.yMarker = (normposy - self.yTrans) / self.imgScale
        #self.signal.xMarkerChanged.emit(self.xMarker * self.imgWidth)
        #self.signal.yMarkerChanged.emit(self.yMarker * self.imgHeight)
        #self.updateGL()

    def setTranslation(self, dx, dy):
        self.xTrans = self.normalizeTranslation(self.normImgWidth*self.imgScale, self.xTrans+dx)
        self.yTrans = self.normalizeTranslation(self.normImgHeight*self.imgScale, self.yTrans+dy)
        self.updateGL()

    def setScale(self, posx, posy, delta):
        normposx, normposy = self.normalizeMousePosition(posx, posy)
        oldscale = self.imgScale
        newscale = self.imgScale + delta
        if newscale > 1.0:
            self.xTrans = normposx - newscale*(normposx-self.xTrans)/oldscale
            self.yTrans = normposy - newscale*(normposy-self.yTrans)/oldscale
            self.xTrans = self.normalizeTranslation(self.normImgWidth*newscale, self.xTrans)
            self.yTrans = self.normalizeTranslation(self.normImgHeight*newscale, self.yTrans)
        else:
            newscale = 1.0
            self.xTrans, self.yTrans = (0., 0.)
        self.imgScale = newscale
        self.updateGL()

    def normalizeTranslation(self, length, transnew):
        transmin = 1.0 - length # 1.0 related with glOrtho
        transmax = 0.0
        if transnew > transmax:
            transnew = transmax
        elif transnew < transmin:
            transnew = transmin
        return transnew

    def normalizeMousePosition(self, posx, posy):
        normposx = float(posx) / self.size().width()
        normposy = 1. - (float(posy) / self.size().height())
        return normposx, normposy


class MarkerWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(MarkerWindow, self).__init__(parent)

        self.FIGURE_WIDTH = 700
        self.FIGURE_HEIGHT = 700
        self.SLIDER_NORMALIZED_END = 50

        self.idx = 0
        self.normMinIntensity, self.normMaxIntensity = (0., 1.)

        self.loadImages() # self.imgs, self.xMarkers, self.yMarkers

        self.initUI()

    def initUI(self):
        #self.glWidget = GLWidget(self.imgs[0], (self.xMarkers[0], self.yMarkers[0]))
        self.glWidget = GLWidget(self.img)

        self.glWidget.setFixedSize(self.FIGURE_WIDTH, self.FIGURE_HEIGHT)
        self.glWidget.signal.xMarkerChanged.connect(self.xMarkerChanged)
        self.glWidget.signal.yMarkerChanged.connect(self.yMarkerChanged)

        #imageSld = QtGui.QSlider(self)
        #imageSld.setOrientation(QtCore.Qt.Horizontal)
        #imageSld.setRange(0, len(self.imgs))
        #imageSld.setSliderPosition(0)
        #imageSld.valueChanged[int].connect(self.changeIndex)

        xMarkerLabel     = QtGui.QLabel('x')
        yMarkerLabel     = QtGui.QLabel('y')
        self.xMarkerEdit = QtGui.QLineEdit('0')
        self.yMarkerEdit = QtGui.QLineEdit('0')

        minIntensityEdit = QtGui.QLineEdit(str(self.normMinIntensity))
        maxIntensityEdit = QtGui.QLineEdit(str(self.normMaxIntensity))

        minIntensitySld = QtGui.QSlider(self)
        minIntensitySld.setOrientation(QtCore.Qt.Horizontal)
        minIntensitySld.setRange(0, self.SLIDER_NORMALIZED_END)
        minIntensitySld.setSliderPosition(int(self.normMinIntensity*self.SLIDER_NORMALIZED_END))
        minIntensitySld.valueChanged[int].connect(partial(self.changeIntensity, 'IMIN', minIntensityEdit))

        maxIntensitySld = QtGui.QSlider(self)
        maxIntensitySld.setOrientation(QtCore.Qt.Horizontal)
        maxIntensitySld.setRange(0, self.SLIDER_NORMALIZED_END)
        maxIntensitySld.setSliderPosition(int(self.normMaxIntensity*self.SLIDER_NORMALIZED_END))
        maxIntensitySld.valueChanged[int].connect(partial(self.changeIntensity, 'IMAX', maxIntensityEdit))

        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(xMarkerLabel)
        hbox1.addWidget(self.xMarkerEdit)
        hbox1.addWidget(yMarkerLabel)
        hbox1.addWidget(self.yMarkerEdit)

        vbox = QtGui.QVBoxLayout()
        #vbox.addWidget(imageSld)
        vbox.addLayout(hbox1)
        vbox.addWidget(minIntensityEdit)
        vbox.addWidget(minIntensitySld)
        vbox.addWidget(maxIntensityEdit)
        vbox.addWidget(maxIntensitySld)

        centralWidget = QtGui.QWidget(self)
        hbox = QtGui.QHBoxLayout(centralWidget)
        hbox.addWidget(self.glWidget)
        hbox.addLayout(vbox)
        self.setCentralWidget(centralWidget)

    def loadImages(self):
        #self.imgs = io.ImageCollection('sample/sample*.tif')
        print(data_dir)
        self.img = io.imread(data_dir + '/chessboard_GRAY_U16.tif')
        #self.xMarkers = [None] * len(self.imgs)
        #self.yMarkers = [None] * len(self.imgs)

    def drawImage(self):
        #marker = (self.xMarkers[self.idx], self.yMarkers[self.idx])
        #img = self.imgs[self.idx]
        img = self.img
        minIntensity = self.normMinIntensity * (256*256-1) # 16 bit pixel
        maxIntensity = self.normMaxIntensity * (256*256-1) # 16 bit pixel
        #img = exposure.rescale_intensity(img, (minIntensity, maxIntensity))
        #self.glWidget.setImage(img, marker)
        self.glWidget.setImage(img)

    def xMarkerChanged(self, pos):
        self.xMarkers[self.idx] = pos
        self.xMarkerEdit.setText(str(pos))

    def yMarkerChanged(self, pos):
        self.yMarkers[self.idx] = pos
        self.yMarkerEdit.setText(str(pos))

    def changeIndex(self, idx):
        self.idx = idx
        self.drawImage()

    def changeIntensity(self, tag, widget, value):
        value = value / float(self.SLIDER_NORMALIZED_END)
        if tag == 'IMAX':
            self.normMaxIntensity = value
        elif tag == 'IMIN':
            self.normMinIntensity = value
        self.drawImage()

    def msgBox(self, msg):
        msgbox = QtGui.QMessageBox()
        msgbox.setText(msg)
        msgbox.exec_()
