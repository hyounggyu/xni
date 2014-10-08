import numpy as np
from scipy import linalg


__all__ = ['ccorr2d']

PARABOLOID = None


def limit_abs_one(val):
    return val if np.fabs(val) < 1. else 1.*np.sign(val)


def init_paraboloid():
    global PARABOLOID
    PARABOLOID = np.zeros((9, 6))
    for i in range(9):
        iy, ix = np.unravel_index(i, (3,3))
        ix = ix + 1
        iy = iy + 1
        PARABOLOID[i,:] = ix*ix, iy*iy, ix*iy, ix, iy, 1


def ccorr2d(ref, trans):
    '''2D Cross-correlation with Paraboloid Fitting.

    References:
        Arec3d - https://codeforge.lbl.gov/anonscm/arec3d/trunk/src/align2dstack.c
        SPIDER - http://spider.wadsworth.org/spider_doc/spider/src/parabl.f
    '''
    global PARABOLOID

    if PARABOLOID == None:
        init_paraboloid()

    if np.shape(ref) != np.shape(trans):
        raise ValueError('Arrays shape should be same.')

    ny, nx = np.shape(ref)

    # 2D Cross-correlation
    ccorr = np.fft.ifft2(np.multiply(np.conj(np.fft.fft2(trans)), np.fft.fft2(ref)))
    peak_y, peak_x = np.unravel_index(np.argmax(ccorr), ccorr.shape)

    # Reference: Stack Overflow: 4148292
    # Given a 2D-array, returns an 3x3 array whose "center" element is arr[y,x]
    arr = np.real(np.roll(np.roll(ccorr, shift=-peak_y+1, axis=0), shift=-peak_x+1, axis=1)[:3,:3])

    # Least square fit
    c, resid, rank, sigma = linalg.lstsq(PARABOLOID, arr.flatten())

    # df/dx = 0, df/dy = 0
    ysh, xsh = 0.0, 0.0
    denom = 4*c[0]*c[1]-c[2]*c[2]
    if denom != 0:
        ysh = limit_abs_one((-2*c[0]*c[4]+c[2]*c[3])/denom - 2.)
        xsh = limit_abs_one((-2*c[1]*c[3]+c[2]*c[4])/denom - 2.)

    yt = peak_y + ysh
    xt = peak_x + xsh

    yt = yt if yt < ny/2. else yt - ny
    xt = xt if xt < nx/2. else xt - nx

    return yt, xt
