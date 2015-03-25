# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore


class progressWindow(QtGui.QMainWindow):

    def __init__(self, async_result, parent=None):
        super(progressWindow, self).__init__(parent)

        self.parent = parent
        self.ar = async_result
        self.initUI()

    def initUI(self):

        self.pbar = QtGui.QProgressBar(self)
        self.pbar.setGeometry(30, 40, 200, 25)

        self.btn = QtGui.QPushButton('Stop', self)
        self.btn.move(40, 80)
        self.btn.clicked.connect(self.stop)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timerEvent)
        self.step = 0

        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('QtGui.QProgressBar')

        self.timer.start(1000)
        self.parent.setEnabled(False)
        self.setEnabled(True)
        self.show()

    def timerEvent(self):

        print(self.ar.progress)

        if self.step >= 100.0:

            self.timer.stop()
            self.parent.setEnabled(True)
            self.close()
            return

        self.step = 100.0 * self.ar.progress / len(self.ar)
        self.pbar.setValue(self.step)

    def stop(self):

        self.timer.stop()
        self.ar.abort()
        self.parent.setEnabled(True)
        self.close()
