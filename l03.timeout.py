# encoding: utf-8

import gevent
from gevent import Timeout

"""
”gevent.joinall()”方法中可以传入timeout参数来设置超时
也可以在全局范围内设置超时时间，如下：
"""

'超时设为2秒，此后所有协程的运行，如果超过两秒就会抛出”Timeout”异常'
timeout = Timeout(2)
timeout.start()


def wait():
    gevent.sleep(10)

try:
    gevent.spawn(wait).join()
except Timeout:
    print "time out happened"


'还可以将超时设置在with语句内，这样该设置只在with语句块中有效'
try:
    with Timeout(1):
        gevent.sleep(10)
except Exception, e:
    print e


'自定义超时所抛出的异常'
class Toolong(Exception):
    pass

with Timeout(1, Toolong):
    gevent.sleep(10)
