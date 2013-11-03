# -*- coding: utf-8 -*-
"""
    xni.normalize
    ~~~~~~~~~~~~~

    :copyright: (c) 2013 by Hyounggyu Kim.
    :license: GPL, see LICENSE for more details.
"""

import os
import numpy as np
from tiff import imread, imwrite

def saturate(pixel):
	return 1. if pixel > 1. else pixel

class Normalize(object):
    def __init__(self, srcdir, tgtdir, fns, bg):
        self.srcdir = srcdir
        self.tgtdir = tgtdir
        self.fns = fns
        self.bg = bg

    def normalize_all(self):
        vsat = np.vectorize(saturate)
        # type casting을 해야하나?
        # why copy False?
        # http://stackoverflow.com/questions/4389517/in-place-type-conversion-of-a-numpy-array
        tif = imread(self.bg)
        img = tif.to_array()
        bg = img.astype(np.float32, copy=False)

        for fn in self.fns:
            tif = imread(os.path.join(self.srcdir, fn))
            img = tif.to_array()
            img = img.astype(np.float32, copy=False)
            img = img / bg
            img = vsat(img)
            img = img*65535.
            img = img.astype(np.uint16, copy=False)
            imwrite(os.path.join(self.tgtdir, fn), img, tif.get_dir())
