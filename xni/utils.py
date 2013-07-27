# -*- coding: utf-8 -*-
"""
    xni.utils
    ~~~~~~~~~~

    :copyright: (c) 2013 by Hyounggyu Kim.
    :license: GPL, see LICENSE for more details.
"""

import os, re

def find_tiff_files(_dir, prefix):
    pattern = '^%s.*(tif|tiff)$' % prefix
    match = re.compile(pattern, re.I).match
    fns = []
    for fn in os.listdir(_dir):
        fn = os.path.normcase(fn)
        if match(fn) is not None:
            fns.append(fn)
    return fns