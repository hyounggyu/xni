import logging
from multiprocessing import Process

import zmq

import tornado.web

class BaseHandler(tornado.web.RequestHandler):
    pass

class MainHandler(BaseHandler):
    def get(self):
        self.write("Hello, world")

def main():
    context = zmq.Context()

    sender = context.socket(zmq.PUSH)
    print ('bind...')
    sender.bind('tcp://127.0.0.1:9305')
    sender.send_string('Hello')

def webserver_main():
    app = tornado.web.Application(
        [
            (r'/', MainHandler),
        ],
    )
    app.listen('8000')
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
