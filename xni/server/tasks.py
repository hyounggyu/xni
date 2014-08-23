import os

from scipy.ndimage.interpolation import shift

from xni.io.tifffile import *

def shift_image(filename, dx, dy, destdir):
    im = imread(filename)
    dest_filename = os.path.join(destdir, os.path.basename(filename))
    imsave(dest_filename, shift(im, (dy, dx)))
