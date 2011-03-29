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
    
    
    def xmlrpc_getAuthorization(self,  Username,  Password,  ClientID):
        ''' Web Authentication at support tickets'''
        ok = True
        #self.XMLRPC_PORT = 7080
        #self.XMLRPC_HOST = 'localhost'
        #self.XMLRPC_PROTO = "http"
        # Authorized
        
        print Username,  Password
        
        sid = self.oDatabase.xmlrpc_createSessionID( Username, Password)
        
        
        print sid
        # Set Information for cuon
        self.dicUser={'Name':Username,'SessionID':sid,'userType':'cuon',  'client':int(ClientID)}

        return self.dicUser   
        
        
    def xmlrpc_getProjects(self, dicUser, public=False):
        
        sSql = "select id,  support_project_number, designation, is_public from support_project where (is_public is not null and is_public = 1  )  "
        sSql += self.getWhere(None,dicUser,2)
        sSql += " order by support_project_number "
        Result = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser)
        print Result
        return Result
    def xmlrpc_getTickets(self, dicUser, id, public = False,  status = 0):
        sSql = "select id, ticket_number,  short_designation  from support_ticket where support_project_id =" + `id` + " " 
        sSql += self.getWhere(None,dicUser,2)
        sSql += " order by ticket_number"
        Result = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser)
        print Result
        return Result
        
    def xmlrpc_getTicketDetails(self, dicUser, id, public = False,  status = 0):
        sSql = "select * from support_ticket where id =" + `id` + "  " 
        sSql += self.getWhere(None,dicUser,2)
        
        Result = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser)
        #print Result
        
        return Result   
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
        
