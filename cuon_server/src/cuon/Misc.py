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
        if result not in ['NONE','ERROR']:
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
        if result not in ['NONE','ERROR']:
           for i in range(len(result)):
               li.append(result[i]['vat_name'])
        
        return li
    def xmlrpc_getFormsAddressNotes(self,iType, dicUser):
        
        sSql = 'select title, id  from dms where insert_from_module = ' + `iType`
        sSql += self.getWhere('', dicUser, Single = 2)
        result = self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
        liValues = []
        if result not in ['NONE','ERROR']:
            for value in result:
                liValues.append(value['title'] + '###' + `value['id']`)
                
                
        if not liValues:
            liValues = 'NONE'
        return liValues
    def xmlrpc_faxData(self, dicUser, faxdata, phone_number):
        ok = False
        Faxserver = None
        Faxport = None
        Faxuser = None
        s = ''
        for i in phone_number:
            if i in ['0','1','2','3','4','5','6','7','8','9']:
                s += i
        phone_number = s
        try:
                       
            cpServer, f = self.getParser(self.CUON_FS + '/server.ini')
            #print cpServer
            #print cpServer.sections()
            
            Faxserver = self.getConfigOption('FAX','HOST', cpServer)
            Faxport = self.getConfigOption('FAX','PORT', cpServer)
            Faxuser = self.getConfigOption('FAX','USER', cpServer)
        
        except:
            pass
            
        self.writeLog( 'send Fax')
        
        filename = '/fax/fax___' + self.createNewSessionID()['SessionID'] 
        if filename:
            faxdata = base64.decodestring(faxdata)
            faxdata = bz2.decompress(faxdata)

            f = open(filename,'wb')
            f.write(faxdata)
            f.close()
            
        if Faxserver and Faxport and Faxuser:
            self.writeLog( 'Faxserver found')
            if filename:
                shellcommand = 'scp -P ' + Faxport.strip() +' '  + filename + ' ' + Faxuser.strip() + '@' + Faxserver.strip() + '://fax'
                self.writeLog( shellcommand)
                liStatus = commands.getstatusoutput(shellcommand)
                self.writeLog( `liStatus`)
                
                shellcommand = 'ssh -p ' + Faxport.strip() +' ' + Faxuser.strip() + '@' + Faxserver.strip() +  ' "sendfax -n -o ' + dicUser['Name'] + ' -d "' + phone_number + '" ' + filename + '"'
                self.writeLog(shellcommand)

                liStatus = commands.getstatusoutput(shellcommand)
                shellcommand = 'ssh -p ' + Faxport.strip() + ' '  + Faxuser.strip() +'@' + Faxserver.strip() + ' "sendfax -n -o ' + dicUser['Name'] + ' -d \"' + phone_number + '\" ' + filename + ' "'
                self.writeLog(shellcommand)
                liStatus = commands.getstatusoutput(shellcommand)
                
                self.writeLog(`liStatus`)
                ok = True
        else:
            if filename:
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
        
    def xmlrpc_getNotes0ID(self, dicUser):
        value = 0
        try:
                       
            cpServer, f = self.getParser(self.CUON_FS + '/clients.ini')
            #print cpServer
            #print cpServer.sections()
            
            value = int(self.getConfigOption('CLIENT_' + `dicUser['client']`,'Notes0_ID', cpServer))
            
        except Exception, params:
            print 'Error by Notes0 ID Read client.cfg'
            print Exception, params
        print 'notes_0_id', value
        return value
    def xmlrpc_sendNotes0(self, dicUser,current_page = -1):
        ok = False
        # For BGU
        if current_page == -1:
            current_page = 12
            
        try:
                       
            cpServer, f = self.getParser(self.CUON_FS + '/clients.ini')
            #print cpServer
            #print cpServer.sections()
            
            value = self.getConfigOption('CLIENT_' + `dicUser['client']`,'sendNotes0', cpServer)
            
            if value and (value == 'Yes' or value == 'YES' or value == 'yes'):
                value = self.getConfigOption('CLIENT_' + `dicUser['client']`,'Pages', cpServer)
                if value and int(value)>0:
                    if int(value)&(2**current_page) == (2**current_page):
                        print 'Notes are in Bitfield', current_page,2**current_page
                        value = self.getConfigOption('CLIENT_' + `dicUser['client']`,'sendNotes0Sender', cpServer)
                        if value and value.find(dicUser['Name']) >= 0:
                            ok = True
                
        except Exception, params:
            print 'Error by Schedul Read user.cfg'
            print Exception, params
        print 'current_page = ', current_page
        return ok 
        
    def xmlrpc_getAdditionalEmailAddressesNotes0(self, addressid, dicUser):
        value = None
        liAddresses = []
        
        try:
                       
            cpServer, f = self.getParser(self.CUON_FS + '/clients.ini')
            #print cpServer
            #print cpServer.sections()
            
            value = self.getConfigOption('CLIENT_' + `dicUser['client']`,'AdditinalEmailAddressesNotes0', cpServer)
            if value:
                liAddresses = value.split(',')
                
        except Exception, params:
            print 'Error by Schedul Read user.cfg'
            print Exception, params
        print 'notes_0_addEmailAddresses', value
        
        # configOption sendMailsNotes0: caller,rep,salesman
        value = None
        try:
                       
            cpServer, f = self.getParser(self.CUON_FS + '/clients.ini')
            #print cpServer
            #print cpServer.sections()
            
            value = self.getConfigOption('CLIENT_' + `dicUser['client']`,'sendMailsNotes0', cpServer)
            if value:
                liValues = value.split(',')
                if liValues:
                    for i in liValues:
                        result = None
                        if i.strip() == 'caller':
                            sSql = 'select staff.email as email from staff, address where  address.caller_id  = staff.id' 
                            sSql += ' and address.id = ' + `addressid`
                            result = self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
                        elif i.strip() == 'rep':
                            sSql = 'select staff.email  as email from staff, address where  address.rep_id  = staff.id' 
                            sSql += ' and address.id = ' + `addressid`
                            result = self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
                        elif i.strip() == 'salesman':
                            sSql = 'select staff.email  as email from staff, address where  address.salesman_id  = staff.id' 
                            sSql += ' and address.id = ' + `addressid`
                            result = self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
                        if result and result not in ['NONE','ERROR']:
                            liAddresses.append(result[0]['email'].strip())
            
        except Exception, params:
            print 'Error by Schedul Read user.cfg'
            print Exception, params
        print 'notes_0_addEmailAddresses', value
        if not liAddresses:
            liAddresses = 'NONE'
                
        return liAddresses
        
