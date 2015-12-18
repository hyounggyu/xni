import numpy as np
from numpy.testing import assert_allclose
from scipy.ndimage.interpolation import shift as ndshift

from xni.adjust import shift


data = np.zeros((3,5,5), dtype='f4') + 3.0


def test_shift_all1():
    res = shift.shift3d(data)
    real = data
    assert_allclose(data, res)


def test_shift_all2():
    res = shift.shift3d(data, vt=1.5)
    real = data[:,2:,:]
    assert_allclose(real, res)


def test_shift_all3():
    res = shift.shift3d(data, vt=[0.5,1.5,0.75])
    real = data[:,2:,:]
    assert_allclose(real, res)


def test_shift_all4():
    res = shift.shift3d(data, vt=[-0.5,-1.5,0.75])
    real = data[:,1:-2,:]
    assert_allclose(real, res)
