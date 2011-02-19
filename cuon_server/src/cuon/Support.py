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
    
    
    def getAuthorization(self,  Username,  Password,  ClientID):
        ''' Web Authentication'''
        ok = True
        #self.XMLRPC_PORT = 7080
        #self.XMLRPC_HOST = 'localhost'
        #self.XMLRPC_PROTO = "http"
        # Authorized
        print 'Server',  self.sv
        print Username,  Password
        
        sid = self.sv.Database.createSessionID( Username, Password)
        
        
        print sid
        # Set Information for cuon
        self.dicUser={'Name':Username,'SessionID':sid,'userType':'cuon',  'client':int(ClientID)}

        return self.dicUser   
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
       
        try:
            if liStatus0:
                liStatus = liStatus0.split(',')
            if liSeverity0:
                liSeverity = liSeverity0.split(',')
            if liPriority0:
                liPriority = liPriority0.split(',')
            if liReproduced0:
                liReproduced = liReproduced0.split(',')    
            if liPlatform0:
                liPlatform = liPlatform0.split(',')    
        except:
            pass
            
            
        return liStatus,  liSeverity, liPriority, liReproduced, liPlatform
        
