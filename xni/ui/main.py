# -*- coding: utf-8 -*-

import os
import sys
import getopt

from PyQt4 import QtGui, uic

from ..dataset.dataset import Dataset

from .progress import progressWindow


dataset = None

def open_dataset(filename):
    return Dataset(filename)


class MainWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.initUI()

    def initUI(self):
        uic.loadUi(os.path.join('xni', 'ui', 'mainwindow.ui'), self)
        self.reconButton.clicked.connect(self.reconDataset)
        self.viewButton.clicked.connect(self.showViewWindow)
        self.actionOpen.triggered.connect(self.openDataset)
        if dataset is not None:
            self.labelDatasetName.setText(dataset.name)

    def showViewWindow(self):
        dataset.update()
        dataset.show(self)

    def openDataset(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, caption='Select file')
        dataset = open_dataset(filename)
        self.labelDatasetName.setText(dataset.name)

    def reconDataset(self):
        self.async_result = dataset.recon()
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


def usage():
    print("""command -i sample.h5""")

def start():
    global app, dataset
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hi:', ['help', 'input='])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit()
        elif o in ('-i', '--input'):
            try:
                dataset = open_dataset(a)
            except OSError as err:
                print(err)
                sys.exit(2)
        else:
            pass

    app = App(sys.argv)
    sys.exit(app.exec_())
