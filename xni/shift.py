# -*- coding: utf-8 -*-
"""
    xni.shift
    ~~~~~~~~~

    :copyright: (c) 2013 by Hyounggyu Kim.
    :license: GPL, see LICENSE for more details.
"""

import os
import numpy as np
from scipy.interpolate import interp1d
from scipy.ndimage.interpolation import shift
#from tiff import imread, imwrite
from skimage import io

class ShiftImage:
    def __init__(self, srcdir, tgtdir, fns, pos):
        self.srcdir = srcdir
        self.tgtdir = tgtdir
        self.fns = fns
        self.pos = pos

        # other interpolation methods are available
        self.interp_x = interp1d(self.pos[:,0], self.pos[:,1])
        self.interp_y = interp1d(self.pos[:,0], self.pos[:,2])

        # set angle array
        self.thetas = np.linspace(self.pos[0,0], self.pos[-1,0], len(self.fns))

    def shift_img(self, img, theta):
        # x axis : '+' -> left, '-' -> right
        # y axis : '+' -> up, '-' -> down
        return shift(img, (-1.*self.interp_y(theta), -1.*self.interp_x(theta)))

    def shift_all(self):
        for fn, theta in zip(self.fns, self.thetas):
            im = io.imread(os.path.join(self.srcdir, fn))
            im = self.shift_img(im, theta)
            io.imsave(os.path.join(self.tgtdir, fn), im)

    def get_pos(self):
        return self.pos

    def get_interp(self):
        return self.interp_x, self.interp_y

    def get_thetas(self):
        return self.thetas
