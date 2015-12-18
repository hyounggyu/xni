import csv
from pathlib import Path

import numpy as np
import h5py
from skimage.external.tifffile import imread


__all__ = ['XNIDataset', 'load_marker_csv', 'create']


class XNIDataset(object):

    _h5 = None

    def __init__(self, fname):
        self._h5 = h5py.File(fname, 'a') # error check

    def __del__(self):
        self._h5.close()

    def load_normed(self):
        return self._h5['/normed/images'][:]

    def load_shifted(self):
        return self._h5['/shifted/images'][:]

    def save_shifted(self, data):
        self._h5.create_dataset('/shifted/images', data=data)

    def get_sinogram(self, data):
        return np.swapaxes(data, 0, 1)


def load_marker_csv(self, fname):
    res = []
    with open(fname, 'r') as csvfile:
        posreader = csv.reader(csvfile, delimiter=',')
        for row in posreader:
            if len(row) == 0:
                continue
            # 1st column is angle theta or projection index
            res.append(list(map(float, row)))
    return np.array(res)


def _create(output, images, bgnds=[], darks=[],
    groupname='original', images_dsetname='images',
    bgnds_dsetname='bgnds', darks_dsetname='darks', dtype='i2', generator=True):

    fd = h5py.File(output, 'w')
    grp = fd.create_group(groupname)

    ny, nx = imread(images[0]).shape # All images are same shape
    if len(bgnds) > 0:
        bgnds_dset = grp.create_dataset(bgnds_dsetname, (len(bgnds), ny, nx), dtype=dtype)
    if len(darks) > 0:
        darks_dset = grp.create_dataset(darks_dsetname, (len(darks), ny, nx), dtype=dtype)
    images_dset = grp.create_dataset(images_dsetname, (len(images), ny, nx), dtype=dtype)

    for i, im in enumerate(bgnds):
        bgnds_dset[i,:,:] = imread(im)[:,:]

    for i, im in enumerate(darks):
        darks_dset[i,:,:] = imread(im)[:,:]

    for i, im in enumerate(images):
        images_dset[i,:,:] = imread(im)[:,:]
        if generator:
            yield i, im


def _findtiff(path, prefix):
    return sorted([p for p in path.iterdir() if p.match(prefix.strip()+'*') and (p.suffix.lower() in ['.tif', '.tiff'])])


def create(path, output, imprefix, bgprefix=None, dkprefix=None):
    path = Path(path)
    images = _findtiff(path, imprefix)
    bgnds = _findtiff(path, bgprefix) if bgprefix != None else []
    darks = _findtiff(path, dkprefix) if dkprefix != None else []
    # TODO: create() will accept pathlib
    images = [str(im) for im in images]
    bgnds = [str(im) for im in bgnds]
    darks = [str(im) for im in darks]
    for i, name in _create(output, images, bgnds, darks):
        print(i, name)
