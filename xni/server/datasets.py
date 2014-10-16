import glob
import os

from . import config


CACHE_DIR = None


def fetch_cache_dir():
    global CACHE_DIR
    # check cache
    CACHE_DIR = config.CACHE_DIR


def find_dataset():
    global CACHE_DIR
    if CACHE_DIR == None:
        fetch_cache_dir()
    datasets = []
    list = glob.glob1(config.CACHE_DIR, '*.xni')
    for l in list:
        if os.path.isdir(os.path.join(config.CACHE_DIR, l)):
            datasets.append(l[:-4])
    return datasets
