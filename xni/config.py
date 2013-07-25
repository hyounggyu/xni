# -*- coding: utf-8 -*-
from PySide import QtGui
import sys, os, glob

def Config():
    config = {}

    # set source image directory
    config['src_dir'] = QtGui.QFileDialog.getExistingDirectory( \
        caption="Select source image directory")

    # set background file
    config['bgnd_fname'], ok = QtGui.QFileDialog.getOpenFileName( \
        caption="Select background image file", \
        filter="TIFF image Files (*.tif *.tiff)")
    if not ok:
        return False

    # set dark image file
    config['dark_fname'], ok = QtGui.QFileDialog.getOpenFileName( \
        caption="Select dark image file", \
        filter="TIFF image Files (*.tif *.tiff)")
    # no dark image
    if not ok:
        config['dark_fname'] = ''

    # set image prefix and name of image files
    config['prefix'], ok = QtGui.QInputDialog.getText(None, \
        "Input image prefix", "Set prefix")
    if not ok or config['prefix'] == u'':
        return False
    # it matches not only "tif" but also "tif?"
    # and it assumes all images are same rotation angle.
    fnames = glob.glob(os.path.join(config['src_dir'], config['prefix']+"*.tif?"))
    config['img_fnames'] = sorted([ os.path.basename(fname) for fname in fnames ])

    # set position file
    config['pos_fname'], ok = QtGui.QFileDialog.getOpenFileName( \
        caption="Select position data file", \
        filter="Text Files (*.txt *.csv)")
    if not ok:
        return False

    # set shifted directory
    config['sft_dir'] = QtGui.QFileDialog.getExistingDirectory( \
        caption="Select shifted image directory")

    return config

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    c = Config()
