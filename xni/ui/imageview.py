from PyQt4 import QtGui
import pyqtgraph as pg

import numpy as np


def swap(im):
    if im.ndim == 2:
        return np.swapaxes(im, 0, 1)
    elif im.ndim == 3:
        return np.swapaxes(im, 1, 2)
    else:
        return None


class ImageViewWindow(QtGui.QMainWindow):

    image = None

    def __init__(self, image, parent=None):
        super(ImageViewWindow, self).__init__(parent)
        self.image = image
        self.initUI()

    def initUI(self):
        imv = pg.ImageView()
        imv.setImage(swap(self.image))
        self.setCentralWidget(imv)
        self.setWindowTitle('ImageView')
        self.show()
