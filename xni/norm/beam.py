import numpy as np

def norm_beam(data, slice_obj, _map=map):
    '''
    return normalised data, average
    '''
    # slice_obj must be tuple
    seq = map(np.average, data[np.index_exp[:] + slice_obj])
    iavg = np.fromiter(seq, dtype=np.double) # intensity average of each image
    iavg = iavg - np.average(iavg) # distance from all average

    mapobj = _map(np.subtract, data, iavg)

    return np.array(list(mapobj)), iavg
