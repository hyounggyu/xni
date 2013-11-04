# -*- coding: utf-8 -*-
"""
    xni.marker
    ~~~~~~~~~~

    :copyright: (c) 2013 by Hyounggyu Kim.
    :license: GPL, see LICENSE for more details.
"""

import sys, os, json
from functools import partial

from PySide import QtGui, QtCore

class MainWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.initUI()
        self.load()

    def initUI(self):
    	self.imageLabel = QtGui.QLabel()
    	self.imageLabel.setBackgroundRole(QtGui.QPalette.Base)
    	self.imageLabel.setSizePolicy(QtGui.QSizePolicy.Ignored,
    		QtGui.QSizePolicy.Ignored)
    	self.imageLabel.setScaledContents(True)

    	scrollArea = QtGui.QScrollArea()
    	scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
    	scrollArea.setWidget(self.imageLabel)
    	self.setCentralWidget(scrollArea)

    	self.resize(500,400)

    def msgBox(self, msg):
        msgbox = QtGui.QMessageBox()
        msgbox.setText(msg)
        msgbox.exec_()

    def load(self):
    	self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(QtGui.QImage('sample.tif')))
    	self.imageLabel.adjustSize()
    	self.scaleFactor = 1.0

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
