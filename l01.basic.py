# encoding: utf-8

import gevent

"""
gevent.spawn() 方法会创建一个新的greenlet协程对象
gevent.joinall() 方法会等待所有传入的greenlet协程运行结束后再退出

step 1. 先进入协程test1，打印12
step 2. 遇到”gevent.sleep(0)”时，test1被阻塞，自动切换到协程test2，打印56
step 3. 之后test2被阻塞，这时test1阻塞已结束，自动切换回test1，打印34
step 4. 当test1运行完毕返回后，此时test2阻塞已结束，再自动切换回test2，打印78
step 5. 所有协程执行完毕，程序退出
"""

def test1():
    print 12
    gevent.sleep(0)
    print 34

def test2():
    print 56
    gevent.sleep(0)
    print 78

gevent.joinall([
    gevent.spawn(test1),
    gevent.spawn(test2),
])


import socket

"""
通过协程分别获取三个网站的IP地址，由于打开远程地址会引起IO阻塞，所以gevent会自动调度不同的协程
可以通过协程对象的”value”属性，来获取协程函数的返回值
"""

urls = ['www.baidu.com', 'www.sohu.com', 'www.sina.com.cn']
jobs = [gevent.spawn(socket.gethostbyname, url) for url in urls]
gevent.joinall(jobs, timeout=5)

print [job.value for job in jobs]

"""
上面例子中，程序运行时间和不用协程是一样的，即 3 个网站打开时间的总和
然而，理论上协程是非阻塞的，那运行时间应该等于最长的那个网站打开时间
其实，这是因为Python标准库里的socket是阻塞式的，DNS解析无法并发，包括像urllib库也一样

如何非阻塞的运行呢？一种方法是使用gevent下的socket模块，不过更常用的方法是使用猴子布丁
"""

from gevent import monkey

""" 
Python中其它标准库也存在阻塞的情况，gevent提供了”monkey.patch_all()”方法将所有标准库都替换
官网建议使用”patch_all()”，而且在程序的第一行就执行
"""
monkey.patch_socket()
jobs = [gevent.spawn(socket.gethostbyname, url) for url in urls]
gevent.joinall(jobs, timeout=5)

print [job.value for job in jobs]
