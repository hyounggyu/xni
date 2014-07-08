# -*- coding: utf-8 -*-
"""
    xni.normalize
    ~~~~~~~~~~~~~

    :copyright: (c) 2014 by Hyounggyu Kim.
    :license: GPL, see LICENSE for more details.
"""

import numpy as np


def normalize(bg, im):
    return np.log(im / bg)
