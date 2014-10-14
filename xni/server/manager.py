import os
import csv
import glob
import multiprocessing
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
from .comm import scatter, gather, get_status_json
from ..align.interpolation import interp_position


SENDER = None
STREAM = None


class BaseHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


class MainHandler(BaseHandler):
    pass


class ShiftHandler(BaseHandler):
    def post(self):
        imfiles_pattern = self.get_argument('imfiles')
        destdir = self.get_argument('destdir')
        posdata = self.get_argument('posdata')

        try:
            imfiles = glob.glob(imfiles_pattern)
            reader = csv.reader(posdata.splitlines())
            pos = []
            for row in reader:
                pos.append([float(row[0]), float(row[1]), float(row[2])])
            dx, dy = interp_position(len(imfiles), pos)
        except Exception as e:
            self.write(str(e))
            return

        args_list = [(imfile, dy_, dx_, destdir) for imfile, dy_, dx_ in zip(imfiles, dy, dx)]
        scatter(SENDER, 'shift_image', args_list)

        self.write('OK')


class CorrelationHandler(BaseHandler):
    def post(self):
        imfiles_pattern = self.get_argument('imfiles')

        imfiles = glob.glob(imfiles_pattern)
        args_list = [(imfiles[i-1], imfiles[i]) for i in range(1, len(imfiles))]
        scatter(SENDER, 'correlation_image', args_list, 'correlation_image_final')

        self.write('OK')


class PathFilesHandler(BaseHandler):
    def post(self):
        pattern = self.get_argument('pattern')

        files = glob.glob(pattern)
        self.write('{} files'.format(len(files)))


class PathDirectoryHandler(BaseHandler):
    def post(self):
        path = self.get_argument('directory')

        if os.path.isdir(path):
            self.write('OK')
        else:
            self.set_status(404)
            self.write('Could not find directory')


class TasksHandler(BaseHandler):
    pass


class StatusHandler(BaseHandler):
    def get(self):
        self.write(get_status_json())


class NoCacheStaticFileHandler(tornado.web.StaticFileHandler):
    def set_extra_headers(self, path):
        # Disable cache
        self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')


def service_web():
    static_path = os.path.join(os.path.dirname(__file__), "html")
    app = tornado.web.Application(
        [
            (r'/', MainHandler),
            (r'/api/v1/path/files/', PathFilesHandler),
            (r'/api/v1/path/directory/', PathDirectoryHandler),
            (r'/api/v1/tasks/', TasksHandler),
            (r'/api/v1/tasks/shift/', ShiftHandler),
            (r'/api/v1/tasks/correlation/', CorrelationHandler),
            (r'/api/v1/tasks/status.json', StatusHandler),
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
    STREAM.on_recv(gather)


def start():
    print('Start XNI manager...')
    if True:
        nproc = multiprocessing.cpu_count() if multiprocessing.cpu_count() < 8 else 8
        for i in range(nproc):
            multiprocessing.Process(target=worker.start).start()
    service_zmq()
    service_web()
    if False:
        webbrowser.open_new(config.WEBSERVER_URI)
    try:
        ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        pass
