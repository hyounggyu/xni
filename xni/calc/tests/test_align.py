import numpy as np
from numpy.testing import assert_allclose

from xni import sample
from xni import dataset
from xni.calc import align

def test_valign():
    data = dataset.load(sample.path('rot420px.h5'), grp='/', dset='data')
    res = align.valign(data)
    real = np.array([28.0*np.sin(i*np.pi/90.0) for i in range(91)])
    assert_allclose(real, res, rtol=0, atol=0.2)
