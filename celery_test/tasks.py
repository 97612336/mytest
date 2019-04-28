
# tasks.py
from celery import Celery
from flask_mail import Message, Mail
from flask import Flask
import config

mail = Mail()
app = Flask(__name__)
app.config.from_object(config)
mail.init_app(app)


# celery -A tasks.celery worker --pool=solo --loglevel=info
# celery -A tasks.celery worker --loglevel=info

def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


celery = make_celery(app)


@celery.task
def send_email(to, subject):
    msg = Message(subject, sender="xkjskk@163.com",recipients=[to])
    msg.html='hello!This is apq!'
    mail.send(msg)
