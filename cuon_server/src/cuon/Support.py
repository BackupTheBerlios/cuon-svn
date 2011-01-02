import time
import time
from datetime import datetime
import random
import xmlrpclib
from twisted.web import xmlrpc
from basics import basics
import Database
import hashlib



class Support(xmlrpc.XMLRPC, basics):
    def __init__(self):
        basics.__init__(self)
        self.oDatabase = Database.Database()
        
    def xmlrpc_getTicketComboBoxEntries(self, dicUser):
        print 'get comboBox Entries'
        cpServer, f = self.getParser(self.CUON_FS + '/clients.ini')
        liStatus0 = self.getConfigOption('CLIENT_' + `dicUser['client']`,'cbTicketStatus', cpServer)
        liSeverity0 = self.getConfigOption('CLIENT_' + `dicUser['client']`,'cbSeverity', cpServer)
        liPriority0 = self.getConfigOption('CLIENT_' + `dicUser['client']`,'cbPriority', cpServer)
        liReproduced0 = self.getConfigOption('CLIENT_' + `dicUser['client']`,'cbReproduced', cpServer)
        liPlatform0 = self.getConfigOption('CLIENT_' + `dicUser['client']`,'cbPlatform', cpServer)
       
        liStatus = ['NONE']
        liSeverity = ['NONE']
        liPriority = ['NONE']
        liReproduced = ['NONE']
        liPlatform = ['NONE']
       
        if liStatus0:
            liStatus = liStatus0.split(',')
        if liSeverity0:
            liSeverity = liSeverity0.split(',')
        if liPriority0:
            liPriority = liPriority0.split(',')
        if liReproduced0:
            liReproduced = liReproduced0.split(',')    
        if liPlatform0:
            liPlatform = liPlatform.split(',')    
            
            
        return liStatus,  liSeverity, liPriority, liReproduced, liPlatform
        
