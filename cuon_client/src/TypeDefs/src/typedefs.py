import xmlrpclib
from xmlrpclib import Server
import cuon.XML.MyXML
import sys
import os

#if len(sys.argv) > 1:
#    fname = sys.argv[1]
#else:

class typedefs:

    def __init__(self):
       
        self.server = os.environ['CUON_SERVER']
        self.homePath = os.environ['CUON_HOME']        

        print 'Server by typedef : ' + self.server
        
    
