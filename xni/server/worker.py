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

        task_id, task_name, length, args_dict, task_final = msg
        task_function = getattr(tasks, task_name)
        for index, args in args_dict.items():
            result = task_function(*args)
            sender.send(pickle.dumps([task_id, task_name, length, {index: result}, task_final]))


if __name__ == '__main__':
    start()
