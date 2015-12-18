import numpy as np
from numpy.testing import assert_allclose
from scipy.ndimage.interpolation import shift as ndshift

from xni.calc import corr


ntry = 100


def test_corr1d():
    A = np.array([1, 3, 5, 3, 1], dtype=np.double)
    A = np.pad(A, 10, mode='constant', constant_values=1)

    ran = np.zeros(ntry, dtype=np.double)
    cor = np.zeros(ntry, dtype=np.double)

    for i in range(ntry):
        ran[i] = np.ceil(np.random.random()*50.-100.)/10.
        B = ndshift(A, (ran[i]), mode='constant', cval=1.0)
        cor[i] = corr.corr1d(A, B)

    assert_allclose(ran, cor, rtol=0, atol=0.1)


def test_corr2d():
    A = np.array([[1, 1, 1, 1, 1],
                  [1, 3, 3, 3, 1],
                  [1, 3, 5, 3, 1],
                  [1, 3, 3, 3, 1],
                  [1, 1, 1, 1, 1]], dtype=np.double)

    A = np.pad(A, 10, mode='constant', constant_values=1)

    ran_dx = np.zeros(ntry, dtype=np.double)
    ran_dy = np.zeros(ntry, dtype=np.double)
    cor_dx = np.zeros(ntry, dtype=np.double)
    cor_dy = np.zeros(ntry, dtype=np.double)

    for i in range(ntry):
        ran_dy[i] = np.ceil(np.random.random()*50.-100.)/10.
        ran_dx[i] = np.ceil(np.random.random()*50.-100.)/10.
        B = ndshift(A, (ran_dy[i], ran_dx[i]), mode='constant', cval=1.0)
        cor_dy[i], cor_dx[i] = corr.corr2d(A, B)

    assert_allclose(ran_dx, cor_dx, rtol=0, atol=0.1)
    assert_allclose(ran_dy, cor_dy, rtol=0, atol=0.1)
