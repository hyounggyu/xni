# -*- coding: utf-8 -*-
"""
    xni.normalize
    ~~~~~~~~~~~~~

    :copyright: (c) 2014 by Hyounggyu Kim.
    :license: GPL, see LICENSE for more details.
"""

import os
import numpy as np


class NormalizeImage:

    def __init__(self, bgimg):
        self.bgimg = bgimg.astype(np.float32, copy=False)
        self.vsat = np.vectorize(self.saturate)

    def norm(self, img):
        return vsat(img / bg)

    def saturate(self, pixel):
        return 1. if pixel > 1. else pixel
