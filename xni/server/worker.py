import pickle

import zmq

from . import tasks
from . import config


VENTILATOR_URI = 'tcp://{}:{}'.format(config.VENTILATOR_HOST, config.VENTILATOR_PORT)

def start():
    context = zmq.Context()
    receiver = context.socket(zmq.PULL)
    receiver.connect(VENTILATOR_URI)

    print('Start XNI worker')

    while True:
        data = receiver.recv()
        args = pickle.loads(data)
        tasks.shift_image(*args)

if __name__ == '__main__':
    start()
