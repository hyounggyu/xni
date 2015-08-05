import os

from .. import sample_dir

__all__ = ['samplepath']

def samplepath(f):
    return os.path.join(sample_dir, f)
