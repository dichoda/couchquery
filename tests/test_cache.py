#!/usr/bin/env python
import sys, os.path
mydir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(mydir, "..")))
from couchquery import *
import httplib2
import time

"""
    Simple test of disabling file based cache with couchquery
"""

this_dir = os.path.abspath(os.path.dirname(__file__))
design_doc = os.path.join(this_dir, 'views')

URL='http://admin:midas@localhost:5984/couchquery_unittest'


class StatCache(object):
    """  Implements httplib2's FileCache interface.
         Keeps statistics on the delegate cache
    """
    def __init__(self, delegate):
       self.delegate = delegate
       self.hits = 0
       self.misses = 0


    def get(self, key):
        val = self.delegate.get(key)
        if val is None:
            self.misses += 1
        else:
            self.hits += 1
        return val

    def set(self, key, val):
        return self.delegate.set(key, val)

    def delete(self, key):
        return self.delegate.delete(key)

    def __str__(self):
       return "(h:%d, m:%d)"%(self.hits, self.misses)


def run_nocache():
    sc = StatCache(NoopHttpCache())
    db = Database(URL, cache=sc)
    try:
        createdb(db)
        return sc, perform(db)
    finally:
	deletedb(db)

def run_cache():
    sc = StatCache(httplib2.FileCache(".cache"))
    db = Database(URL, cache=sc)
    try:
        createdb(db)
        return sc, perform(db)
    finally:
        deletedb(db)

def perform(db):
    for x in xrange(100):
	doc = { '_id':  str(x), "value": "document %d" % x }
	db.create(doc)

    t = time.time()
    for z in xrange(10):
        for x in xrange(120):
            try:
	        y = db.get(str(x))
            except CouchDBDocumentDoesNotExist: 
                pass
         
    return time.time() - t


if __name__ == '__main__':
   sc1, t1 = run_nocache()
   sc2, t2 = run_cache()
   print "No Cache: %f %s" % (t1, str(sc1))
   print "W/Cache:  %f %s" % (t2, str(sc2))
