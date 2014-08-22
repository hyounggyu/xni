import zmq

def start():
    context = zmq.Context()
    receiver = context.socket(zmq.PULL)
    receiver.connect('tcp://127.0.0.1:9305')

    while True:
        s = receiver.recv_string()
        print(s)

if __name__ == '__main__':
    start()
