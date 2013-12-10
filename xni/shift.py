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


class ShiftImage:

    def __init__(self, centposarray, startangle, endangle, nangles):
        # pos: numpy array (angle, delta_x, delta_y)
        # NOTE: other interpolation methods are also available
        self.interp_x = interp1d(pos[:,0], pos[:,1])
        self.interp_y = interp1d(pos[:,0], pos[:,2])

        # set angle array
        self.thetas = np.linspace(startangle, endangle, nangles)

    def shift(self, img, theta):
        # x axis : '+' -> left, '-' -> right
        # y axis : '+' -> up, '-' -> down
        return shift(img, (-self.interp_y(theta), -self.interp_x(theta)))
