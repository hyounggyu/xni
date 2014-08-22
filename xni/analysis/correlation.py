import numpy as np

def ccorr2d(A, B):
    return np.fft.iftt2(np.multiply(np.conj(np.fft.fft2(A)), np.fft.fft2(B)))
