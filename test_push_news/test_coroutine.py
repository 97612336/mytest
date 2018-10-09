from tornado import gen
from tornado.ioloop import IOLoop


@gen.coroutine
def myRoutine():
    raise Exception("Exception")
    return 'hello'


@gen.coroutine
def test():
    print("here 1")
    res = yield gen.Task(myRoutine)
    print("here 2")


test()

IOLoop.instance().start()
