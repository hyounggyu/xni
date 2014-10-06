import errno

import zmq

from . import tasks
from . import config



CONTEXT = zmq.Context()
RECEIVER = CONTEXT.socket(zmq.PULL)
RECEIVER.connect(config.VENTILATOR_URI)
SENDER = CONTEXT.socket(zmq.PUSH)
SENDER.connect(config.SINK_URI)


def start():
    print('Start XNI worker...')

    while True:
        try:
            args = RECEIVER.recv_pyobj()
        except KeyboardInterrupt:
            break
        tasks.shift_image(*args)
        SENDER.send('finish')

if __name__ == '__main__':
    start()
