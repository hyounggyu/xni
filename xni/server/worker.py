import errno

import zmq

from . import tasks
from . import config


def start():
    context = zmq.Context()
    receiver = context.socket(zmq.PULL)
    receiver.connect(config.VENTILATOR_URI)
    sender = context.socket(zmq.PUSH)
    sender.connect(config.SINK_URI)

    print('Start XNI worker...')

    while True:
        try:
            args = receiver.recv_pyobj()
        except KeyboardInterrupt:
            break
        tasks.shift_image(*args)
        sender.send(b'finish')


if __name__ == '__main__':
    start()
