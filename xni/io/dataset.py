import h5py
from skimage.external.tifffile import imread


def create(output, images, bgnds=[], darks=[],
    groupname='original', images_dsetname='images',
    bgnds_dsetname='bgnds', darks_dsetname='darks', dtype='i2', generator=True):

    fd = h5py.File(output, 'w')
    grp = fd.create_group(groupname)

    ny, nx = imread(images[0]).shape # All images are same shape
    if len(bgnds) > 0:
        bgnds_dset = grp.create_dataset(bgnds_dsetname, (len(bgnds), ny, nx), dtype=dtype)
    if len(darks) > 0:
        darks_dset = grp.create_dataset(darks_dsetname, (len(darks), ny, nx), dtype=dtype)
    images_dset = grp.create_dataset(images_dsetname, (len(images), ny, nx), dtype=dtype)

    for i, im in enumerate(bgnds):
        bgnds_dset[i,:,:] = imread(im)[:,:]

    for i, im in enumerate(darks):
        darks_dset[i,:,:] = imread(im)[:,:]

    for i, im in enumerate(images):
        images_dset[i,:,:] = imread(im)[:,:]
        if generator:
            yield i, im

def load(filename, grp='original', dset='images'):
    '''
    default datatype is double
    '''
    with h5py.File(filename, 'r') as f:
        dset = f[grp][dset]
        with dset.astype('double'):
            out = dset[:]
    return out

def send(dset, ip='127.0.0.1', port='5550'):
    import zmq
    context = zmq.Context()

    print('Listen to {}:{}'.format(ip, port))
    socket  = context.socket(zmq.REP)
    socket.bind('tcp://{}:{}'.format(ip, port))

    message = socket.recv()
    print(message)
    socket.send(dset[0].dumps())

def recv(ip='127.0.0.1', port='5550'):
    import zmq
    import numpy as np

    context = zmq.Context()

    print('Connecting to {}:{}'.format(ip, port))
    socket = context.socket(zmq.REQ)
    socket.connect('tcp://{}:{}'.format(ip, port))

    socket.send(b'Hello')

    message = socket.recv()
    return np.loads(message)
