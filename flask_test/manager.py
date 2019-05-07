from flask import Flask
from flask_script import Manager

app = Flask(__name__)

# 添加manager文件启动
manager = Manager(app=app)


@app.route('/', methods=['GET'])
def index():
    return '你好'


if __name__ == '__main__':
    app.debug = True
    manager.run()
