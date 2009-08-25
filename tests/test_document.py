import os

from couchquery import *

this_dir = os.path.abspath(os.path.dirname(__file__))
design_doc = os.path.join(this_dir, 'views')

def setup_module(module):
    db = Database('http://localhost:5984/couchquery_unittest')
    createdb(db)
    db.sync_design_doc('banzai', design_doc)
    module.db = db

lectroids = [
    {'type':'red-lectroid',   'name':'John Whorfin'},
    {'type':'black-lectroid', 'name':'John Parker'},
    {'type':'red-lectroid',   'name':'John Bigboote'},
    {'type':'red-lectroid',   'name':"John O'Connor"},
    {'type':'red-lectroid',   'name':"John Gomez"},
    {'type':'black-lectroid', 'name':"John Emdall"},
    {'type':'red-lectroid',   'name':"John YaYa"},
    {'type':'red-lectroid',   'name':"John Small Berries"},
]

def test_simple_add():
    for doc in lectroids:
        assert db.create(doc)['ok'] == True

def test_bulk_update():
    alldocs = db.views.all()
    alldocs.species = 'lectroid'
    alldocs.save()

def test_views():
    rows = db.views.banzai.byType()
    assert len(rows) is 8
    assert type(rows[0]) is Document
    assert rows.offset is 0

def test_subview():    
    rows = db.views.banzai.byType()
    reds = rows['red-lectroid']
    assert len(reds) is 6
    assert type(rows[0]) is Document
    assert reds.offset is 2

def test_bulk_add():
    db.create(lectroids)
    assert len(db.views.all()) is 17


    
# def test_bulk_delete():
#     alldocs = db.views.all()
#     alldocs.delete()

def teardown_module(module):
    deletedb(module.db)