import collections

import numpy as np


def fromiter(iter_obj, dtype='f4'):
    return np.array(list(iter_obj), dtype=dtype)

def isvector(val):
    return isinstance(val, (collections.Sequence, np.ndarray))
