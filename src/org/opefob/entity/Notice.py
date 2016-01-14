'''
Created on Dec 4, 2015

@author: gaob
'''

import json, httplib,string
from elasticsearch import Elasticsearch
from datetime import datetime
from time import gmtime, strftime

class Notice(object):
    '''
    The class to represent a ntoce published on fbo.gov
    
    '''
    
    type_set =set(['PRESOL','SRCSGT','COMBINE','ARCHIVE','AWARD','MOD','SNOTE'])
    
    attribute_set =set(['DATE','YEAR','AGENCY','OFFICE','LOCATION','ZIP','CLASSCOD','NAICS','OFFADD',
                        'SUBJECT','SOLNBR','RESPDATE','CONTACT','DESC','LINK', 'URL','DESC','SETASIDE',
                        'POPCOUNTRY', 'POPZIP', 'POPADDRESS',
                        'AWDNBR', 'AWDAMT','AWDDATE','AWARDEE',
                        'ARCHDATE'])
    
    arc_attribute_set = set(['SOLNBR','ARCHDATE'])
    awd_attribute_set = set(['DATE','YEAR','AGENCY','OFFICE','LOCATION','ZIP','CLASSCOD','NAICS','OFFADD',
                        'SUBJECT','SOLNBR','RESPDATE','CONTACT','DESC','LINK', 'URL','DESC','SETASIDE',
                        'POPCOUNTRY', 'POPZIP', 'POPADDRESS','SOLNBR','AWDNBR', 'AWDAMT','AWDDATE','AWARDEE'])
    
    es = Elasticsearch()
    
    lastReleaseDate = datetime.now()
    
    def getID(self):
        if self.isArchive():
            return 'ARC'+ self.content.get('SOLNBR')
        if self.isAward():
            return self.content.get('AWDNBR')

        return self.content.get('SOLNBR')
    
    def __init__(self, type="PRESOL"):
        
        '''
        Constructor
        '''
        self.content = dict()
        self.content.update(NoticeType=type)
        self.content.update(loadtimestamp=datetime.now())
        self.curentTag = ''


    def isAward(self):
        return self.content.get('NoticeType') == 'AWARD'
    
    def isArchive(self):
        return self.content.get('NoticeType') == 'ARCHIVE'    
    
    def isNotice(self):
        return self.content.get('NoticeType') in ['PRESOL','SRCSGT','COMBINE']
    
    def isMod(self):
        return self.content.get('NoticeType') == 'MOD'
     
     
    def complete(self):
        self.post()
        
    
    def post(self):
        
        if (self.isMod()):
            return
        print self.getID()
        self.polish()
        if (self.isAward()):
            res = Notice.es.index(index="fbo", doc_type='award', id=self.getID(), body=self.content)
        else:    
            res = Notice.es.index(index="fbo", doc_type='notice', id=self.getID(), body=self.content)
       
              
    def polish(self):
        
        '''
        Transformation here, combine the date and year.
        
        '''
               
        if ((self.content.get('DATE') != None) and (self.content.get('YEAR') != None)):
            try:
                s_date = '' + self.content.get('DATE'); 
                s_year = '20' + self.content.get('YEAR');
                year = int(s_year)
                month = int(s_date[0:2])
                day = int(s_date[2:])
                Notice.lastReleaseDate = datetime(year,month,day)
                self.content.update(timestamp=Notice.lastReleaseDate)
                self.content.pop('DATE')
                self.content.pop('YEAR')  
            except ValueError:
                self.content.update(timestamp=Notice.lastReleaseDate)
                self.content.pop('DATE')
                self.content.pop('YEAR')  
              
            
            if (self.content.get('RESPDATE') != None):
                try:
                    resp_date = self.content.get('RESPDATE')
                    r_month = int(resp_date[0:2])
                    r_day = int(resp_date[2:4])
                    r_year = int('20' + resp_date[4:])
                    resdate = datetime(r_year,r_month,r_day)
                    self.content.pop('RESPDATE')
                    self.content.update(RESPDATE=resdate.strftime('%m/%d/%Y'))
                except ValueError:
                    pass
                    
    
    def start_tag(self,tag,atts):
        if ((self.isArchive() and (tag in Notice.arc_attribute_set)) or
            (self.isAward() and (tag in Notice.awd_attribute_set)) or 
            (self.isNotice() and (tag in Notice.attribute_set))):
             
            self.curentTag = tag
        else: 
            self.curentTag = None
    
    def addData(self,data):
        
        '''
        filter data for non ascii
        data = unicode(data);
        '''
        
        var_unicode = unicode(data,errors='replace')
        data = var_unicode.encode('ascii','replace')
        if ((self.curentTag <> None) and (len(self.curentTag) > 0)):
            content = self.content
            tag = self.curentTag
            if (content.get(self.curentTag) == None):
                value = data
            else: 
                value = content.get(self.curentTag)  + data
            
            if  value.count('\n')==1:
                value=value.replace("\n","")
            
            self.content[tag]=value
        
    

   