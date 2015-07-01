import numpy as np
from numpy.testing import assert_allclose

from scipy.ndimage.interpolation import shift
import matplotlib.pyplot as plt

from xni.align import correlation

ntry = 100

def test_corr1d():
    A = np.array([1, 3, 5, 3, 1], dtype=np.double)
    A = np.pad(A, 10, mode='constant', constant_values=1)

    rand = np.zeros(ntry, dtype=np.double)
    corr = np.zeros(ntry, dtype=np.double)

    for i in range(ntry):
        rand[i] = np.ceil(np.random.random()*50.-100.)/10.
        B = shift(A, (rand[i]), mode='constant', cval=1.0)
        corr[i] = correlation.corr1d(A, B)

    assert_allclose(rand, corr, rtol=0, atol=0.1)


def test_corr2d():
    A = np.array([[1, 1, 1, 1, 1],
                  [1, 3, 3, 3, 1],
                  [1, 3, 5, 3, 1],
                  [1, 3, 3, 3, 1],
                  [1, 1, 1, 1, 1]], dtype=np.double)

    A = np.pad(A, 10, mode='constant', constant_values=1)

    rand_dx = np.zeros(ntry, dtype=np.double)
    rand_dy = np.zeros(ntry, dtype=np.double)
    corr_dx = np.zeros(ntry, dtype=np.double)
    corr_dy = np.zeros(ntry, dtype=np.double)

    for i in range(ntry):
        rand_dy[i] = np.ceil(np.random.random()*50.-100.)/10.
        rand_dx[i] = np.ceil(np.random.random()*50.-100.)/10.
        B = shift(A, (rand_dy[i], rand_dx[i]), mode='constant', cval=1.0)
        corr_dy[i], corr_dx[i] = correlation.corr2d(A, B)

    assert_allclose(rand_dx, corr_dx, rtol=0, atol=0.1)
    assert_allclose(rand_dy, corr_dy, rtol=0, atol=0.1)
