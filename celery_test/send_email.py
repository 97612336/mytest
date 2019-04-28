from flask import Flask
import config
from tasks import send_email

app = Flask(__name__)
app.config.from_object(config)


@app.route('/')
def hello_world():
    send_email.delay("97612336@qq.com", 'hello world')
    return 'Hello World!%s' % (app.config['MAIL_USERNAME'])


if __name__ == '__main__':
    app.run(port=8123)
