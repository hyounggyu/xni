import numpy as np
from scipy import linalg

__all__ = ['corr1d', 'corr2d']


def _limit_abs_one(val):
    return val if np.fabs(val) < 1. else 1.*np.sign(val)


def corr1d(ref, trans):
    '''1D Cross-correlation with Curve Fitting.
    '''
    if np.shape(ref) != np.shape(trans):
        raise ValueError('Arrays shape should be same.')

    n, = np.shape(ref)

    corr = np.fft.ifft(np.multiply(np.conj(np.fft.fft(ref)), np.fft.fft(trans)))
    peak, = np.unravel_index(np.argmax(corr), corr.shape)
    arr = np.real(np.roll(corr, shift=-peak+1)[:3])

    sh = 0.0
    if arr[0]+arr[2] != 2.*arr[1]:
        sh = (arr[0]-arr[2]) / (2.*(arr[0]-2.*arr[1]+arr[2]))

    t = peak + _limit_abs_one(sh)
    t = t if t < n/2. else t - n

    return t


def _init_paraboloid():
    paraboloid = np.zeros((9, 6))
    for i in range(9):
        iy, ix = np.unravel_index(i, (3,3))
        ix = ix + 1
        iy = iy + 1
        paraboloid[i,:] = ix*ix, iy*iy, ix*iy, ix, iy, 1
    return paraboloid


PARABOLOID = _init_paraboloid()


def corr2d(ref, trans):
    '''2D Cross-correlation with Paraboloid Fitting.

    References:
        Arec3d - https://codeforge.lbl.gov/anonscm/arec3d/trunk/src/align2dstack.c
        SPIDER - http://spider.wadsworth.org/spider_doc/spider/src/parabl.f
    '''
    global PARABOLOID

    if np.shape(ref) != np.shape(trans):
        raise ValueError('Arrays shape should be same.')

    ny, nx = np.shape(ref)

    # 2D Cross-correlation
    corr = np.fft.ifft2(np.multiply(np.conj(np.fft.fft2(ref)), np.fft.fft2(trans)))
    peak_y, peak_x = np.unravel_index(np.argmax(corr), corr.shape)

    # Reference: Stack Overflow: 4148292
    # Given a 2D-array, returns an 3x3 array whose "center" element is arr[y,x]
    arr = np.real(np.roll(np.roll(corr, shift=-peak_y+1, axis=0), shift=-peak_x+1, axis=1)[:3,:3])

    # Least square fit
    c, resid, rank, sigma = linalg.lstsq(PARABOLOID, arr.flatten())

    # df/dx = 0, df/dy = 0
    ysh, xsh = 0.0, 0.0
    denom = 4*c[0]*c[1]-c[2]*c[2]
    if denom != 0:
        ysh = _limit_abs_one((-2*c[0]*c[4]+c[2]*c[3])/denom - 2.)
        xsh = _limit_abs_one((-2*c[1]*c[3]+c[2]*c[4])/denom - 2.)

    yt = peak_y + ysh
    xt = peak_x + xsh

    yt = yt if yt < ny/2. else yt - ny
    xt = xt if xt < nx/2. else xt - nx

    return yt, xt
