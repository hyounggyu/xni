# -*- coding: utf-8 -*-

import os
import sys

from PyQt4 import QtGui, uic

from ..dataset.dataset import Dataset

from .progress import progressWindow

class MainWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.d = Dataset()
        self.initUI()

    def initUI(self):
        uic.loadUi(os.path.join('xni', 'ui', 'mainwindow.ui'), self)
        self.openButton.clicked.connect(self.openDataset)
        self.reconButton.clicked.connect(self.reconDataset)
        self.viewButton.clicked.connect(self.showViewWindow)

    def showViewWindow(self):
        self.d.update()
        self.d.show(self)

    def openDataset(self):
        fn = QtGui.QFileDialog.getOpenFileName(self, caption='Select file')

    def reconDataset(self):
        self.async_result = self.d.recon()
        progressWindow(self.async_result, parent=self)
        #self.statusBar().showMessage('Done')


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


def start():
    global app
    app = App(sys.argv)
    sys.exit(app.exec_())
