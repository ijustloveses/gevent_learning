# encoding: utf-8

import gevent
from gevent.event import Event

print '----------------- Event ---------------------'

'一个事件可以有多个任务等待，一旦set，全部唤醒'
evt = Event()


def setter():
    print "Setter: wait!"
    gevent.sleep(3)
    print "Setter: OK, done"
    '唤醒'
    evt.set()


def waiter():
    print "Waiter: waiting ..."
    '等待'
    evt.wait()
    print "Waiter: My turn"
    

gevent.joinall([
    gevent.spawn(setter),
    gevent.spawn(waiter),
    gevent.spawn(waiter),
    gevent.spawn(waiter),
    gevent.spawn(waiter),
    gevent.spawn(waiter),
])

print '----------------- AsyncResult ---------------------'

from gevent.event import AsyncResult

'一个事件可以有多个任务等待，一旦set，全部唤醒'
aevt = AsyncResult()


def setter():
    print "Setter: wait!"
    gevent.sleep(3)
    print "Setter: OK, done"
    '唤醒，并传递消息'
    aevt.set("result here")

def waiter():
    print "Waiter: waiting ..."
    '等待，并在唤醒时获取消息'
    message = aevt.get()
    print 'Waiter: Got message: %s' % message
    

gevent.joinall([
    gevent.spawn(setter),
    gevent.spawn(waiter),
    gevent.spawn(waiter),
    gevent.spawn(waiter),
    gevent.spawn(waiter),
    gevent.spawn(waiter),
])
