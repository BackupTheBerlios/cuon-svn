from twisted.web import xmlrpc
import os
import sys
import time
import random	
import xmlrpclib
import string
from basics import basics
from cuon.SQL import SQL
from ConfigParser import ConfigParser


class Database(xmlrpc.XMLRPC, SQL):
    def __init__(self):
        basics.__init__(self)
        SQL.__init__(self)
        
    def xmlrpc_is_running(self):
        return 12
        
    def getValue(self, sKey):
        v = 'NONE'
        sSql = "select svalue from cuon where skey = '" + sKey + "'"
        result = self.xmlrpc_executeNormalQuery(sSql)
        if result != 'NONE':
           try:
              v = result[0]['svalue']
           except:
              v = 'NONE'
        if not v:
            v = 'NONE'
            
        return v
    def saveValue(self, sKey, cKey):
        self.out('py_saveValue cKey = ' + cKey)
        sSql = "select skey from cuon where skey = '" + sKey + "'"
        result = self.xmlrpc_executeNormalQuery(sSql)
        self.out('py_saveValue result = ' + `result`)
        if result != 'NONE':
           sSql = "update cuon set svalue = '" + cKey +"' where skey = '" + sKey + "'"
        else:
           sSql = "insert into cuon (skey, svalue) values ('" + sKey + "','" + cKey +"')"
        self.out('py_saveValue sSql = ' + `sSql`)
        result = self.xmlrpc_executeNormalQuery(sSql)
        return result

    def xmlrpc_createPsql(self, sDatabase, sHost, sPort, sUser,  sSql):

        # os.system('pysql ' + '-h ' + sHost + '-p ' + sPort + ' -U ' + sUser + ' ' + sDatabase + ' < ' + sSql) 
        
        sysCommand = 'echo \"' + sSql + '\" | ' + 'psql  ' + '-h ' + sHost + ' -p ' + sPort + ' -U ' + sUser +   ' '  + sDatabase
        
        os.system(sysCommand)
        
        return sysCommand

#context.exSaveInfoOfTable(sKey, oKey )
    
    def checkUser(self, sUser, sID, userType = None):
        ok = None
        dSession = {}
        print sUser, userType
        if userType:
           if userType == 'cuon':
                try:
                    #dSession['SessionID'] = self.dicVerifyUser[sUser]['SessionID']
                    #dSession['endTime'] = self.dicVerifyUser[sUser]['endTime']
                    dSession['SessionID'] = self.getValue('user_' + sUser + '_Session_ID')
                    dSession['endTime'] = float(self.getValue('user_' + sUser + '_Session_endTime'))
                    if sID == dSession['SessionID'] and self.checkEndTime(dSession['endTime']):
                        ok = sUser
                except:
                    #dSession['SessionID'] = self.getValue('user_' + sUser + '_Session_ID')
                    #dSession['endTime'] = float(self.getValue('user_' + sUser + '_Session_endTime'))
                    #self.out('py_checkUser dSession is found')
                    ok = 'Test'
                    
        #self.out('Session = ' + `dSession`)
