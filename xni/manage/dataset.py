import h5py
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

def _findtiff(path, prefix):
    return sorted([p for p in path.iterdir() if p.match(prefix.strip()+'*') and (p.suffix.lower() in ['.tif', '.tiff'])])

def start_create(args):
    path = Path(args.path)
    images = _findtiff(path, args.image_prefix)
    bgnds = _findtiff(path, args.background_prefix) if args.background_prefix != None else []
    darks = _findtiff(path, args.dark_prefix) if args.dark_prefix != None else []
    # TODO: dataset.create will accept pathlib
    images = [str(im) for im in images]
    bgnds = [str(im) for im in bgnds]
    darks = [str(im) for im in darks]
    for i, name in create(args.output, images, bgnds, darks):
        print(i, name)

def load(filename, grp='original', dset='images'):
    '''
    default datatype is double
    '''
    with h5py.File(filename, 'r') as f:
        dset = f[grp][dset]
        with dset.astype('double'):
            out = dset[:]
    return out

def send(*dsets, ip='127.0.0.1', port='5550'):
    context = zmq.Context()

    with context.socket(zmq.REP) as socket:
        socket.bind('tcp://{}:{}'.format(ip, port))
        index = socket.recv_pyobj()
        for dset in dsets[:-1]:
            socket.send_pyobj(dset[index], flags=zmq.SNDMORE)
        socket.send_pyobj(dsets[-1][index])
        socket.recv() # wait bye message


def recv(index=None, ip='127.0.0.1', port='5550', timeout=10):
    '''
    timeout = unit sec
    '''
    if index == None:
        index = np.index_exp[0:1]

    with zmq.Context() as context:
        with context.socket(zmq.REQ) as socket:
            # https://github.com/zeromq/pyzmq/issues/132
            socket.setsockopt(zmq.LINGER, 0)
            socket.connect('tcp://{}:{}'.format(ip, port))
            socket.send_pyobj(index)
            poller = zmq.Poller()
            poller.register(socket, zmq.POLLIN)
            if poller.poll(timeout*1000):
                parts = [socket.recv_pyobj()]
            else:
                raise IOError('Timeout reciving data')
            while socket.getsockopt(zmq.RCVMORE):
                part = socket.recv_pyobj()
                parts.append(part)
            socket.send(b'BYE')
    return parts
