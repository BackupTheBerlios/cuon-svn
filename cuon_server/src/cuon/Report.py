import random
import xmlrpclib
from twisted.web import xmlrpc
 
from basics import basics
import Database

class Report(xmlrpc.XMLRPC, basics):
    def __init__(self):
        basics.__init__(self)
        self.oDatabase = Database.Database()
        self.debugFinances = 1
     

    def xmlrpc_server_hibernation_incoming_document(self, dicOrder, dicUser):
        print `self.report_server`
        return self.report_server.ReportServer.server_hibernation_incoming_document(dicOrder, dicUser)
        
