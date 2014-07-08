from celery import Task

from .celery import app
from .databasetask import DatabaseTask

@app.task
def add(x, y):
    return x + y

@app.task(base=DatabaseTask)
def read():
    read.db.set('a','b')
    return read.db.get('a')
