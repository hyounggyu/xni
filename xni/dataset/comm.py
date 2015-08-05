import socket
import struct
import pickle

import numpy as np


def serve(data, host='', port=5051):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    conn, addr = s.accept()
    print('Connected by', addr)
    r = conn.recv(1024)
    if not r:
        raise RuntimeError("socket connection broken")
    msg = data.dumps()
    length = len(msg)
    conn.send(struct.pack('!Q', length))
    conn.sendall(msg)
    conn.close()


def get(index=(0, None, 1), host='127.0.0.1', port=5051):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    print('send hello')
    s.sendall(b'Hello')
    length = s.recv(struct.calcsize('!Q'))
    length, = struct.unpack('!Q', length)
    data = b''
    recvsize = 0
    while recvsize < length:
        chunk = s.recv(1024)
        if chunk == b'':
            raise RuntimeError("socket connection broken")
        recvsize += len(chunk)
        data += chunk
    s.close()
    return pickle.loads(data)
