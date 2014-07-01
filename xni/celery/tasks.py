from celery import Task
import redis

from .celery import app

class DatabaseTask(Task):
    abstract = True
    _db = None

    @property
    def db(self):
        if self._db is None:
            self._db = redis.StrictRedis(db=1) # add database information
        return self._db

@app.task
def add(x, y):
    return x + y

@app.task(base=DatabaseTask)
def read():
    read.db.set('a','b')
    return read.db.get('a')
