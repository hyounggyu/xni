# -*- coding: utf-8 -*-

import os
import sys
import getopt

from PyQt4 import QtGui, uic

from ..dataset.dataset import Dataset

from .progress import ProgressWindow
from .imageview import ImageViewWindow

dataset = None


class MainWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.initUI()

    def initUI(self):
        uic.loadUi(os.path.join('xni', 'ui', 'mainwindow.ui'), self)

        self.allsliceRadioButton.toggled.connect(self.disableSliceNumberSlider)
        self.onesliceRadioButton.toggled.connect(self.enableSliceNumberSlider)
        self.slicenumberSlider.valueChanged.connect(self.changedSliceNumberSlider)

        self.reconrunButton.clicked.connect(self.reconRun)
        self.reconviewButton.clicked.connect(self.reconView)

        self.actionOpen.triggered.connect(self.openDataset)

        if dataset is not None:
            self.updateUI()

    def updateUI(self):
        self.labelDatasetName.setText(dataset.name)
        self.slicenumberSlider.setMaximum(dataset.nslice)
        self.reconrunButton.setEnabled(True)

    def openDataset(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, caption='Select file')
        dataset = Dataset(filename)
        self.updateUI()

    def reconRun(self):
        if self.onesliceRadioButton.isChecked():
            slice_number = self.slicenumberSlider.value()
            dataset.recon_sync(slice_number)
            self.reconviewButton.setEnabled(True)
        elif self.allsliceRadioButton.isChecked():
            self.async_result = dataset.recon()
            ProgressWindow(self.async_result, parent=self)
        else:
            pass

        self.statusBar().showMessage('Done')

    def reconView(self):
        ImageViewWindow(dataset.recon, parent=self)

    def disableSliceNumberSlider(self):
        self.slicenumberSlider.setEnabled(False)

    def enableSliceNumberSlider(self):
        self.slicenumberSlider.setEnabled(True)

    def changedSliceNumberSlider(self, slice_number):
        self.slicenumberLineEdit.setText(str(slice_number))


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
                dataset = Dataset(a)
            except OSError as err:
                print(err)
                sys.exit(2)
        else:
            pass

    app = App(sys.argv)
    sys.exit(app.exec_())
