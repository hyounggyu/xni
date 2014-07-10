from celery import Task

from .celery import app
from .databasetask import DatabaseTask

from ..recon import preprocess

@app.task
def add(x, y):
    return x + y

@app.task(base=DatabaseTask)
def read():
    read.db.set('a','b')
    return read.db.get('a')

@app.task
def normalize(bg, im):
    return preprocess.normalize(bg, im)
