import sys
import json
import csv
import string
import urllib
import time
import hashlib
import re
import logging
import uuid

import tornado.web
import tornado.ioloop
import tornado.database


class HandlerMixin(object):
    listeners = {}

    # 将user_id和callback存入listensers
    def add_listener(self, user_id, callback):
        handler = HandlerMixin
        if user_id not in handler.listeners:
            handler.listeners[user_id] = {'callback': set()}
        user_callback = handler.listeners[user_id]['callback']
        user_callback.add(callback)

    # 将user_id从listeners中移除，并删除callback
    def del_listener(self, user_id, callback):
        handler = HandlerMixin
        if user_id in handler.listeners:
            user_callback = handler.listeners[user_id]['callback']
            if callback in user_callback:
                user_callback.remove(callback)
                del callback
        if len(handler.listeners[user_id]['callback']) == 0:
            del handler.listeners[user_id]

    # 调用某个listenser的callback, 即推送消息
    def send_message(self, user_id, message):
        handler = HandlerMixin
        if user_id in handler.listeners:
            user_callback = handler.listeners[user_id]['callback']
            for one_callback in user_callback:
                one_callback(message)
            del handler.listeners[user_id]

    # 定义可发起请求的客户端domain
    available_domains = ['https://cyx.autoforce.net']

    # 这一句是申明该函数要使用异步机制
    @tornado.web.gen.coroutine
    def get(self):
        user = {
            "id": self.get_argument("id", '').replace('"', ''),
            "name": self.get_argument("name", '').replace('"', ''),
        }
        self.add_listener(self.user_id, self._callback)

    # 处理用户断线、超时、关闭浏览器等情况
    def on_connection_close(self):
        self.del_listener(self.user_id, self._callback)

    def on_finish(self):
        pass

    # 监测客户端请求HTTP头中的origin信息，确保是自己的domain
    def _check_origin(self, origin):
        domain = string.replace(origin, 'https://', '')
        domain = string.replace(origin, 'http://', '')
        return domain in self.available_domains

    # 这就是回调函数的定义
    def _callback(self, message):
        # 确保在客户端保持连接时才继续执行
        if self.request.connection.stream.closed():
            return

        # 检查origin来确保通信安全
        headers = dict(self.request.headers)
        origin = headers.get("Origin", None)
        if origin is None or self._check_origin(origin) is False:
            if origin is None:
                origin = '-'
            self.finish()
            return

        # 准备推送消息的http头
        self.set_header("Content-Type", "text/plain")
        self.set_header("Access-Control-Allow-Origin", origin)
        self.set_header("Access-Control-Allow-Methods", "GET,POST")
        self.set_header("Access-Control-Allow-Credentials", "true")
        data = {"msg": message, "sys_time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}
        self.finish(data)
