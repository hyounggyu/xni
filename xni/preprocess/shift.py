# -*- coding: utf-8 -*-
"""
    xni.shift
    ~~~~~~~~~

    :copyright: (c) 2014 by Hyounggyu Kim.
    :license: GPL, see LICENSE for more details.
"""

from scipy.ndimage.interpolation import shift

def shift_image(im, dx, dy):
    return shift(im, (dy, dy))
