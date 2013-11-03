# -*- coding: utf-8 -*-
"""
    xni.config
    ~~~~~~~~~~

    :copyright: (c) 2013 by Hyounggyu Kim.
    :license: GPL, see LICENSE for more details.
"""

import sys, os, json
from functools import partial

import numpy as np

import matplotlib
matplotlib.use('Qt4Agg')
matplotlib.rcParams['backend.qt4']='PySide'
import pylab
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PySide import QtGui, QtCore

from normalize import Normalize
from shift import ShiftImage
from tiff import imread, imwrite
from utils import find_tiff_files, read_pos_from_csv

class MainWindow(QtGui.QMainWindow):

    conf = { 'Base': {} }

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.conf['Base']['srcdir'] = os.curdir
        self.shiftimage = None
        self.imgs = None
        self.initUI()

    def initUI(self):
        self.srcdirLabel  = QtGui.QLabel('Source directory')
        self.prefixLabel  = QtGui.QLabel('Image file prefix')
        self.bgndimgLabel = QtGui.QLabel('Background image file')
        self.darkimgLabel = QtGui.QLabel('Dark image file')
        self.nordirLabel  = QtGui.QLabel('Normalized image directory')
        self.sftdirLabel  = QtGui.QLabel('Shifted image directory')
        self.posfnLabel   = QtGui.QLabel('Position data file')

        self.srcdirEdit   = QtGui.QLineEdit()
        self.prefixEdit   = QtGui.QLineEdit()
        self.bgndimgEdit  = QtGui.QLineEdit()
        self.darkimgEdit  = QtGui.QLineEdit()
        self.nordirEdit   = QtGui.QLineEdit()
        self.sftdirEdit   = QtGui.QLineEdit()
        self.posfnEdit    = QtGui.QLineEdit()

        self.srcdirBtn    = QtGui.QPushButton('Select')
        self.bgndimgBtn   = QtGui.QPushButton('Select')
        self.darkimgBtn   = QtGui.QPushButton('Select')
        self.nordirBtn    = QtGui.QPushButton('Select')
        self.sftdirBtn    = QtGui.QPushButton('Select')
        self.posfnBtn     = QtGui.QPushButton('Select')
        self.runnormalBtn  = QtGui.QPushButton('Normalize All')
        self.plotshiftBtn = QtGui.QPushButton('Plot Position')
        self.runshiftBtn  = QtGui.QPushButton('Shift All')

        self.srcdirEdit.textChanged[str].connect(partial(self.setConfig, 'Base', 'srcdir'))
        self.srcdirEdit.textEdited[str].connect(partial(self.setConfig, 'Base', 'srcdir'))
        self.prefixEdit.textChanged[str].connect(self.setImages)
        self.prefixEdit.textEdited[str].connect(self.setImages)
        self.bgndimgEdit.textChanged[str].connect(partial(self.setConfig, 'Base', 'bgndimg'))
        self.bgndimgEdit.textEdited[str].connect(partial(self.setConfig, 'Base', 'bgndimg'))
        self.darkimgEdit.textChanged[str].connect(partial(self.setConfig, 'Base', 'darkimg'))
        self.darkimgEdit.textEdited[str].connect(partial(self.setConfig, 'Base', 'darkimg'))
        self.nordirEdit.textChanged[str].connect(partial(self.setConfig, 'Normalize', 'nordir'))
        self.nordirEdit.textEdited[str].connect(partial(self.setConfig, 'Normalize', 'nordir'))
        self.sftdirEdit.textChanged[str].connect(partial(self.setConfig, 'Shift', 'sftdir'))
        self.sftdirEdit.textEdited[str].connect(partial(self.setConfig, 'Shift', 'sftdir'))
        self.posfnEdit.textChanged[str].connect(partial(self.setConfig, 'Shift', 'posfn'))
        self.posfnEdit.textEdited[str].connect(partial(self.setConfig, 'Shift', 'posfn'))

        self.srcdirBtn.clicked.connect(partial(self.selectDirectory, self.srcdirEdit))
        self.bgndimgBtn.clicked.connect(partial(self.selectFile, self.bgndimgEdit, 'TIFF image File (*.tif *.tiff)'))
        self.darkimgBtn.clicked.connect(partial(self.selectFile, self.darkimgEdit, 'TIFF image File (*.tif *.tiff)'))
        self.nordirBtn.clicked.connect(partial(self.selectDirectory, self.nordirEdit))
        self.sftdirBtn.clicked.connect(partial(self.selectDirectory, self.sftdirEdit))
        self.posfnBtn.clicked.connect(partial(self.selectFile, self.posfnEdit, 'Comma Seperated Values File (*.txt *.csv)'))
        self.runnormalBtn.clicked.connect(self.runNormal)
        self.plotshiftBtn.clicked.connect(self.plotShift)
        self.runshiftBtn.clicked.connect(self.runShift)

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
        grid2.addWidget(self.nordirLabel,  1, 0)
        grid2.addWidget(self.nordirEdit,   1, 1)
        grid2.addWidget(self.nordirBtn,    1, 2)
        group2 = QtGui.QGroupBox('Normalize Configuration')
        group2.setLayout(grid2)

        grid3 = QtGui.QGridLayout()
        grid3.setSpacing(10)
        grid3.addWidget(self.sftdirLabel,  1, 0)
        grid3.addWidget(self.sftdirEdit,   1, 1)
        grid3.addWidget(self.sftdirBtn,    1, 2)
        grid3.addWidget(self.posfnLabel,   2, 0)
        grid3.addWidget(self.posfnEdit,    2, 1)
        grid3.addWidget(self.posfnBtn,     2, 2)
        group3 = QtGui.QGroupBox('Shift Configuration')
        group3.setLayout(grid3)

        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(self.runnormalBtn)
        hbox1.addWidget(self.plotshiftBtn)
        hbox1.addWidget(self.runshiftBtn)

        centralWidget = QtGui.QWidget(self)
        vbox = QtGui.QVBoxLayout(centralWidget)
        vbox.addStretch(1)
        vbox.addWidget(group1)
        vbox.addWidget(group2)
        vbox.addWidget(group3)
        vbox.addLayout(hbox1)
        self.setCentralWidget(centralWidget)

        self.statusBar().showMessage('Ready')

        loadAction = QtGui.QAction('Load', self)
        loadAction.setStatusTip('Load Configuration')
        loadAction.triggered.connect(self.loadConfig)
        saveAction = QtGui.QAction('Save', self)
        saveAction.setStatusTip('Save Configuration')
        saveAction.triggered.connect(self.saveConfig)
        quitAction = QtGui.QAction('Quit', self)
        quitAction.setStatusTip('Quit')
        quitAction.triggered.connect(QtCore.QCoreApplication.instance().quit)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        fileMenu.addAction(loadAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(quitAction)

        self.setWindowTitle('Configuration')

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

        try:
            self.conf = json.loads(open(fn, "r").read())
        except IOError as e:
            self.msgBox("IOError({0}): {1}".format(e.errno, e.strerror))
            return
        except ValueError as e:
            self.msgBox("ValueError: " + e.message)
            return

        if 'Base' in self.conf:
            c = self.conf['Base']
            if 'srcdir' in c:
                self.srcdirEdit.setText(c['srcdir'])
            if 'prefix' in c:
                self.prefixEdit.setText(c['prefix'])
            if 'bgndimg' in c:
                self.bgndimgEdit.setText(c['bgndimg'])
            if 'darkimg' in c:
                self.darkimgEdit.setText(c['darkimg'])

        if 'Normalize' in self.conf:
            c = self.conf['Normalize']
            if 'nordir' in c:
                self.sftdirEdit.setText(c['nordir'])

        if 'Shift' in self.conf:
            c = self.conf['Shift']
            if 'sftdir' in c:
                self.sftdirEdit.setText(c['sftdir'])
            if 'posfn' in c:
                self.posfnEdit.setText(c['posfn'])

    def saveConfig(self):
        fn, _ = QtGui.QFileDialog.getSaveFileName(self, caption="Save configuration", dir=self.conf['Base']['srcdir'], filter="Json file (*.json)")
        try:
            f = open(fn, "w")
            f.write(json.dumps(self.conf, indent=4, sort_keys=True))
        except IOError as e:
            self.msgBox("IOError({0}): {1}".format(e.errno, e.strerror))
            return

    def runNormal(self):
        try:
            srcdir = self.conf['Base']['srcdir']
            nordir = self.conf['Normalize']['nordir']
            bg = self.conf['Base']['bgndimg']
            nor = Normalize(srcdir, nordir, self.imgs, bg)
            nor.normalize_all()
        except IOError as e:
            self.msgBox("IOError({0}): {1}".format(e.errno, e.strerror))
            return
        except KeyError:
            self.msgBox("Please check configurations")
            return
        except ValueError:
            self.msgBox("ValueError: " + e.message)
            return

    def initShift(self):
        try:
            pos, errors = read_pos_from_csv(self.conf['Shift']['posfn'], 0, 5, 6)
            srcdir = self.conf['Base']['srcdir']
            sftdir = self.conf['Shift']['sftdir']
            self.shiftimage = ShiftImage(srcdir, sftdir, self.imgs, pos)
        except IOError as e:
            self.msgBox("IOError({0}): {1}".format(e.errno, e.strerror))
            return False
        except KeyError:
            self.msgBox("Please check configurations")
            return False

        if not (os.path.isdir(srcdir) and os.path.isdir(sftdir)):
            return False

        errlines = ','.join([str(i) for i in errors])
        self.statusBar().showMessage("Position array shape is {0}, Parsing failed lines are {1}".format(pos.shape, errlines))
        return True

    def plotShift(self):
        if not self.initShift():
            return
        interp_x, interp_y = self.shiftimage.get_interp()
        pos = self.shiftimage.get_pos()
        thetas = self.shiftimage.get_thetas()
        new_thetas = np.linspace(thetas[0], thetas[-1], 900)

        self.plotw = PlotWindow()
        fig = self.plotw.getFigure()
        ax = fig.add_subplot(111)
        ax.plot(pos[:,0], pos[:,1], 'x', pos[:,0], pos[:,2], 'o')
        ax.plot(new_thetas, interp_x(new_thetas))
        ax.plot(new_thetas, interp_y(new_thetas))
        self.plotw.showIU()

    def runShift(self):
        if not self.initShift():
            return
        
        sftdir = self.conf['Shift']['sftdir']

        # copy background and dark data (To make same image file type)
        try:
            bgndimg = self.conf['Base']['bgndimg']
            darkimg = self.conf['Base']['darkimg']
        except KeyError:
            bgndimg = ''
            darkimg = ''

        try:
            if bgndimg != '':
                tif = imread(bgndimg)
                imwrite(os.path.join(sftdir, os.path.basename(bgndimg)), tif.to_array(), tif.get_dir())
            if darkimg != '':
                tif = imread(darkimg)
                imwrite(os.path.join(sftdir, os.path.basename(darkimg)), tif.to_array(), tif.get_dir())
            self.shiftimage.shift_all()
        except IOError as e:
            self.msgBox("IOError({0}): {1}".format(e.errno, e.strerror))
        except ValueError:
            self.msgBox("ValueError: " + e.message)

    def msgBox(self, msg):
        msgbox = QtGui.QMessageBox()
        msgbox.setText(msg)
        msgbox.exec_()

class PlotWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(PlotWindow, self).__init__(parent)
        self.fig = Figure(figsize=(600,600), dpi=72, facecolor=(1,1,1), edgecolor=(0,0,0))

    def showIU(self):
        canvas = FigureCanvas(self.fig)
        self.setCentralWidget(canvas)
        self.setWindowTitle('Plot')
        self.show()

    def getFigure(self):
        return self.fig

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
