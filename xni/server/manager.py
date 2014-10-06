import os
import csv
import glob
from multiprocessing import Process, cpu_count
import webbrowser

import zmq

# https://github.com/ipython/ipython/blob/master/IPython/html/notebookapp.py
# Install the pyzmq ioloop. This has to be done before anything else from
# tornado is imported.
from zmq.eventloop import ioloop
from zmq.eventloop import zmqstream
ioloop.install()

import tornado.web

from . import config
from . import worker
from .utils import interp_position


SENDER = None
STREAM = None


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
            reader = csv.reader(posdata.splitlines())
            pos = []
            for row in reader:
                pos.append([float(row[0]), float(row[1]), float(row[2])])
            dx, dy = interp_position(len(imfiles), pos)
        except Exception as e:
            self.write(str(e))
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


def status(msg):
    print(msg)


def service_web():
    static_path = os.path.join(os.path.dirname(__file__), "html")
    app = tornado.web.Application(
        [
            (r'/', MainHandler),
            (r'/api/v1/shift/', ShiftHandler),
            (r'/api/v1/path/', PathHandler),
            (r'/app/(.*)', NoCacheStaticFileHandler, {'path': static_path})
        ],
    )
    app.listen(config.WEBSERVER_PORT)


def service_zmq():
    global SENDER, STREAM
    context = zmq.Context()
    SENDER = context.socket(zmq.PUSH)
    SENDER.bind(config.VENTILATOR_URI)
    receiver = context.socket(zmq.PULL)
    receiver.bind(config.SINK_URI)
    STREAM = zmqstream.ZMQStream(receiver)
    STREAM.on_recv(status)


def start():
    print('Start XNI manager...')
    if True:
        nproc = cpu_count() if cpu_count() < 8 else 8
        for i in range(nproc):
            Process(target=worker.start).start()
    service_zmq()
    service_web()
    if False:
        webbrowser.open_new(config.WEBSERVER_URI)
    try:
        ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        pass
