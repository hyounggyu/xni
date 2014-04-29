from __future__ import absolute_import

from celery import Celery

app = Celery('xni.celery',
             broker='amqp://',
             backend='redis://localhost',
             include=['xni.celery.tasks'])

if __name__ == '__main__':
    app.start()
