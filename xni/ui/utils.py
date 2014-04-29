# -*- coding: utf-8 -*-
"""
    xni.utils
    ~~~~~~~~~

    :copyright: (c) 2013 by Hyounggyu Kim.
    :license: GPL, see LICENSE for more details.
"""

import os, re
import numpy as np

def find_tiff_files(_dir, prefix):
    pattern = '^%s.*(tif|tiff)$' % prefix
    match = re.compile(pattern, re.I).match
    fns = []
    for fn in os.listdir(_dir):
        fn = os.path.normcase(fn)
        if match(fn) is not None:
            fns.append(fn)
    return fns

def read_pos_from_csv(fname, angle_field, dx_field, dy_field):
    """read position data"""
    import csv
    with open(fname, 'rbU') as f:
        reader = csv.reader(f)
        pos = []
        valerrors = []
        nrow = 0
        for row in reader:
            try:
                pos.append([float(row[angle_field]), float(row[dx_field]), float(row[dy_field])])
            except ValueError:
                valerrors.append(nrow)
            nrow = nrow + 1
        pos = np.array(pos)
    return pos, valerrors
