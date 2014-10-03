import os
import glob
from multiprocessing import Process, cpu_count
import webbrowser

import zmq

import tornado.web

from . import config
from . import worker
from .utils import read_position

CONTEXT = zmq.Context()
SENDER = CONTEXT.socket(zmq.PUSH)
SENDER.bind('tcp://{}:{}'.format(config.VENTILATOR_HOST, config.VENTILATOR_PORT))


class BaseHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


class MainHandler(BaseHandler):
    pass


class ShiftHandler(BaseHandler):
    def post(self):
        imfiles = self.get_argument('imfiles')
        destdir = self.get_argument('destdir')
        posdata = self.get_argument('posdata')

        try:
            imfiles = glob.glob(imfiles)
            imfiles, dx, dy = read_position(imfiles, posdata)
        except Exception as e:
            self.write(e)
            return

        for imfile, dx_, dy_ in zip(imfiles, dx, dy):
            SENDER.send_pyobj((imfile, dx_, dy_, destdir))

        self.write('OK')


class PathHandler(BaseHandler):
    def post(self):
        path = self.get_argument('path')
        dirname = os.path.dirname(path)
        pattern = os.path.basename(path)

        if os.path.isdir(dirname):
            if pattern == '':
                self.write('OK')
            else:
                files = glob.glob1(dirname, pattern)
                self.write('{} files'.format(len(files)))


class NoCacheStaticFileHandler(tornado.web.StaticFileHandler):
    def set_extra_headers(self, path):
        # Disable cache
        self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')


def main():
    static_path = os.path.join(os.path.dirname(__file__), "webapp", "app")
    app = tornado.web.Application(
        [
            (r'/', MainHandler),
            (r'/api/v1/shift/', ShiftHandler),
            (r'/api/v1/path/', PathHandler),
            (r'/app/(.*)', NoCacheStaticFileHandler, {'path': static_path})
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
    print('Start XNI manager...')
    if not debug:
        nproc = cpu_count() if cpu_count() < 8 else 8
        for i in range(nproc):
            Process(target=worker.start).start()
    main()
