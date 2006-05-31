import xmlrpclib
from twisted.web import xmlrpc
from twisted.internet import defer
from twisted.internet import reactor
from twisted.web import server
import os
import sys
import time
import random	
import xmlrpclib
from basics import basics
    

class CuonFuncs(xmlrpc.XMLRPC):
##    def __init__(self):
##        basics.__init__(self)
##    
    def xmlrpc_test1(self, f, s):
        f = open(f, 'a') 
        f.write(s)
        f.close()
        return 'Hallo'
    
    
