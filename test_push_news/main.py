#!/usr/bin/python
import os
import sys
import tornado.options
import tornado.ioloop
import tornado.web

from test_push_news import Pushserver

settings = {
    "debug": False
}

application = tornado.web.Application([
    (r"/start_listening", Pushserver.StartListeningHandler),
], **settings)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    application.listen(int(sys.argv[1]))
    tornado.ioloop.IOLoop.instance().start()