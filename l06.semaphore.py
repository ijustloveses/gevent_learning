# encoding: utf-8

import gevent
from gevent.lock import BoundedSemaphore

sem = BoundedSemaphore(2)

def worker(n):
    sem.acquire()
    print "authorized [%i]" % n
    gevent.sleep(0)
    sem.release()
    print "leave [%i]" % n


gevent.joinall([gevent.spawn(worker, i) for i in xrange(1, 6)])
