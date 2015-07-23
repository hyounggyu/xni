import numpy as np

from ..._shared import fromiter


def beam(data, slice_obj, _map=map):
    '''
    return normalised data, average
    '''
    # slice_obj must be tuple
    seq = map(np.average, data[np.index_exp[:] + slice_obj])
    iavg = np.fromiter(seq, dtype=np.double) # intensity average of each image
    iavg = iavg - np.average(iavg) # distance from all average

    mapobj = _map(np.subtract, data, iavg)

    return np.array(list(mapobj)), iavg


def absorp(data, bg, dk=None, _map=map):
    f = lambda im: im / bg
    map_obj = _map(f, data)
    return fromiter(map_obj)
