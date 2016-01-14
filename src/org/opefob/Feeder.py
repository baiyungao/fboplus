'''
Created on Dec 4, 2015
This file is to feed the fbo xml to elasticsearch

@author: gaob
'''
import sgmllib
import cgi, string, sys, os
from org.opefob.entity.Notice import Notice
from os import walk

class FBOFeeder(sgmllib.SGMLParser):

    '''
    The class to load daily feed data from fbo.gov
    ftp://ftp.fbo.gov/
    '''
    def __init__(self, outfile=None, infile=None):
        '''
        Constructor
        '''
        sgmllib.SGMLParser.__init__(self)
        
        if not outfile:
             outfile = sys.stdout
             self.write = outfile.write
        if infile:
             self.load(infile)
             
    
    def load(self, file):
        print 'LOAD FILE ...', file
        while 1:
            s = file.read(8192)
            if not s:
                break
            self.feed(s)
        self.close()
        
    def handle_data(self, data):
         try:
             self.currentNotice.addData(data)   
         except AttributeError:
                    pass    
             
    def unknown_starttag(self, tag, attrs):
        tag = string.upper(tag)
        if (tag in Notice.type_set):
            self.currentNotice = Notice(tag)
        else:
            try:
                if (self.currentNotice != None):
                    self.currentNotice.start_tag(tag, attrs)
            except AttributeError:
                    pass
                
    def do_tag(self, attrs):
       print 'Do tag:', attrs
    
    def unknown_endtag(self, tag):
        tag = string.upper(tag)
        if (tag in Notice.type_set):
            self.currentNotice.complete() 
               
    
    
files = []
directory_path = "C:/fboNotice/"
completed_path = "C:/fboNoticeLoaded/"
for (dirpath, dirnames, filenames) in walk(directory_path):
    files.extend(filenames)
    
    
for f in files:
    print 'loading file ...=>' , f
    c = FBOFeeder()
    c.load(open(directory_path + f))
    os.rename(directory_path + f, completed_path + f)
  
'''
c = FBOFeeder()
c.load(open("c:/001/python/fbo/FBOFeed20160103.xml"))
'''   
    