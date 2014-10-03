import os
import json
import pickle
import logging
from multiprocessing import Process, cpu_count
import webbrowser

import zmq

import tornado.web

from . import config
from . import worker

CONTEXT = zmq.Context()
SENDER = CONTEXT.socket(zmq.PUSH)
SENDER.bind('tcp://{}:{}'.format(config.VENTILATOR_HOST, config.VENTILATOR_PORT))


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


def main(HOST='127.0.0.1', PORT=8000):
    app = tornado.web.Application(
        [
            (r'/', MainHandler),
            (r'/shift/', ShiftHandler),
        ],
    )
    webserver_uri = 'http://{}:{}/'.format(config.WEBSERVER_HOST, config.WEBSERVER_PORT)
    app.listen('{}'.format(config.WEBSERVER_PORT))
    # Open web browser
    webbrowser.open_new('{}app/index.html'.format(webserver_uri))
    # Start Tornado
    print('Listen {}...'.format(webserver_uri))
    tornado.ioloop.IOLoop.instance().start()


def start(debug=False):
    if debug:
        print('Start XNI manager...')
        nproc = cpu_count() if cpu_count() < 8 else 8
        for i in range(nproc):
            Process(target=worker.start).start()
    main()
