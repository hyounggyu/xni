import os

from .. import data_dir

__all__ = ['datapath']

def datapath(f):
    return os.path.join(data_dir, f)
