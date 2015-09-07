import numpy as np
from numpy.testing import assert_allclose
from scipy.ndimage.interpolation import shift as ndshift

from xni.adjust import norm

im = np.zeros((5,5), dtype='f4') + 12.0
bg = np.zeros(im.shape, dtype=im.dtype) + 4.0
dk = np.zeros(im.shape, dtype=im.dtype) + 2.0
bp = 1.0
bc = (2.0, 1.0)
r0 = 3.0 # 12.0 / 4.0
r1 = 5.0 # (12.0 - 2.0) / (4.0 - 2.0)
r2 = 4.5 # 12.0 - 1.0; (11.0 - 2.0) / (4.0 - 2.0)
r3 = 9.0 # 12.0 - 1.0; (11.0 - 2.0)

def test_normfunc1():
    '''
    no dark field
    '''
    norm_func = norm.set_normfunc(bg)
    res = norm_func(im)
    real = np.zeros(im.shape, dtype=im.dtype)+r0
    assert_allclose(real, res)

def test_normfunc2():
    norm_func = norm.set_normfunc(bg, dk)
    res1 = norm_func(im)
    res2 = norm_func(im, bp=bp)
    res3 = norm_func(im, bp=bp, bc=bc)
    real1 = np.zeros(im.shape, dtype=im.dtype)+r1
    real2 = np.zeros(im.shape, dtype=im.dtype)+r2
    real3 = ndshift(np.zeros(im.shape, dtype=im.dtype)+r2, bc, mode='constant', cval=r3)
    assert_allclose(real1, res1)
    assert_allclose(real2, res2)
    assert_allclose(real3, res3)

def test_norm_all1():
    norm_func = norm.set_normfunc(bg, dk)
    res = norm.norm_all(np.array([im, im]), bg, dk=dk)
    real = np.zeros(im.shape, dtype=im.dtype)+r1
    real = np.array([real, real])
    assert_allclose(real, res)

def test_norm_all2():
    norm_func = norm.set_normfunc(bg, dk)
    res = norm.norm_all(np.array([im, im]), bg, dk=dk, beam_power=np.array([bp,bp]), beam_center=np.array([bc, bc]), crop=False)
    real = ndshift(np.zeros(im.shape, dtype=im.dtype)+r2, bc, mode='constant', cval=r3)
    real = np.array([real, real])
    assert_allclose(real, res)
