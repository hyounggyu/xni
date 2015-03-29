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

        # Reconstruction Group
        self.radioButtonSliceRange.toggled.connect(self.toggleSliceRange)
        self.radioButtonOneSlice.toggled.connect(self.toggleOneSlice)
        self.horizontalSliderSliceNumber.valueChanged.connect(self.changedSliceNumberSlider)
        self.buttonReconRun.clicked.connect(self.reconRun)
        self.buttonReconView.clicked.connect(self.reconView)

        # Menu
        self.actionOpen.triggered.connect(self.openDataset)

        if dataset is not None:
            self.updateUI()

    def updateUI(self):
        # Update UI when the dataset loads
        self.labelDatasetName.setText(dataset.name)
        self.horizontalSliderSliceNumber.setMaximum(dataset.max_slice_num)
        self.buttonReconRun.setEnabled(True)
        # check recon data
        # check alignment data

    def openDataset(self):
        global dataset
        filename = QtGui.QFileDialog.getOpenFileName(self, caption='Select file')
        dataset = Dataset(filename)
        self.updateUI()

    def reconRun(self):
        start = 0
        end = 1
        step = 1
        if self.radioButtonOneSlice.isChecked():
            start = self.horizontalSliderSliceNumber.value()
            end = start+1
            step = 1
        elif self.radioButtonSliceRange.isChecked():
            start = int(self.lineEditSliceNumberStart.text())
            end = int(self.lineEditSliceNumberEnd.text())
            step = int(self.lineEditSliceNumberStep.text())
        else:
            pass
        dataset.recon(start, end, step)
        ProgressWindow(dataset, parent=self)

        # wait?
        #self.buttonReconView.setEnabled(True)
        #self.statusBar().showMessage('Done')

    def reconView(self):
        ImageViewWindow(dataset.recon_data, parent=self)

    def toggleSliceRange(self):
        self.horizontalSliderSliceNumber.setEnabled(False)
        self.lineEditSliceNumberStart.setEnabled(True)
        self.lineEditSliceNumberEnd.setEnabled(True)
        self.lineEditSliceNumberStep.setEnabled(True)

    def toggleOneSlice(self):
        self.horizontalSliderSliceNumber.setEnabled(True)
        self.lineEditSliceNumberStart.setEnabled(False)
        self.lineEditSliceNumberEnd.setEnabled(False)
        self.lineEditSliceNumberStep.setEnabled(False)

    def changedSliceNumberSlider(self, slice_number):
        self.lineEditSliceNumber.setText(str(slice_number))


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
