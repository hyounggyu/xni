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

FILTERS = {
  'TIFF': 'TIFF image File (*.tif *.tiff)',
  'CSV' : 'Comma Seperated Values File (*.txt *.csv)',
  'CFG' : 'Config file (*.cfg)'
}

class ConfigWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(ConfigWindow, self).__init__(parent)
        self.initConfig()
        self.initUI()

    def initUI(self):
        self.srcdirLabel  = QtGui.QLabel('*Source directory')
        self.srcdirEdit   = QtGui.QLineEdit()
        self.srcdirBtn    = QtGui.QPushButton('Select')

        self.frstimgLabel= QtGui.QLabel('*First image')
        self.frstimgEdit = QtGui.QLineEdit()
        self.frstimgBtn  = QtGui.QPushButton('Select')

        self.lastimgLabel = QtGui.QLabel('*Last image')
        self.lastimgEdit  = QtGui.QLineEdit()
        self.lastimgBtn   = QtGui.QPushButton('Select')

        self.bgndimgLabel = QtGui.QLabel('Background image')
        self.bgndimgEdit  = QtGui.QLineEdit()
        self.bgndimgBtn   = QtGui.QPushButton('Select')

        self.darkimgLabel = QtGui.QLabel('Dark image')
        self.darkimgEdit  = QtGui.QLineEdit()
        self.darkimgBtn   = QtGui.QPushButton('Select')

        self.poscsvLabel  = QtGui.QLabel('Position data')
        self.poscsvEdit   = QtGui.QLineEdit()
        self.poscsvBtn    = QtGui.QPushButton('Select')

        self.loadBtn      = QtGui.QPushButton('Load')
        self.saveBtn      = QtGui.QPushButton('Save')

        self.srcdirEdit.textChanged[str].connect (partial(self.setConfig, 'Base', 'SourceDirectory'))
        self.srcdirEdit.textEdited[str].connect  (partial(self.setConfig, 'Base', 'SourceDirectory'))
        self.srcdirBtn.clicked.connect           (partial(self.selectDirectory, self.srcdirEdit))

        self.frstimgEdit.textChanged[str].connect(partial(self.setConfig, 'Base', 'FirstImage'))
        self.frstimgEdit.textEdited[str].connect (partial(self.setConfig, 'Base', 'FirstImage'))
        self.frstimgBtn.clicked.connect          (partial(self.selectFile, self.frstimgEdit, 'TIFF'))

        self.lastimgEdit.textChanged[str].connect(partial(self.setConfig, 'Base', 'LastImage'))
        self.lastimgEdit.textEdited[str].connect (partial(self.setConfig, 'Base', 'LastImage'))
        self.lastimgBtn.clicked.connect          (partial(self.selectFile, self.lastimgEdit, 'TIFF'))

        self.bgndimgEdit.textChanged[str].connect(partial(self.setConfig, 'Base', 'BackgroundImage'))
        self.bgndimgEdit.textEdited[str].connect (partial(self.setConfig, 'Base', 'BackgroundImage'))
        self.bgndimgBtn.clicked.connect          (partial(self.selectFile, self.bgndimgEdit, 'TIFF'))

        self.darkimgEdit.textChanged[str].connect(partial(self.setConfig, 'Base', 'DarkImage'))
        self.darkimgEdit.textEdited[str].connect (partial(self.setConfig, 'Base', 'DarkImage'))
        self.darkimgBtn.clicked.connect          (partial(self.selectFile, self.darkimgEdit, 'TIFF'))

        self.poscsvEdit.textChanged[str].connect(partial(self.setConfig, 'Base', 'PositionCSVFile'))
        self.poscsvEdit.textEdited[str].connect (partial(self.setConfig, 'Base', 'PositionCSVFile'))
        self.poscsvBtn.clicked.connect          (partial(self.selectFile, self.poscsvEdit, 'CSV'))

        self.loadBtn.clicked.connect(self.loadConfig)

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
        srcdir = self.getConfig('Base', 'SourceDirectory')
        print srcdir
        directory = QtGui.QFileDialog.getExistingDirectory(self, caption='Select directory', dir=srcdir)
        widget.setText(directory)

    def selectFile(self, widget, _filter):
        srcdir = self.getConfig('Base', 'SourceDirectory')
        if _filter in FILTERS.keys():
            _filter = FILTERS[_filter]
        else:
            _filter = ''
        print srcdir, type(srcdir)
        fn, _ = QtGui.QFileDialog.getOpenFileName(self, caption='Select file', dir=srcdir, filter=_filter)
        widget.setText(fn)

    def initConfig(self):
        self.config = ConfigParser.RawConfigParser()

    def getConfig(self, section, option):
        if self.config.has_option(section, option):
            return self.config.get(section, option)
        else:
            return ''

    def setConfig(self, section, option, value):
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, option, value)

    def loadConfig(self):
        srcdir = self.getConfig('Base', 'SourceDirectory')
        fn, _ = QtGui.QFileDialog.getOpenFileName(self, caption="Load configuration", dir=srcdir, filter=FILTERS['CFG'])
        self.config.read(fn)
        self.srcdirEdit.setText ( self.getConfig('Base', 'SourceDirectory') )
        self.frstimgEdit.setText( self.getConfig('Base', 'FirstImage'     ) )
        self.lastimgEdit.setText( self.getConfig('Base', 'LastImage'      ) )
        self.bgndimgEdit.setText( self.getConfig('Base', 'BackgroundImage') )
        self.darkimgEdit.setText( self.getConfig('Base', 'DarkImage'      ) )
        self.poscsvEdit.setText ( self.getConfig('Base', 'PositionCSVFile') )

    def saveConfig(self):
        srcdir = self.getConfig('Base', 'SourceDirectory')
        fn, _ = QtGui.QFileDialog.getSaveFileName(self, caption="Save configuration", dir=srcdir, filter=FILTERS['CFG'])
        f = open(fn, "w")
        self.config.write(f)

    def msgBox(self, msg):
        msgbox = QtGui.QMessageBox()
        msgbox.setText(msg)
        msgbox.exec_()
