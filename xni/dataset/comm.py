import socket
import struct
import pickle

import numpy as np

# First byte is reserved
# Java doen't have unsigned type
DTYPE = '>f4'
ARRINFOTYPE = '!ciii'


def getheader(arr):
    if len(arr.shape) == 2:
        shape = (1,) + arr.shape
    elif len(arr.shape) == 3:
        shape = arr.shape
    else:
        raise TypeError('2d or 3d array only')
    return struct.pack(ARRINFOTYPE, b'\x00', *shape)


def getarrinfo(msg):
    tmp, *shape = struct.unpack(ARRINFOTYPE, msg)
    # Receive only 32bit float type
    dtype = DTYPE
    size = 4
    count = shape[0]*shape[1]*shape[2]
    length = count * size
    return dtype, shape, count, length


def serve(data, host='', port=5051):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print('Listen to {}:{}...'.format(host, port))
    s.listen(1)
    try:
        conn, addr = s.accept()
    except:
        s.close()
        return

    print('Connected by {}'.format(addr))
    r = conn.recv(1) # Wait client
    if not r: raise RuntimeError("socket connection broken")
    conn.send(getheader(data))
    conn.sendall(data.astype(DTYPE).tobytes()) # Big endian 32bit float


def get(host='127.0.0.1', port=5051):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.sendall(b'\x00') # Send hello
    msg = s.recv(struct.calcsize(ARRINFOTYPE)) # Receive data length
    dtype, shape, count, length = getarrinfo(msg)
    data = []
    recvsize = 0
    while recvsize < length:
        chunk = s.recv(1024)
        if chunk == b'':
            raise RuntimeError("socket connection broken")
        recvsize += len(chunk)
        data.append(chunk)
    s.close()
    return np.frombuffer(b''.join(data), dtype=dtype, count=count, offset=0).reshape(shape)
