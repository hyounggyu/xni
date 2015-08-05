import numpy as np
import h5py

from xni.sample import samplepath
from xni.align import align_rot_axis

from numpy.testing import assert_allclose


def test_rot_axis():
    f = h5py.File(samplepath('rot420px.h5'),'r')
    data = f['data'][:]
    res = align_rot_axis(data)
    real = -np.array([28.0*np.sin(i*np.pi/90.0) for i in range(91)])
    assert_allclose(real, res, rtol=0, atol=0.02)
