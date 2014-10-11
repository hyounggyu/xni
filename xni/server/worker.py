import errno
import pickle

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
            msg = receiver.recv_pyobj()
        except KeyboardInterrupt:
            break
        task_id, length, data = msg
        for index, args in data.items():
            result = 'filename'
            #tasks.shift_image(*args)
            result_msg = pickle.dumps([task_id, length, {index: result}])
            sender.send(result_msg)


if __name__ == '__main__':
    start()
