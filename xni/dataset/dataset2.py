import numpy as np
import h5py


class Dataset:

    fd = None

    def __init__(self, filename):
        self.fd = h5py.File(filename,'r')

    def dataset_list(self):
        list = []
        for name in self.fd.keys():
            list.append(name)
        return list

    def get(self, name):
        return self.fd[name]
