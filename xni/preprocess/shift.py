# -*- coding: utf-8 -*-
"""
    xni.shift
    ~~~~~~~~~

    :copyright: (c) 2014 by Hyounggyu Kim.
    :license: GPL, see LICENSE for more details.
"""

import numpy as np
from scipy.ndimage.interpolation import shift


def shift_image(im, dx, dy):
    return shift(im, (dy, dx))

def sum_x(im):
    return np.sum(im, axis=1)

def vertical_align(im0_y, im_y, start, end, dy_max):
    """
    dy_max: -dy_max <= dy <= dy_max
    """
    corr = np.correlate(im_y[start-dy_max:end+dy_max], im0_y[start:end])
    dy = dy_max - np.argmax(corr)
    return dy
