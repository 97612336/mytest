import os

CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/0"
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
MAIL_SERVER = 'smtp.163.com'
MAIL_PORT = 25
MAIL_USE_TLS = True
MAIL_USERNAME = "xkjskk@163.com"
MAIL_PASSWORD = os.getenv("email_psd")
