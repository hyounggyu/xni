# -*- coding: utf-8 -*-
"""
    xni.shift
    ~~~~~~~~~

    :copyright: (c) 2013 by Hyounggyu Kim.
    :license: GPL, see LICENSE for more details.
"""

import tiff, config
import numpy as np
from scipy.interpolate import interp1d
from scipy.ndimage.interpolation import shift
import matplotlib.pyplot as plt
import sys, os, re
from PySide import QtGui

class ShiftImage:
    def __init__(self, conf=''):
        self.conf = config.Config() if conf == '' else conf
        self.read_pos()

    def read_pos(self):
        # read position data
        f = open(self.conf['pos_fname'], 'U')
        lines = f.readlines()
        # comma seperated 5 numbers
        pattern = r'(-*[\d.]+),+(-*[\d.]+),+(-*[\d.]+),+(-*[\d.]+),+(-*[\d.]+),*'
        prog = re.compile(pattern)
        pos = []
        for line in lines:
            m = prog.match(line)
            if m == None:
                continue
            pos.append([float(m.group(1)), float(m.group(4)), float(m.group(5))])
        self.pos = np.array(pos)
        # other interpolation methods are available
        self.interp_x = interp1d(self.pos[:,0], self.pos[:,1])
        self.interp_y = interp1d(self.pos[:,0], self.pos[:,2])        
        # set angle array
        self.thetas = np.linspace(self.pos[0,0], self.pos[-1,0], len(self.conf['img_fnames']))
    
    def plot_pos(self):
        new = np.linspace(self.thetas[0], self.thetas[-1], 900)
        plt.plot(self.pos[:,0], self.pos[:,1], 'x', self.pos[:,0], self.pos[:,2], 'o')
        plt.plot(new, self.interp_x(new))
        plt.plot(new, self.interp_y(new))
        plt.show()

    def shift_img(self, img, theta):
        # x axis : '+' -> left, '-' -> right
        # y axis : '+' -> up, '-' -> down
        return shift(img, (-1.*self.interp_y(theta), -1.*self.interp_x(theta)))

    def shift_all(self):
        # copy background and dark data (To make same image file type)
        tif = tiff.imread(self.conf['bgnd_fname'])
        tiff.imwrite(os.path.join(self.conf['sft_dir'],\
            os.path.basename(self.conf['bgnd_fname'])),\
            tif.to_array(), tif.get_dir())

        if self.conf['dark_fname'] != '':
            tif = tiff.imread(self.conf['dark_fname'])
            tiff.imwrite(os.path.join(self.conf['sft_dir'],\
                os.path.basename(self.conf['dark_fname'])),\
                tif.to_array(), tif.get_dir())
            
        for fname, theta in zip(self.conf['img_fnames'], self.thetas):
            tif = tiff.imread(os.path.join(self.conf['src_dir'], fname))
            img = self.shift_img(tif.to_array(), theta)
            tiff.imwrite(os.path.join(self.conf['sft_dir'], fname),\
                img, tif.get_dir())

    def get_config(self):
        return self.c

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    s = ShiftImage()
    s.plot_pos()
    s.shift_all()
