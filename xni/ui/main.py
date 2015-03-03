# -*- coding: utf-8 -*-

import sys

from PyQt4 import QtGui

from view import ViewWindow

class MainWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.initUI()

    def initUI(self):

        openAction = QtGui.QAction('Open Dataset', self)
        openAction.triggered.connect(self.showViewWindow)
        newAction = QtGui.QAction('New Dataset', self)

        fileMenu = QtGui.QMenu("File", self)
        fileMenu.addAction(openAction)
        fileMenu.addAction(newAction)

        self.menuBar().addMenu(fileMenu)

        self.statusBar().showMessage('Ready')
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('XNI')

    def showViewWindow(self):
        self.viewwindow = ViewWindow(self)
        self.viewwindow.show()


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
