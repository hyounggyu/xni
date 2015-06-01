import numpy as np
from scipy.ndimage.interpolation import shift

from xni.align import correlation

np.set_printoptions(precision=3)

A = np.array([1, 3, 5, 3, 1], dtype=np.double)
A = np.pad(A, 10, mode='constant', constant_values=1)

err_x, err_y = 0, 0

DEBUG = False

for _ in range(1000):
    rand = np.ceil(np.random.random()*50.-100.)/10.
    B = shift(A, (rand), mode='constant', cval=1.0)
    corr = correlation.corr1d(A, B)
    if DEBUG == True:
        print (A)
        print (B)
        print (rand)
        print (corr)
        print (np.fabs(rand-corr))
    err_y = err_y + (0 if np.fabs(rand-corr) < 0.1 else 1)

print ('----')
print (err_y, err_x)
