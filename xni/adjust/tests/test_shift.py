import numpy as np
from numpy.testing import assert_allclose
from scipy.ndimage.interpolation import shift as ndshift

from xni.adjust import shift

data = np.zeros((3,5,5), dtype='f4') + 3.0

def test_shift_all1():
    res = shift.shift_all(data, crop=False)
    assert_allclose(data, res)
