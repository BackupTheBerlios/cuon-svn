#! /usr/bin/python
from twisted.web import xmlrpc
#import os
#import sys
#import time
#import random	
import xmlrpclib
#import psycopg
#from basics import basics
#from ConfigParser import ConfigParser

try:
    import aiml
except:
    print 'No AI'
import SimpleXMLRPCServer
from ai_main import ai_main


class ai(xmlrpc.XMLRPC, ai_main):

    def __init__(self):
        ai_main.__init__(self)


    def xmlrpc_getAnswer(self, question):
        answer = 'NO DATA FOUND'
        question = self.checkQ(question)
        f = open('/root/cuonai.log','a')
        f.write(`question` + '\n')
        try:
            answer = self.k.respond(question.decode('utf-7'))
            f.write(`answer` + '\n')

        except:
            pass
        
        f.write('\n')
        f.close()
        #return  answer.decode('latin-1').encode('utf-7')
        return  answer
    


