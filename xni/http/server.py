from __future__ import absolute_import

from flask import Flask
from xni.celery.tasks import add

app = Flask(__name__)

@app.route('/')
def index():
    result = add.delay(4,4)
    return "Hello, world! %d" % result.get()
