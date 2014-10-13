import os
import csv

import numpy as np
from scipy.ndimage.interpolation import shift

from xni.io.tifffile import *
from xni.align import correlation


def shift_image(filename, dy, dx, destdir):
    im = imread(filename)
    dest_filename = os.path.join(destdir, os.path.basename(filename))
    imsave(dest_filename, shift(im, (dy, dx)))
    return dest_filename


def correlation_image(ref_fname, trans_fname):
    dirname = os.path.dirname(ref_fname)
    ref = imread(ref_fname)
    trans = imread(trans_fname)
    dy, dx = correlation.ccorr2d(ref, trans)
    return (dy, dx, dirname)


def correlation_image_final(list):
    dirname = list[0][2]

    posdata = np.zeros((len(list)+1, 3)) # Index, x, y
    posdata[:,0] = np.arange(len(list)+1) # Index
    posdata[0,1:] = 0, 0 # Start from zero
    for i in range(len(list)):
        posdata[i+1,1:] = posdata[i,1:] + np.array([list[i][0], list[i][1]])

    csvfilename = os.path.join(dirname, 'correlation.csv')
    with open(csvfilename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in posdata:
            writer.writerow(row)
