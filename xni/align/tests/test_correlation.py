import numpy as np
from scipy.ndimage.interpolation import shift
import matplotlib.pyplot as plt

from xni.align import correlation

np.set_printoptions(precision=3)


def test_corr1d():
    A = np.array([1, 3, 5, 3, 1], dtype=np.double)
    A = np.pad(A, 10, mode='constant', constant_values=1)
    err_count = 0
    ntry = 1000

    for _ in range(ntry):
        rand = np.ceil(np.random.random()*50.-100.)/10.
        B = shift(A, (rand), mode='constant', cval=1.0)
        corr = correlation.corr1d(A, B)
        err_count = err_count + (0 if np.fabs(rand-corr) < 0.1 else 1)

    print ('----')
    print (err_count)


def test_corr2d():
    A = np.array([[1, 1, 1, 1, 1],
                  [1, 3, 3, 3, 1],
                  [1, 3, 5, 3, 1],
                  [1, 3, 3, 3, 1],
                  [1, 1, 1, 1, 1]], dtype=np.double)

    A = np.pad(A, 10, mode='constant', constant_values=1)

    err_x, err_y = 0, 0
    ntry = 1000

    for _ in range(ntry):
        rand_dy = np.ceil(np.random.random()*50.-100.)/10.
        rand_dx = np.ceil(np.random.random()*50.-100.)/10.
        B = shift(A, (rand_dy, rand_dx), mode='constant', cval=1.0)
        corr_dy, corr_dx = correlation.corr2d(A, B)
        err_y = err_y + (0 if np.fabs(rand_dy-corr_dy) < 0.1 else 1)
        err_x = err_x + (0 if np.fabs(rand_dx-corr_dx) < 0.1 else 1)

    print ('----')
    print (err_y, err_x)

# ValueError
#print (correlation.corr2d(A, C))
