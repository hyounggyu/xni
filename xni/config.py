# -*- coding: utf-8 -*-
"""
    xni.config
    ~~~~~~~~~~

    :copyright: (c) 2013 by Hyounggyu Kim.
    :license: GPL, see LICENSE for more details.
"""

from functools import partial
import ConfigParser

import numpy as np

from PySide import QtGui, QtCore


class ConfigWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(ConfigWindow, self).__init__(parent)
        self.initConfig()
        self.initUI()

    def initUI(self):
        self.srcdirLabel  = QtGui.QLabel('*Source directory')
        self.srcdirEdit   = QtGui.QLineEdit()
        self.srcdirEdit.textChanged[str].connect(partial(self.setConfig, 'Base', 'SourceDirectory'))
        self.srcdirEdit.textEdited[str].connect(partial(self.setConfig, 'Base', 'SourceDirectory'))
        self.srcdirBtn    = QtGui.QPushButton('Select')
        self.srcdirBtn.clicked.connect(partial(self.selectDirectory, self.srcdirEdit))

        self.frstimgLabel= QtGui.QLabel('*First image')
        self.frstimgEdit = QtGui.QLineEdit()
        self.frstimgBtn  = QtGui.QPushButton('Select')

        self.lastimgLabel = QtGui.QLabel('*Last image')
        self.lastimgEdit  = QtGui.QLineEdit()
        self.lastimgBtn   = QtGui.QPushButton('Select')

        self.bgndimgLabel = QtGui.QLabel('Background image')
        self.bgndimgEdit  = QtGui.QLineEdit()
        self.bgndimgEdit.textChanged[str].connect(partial(self.setConfig, 'Base', 'BackgroundImage'))
        self.bgndimgEdit.textEdited[str].connect(partial(self.setConfig, 'Base', 'BackgroundImage'))
        self.bgndimgBtn   = QtGui.QPushButton('Select')
        self.bgndimgBtn.clicked.connect(partial(self.selectFile, self.bgndimgEdit, 'TIFF'))

        self.darkimgLabel = QtGui.QLabel('Dark image')
        self.darkimgEdit  = QtGui.QLineEdit()
        self.darkimgEdit.textChanged[str].connect(partial(self.setConfig, 'Base', 'DarkImage'))
        self.darkimgEdit.textEdited[str].connect(partial(self.setConfig, 'Base', 'DarkImage'))
        self.darkimgBtn   = QtGui.QPushButton('Select')
        self.darkimgBtn.clicked.connect(partial(self.selectFile, self.darkimgEdit, 'TIFF'))

        self.poscsvLabel  = QtGui.QLabel('Position data file')
        self.poscsvEdit   = QtGui.QLineEdit()
        self.poscsvEdit.textChanged[str].connect(partial(self.setConfig, 'Base', 'PositionCSVFile'))
        self.poscsvEdit.textEdited[str].connect(partial(self.setConfig, 'Base', 'PositionCSVFile'))
        self.poscsvBtn    = QtGui.QPushButton('Select')
        self.poscsvBtn.clicked.connect(partial(self.selectFile, self.poscsvEdit, 'CSV'))

        self.loadBtn      = QtGui.QPushButton('Load Config')
        self.loadBtn.clicked.connect(self.loadConfig)
        self.saveBtn      = QtGui.QPushButton('Save Config')
        self.saveBtn.clicked.connect(self.saveConfig)

        grid1 = QtGui.QGridLayout()
        grid1.setSpacing(10)
        grid1.addWidget(self.srcdirLabel,   1, 0)
        grid1.addWidget(self.srcdirEdit,    1, 1)
        grid1.addWidget(self.srcdirBtn,     1, 2)
        grid1.addWidget(self.frstimgLabel,  2, 0)
        grid1.addWidget(self.frstimgEdit,   2, 1)
        grid1.addWidget(self.frstimgBtn,    2, 2)
        grid1.addWidget(self.lastimgLabel,  3, 0)
        grid1.addWidget(self.lastimgEdit,   3, 1)
        grid1.addWidget(self.lastimgBtn,    3, 2)
        grid1.addWidget(self.bgndimgLabel,  4, 0)
        grid1.addWidget(self.bgndimgEdit,   4, 1)
        grid1.addWidget(self.bgndimgBtn,    4, 2)
        grid1.addWidget(self.darkimgLabel,  5, 0)
        grid1.addWidget(self.darkimgEdit,   5, 1)
        grid1.addWidget(self.darkimgBtn,    5, 2)
        grid1.addWidget(self.poscsvLabel,   6, 0)
        grid1.addWidget(self.poscsvEdit,    6, 1)
        grid1.addWidget(self.poscsvBtn,     6, 2)
        group1 = QtGui.QGroupBox('Base Configuration')
        group1.setLayout(grid1)

        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(self.loadBtn)
        hbox1.addWidget(self.saveBtn)

        centralWidget = QtGui.QWidget(self)
        vbox = QtGui.QVBoxLayout(centralWidget)
        vbox.addStretch(1)
        vbox.addWidget(group1)
        vbox.addLayout(hbox1)
        self.setCentralWidget(centralWidget)

    def selectDirectory(self, widget):
        directory = QtGui.QFileDialog.getExistingDirectory(self,
            caption='Select directory', dir=self.getConfig('Base', 'SourceDirectory'))
        widget.setText(directory)

    def selectFile(self, widget, _filter):
        if _filter == 'TIFF':
            _filter = 'TIFF image File (*.tif *.tiff)'
        elif _filter == 'CSV':
            _filter = 'Comma Seperated Values File (*.txt *.csv)'
        else:
            _filter = ''
        fname, _ = QtGui.QFileDialog.getOpenFileName(self,
            caption='Select file', dir=self.getConfig('Base', 'SourceDirectory'), filter=_filter)
        widget.setText(fname)

    def initConfig(self):
        self.config = ConfigParser.RawConfigParser()

    def getConfig(self, section, key):
        return self.config.get(section, key)

    def setConfig(self, section, key, value):
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, value)

    def loadConfig(self):
        fn, _ = QtGui.QFileDialog.getOpenFileName(self,
            caption="Load configuration", dir=self.getConfig('Base', 'SourceDirectory'), filter="Config file (*.cfg)")

        self.config.read(fn)

        self.srcdirEdit.setText ( self.getConfig('Base', 'SourceDirectory') )
        self.bgndimgEdit.setText( self.getConfig('Base', 'BackgroundImage') )
        self.darkimgEdit.setText( self.getConfig('Base', 'DarkImage'      ) )
        self.poscsvEdit.setText ( self.getConfig('Base', 'PositionCSVFile') )

    def saveConfig(self):
        fn, _ = QtGui.QFileDialog.getSaveFileName(self,
            caption="Save configuration", dir=config('Base', 'SourceDirectory'), filter="Config file (*.cfg)")
        f = open(fn, "w")
        self.config.write(f)