##        if dSession:
##            if sID == dSession['SessionID'] and self.checkEndTime(dSession['endTime']):
##                ok = sUser
##        
##        self.out('end checkUser ok = ' + `ok`)
        return ok
        
    def authenticate(self, name, password, request):
        ok = False
        cParser = ConfigParser()
        cParser.read('/etc/cuon/user.cfg')
        sP = cParser.get('password',name)
        self.writeLog('Password = ' + sP )
        if sP == password:
            ok = True
            
        return ok
        
    def xmlrpc_createSessionID(self, sUser, sPassword):
        self.out('1 -- createSessionID start')
        s = ''
        if self.authenticate(name=sUser,password=sPassword,request=None):
            self.out('2 -- createSessionID User found ')
            s = self.createNewSessionID()
            self.out('3 -- createSessionID id created for ' + sUser + ' = '  + `s`)
            self.saveValue('user_'+ sUser + '_Session_ID' , s['SessionID'])
            self.saveValue('user_'+ sUser + '_Session_endTime' , `s['endTime']`)
            #context.exSaveInfoOfTable('user_' + sUser , s)
            self.out('4 -- createSessionID User is write ')
            #self.dicVerifyUser[sUser] = {}
            #self.dicVerifyUser[sUser]['SessionID'] = s['SessionID']
            #self.dicVerifyUser[sUser]['endTime'] = `s['endTime']`
            
        else:
            self.out('createSessionID User not found')
        if not s.has_key('SessionID'):
            s['SessionID'] = 'TEST'
        self.out('createSessionID ID = ' + `s`)
        return s['SessionID']
    def xmlrpc_checkVersion(self, VersionClient, version):
        ok = 'O.K.'
        if version['Major'] != VersionClient['Major'] or version['Minor'] != VersionClient['Minor'] or version['Rev'] != VersionClient['Rev']:
            ok = 'Wrong'

        return ok
        
    def xmlrpc_getLastVersion(self):
        self.writeLog('Start check version')
        id = 0
        version = '0.0.0'
        dicUser={'Name':'zope'}
        sSql = 'select last_value from cuon_clients_id'
        self.writeLog('Start check version sql= ' + `sSql`)
        result = self.xmlrpc_executeNormalQuery(sSql, dicUser)
        self.writeLog('LastVersion = ' + `result`)
            
        if result != 'NONE':
            try:
                id = int(result[0]['last_value'])
            except:
                id = -1
        else:
           id = -1
        if id == -1:
           version = 0
        else:
           sSql = 'select version from cuon_clients where id = ' + `id`
           result = self.xmlrpc_executeNormalQuery(sSql, dicUser)
           
           if result != 'NONE':
              version = result[0]['version']
        self.writeLog('check version id, version = ' + `id` + ', ' + `version` )  
        return id, version
    def xmlrpc_getInfo(self, sSearch):
        return self.getValue(sSearch)
    def xmlrpc_saveInfo(self, sKey, cKey):
        return self.saveValue(sKey, cKey)
    
    def xmlrpc_getListOfClients(self, dicUser):
        self.writeLog('Start List Of Clients')
        sSql = "select id from clients"
        dicClients = self.xmlrpc_executeNormalQuery(sSql, dicUser)
        liClients = []
        self.writeLog('Clients = ' + `dicClients`)

        if dicClients != 'NONE':
           for i in dicClients:
              self.writeLog('i = ' + `i`)
              cli = i['id']
              self.writeLog('cli = ' + `cli`)
              
              liClients.append(cli)
        
        self.writeLog('liClients = ' + `liClients`)
        return liClients
    
    def xmlrpc_checkExistSequence(self, sName, dicUser):

        sSql = "select relname from pg_class where relname = '" + sName + "'"
        dicName = self.xmlrpc_executeNormalQuery(sSql, dicUser)
        ok = 0

        if dicName != 'NONE':
            ok = len(dicName)

        return  ok
        
    
    def xmlrpc_checkExistTable(self, sName, dicUser):
        sSql = "select tablename from pg_tables where tablename = '" + sName + "'"
        dicName = self.xmlrpc_executeNormalQuery(sSql, dicUser)
        ok = 0

        if dicName != 'NONE':
            ok = len(dicName)

        return  ok
        
    def xmlrpc_checkExistColumn(self, sTableName, sColumnName, dicUser):
        sSql =  "select attname from pg_attribute where attrelid = ( select relfilenode from pg_class where relname = '" + sTableName +"')" 
        
        # and atttypmod != -1 )"
        
        dicName = self.xmlrpc_executeNormalQuery(sSql, dicUser)
        ok = 0
        #print `dicName`
        
        for i in range(len(dicName)):
            #print dicName[i]['attname']
            if sColumnName == dicName[i]['attname']:
               ok = 1
    

        return ok
        
    def xmlrpc_checkTypeOfColumn(self, sTable, sColumn, sType, iSize, dicUser ):
        
        bCheck = 0
        sSql = "select typname from pg_type where pg_type.oid = (select atttypid from pg_attribute where attrelid = (select relfilenode from pg_class where relname = \'"
        
        sSql = sSql + sTable + "\') and attname = \'" + sColumn + "\' ) "
        
        result = self.xmlrpc_executeNormalQuery(sSql, dicUser )
        #print result 
        self.writeLog('types by ColumnCheck: ' + `result[0]['typname']` + ' ### ' + `sType`)
        if string.find(result[0]['typname'],sType) > -1 :
           self.writeLog( 'type is equal')
           if string.find(sType,'char') > -1:
              result2 = self.xmlrpc_getSizeOfColumn(sTable, sColumn, dicUser)
              
              if (result2[0]['atttypmod'] -4) == iSize:
                 bCheck = 1
           else:
              bCheck = 1
        
        return bCheck
    
    def xmlrpc_getSizeOfColumn(self, sTable, sColumn, dicUser):
        sSql = "select pg_attribute.atttypmod from pg_attribute where  attrelid = (select relfilenode from pg_class where relname = \'" + sTable + "\') and attname = \'" + sColumn + "\'"
        result = self.xmlrpc_executeNormalQuery(sSql, dicUser)
        return result


    def xmlrpc_logout(self, sUser):
        self.saveValue('user_' + sUser,{'SessionID':'0', 'endTime': 0})
       
    def xmlrpc_createGroup(self, sGroup, dicUser):
        # check the group
        sSql = "select groname from pg_group where groname = '" + sGroup + "'"
        dicName = self.xmlrpc_executeNormalQuery(sSql, dicUser)
        
        if len(dicName):
           ok = 'Group exists'
        else:
           sSql = 'CREATE GROUP ' + sGroup
           ok = self.xmlrpc_executeNormalQuery(sSql,dicUser )
        
        return ok
        
    def xmlrpc_createUser(self, sUser, sPassword,  dicUser, createDBUser=1):
        ok = 'No action'
        if createDBUser:
            # check the user
            
            sSql = "select usename from pg_user where usename = '" + sUser + "'"
            dicName = self.xmlrpc_executeNormalQuery(sSql, dicUser)
            
            if len(dicName):
               ok = 'User exists'
            else:
               sSql = 'CREATE USER ' + sUser
               ok = self.xmlrpc_executeNormalQuery(sSql, dicUser)
            
        # context.Cuon.src.Databases.py_saveValue('user_'+ sUser, sPassword)
        
        return ok

    def xmlrpc_addGrantToGroup(self, sGrants, sGroup, sTable, dicUser):
        # check the group
        ok = 'ERROR'
        
        sSql = "select groname from pg_group where groname = '" + sGroup + "'"
        dicName = self.xmlrpc_executeNormalQuery(sSql, dicUser)
        if len(dicName):
           ok = 'GROUP'
           sSql = 'Grant ' +sGrants + ' ON '  + sTable + ' TO GROUP ' + sGroup
           ok = self.xmlrpc_executeNormalQuery(sSql, dicUser)
         
        
        else:
           ok = 'Group does not exist'
        
        return ok
    def xmlrpc_addUserToGroup(self, sUser, sGroup, dicUser):
        
        # check the user
        self.writeLog(dicUser['Name'])
        self.writeLog(dicUser['SessionID'])
        
        sSql = "select usename from pg_user where usename = '" + sUser + "'"
        dicName = self.xmlrpc_executeNormalQuery(sSql, dicUser)
        ok = 'ERROR'
        if len(dicName):
           # check the group
           sSql = "select groname from pg_group where groname = '" + sGroup + "'"
           dicName = self.xmlrpc_executeNormalQuery(sSql, dicUser)
           ok = 'USER'
           if len(dicName):
              ok = 'GROUP'
              sSql = 'ALTER GROUP ' +sGroup + ' ADD USER ' + sUser
              ok = self.xmlrpc_executeNormalQuery(sSql, dicUser)
         
        
        else:
           ok = 'Group or User does not exist'
        
        return ok
        
    def xmlrpc_createCuon(self, dicUser):
        
        self.writeLog('start py_createCuon')
        retValue = True
        ok = self.xmlrpc_checkExistTable('cuon', dicUser)
        self.writeLog('py_createCuon1 ' + `ok`)
        if ok == 0:
           retValue = False
           sSql = 'create table cuon ( skey varchar(255) NOT NULL UNIQUE , svalue text NOT NULL, PRIMARY KEY (skey) )'
           ok = self.xmlrpc_executeNormalQuery(sSql, dicUser)
           
        return retValue
        
        
    def saveWebshopRecord(self, sNameOfTable='EMPTY', id=0, id_field='id', dicValues ={}, dicUser={}):
        import string
        import types
        
        context.logging.writeLog('begin RECORD2')
        dicUser['Database'] = 'osCommerce'
        
        if id > -1:
            # update
            sSql = 'update ' + sNameOfTable + ' set  '
            
            for i in dicValues.keys():
                sSql = sSql + i
                liValue = dicValues[i]
                if liValue[1] == 'string' or liValue[1] == 'varchar':
                    sSql = sSql  + " = \'" + liValue[0]+ "\', "
        
                elif liValue[1] == 'int':
                    sSql = sSql  + " =  " + `int(liValue[0])` + ", "
        
                elif liValue[1] == 'float':
                    sSql = sSql  + " = " + `float(liValue[0])` + ", "
        
                elif liValue[1] == 'date':
                    if len(liValue[0]) < 10:
                        sSql = sSql  + " = NULL, "
                    else:
                        sSql = sSql  + " = \'" + liValue[0]+ "\', "
        
                elif liValue[1] ==  'bool':
                    context.logging.writeLog('REC2-bool ')
                    if liValue[0] == 1:
                        liValue[0] = 'True'
                    if liValue[0] == 0:
                        liValue[0] = 'False'
                    sSql = sSql + " = " + liValue[0] + ", "
                else:
                    sSql = sSql  + " = \'" + liValue[0]+ "\', "
            
            sSql = sSql[0:string.rfind(sSql,',')]
        
            sSql = sSql + ' where ' + id_field + ' = ' + `id`
            #print sSql
        else:
            context.logging.writeLog('new RECORD2')
            sSql = 'insert into  ' + sNameOfTable + ' (  '
            sSql2 = 'values ('
            context.logging.writeLog('REC2-1 ' + `sSql` + `sSql2`)
            for i in dicValues.keys():
                sSql = sSql + i + ', '
                context.logging.writeLog('REC2-1.1 ' + `sSql`)
                liValue = dicValues[i]
                context.logging.writeLog('REC2-1.2 ' + `liValue`)
                if liValue == None :
                    sSql2 = sSql2 + "\'\', " 
                else:
                    if liValue[1] ==  'string' or liValue[1] == 'varchar':
                        if len(liValue[0]) == 0:
                            sSql2 = sSql2 + "\'\', " 
                        else:
                            sSql2 = sSql2  + "\'" + liValue[0] + "\', "
                        context.logging.writeLog('REC2-2 ' + `sSql` + `sSql2`)
                    elif liValue[1] == 'int':
                        sSql2 = sSql2  + `int(liValue[0])` + ", "
                        context.logging.writeLog('REC2-3 ' + `sSql` + `sSql2`)
                    elif liValue[1] == 'float':
                        sSql2 = sSql2  + `float(liValue[0])` + ", "
                        context.logging.writeLog('REC2-4 ' + `sSql` + `sSql2`)
                    elif liValue[1] == 'date':
                        if len(liValue[0]) < 10:
                            sSql2 = sSql2  +  " NULL, "
                        else:
                            sSql2 = sSql2  + " \'" + liValue[0] + "\', "
                            context.logging.writeLog('REC2-5 ' + `sSql` + `sSql2`)
                    elif liValue[1] ==  'bool':
                        context.logging.writeLog('REC2-bool ')
                        if liValue[0] == 1:
                           liValue[0] = 'True'
                        if liValue[0] == 0:
                           liValue[0] = 'False'
        
                        sSql2 = sSql2  +"\'" + liValue[0] + "\', "
                        context.logging.writeLog('REC2-6 ' + `sSql` + `sSql2`)
                    else:
                        sSql2 = sSql2  +  " \'" + liValue[0] + "\', "
                        context.logging.writeLog('REC2-6 ' + `sSql` + `sSql2`) 
             
                        
            context.logging.writeLog('REC2-10 ' + `sSql` + '__' + `sSql2`) 
            sSql = sSql[0:sSql.rfind(',')]
            sSql2 = sSql2[0:sSql2.rfind(',')]
            #sSql2 = sSql2 + 'nextval(\'' + sNameOfTable + '_id\'), current_user, \'create\''  
            
            # set brackets and add
            sSql = sSql + ') ' + sSql2 + ')'
        
            # execute insert
            context.logging.writeLog('SQL by RECORD2 = ' + `sSql`)
            #print sSql
            context.py_executeNormalQuery(sSql, dicUser)
        
            # find last id 
        
            sSql = 'select max(' + id_field + ') as last_value from ' + sNameOfTable 
            # sSql = sSql[0:string.rfind(sSql,',')]
        
            
        
        #print sSql
        #return printed
                   
        return context.py_executeNormalQuery(sSql,dicUser)
                
