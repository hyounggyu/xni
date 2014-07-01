from celery import Celery

app = Celery('xni.celery',
             broker='amqp://',
             backend='redis://localhost',
             include=['xni.celery.tasks'])

app.conf.update(
    CELERY_RESULT_SERIALIZER = 'msgpack',
    CELERY_TASK_SERIALIZER = 'msgpack',
    CELERY_ACCEPT_CONTENT = ['msgpack'],
)

if __name__ == '__main__':
    app.start()
