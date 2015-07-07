import h5py
import msgpack
import numpy as np
from skimage.external.tifffile import imread
import zmq


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
    context = zmq.Context()

    print('Listen to {}:{}'.format(ip, port))
    with context.socket(zmq.REP) as socket:
        socket.bind('tcp://{}:{}'.format(ip, port))
        while True:
            message = socket.recv()
            start, end, step = msgpack.unpackb(message)
            if start < 0:
                break
            socket.send(dset[start:end:step].dumps())

def recv(_slice=(0,1,1), ip='127.0.0.1', port='5550'):
    context = zmq.Context()

    print('Connecting to {}:{}'.format(ip, port))
    with context.socket(zmq.REQ) as socket:
        socket.connect('tcp://{}:{}'.format(ip, port))
        socket.send(msgpack.packb(_slice))
        message = socket.recv()

    return np.loads(message)

def bye(ip='127.0.0.1', port='5550'):
    context = zmq.Context()
    print('Bye! to {}:{}'.format(ip, port))
    with context.socket(zmq.REQ) as socket:
        socket.connect('tcp://{}:{}'.format(ip, port))
        socket.send(msgpack.packb([-1,0,0]))
