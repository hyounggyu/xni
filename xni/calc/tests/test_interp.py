import numpy as np
from numpy.testing import assert_allclose

from xni.calc import interp


# theta(Degree), center_y, center_x
pos = np.array([ [  0.0,  0.0,  0.0],
                 [ 45.0, 20.0, 10.0],
                 [ 90.0, 30.0, 20.0],
                 [135.0, 20.0, 10.0],
                 [180.0,  0.0,  0.0] ])


def test_interp_center_pos():
    res = interp.interp_center_pos(pos, 11)
    real = np.array([ [  0.,  -8., -16., -22., -26., -30., -26., -22., -16.,  -8.,   0.],
                      [  0.,  -4.,  -8., -12., -16., -20., -16., -12.,  -8.,  -4.,   0.] ])
    assert_allclose(real, res, rtol=0, atol=0.01)
