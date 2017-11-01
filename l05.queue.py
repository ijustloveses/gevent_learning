# encoding: utf-8

import gevent
from gevent.queue import Queue

products = Queue()


def consumer(name):
    while not products.empty():
        print "%s got %s" % (name, products.get())
        gevent.sleep(0)

    print "%s Quit" % (name)


def producer():
    for i in xrange(1, 10):
        products.put(i)
    print "producer done"

"""
put和get方法都是阻塞式的，故此
1. 下面程序中会首先打印 "producer done"
2. consumer 需要使用 gevent.sleep(0) 来释放处理权，故此 3 个 consumer 会交替从 queue 中读取数据
"""
gevent.joinall([
    gevent.spawn(producer),
    gevent.spawn(consumer, 'steve'),
    gevent.spawn(consumer, 'john'),
    gevent.spawn(consumer, 'nancy'),
])

"""
非阻塞的版本：put_nowait和get_nowait。如果调用get方法时队列为空，则抛出”gevent.queue.Empty”异常。
"由于需要事先往 queue 中写入数据，故此这里仍然使用阻塞的 put，不过后面使用非阻塞的 get_nowait"
"""

def nonblock_consumer(name):
    '为了避免报出异常，这里同样需要判断是否为空'
    while not products.empty():
        'non-block get'
        print "%s got %s" % (name, products.get_nowait())
        '仍然需要使用 sleep 交出 queue 的控制权，否则会非阻塞的不同从 queue 中读取数据'
        gevent.sleep(0)
    print "%s Quit" % (name)

"我们会看到，非阻塞的结果和阻塞的结果一致，其区别只是 consumer 协程内部是否阻塞而已"
gevent.joinall([
    gevent.spawn(producer),
    gevent.spawn(nonblock_consumer, 'steve'),
    gevent.spawn(nonblock_consumer, 'john'),
    gevent.spawn(nonblock_consumer, 'nancy'),
])
