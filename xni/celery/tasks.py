from celery import Task

from .celery import app
from .databasetask import DatabaseTask
from ..preprocess.shift import sum_x, vertical_align

@app.task
def add(x, y):
    return x + y

@app.task(base=DatabaseTask)
def read():
    read.db.set('a','b')
    return read.db.get('a')

@app.task(base=DatabaseTask)
def task_vertical_align(y0, im, start, end, dy_max):
    y0 = task_vertical_align.fetch(y0)
    im = task_vertical_align.fetch(im)
    y = sum_x(im)
    dy = vertical_align(y0, y, start, end, dy_max)
    return dy

@app.task(base=DatabaseTask)
def task_vertical_align2(im0, im, start, end, dy_max):
    im0 = task_vertical_align.fetch(im0)
    im = task_vertical_align.fetch(im)
    y0 = sum_x(im0)
    y = sum_x(im)
    dy = vertical_align(y0, y, start, end, dy_max)
    return dy
