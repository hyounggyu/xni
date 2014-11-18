import glob
import os
import io
import shutil

import numpy as np

from ..io.tifffile import *
from . import config


__all__ = ['list_datasets', 'create_dataset', 'remove_dataset']

def fetch_dataset_dir(name):
    return os.path.join(config.CACHE_DIR, name+'.xni')


def list_datasets():
    datasets = []
    list = glob.glob1(config.CACHE_DIR, '*.xni')
    for l in list:
        if os.path.isdir(os.path.join(config.CACHE_DIR, l)):
            datasets.append({'name': l[:-4]})
    return datasets


def create_dataset(name, projections):
    cache = fetch_dataset_dir(name)
    if os.path.exists(cache):
        raise Exception('Dataset already exists')
    else:
        os.mkdir(cache)
    filename = os.path.join(cache, 'original.dat')

    stream = io.BytesIO(projections[0]['body'])
    tif = TiffFile(stream, name=projections[0]['filename'])
    im = tif.asarray()
    height, width = np.shape(im)
    max_value = 2**(tif.pages[0].bits_per_sample) - 1 # uint8 or uin16
    nproj = len(projections)
    fp = np.memmap(filename, dtype=np.double, mode='w+', shape=(nproj, height, width))

    for i in range(0, nproj):
        stream = io.BytesIO(projections[i]['body'])
        tif = TiffFile(stream, name=projections[i].filename)
        im = tif.asarray().astype(np.double, copy=False) / max_value
        fp[i] = im


def remove_dataset(name):
    cache = fetch_dataset_dir(name)
    shutil.rmtree(cache)
