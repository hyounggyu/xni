import sys

import numpy as np
import h5py
from PyQt4 import QtGui
import pyqtgraph as pg

from .. import dataset


def _swap(data):
    if data.ndim == 2:
        return np.swapaxes(data, 0, 1)
    elif data.ndim == 3:
        return np.swapaxes(data, 1, 2)
    else:
        return None


class ViewWindow(QtGui.QMainWindow):

    def __init__(self, data, parent=None):
        super(ViewWindow, self).__init__(parent)
        imv = pg.ImageView()
        imv.setImage(_swap(data))
        self.setCentralWidget(imv)
        self.setWindowTitle('ImageView')


def show(data):
    app = QtGui.QApplication(sys.argv)
    win = ViewWindow(data)
    win.show()
    win.activateWindow()
    win.raise_()
    return app.exec_()


def start_view(args):
    group_name = 'original' if args.group == None else args.group
    dataset_name = 'images' if args.dataset == None else args.dataset
    data = dataset.load(args.filename, grp=group_name, dset=dataset_name)
    sys.exit(show(data))


def start_remoteview(args):
    host = '127.0.0.1' if args.host == None else args.host
    port = 5051 if args.port == None else args.port
    step = 1 if args.step == None else args.step
    timeout = 10 if args.timeout == None else args.timeout
    print("Connect to {}:{}...".format(host, port))
    try:
        data = dataset.get(index=(0, None, step), host=host, port=port)
    except Exception as e:
        print('Exception: {}'.format(e))
        sys.exit(1)
    print('Data shape: {}'.format(data.shape))
    ret = show(data)
    sys.exit(ret)
