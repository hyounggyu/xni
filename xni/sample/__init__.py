import os

from .. import sample_dir

__all__ = ['path']

def path(f):
    return os.path.join(sample_dir, f)
