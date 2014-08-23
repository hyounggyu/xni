import json
import pickle
import logging
from multiprocessing import Process

import zmq

import tornado.web

from . import worker

class BaseHandler(tornado.web.RequestHandler):
    pass

class MainHandler(BaseHandler):
    def get(self):
        self.write("Hello, world")

class ShiftHandler(BaseHandler):
    def get(self):
        self.write('Hello')

    def post(self):
        from .utils import read_position
        config = self.get_arguments('config', None)
        config = json.loads(config[0])

        try:
            imfiles = config['image_files']
            posfile = config['position_file'][0]
            destdir = config['dest_directory'][0]
            imfiles, dx, dy = read_position(imfiles, posfile)
        except Exception as e:
            self.write(e)
            return
        for imfile, dx_, dy_ in zip(imfiles, dx, dy):
            sender.send(pickle.dumps((imfile, dx_, dy_, destdir)))

        files = []
        if 'background_files' in config:
            files.extend(config['background_files'])
        if 'dark_files' in config:
            files.extend(config['dark_files'])
        for file in files:
            sender.send(pickle.dumps((file, 0, 0, destdir)))

        self.write('OK')


def main():
    app = tornado.web.Application(
        [
            (r'/', MainHandler),
            (r'/shift/', ShiftHandler),
        ],
    )
    app.listen('8000')
    tornado.ioloop.IOLoop.instance().start()

def start():
    global sender
    context = zmq.Context()
    sender = context.socket(zmq.PUSH)
    sender.bind('tcp://127.0.0.1:9305')
    for i in range(4):
        Process(target=worker.start).start()
    main()
