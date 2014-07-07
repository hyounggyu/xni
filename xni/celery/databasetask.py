from celery import Task

import redis
import numpy as np

class DatabaseTask(Task):
    abstract = True
    _db = None

    def __init__(self):
        super(DatabaseTask, self).__init__()
        self._db = redis.StrictRedis() # add database information db=?

    @property
    def db(self):
        return self._db

    def fetch(self, data):
        if type(data) is str:
            dumps = self.db.get(data)
            return np.loads(dumps)
        elif isinstance(data, np.ndarray):
            return data
        else:
            return None
