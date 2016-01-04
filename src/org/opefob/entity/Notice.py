'''
Created on Dec 4, 2015

@author: gaob
'''

import json, httplib
from elasticsearch import Elasticsearch
from datetime import datetime

class Notice(object):
    '''
    The class to represent a ntoce published on fbo.gov
    
    '''
    
    type_set =set(['PRESOL','SRCSGT','COMBINE','ARCHIVE'])
    
    attribute_set =set(['DATE','YEAR','AGENCY','OFFICE','LOCATION','ZIP','CLASSCOD','NAICS','OFFADD',
                        'SUBJECT','SOLNBR','RESPDATE','CONTACT','DESC','LINK','DESC','SETASIDE',
                        'POPCOUNTRY', 'POPZIP', 'POPADDRESS'])
    
    
    def getID(self):
        if (self.content.get('NoticeType') == 'PRESOL'):
            return self.content.get('SOLNBR')

    def __init__(self, type="presol"):
        
        '''
        Constructor
        '''
        self.content = dict()
        self.content.update(NoticeType=type)
        self.content.update(timestamp=datetime.now())
        self.curentTag = ''
        self.es = Elasticsearch()
        print 'new notice:' , self.content
        
     
    def complete(self):
        print "notice completed:", self.content
        self.post()
        
    
    def post(self):
        
        print self.content
        res = self.es.index(index="fbo", doc_type='notice', id=self.content.get('SOLNBR'), body=self.content)
        
        print res
        
    
    def start_tag(self,tag,atts):
        if (tag in Notice.attribute_set):
            self.curentTag = tag
        else: 
            self.curentTag = None
    
    def addData(self,data):
        if ((self.curentTag <> None) and (len(self.curentTag) > 0)):
            content = self.content
            tag = self.curentTag
            if (content.get(self.curentTag) == None):
                value = data
            else: 
                value = content.get(self.curentTag)  + data
            
            self.content[tag]=value
        
            