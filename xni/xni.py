# -*- coding: utf-8 -*-
"""
    xni.xni
    ~~~~~~~

    :copyright: (c) 2013 by Hyounggyu Kim.
    :license: GPL, see LICENSE for more details.
"""

import sys
from functools import partial

from PySide import QtGui, QtCore

from config import ConfigWindow
from marker import MarkerWindow


class MainWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('XNI')

        self.configBtn = QtGui.QPushButton('Configuration')
        self.configBtn.clicked.connect(self.showConfigWindow)

        self.markerBtn  = QtGui.QPushButton('Set Marker')
        self.markerBtn.clicked.connect(self.showMarkerWindow)

        centralWidget = QtGui.QWidget(self)
        vbox = QtGui.QVBoxLayout(centralWidget)
        vbox.addWidget(self.configBtn)
        vbox.addWidget(self.markerBtn)
        self.setCentralWidget(centralWidget)

    def showConfigWindow(self):
        config = ConfigWindow()
        config.show()

    def showMarkerWindow(self):
    	marker = MarkerWindow()
    	marker.show()

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
