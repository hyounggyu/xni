import os, sys

import numpy as np

sys.path.append('../io')

from tifffile import *

if not os.path.exists('sample'):
    os.mkdir('sample')

max_value = 2**16-1 # uint16

for i in range(361):
    arr = np.zeros(361, dtype=np.uint16)
    arr[i] = max_value
    imsave('sample/test-{0:03d}.tif'.format(i), arr.reshape((19,19)))
