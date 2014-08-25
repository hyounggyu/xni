import pickle

import zmq

from . import tasks

def start():
    context = zmq.Context()
    receiver = context.socket(zmq.PULL)
    receiver.connect('tcp://127.0.0.1:9305')

    print('Start XNI worker')

    while True:
        data = receiver.recv()
        args = pickle.loads(data)
        tasks.shift_image(*args)

if __name__ == '__main__':
    start()
