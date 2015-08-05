import os

from .. import data_dir

__all__ = ['samplepath']

def samplepath(f):
    return os.path.join(data_dir, f)
