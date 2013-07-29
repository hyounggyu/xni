# -*- coding: utf-8 -*-
"""
    xni.config
    ~~~~~~~~~~

    :copyright: (c) 2013 by Hyounggyu Kim.
    :license: GPL, see LICENSE for more details.
"""

import sys, os, json
from functools import partial

import matplotlib
matplotlib.use('Qt4Agg')
matplotlib.rcParams['backend.qt4']='PySide'
import pylab
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PySide import QtGui, QtCore
from utils import find_tiff_files

class MainWindow(QtGui.QMainWindow):

    conf = { 'Base': {} }

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.conf['Base']['srcdir'] = os.curdir
        self.initUI()

    def initUI(self):
        self.srcdirLabel  = QtGui.QLabel('Source directory')
        self.prefixLabel  = QtGui.QLabel('Image file prefix')
        self.bgndimgLabel = QtGui.QLabel('Background image file')
        self.darkimgLabel = QtGui.QLabel('Dark image file')
        self.sftdirLabel  = QtGui.QLabel('Shifted image directory')
        self.posfnLabel   = QtGui.QLabel('Position data file')

        self.srcdirEdit   = QtGui.QLineEdit()
        self.prefixEdit   = QtGui.QLineEdit()
        self.bgndimgEdit  = QtGui.QLineEdit()
        self.darkimgEdit  = QtGui.QLineEdit()
        self.sftdirEdit   = QtGui.QLineEdit()
        self.posfnEdit    = QtGui.QLineEdit()

        self.srcdirBtn    = QtGui.QPushButton('Select')
        self.bgndimgBtn   = QtGui.QPushButton('Select')
        self.darkimgBtn   = QtGui.QPushButton('Select')
        self.sftdirBtn    = QtGui.QPushButton('Select')
        self.posfnBtn     = QtGui.QPushButton('Select')
        self.initshiftBtn = QtGui.QPushButton('Init')
        self.plotshiftBtn = QtGui.QPushButton('Plot')
        self.runshiftBtn  = QtGui.QPushButton('Run')
        self.loadBtn      = QtGui.QPushButton('Load')
        self.saveBtn      = QtGui.QPushButton('Save')
        self.exitBtn      = QtGui.QPushButton('Exit')

        self.srcdirEdit.textChanged[str].connect(partial(self.setConfig, 'Base', 'srcdir'))
        self.srcdirEdit.textEdited[str].connect(partial(self.setConfig, 'Base', 'srcdir'))
        self.prefixEdit.textChanged[str].connect(self.setImages)
        self.prefixEdit.textEdited[str].connect(self.setImages)
        self.bgndimgEdit.textChanged[str].connect(partial(self.setConfig, 'Base', 'bgndimg'))
        self.bgndimgEdit.textEdited[str].connect(partial(self.setConfig, 'Base', 'bgndimg'))
        self.darkimgEdit.textChanged[str].connect(partial(self.setConfig, 'Base', 'darkimg'))
        self.darkimgEdit.textEdited[str].connect(partial(self.setConfig, 'Base', 'darkimg'))
        self.sftdirEdit.textChanged[str].connect(partial(self.setConfig, 'Shift', 'sftdir'))
        self.sftdirEdit.textEdited[str].connect(partial(self.setConfig, 'Shift', 'sftdir'))
        self.posfnEdit.textChanged[str].connect(partial(self.setConfig, 'Shift', 'posfn'))
        self.posfnEdit.textEdited[str].connect(partial(self.setConfig, 'Shift', 'posfn'))

        self.srcdirBtn.clicked.connect(partial(self.selectDirectory, self.srcdirEdit))
        self.bgndimgBtn.clicked.connect(partial(self.selectFile, self.bgndimgEdit, 'TIFF image File (*.tif *.tiff)'))
        self.darkimgBtn.clicked.connect(partial(self.selectFile, self.darkimgEdit, 'TIFF image File (*.tif *.tiff)'))
        self.sftdirBtn.clicked.connect(partial(self.selectDirectory, self.sftdirEdit))
        self.posfnBtn.clicked.connect(partial(self.selectFile, self.posfnEdit, 'Comma Seperated Values File (*.txt *.csv)'))
        self.initshiftBtn.clicked.connect(self.initShift)
        self.plotshiftBtn.clicked.connect(self.plotShift)
        self.runshiftBtn.clicked.connect(self.runShift)
        self.loadBtn.clicked.connect(self.loadConfig)
        self.saveBtn.clicked.connect(self.saveConfig)
        self.exitBtn.clicked.connect(QtCore.QCoreApplication.instance().quit)

        grid1 = QtGui.QGridLayout()
        grid1.setSpacing(10)
        grid1.addWidget(self.srcdirLabel,  1, 0)
        grid1.addWidget(self.srcdirEdit,   1, 1)
        grid1.addWidget(self.srcdirBtn,    1, 2)
        grid1.addWidget(self.prefixLabel,  2, 0)
        grid1.addWidget(self.prefixEdit,   2, 1)
        grid1.addWidget(self.bgndimgLabel, 3, 0)
        grid1.addWidget(self.bgndimgEdit,  3, 1)
        grid1.addWidget(self.bgndimgBtn,   3, 2)
        grid1.addWidget(self.darkimgLabel, 4, 0)
        grid1.addWidget(self.darkimgEdit,  4, 1)
        grid1.addWidget(self.darkimgBtn,   4, 2)
        group1 = QtGui.QGroupBox('Base Configuration')
        group1.setLayout(grid1)

        grid2 = QtGui.QGridLayout()
        grid2.setSpacing(10)
        grid2.addWidget(self.sftdirLabel,  1, 0)
        grid2.addWidget(self.sftdirEdit,   1, 1)
        grid2.addWidget(self.sftdirBtn,    1, 2)
        grid2.addWidget(self.posfnLabel,   2, 0)
        grid2.addWidget(self.posfnEdit,    2, 1)
        grid2.addWidget(self.posfnBtn,     2, 2)
        group2 = QtGui.QGroupBox('Shift Configuration')
        # Checkable?
