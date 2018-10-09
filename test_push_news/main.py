import logging
import os

import tornado

from tornado.options import define
import tornado.web


class MyApplication(tornado.web.Application):
    def __init__(self):
        handlers = [(r'/', pullServer), (r'/send', pushServer)]
        setting = dict(
            debug=True,
            template_path=os.path.join(os.path.dirname(__file__), "template"),
        )
        tornado.web.Application.__init__(self, handlers, **setting)


class pullServer(tornado.web.RequestHandler):
    @tornado.web.asynchronous  # 这个的作用是使用异步，让get不自动断开连接，直到接到服务器推送过来的消息后，再self.finish()，断开连接
    def get(self):
        uid = self.get_argument("uid")
        print(uid)
        add_uid(uid, self.callback)

    # 这一步很关键，当浏览器发送请求后，这个回调函数就会被注册到消息队列中，当服务器发送消息后，会调用所有已经被注册的callback（），把消息推到浏览器上
    def callback(self, message):
        self.write(message)
        self.finish()


# 发送消息页面
class pushServer(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

    def post(self):
        msg = self.get_argument("message")
        # 通过send后，所有已注册的回调函数都会被执行，把“message”推送到浏览器
        send(msg)


UidList = {}  # 保存回调函数，即需要推送消息的都在这里


# 添加队列
def add_uid(uid, callback):
    if uid not in UidList:
        UidList[uid] = callback
        print(callback)


# 发送消息
def send(message):
    for i in UidList:
        callback = UidList[i]
        callback(message)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(MyApplication())
    http_server.listen(8009)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
