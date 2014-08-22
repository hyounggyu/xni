import logging
from multiprocessing import Process

import zmq

import tornado.web

import worker

class BaseHandler(tornado.web.RequestHandler):
    pass

class MainHandler(BaseHandler):
    def get(self):
        self.write("Hello, world")
        sender.send_string('Hello')

def main():
    app = tornado.web.Application(
        [
            (r'/', MainHandler),
        ],
    )
    app.listen('8000')
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    global sender
    context = zmq.Context()
    sender = context.socket(zmq.PUSH)
    sender.bind('tcp://127.0.0.1:9305')
    p = Process(target=worker.start)
    p.start()
    main()
    p.join()
