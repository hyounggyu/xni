import errno

import zmq

from . import tasks
from . import config


RECEIVER = None
SENDER = None


def start():
    global RECEIVER, SENDER
    context = zmq.Context()
    RECEIVER = context.socket(zmq.PULL)
    RECEIVER.connect(config.VENTILATOR_URI)
    SENDER = context.socket(zmq.PUSH)
    SENDER.connect(config.SINK_URI)

    print('Start XNI worker...')

    while True:
        try:
            args = RECEIVER.recv_pyobj()
        except KeyboardInterrupt:
            break
        tasks.shift_image(*args)
        SENDER.send(b'finish')


if __name__ == '__main__':
    start()
