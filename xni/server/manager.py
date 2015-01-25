import os
import csv
import glob
import json
import webbrowser

import tornado.ioloop
import tornado.web

from . import config
from .dataset import *
from ..align.interpolation import interp_position


class BaseHandler(tornado.web.RequestHandler):
    pass


class DatasetHandler(BaseHandler):
    def get(self, dataset_name=None):
        if dataset_name == None or dataset_name == '':
            datasets = list_datasets()
            if len(datasets) == 0:
                self.set_status(404)
                self.write('Could not find datasets')
            else:
                self.write(json.dumps(datasets))
        else:
            self.write('OK')

    def post(self):
        name = self.get_argument('name')
        projections = self.request.files['projections']
        create_dataset(name, projections)
        self.write('OK')

    def delete(self):
        name = self.get_argument('name')
        remove_dataset(name)
        self.write('OK')


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
        #scatter(SENDER, 'shift_image', args_list)

        self.write('OK')


class CorrelationHandler(BaseHandler):
    def post(self):
        imfiles_pattern = self.get_argument('imfiles')

        imfiles = glob.glob(imfiles_pattern)
        args_list = [(imfiles[i-1], imfiles[i]) for i in range(1, len(imfiles))]
        #scatter(SENDER, 'correlation_image', args_list, 'correlation_image_final')

        self.write('OK')


def start():
    print('Start XNI manager...')
    app = tornado.web.Application(
        [
            (r'/api/v1/dataset$', DatasetHandler),
            (r'/api/v1/dataset/(.*)', DatasetHandler),
        ],
    )
    app.listen(config.SERVER_PORT)
    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        pass
