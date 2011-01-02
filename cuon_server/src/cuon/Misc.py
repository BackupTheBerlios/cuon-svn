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
import types
import bz2
import zipfile
   
import os.path
import shlex, subprocess



class Misc(xmlrpc.XMLRPC, basics):
    def __init__(self):
        basics.__init__(self)
        self.oDatabase = Database.Database()
        self.myHelpServer = self.getMyHelpServer()
        self.setDefaultValues2Database()
        
        
    def setDefaultValues2Database(self):
        
        for key in self.DIC_USER.keys():
            sSql = " select * from cuon_values where name = '" + key +"'"
            result = self.oDatabase.xmlrpc_executeNormalQuery(sSql)
            print result
            if result and result not in ['ERROR', 'NONE']:
                if isinstance(self.DIC_USER[key],  types.StringType):  
                    sSql = " update cuon_values  set type_c = '" + self.DIC_USER[key] + "' where name = '" + key + "'"
                    print sSql
                    result = self.oDatabase.xmlrpc_executeNormalQuery(sSql)
            else:
                 if isinstance(self.DIC_USER[key],  types.StringType):  
                    sSql = " insert into cuon_values  (id, name,  type_c) values ((select nextval('cuon_values_id')), '" + key + "', '" + self.DIC_USER[key] + "' )"
                    print sSql
                    result = self.oDatabase.xmlrpc_executeNormalQuery(sSql)    
                    
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
        result = self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
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
        sFaxPath = "/var/spool/cuon-fax"
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
            self.writeLog('Faxserver = ' + Faxserver)
            
        except:
            pass
            
        self.writeLog( 'send Fax')
        
        filename = sFaxPath + '/fax___' + self.createNewSessionID()['SessionID'] 
        if filename:
            faxdata = base64.decodestring(faxdata)
            faxdata = bz2.decompress(faxdata)

            f = open(filename,'wb')
            f.write(faxdata)
            f.close()
            sSql = "select email from staff where cuon_username = '" +  dicUser['Name'] + "' "
            sSql += self.getWhere("",dicUser,2)
            result = self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
            sEmail = None
            if result and result not in ['NONE','ERROR']:
                sEmail = result[0]['email']
                
        if Faxserver and Faxport and Faxuser:
            self.writeLog( 'Faxserver found')
            if filename:
                shellcommand = 'scp -P ' + Faxport.strip() +' '  + filename + ' ' + Faxuser.strip() + '@' + Faxserver.strip() + ':/' +sFaxPath
                self.writeLog( shellcommand)
                liStatus = commands.getstatusoutput(shellcommand)
                self.writeLog( `liStatus`)
                # new Parameter
                # -D -R send email when all ok
                # -f emailaddress
                
                
                    
                shellcommand = 'ssh -p ' + Faxport.strip() +' ' + Faxuser.strip() + '@' + Faxserver.strip() +  ' "sendfax -n '
                if sEmail:
                    shellcommand += ' -f ' + sEmail
                shellcommand += ' -D -R -o ' + dicUser['Name'] + ' -d "' + phone_number + '" ' + filename + '"'
                self.writeLog(shellcommand)

                liStatus = commands.getstatusoutput(shellcommand)
                #shellcommand = 'ssh -p ' + Faxport.strip() + ' '  + Faxuser.strip() +'@' + Faxserver.strip() + ' "sendfax -n -o ' + dicUser['Name'] + ' -d \"' + phone_number + '\" ' + filename + ' "'
                #self.writeLog(shellcommand)
                #liStatus = commands.getstatusoutput(shellcommand)
                
                self.writeLog(`liStatus`)
                ok = True
        else:
            if filename:
                shellcommand = 'sendfax -n '
                if sEmail:
                    shellcommand += ' -f ' + sEmail
                shellcommand += ' -o ' + dicUser['Name'] + ' -d "' + phone_number + '" ' + filename
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
        
    
    def xmlrpc_getEmailAddresses(self, sType, dicUser):
        value = None
        liAddresses = []
        
        try:
                       
            cpServer, f = self.getParser(self.CUON_FS + '/clients.ini')
            #print cpServer
            #print cpServer.sections()
            
            value = self.getConfigOption('CLIENT_' + `dicUser['client']`,sType, cpServer)
            if value:
                liAddresses = value.split(',')
                
        except Exception, params:
            print 'Error by Schedul Read user.cfg'
            print Exception, params
        
        
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
        
        
        
    def xmlrpc_dmsCheckPermissions(self,id,dicUser):
        bUser = False
        bGroup = False
        bAll = False
        allRights = False
        dicRights = {}
        dicRights['Ur'] = True
        dicRights['Uw'] = True
        dicRights['Ux'] = True
        dicRights['Gr'] = True
        dicRights['Gw'] = True
        dicRights['Gx'] = True
        dicRights['Ar'] = True
        dicRights['Aw'] = True
        dicRights['Ax'] = True
        
        groups = None
        liGroups = []
        # read configfile for group
        try:
                       
            cpServer, f = self.getParser(self.CUON_FS + '/user.cfg')
            #print cpServer
            #print cpServer.sections()
            
            groups = self.getConfigOption('GROUPS',dicUser['Name'], cpServer)
        
        except:
            pass
        if groups:
            liGroups = groups.split(',')
        
        sSql = 'select document_rights_activated, document_rights_user_read, document_rights_user_write, document_rights_user_execute, document_rights_group_read, document_rights_group_write, document_rights_group_execute, document_rights_all_read, document_rights_all_write, document_rights_all_execute, document_rights_user,  document_rights_groups from dms where id = ' + `id` 
        result = self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
        if result and result not in ['ERROR','NONE']:
            for key in result[0].keys():
                if key == 'document_rights_groups' or key == 'document_rights_user':
                    pass
                else:
                    if result[0][key] == 't':
                        print 'Set True = ',key
                        result[0][key] = True
                    else:
                        print 'Set False = ',key
                        result[0][key] = False
            if result[0]['document_rights_activated']: 
                print 'Rights are activated'
            
                if result[0]['document_rights_user'] == dicUser['Name']:
                    print 'User equal'
                    bUser = True
            else:
                allRights = True
        else:
            allRights = True
            
            
        dicRights['Read'] = True
        dicRights['Write'] = True
        dicRights['Execute'] = True
   
        if not allRights:
            dicRights['Ur'] = result[0]['document_rights_user_read'] and bUser
            dicRights['Uw'] = result[0]['document_rights_user_write'] and bUser
            dicRights['Ux'] = result[0]['document_rights_user_execute'] and bUser
            if result[0]['document_rights_groups'] in liGroups:
                bGroup = True
                
            dicRights['Gr'] = result[0]['document_rights_group_read'] and bGroup
            dicRights['Gw'] = result[0]['document_rights_group_write'] and bGroup
            dicRights['Gx'] = result[0]['document_rights_group_execute'] and bGroup
            
            dicRights['Ar'] = result[0]['document_rights_all_read'] 
            dicRights['Aw'] = result[0]['document_rights_all_write'] 
            dicRights['Ax'] = result[0]['document_rights_all_execute'] 
            dicRights['Read'] = False
            dicRights['Write'] = False
            dicRights['Execute'] = False

            if dicRights['Ur'] or dicRights['Gr'] or dicRights['Ar']:
                dicRights['Read'] = True
            if dicRights['Uw'] or dicRights['Gw'] or dicRights['Aw']:
                dicRights['Write'] = True
        
            if dicRights['Ux'] or dicRights['Gx'] or dicRights['Ax']:
                dicRights['Execute'] = True


        #Workaround
        #dicRights['Read'] = False
                
        
        return dicRights
        
    

    def xmlrpc_saveDia(self, sType, dicData):
        print sType
        print dicData

        return 'Hallo'

    def xmlrpc_getTextExtract(self, id, sFileSuffix,  dicUser):
        s = None
        sReturn = False
        sText = None
        imageData = None
        if sFileSuffix in ['pdf', 'txt']:
                
            sSql = 'select document_image from dms where id = ' + `id`
            liResult = self.oDatabase.xmlrpc_executeNormalQuery( sSql, dicUser )
            if liResult:
                s = liResult[0]['document_image']
                try:
                    b = base64.decodestring(s)
                    imageData = bz2.decompress(b)
                except Exception, param:
                    print Exception, param
                    imageData = None
    
            if imageData:
                try: 
                    ratio = "10"
                    sOutFile = "/tmp/" + self.getNewUUID() 
                    sInFile = "/tmp/" + self.getNewUUID() 
                    f = open(sOutFile + '.' + sFileSuffix, "w")
                    f.write(imageData)
                    f.close()
                    #print "files = ",  sOutFile,  sInFile
                    shellcommand = shlex.split("/usr/share/cuon/cuon_server/bin/getOts.sh " +sFileSuffix+ " " +  ratio + " " + sInFile + " " + sOutFile)
                    liStatus = subprocess.call(shellcommand)
                    #print "ots command = ",  shellcommand, liStatus
                    
                    f = open(sInFile, "r")
                    sText = f.read()
                    f.close()
                    #print "s = ",  sReturn
                    #liStatus = commands.getstatusoutput(shellcommand)
                    #print shellcommand, liStatus
                except Exception,  param:
                    print 'write files'
                    print Exception,  param
                
            
                if sText:
                    try:
                        sText = sText.decode('utf-8')
                        #print 'utf-8'
                    except Exception,  param:
                        print 'try to decode'
                        print Exception,  param
                        
                    sReturn = self.xmlrpc_updateDmsExtract(id, sText, dicUser)
                
        return sReturn


    def xmlrpc_updateDmsExtract(self,  id, sExtract, dicUser):
        #print 'update DMS = ',  id ,  sExtract
       
        liResult = False
#        try:
#            b = bz2.compress(sExtract)
#
#            imageData = base64.encodestring(b)
#        except Exception, param:
#            print Exception, param
#            imageData = None
            
       # print 'base64 codiert',  imageData
        if sExtract:
            
            sSql = "update dms set dms_extract = '" + sExtract + "' where id = " + `id`
            liResult = self.oDatabase.xmlrpc_executeNormalQuery( sSql, dicUser )
            
        return liResult
        
        
