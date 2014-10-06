import numpy as np
from scipy import linalg


__all__ = ['ccorr2d']

PARABOLOID = None


def limit_abs_one(val):
    return val if np.fabs(val) < 1. else 1.*np.sign(val)


def ccorr2d(ref, trans):
    '''2D Cross-correlation with Paraboloid Fitting.

    References:
        Arec3d
        SPIDER - http://spider.wadsworth.org/spider_doc/spider/src/parabl.f
        http://stackoverflow.com/questions/4148292/how-do-i-select-a-window-from-a-numpy-array-with-periodic-boundary-conditions
    '''
    global PARABOLOID

    # 2D Cross-correlation
    ccorr = np.fft.ifft2(np.multiply(np.conj(np.fft.fft2(trans)), np.fft.fft2(ref)))
    peak_y, peak_x = np.unravel_index(np.argmax(ccorr), ccorr.shape)

    # Given a 2D-array, returns an 3x3 array whose "center" element is arr[y,x]
    arr = np.real(np.roll(np.roll(ccorr, shift=-peak_y+1, axis=0), shift=-peak_x+1, axis=1)[:3,:3])

    if PARABOLOID == None:
        PARABOLOID = np.zeros((9, 6))
        for i in range(9):
            iy, ix = np.unravel_index(i, (3,3))
            ix = ix + 1
            iy = iy + 1
            PARABOLOID[i,:] = ix*ix, iy*iy, ix*iy, ix, iy, 1

    # Least square fit
    c, resid, rank, sigma = linalg.lstsq(PARABOLOID, arr.flatten())

    # df/dx = 0, df/dy = 0
    denom = 4*c[0]*c[1]-c[2]*c[2]
    if denom == 0:
        raise ValueError('Denominator is zero')
    ysh = limit_abs_one((-2*c[0]*c[4]+c[2]*c[3])/denom - 2.)
    xsh = limit_abs_one((-2*c[1]*c[3]+c[2]*c[4])/denom - 2.)

    return peak_y+ysh, peak_x+xsh
