from __future__ import absolute_import

from flask import Flask, request
from xni.io.tifffile import *
from xni.celery.tasks import add

app = Flask(__name__)

@app.route('/')
def index():
    result = add.delay(4,4)
    return "Hello, world! %d" % result.get()

@app.route('/uploads', methods=['POST'])
def post_uploads():
    for name, file in request.files.items():
        try:
            with TIFFfile(file.stream) as tif:
                print(tif[0].tags)
                print(tif[0].asarray())
        except Exception as e:
            print(e)
    return 'OK'
