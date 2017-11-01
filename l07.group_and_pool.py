# encoding: utf-8

import gevent
from gevent.pool import Group
from gevent import getcurrent

group = Group()


def hello_from(n):
    print "size of group is %s" % len(group)
    print "hello from greenlet %s" % id(getcurrent())

group.map(hello_from, xrange(3))


def intensive(n):
    gevent.sleep(3 - n)
    return 'task', n

print 'Ordered'

ogroup = Group()
for i in ogroup.imap(intensive, xrange(3)):
    print i

print 'Unordered'

igroup = Group()
for i in igroup.imap_unordered(intensive, xrange(3)):
    print i


from gevent.pool import Pool

pool = Pool(2)

def hello(n):
    print "size of pool is %s" % len(pool)

pool.map(hello, xrange(3))
