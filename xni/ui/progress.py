# -*- coding: utf-8 -*-

import os

from PyQt4 import QtGui, QtCore, uic


class progressWindow(QtGui.QMainWindow):

    step = 0

    def __init__(self, async_result, parent=None):
        super(progressWindow, self).__init__(parent)

        self.parent = parent
        self.ar = async_result
        self.initUI()

    def initUI(self):
        uic.loadUi(os.path.join('xni', 'ui', 'progresswindow.ui'), self)

        self.stopButton.clicked.connect(self.stop)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timerEvent)
        self.timer.start(1000)
        self.parent.setEnabled(False)
        self.setEnabled(True)
        self.show()

    def timerEvent(self):
        if self.step >= 100.0:
            self.timer.stop()
            self.parent.setEnabled(True)
            self.close()
            return
        self.step = 100.0 * self.ar.progress / len(self.ar)
        self.progressBar.setValue(self.step)

    def stop(self):
        self.timer.stop()
        self.ar.abort()
        self.parent.setEnabled(True)
        self.close()
