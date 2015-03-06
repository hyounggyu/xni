import os
import h5py

PATH='/Users/hgkim/Data/workspaces/XrayNanoImaging/ipython/sample'

class Dataset:

    def __init__(self):
        # self.hf = h5py.File(os.path.join(PATH,'tm181x400x400.h5'),'r')
        # self.origin = self.hf['original'][:]
        self.hf = h5py.File(os.path.join(PATH,'phantom3d.h5'),'r')
        self.origin = self.hf['Dataset1'][:]
