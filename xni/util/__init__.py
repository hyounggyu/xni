import collections

import numpy as np

def fromiter(iter_obj):
    return np.array(list(iter_obj))

def isvector(val):
    return isinstance(val, (collections.Sequence, np.ndarray))
