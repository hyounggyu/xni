from xni import dataset
from xni import sample

import numpy as np

data = dataset.load(sample.path('rot420px.h5'), dset='data', grp='/')

#arr = np.zeros((3,3,3), dtype='f4')
#arr = arr + 1

dataset.serve(data)
