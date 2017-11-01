# encoding: utf-8

import gevent


def win():
    return "you win"


def fail():
    raise Exception("you failed")

winner = gevent.spawn(win)
loser = gevent.spawn(fail)

'协程状态已启动, 可以用协程对象的”started”属性来判断'
print winner.started   # True
print loser.started    # True

"""
在Greenlet中发生的异常，不会被抛到Greenlet外面
控制台会打出Stacktrace，但程序不会停止
"""
try:
    gevent.joinall([winner, loser])
except Exception, e:
    " 这段永远不会被执行 "
    print "this should not be reached, never"

'协程状态已停止, 可以用协程对象的”ready()”方法来判断'
print winner.ready()    # True
print loser.ready()     # True

'对于已停止的协程，可以用”successful()”方法来判断其是否成功运行且没抛异常'
print winner.value    # you win
print loser.value     # None !!!

print winner.successful()   # True
print loser.successful()    # False

'greenlet协程运行过程中发生的异常是不会被抛出到协程外的，因此需要用协程对象的”exception”属性或者 get() 来获取协程中的异常'
print loser.exception     # you failed
print loser.get()         # 整个 exception 堆栈