#        group2.setCheckable(True)
#        group2.setChecked(False)
        group2.setLayout(grid2)

        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(self.initshiftBtn)
        hbox1.addWidget(self.plotshiftBtn)
        hbox1.addWidget(self.runshiftBtn)

        hbox2 = QtGui.QHBoxLayout()
        hbox2.addWidget(self.loadBtn)
        hbox2.addWidget(self.saveBtn)
        hbox2.addWidget(self.exitBtn)

        centralWidget = QtGui.QWidget(self)
        vbox = QtGui.QVBoxLayout(centralWidget)
        vbox.addStretch(1)
        vbox.addWidget(group1)
        vbox.addWidget(group2)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)

        self.setCentralWidget(centralWidget)
        self.setWindowTitle('Configuration')
        self.statusBar().showMessage('Ready')

    def selectDirectory(self, widget):
        directory = QtGui.QFileDialog.getExistingDirectory(self, dir=self.conf['Base']['srcdir'], caption="Select directory")
        widget.setText(directory)

    def selectFile(self, widget, _filter):
        fn, _ = QtGui.QFileDialog.getOpenFileName(self, caption="Select file", dir=self.conf['Base']['srcdir'], filter=_filter)
        widget.setText(fn)

    def setConfig(self, section, option, text):
        if not section in self.conf:
            self.conf[section] = dict()
        self.conf[section][option] = text

    def setImages(self, text):
        self.imgs = find_tiff_files(self.conf['Base']['srcdir'], text)
        self.setConfig('Base', 'prefix', text)
        self.statusBar().showMessage('%d (tiff files)' % len(self.imgs))

    def loadConfig(self):
        fn, _ = QtGui.QFileDialog.getOpenFileName(self, caption="Load configuration", dir=self.conf['Base']['srcdir'], filter="Json file (*.json)")
        # try:
        f = open(fn, "r")
        # except:
        self.conf = json.loads(f.read())
        # if 'Base' dose not exist
        c = self.conf['Base']
        self.srcdirEdit.setText(self.conf['Base']['srcdir'])
        if 'prefix' in c:
            self.prefixEdit.setText(self.conf['Base']['prefix'])
        if 'bgndimg' in c:
            self.bgndimgEdit.setText(self.conf['Base']['bgndimg'])
        if 'darkimg' in c:
            self.darkimgEdit.setText(self.conf['Base']['darkimg'])

        if 'Shift' in self.conf:
            c = self.conf['Shift']
            if 'sftdir' in c:
                self.sftdirEdit.setText(self.conf['Shift']['sftdir'])
            if 'posfn' in c:
                self.posfnEdit.setText(self.conf['Shift']['posfn'])

    def saveConfig(self):
        fn, _ = QtGui.QFileDialog.getSaveFileName(self, caption="Save configuration", dir=self.conf['Base']['srcdir'], filter="Json file (*.json)")
        # try:
        f = open(fn, "w")
        # except:
        f.write(json.dumps(self.conf, indent=4, sort_keys=True))

    def initShift(self):
        pass

    def plotShift(self):
        self.plotw = PlotWindow()

    def runShift(self):
        pass

class PlotWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(PlotWindow, self).__init__(parent)
        self.initUI()

    def initUI(self):
        fig = Figure(figsize=(600,600), dpi=72, facecolor=(1,1,1), edgecolor=(0,0,0))
        ax = fig.add_subplot(111)
        ax.plot([0,1])
        canvas = FigureCanvas(fig)
        self.setCentralWidget(canvas)
        self.setWindowTitle('Plot')
        self.show()

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
