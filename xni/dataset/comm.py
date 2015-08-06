import socket
import struct
import pickle

import numpy as np


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
    r = conn.recv(struct.calcsize('!3i')) # Receive index
    if not r: raise RuntimeError("socket connection broken")
    start, end, step = struct.unpack('!3i', r) # Unpacking three integers
    # end, step values cannot be zero
    end = None if end == 0 else end
    step = None if step == 0 else step
    msg = data[start:end:step].dumps()
    conn.send(struct.pack('!Q', len(msg)))
    conn.sendall(msg)


def get(index=(0, None, 1), host='127.0.0.1', port=5051):
    '''
    index = (start, end, step)
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    # If end and/or step are None, it will be changed zero.
    # zero end/step are unpacked None
    idx = tuple(map(lambda v: int(v or 0), index))
    s.sendall(struct.pack('!3i', *idx)) # Packing three integers
    length = s.recv(struct.calcsize('!Q')) # Receive data length
    length, = struct.unpack('!Q', length)
    data = []
    recvsize = 0
    while recvsize < length:
        chunk = s.recv(1024)
        if chunk == b'':
            raise RuntimeError("socket connection broken")
        recvsize += len(chunk)
        data.append(chunk)
    s.close()
    return pickle.loads(b''.join(data))
