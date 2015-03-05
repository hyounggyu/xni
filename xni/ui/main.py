# -*- coding: utf-8 -*-

import sys

from PyQt4 import QtGui, uic

from view import ViewWindow

class MainWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.initUI()

    def initUI(self):
        uic.loadUi('mainwindow.ui', self)
        self.viewButton.clicked.connect(self.showViewWindow)

    def showViewWindow(self):
        viewwindow = ViewWindow(self)
        viewwindow.show()


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
