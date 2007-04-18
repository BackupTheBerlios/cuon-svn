import time
from datetime import datetime
import random
import xmlrpclib
from xmlrpclib import ServerProxy
from twisted.web import xmlrpc
 
from basics import basics
import Database
import commands
import bz2
import base64

class Misc(xmlrpc.XMLRPC, basics):
    def __init__(self):
        basics.__init__(self)
        self.oDatabase = Database.Database()
        self.myHelpServer = self.getMyHelpServer()

    def getMyHelpServer(self):
        """
        if the CUON_SERVER environment-variable begins with https,
        then the server use SSL for security.
        @return: Server-Object for xmlrpc
        """
        
        sv = None
        try:
            if self.ONLINE_BOOK[0:5] == 'https':
                #sv =  Server( self.td.server  , SSL_Transport(), encoding='utf-8')
                sv =  ServerProxy( self.ONLINE_BOOK,allow_none = 1 ) 
            else:
                sv = ServerProxy(self.ONLINE_BOOK)
                
        except:
            print 'Server error'
            
        
        return sv

    def xmlrpc_getHelpBook(self):
        #Server = xmlrpclib.ServerProxy(self.getHelpServer())

        #print self.getHelpServer()
        #print self.getHelpServer().getRPCVersionSupported()
        print 'Helpserver = ', self.myHelpServer
        
        s = self.myHelpServer.getPageHTML(u"Benutzerhandbuch")
        return s
        
    def xmlrpc_getListOfTOPs (self, dicuser):
        sSql = 'select id, number from terms_of_payment'
        sSql = sSql + context.sql.py_getWhere("",dicUser,1)
        result = oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
        li = []
        if result != 'NONE':
           for i in range(len(result)):
               li.append(result[i]['id'] + '    ' + result[i]['number'])
        
        return li
   
    def xmlrpc_getListOfTaxVat(self, dicUser):
        sSql = 'select vat_name from tax_vat'
        sSql += self.getWhere("",dicUser,1)
        sSql += ' order by id '
        print sSql 
        result = self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
        li = []
        if result != 'NONE':
           for i in range(len(result)):
               li.append(result[i]['vat_name'])
        
        return li
    def xmlrpc_getFormsAddressNotes(self,iType, dicUser):
        
        sSql = 'select title, id  from dms where insert_from_module = ' + `iType`
        sSql += self.getWhere('', dicUser, Single = 2)
        result = self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
        liValues = []
        if result != 'NONE':
            for value in result:
                liValues.append(value['title'] + '###' + `value['id']`)
                
                
        if not liValues:
            liValues = 'NONE'
        return liValues
    def xmlrpc_faxData(self, dicUser, faxdata, phone_number):
        print 'send Fax'
        ol = False
        filename = 'fax___' + self.createNewSessionID()['SessionID'] 
        if filename:
            faxdata = base64.decodestring(faxdata)
            faxdata = bz2.decompress(faxdata)

            f = open(filename,'wb')
            f.write(faxdata)
            f.close()
            
            
        
            shellcommand = 'sendfax -n -o ' + dicUser['Name'] + ' -d "' + phone_number + '" ' + filename
            liStatus = commands.getstatusoutput(shellcommand)
            print shellcommand
            print  liStatus
            ok = True
            #shellcommand = 'rm ' + filename
            #liStatus = commands.getstatusoutput(shellcommand)
            #print shellcommand, liStatus
        return ok 
    def xmlrpc_getForm(self, id, dicUser):
        sSql = "select * from dms where id = " + `id` 
        print sSql
        return self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
        
