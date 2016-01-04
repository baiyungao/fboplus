'''
Created on Dec 4, 2015

@author: gaob
'''

from elasticsearch import Elasticsearch
from datetime import datetime

class MyClass():
    '''
    classdocs
    '''
    i=[567]
    def f(self):
        return 'Hello'
    
    
print MyClass.i

my = MyClass()
print my.f()

my.i.append(456)

print MyClass.i
print my.i

you = MyClass();
you.i.append(6)
print my.i
print you.i

es = Elasticsearch()
'''  
doc = {
    'author': 'Chloe Gao',
    'text': 'Elasticsearch: cool. bonsai cool.',
    'timestamp': datetime.now(),
}


res = es.index(index="fbo", doc_type='notice', id=1, body=doc)
print(res['created'])
'''


res = es.search(index="fbo", body={"query": {"match_all": {}}})
print("Got %d Hits:" % res['hits']['total'])
for hit in res['hits']['hits']:
    print(hit)


