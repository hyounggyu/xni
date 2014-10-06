import os, sys
import numpy as np

sys.path.append(os.path.join('..','..'))

from xni.align import correlation

A = np.array([[1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1],
              [1, 1, 1, 3, 3],
              [1, 1, 1, 3, 3],
              [1, 1, 1, 1, 1]])

B = np.array([[1, 1, 1, 1, 1],
              [1, 3, 3, 1, 1],
              [1, 3, 3, 1, 1],
              [1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1]])

# expected (1,2)
print (correlation.ccorr2d(A, B))
