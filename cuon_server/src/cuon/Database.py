from twisted.web import xmlrpc
import os
import sys
import time
import random	
import xmlrpclib
import psycopg
from basics import basics
from cuon.SQL import SQL
from ConfigParser import ConfigParser


class Database(xmlrpc.XMLRPC, SQL):
    def __init__(self):
        basics.__init__(self)
        SQL.__init__(self)
        
    def getValue(self, sKey):
        v = None
        sSql = "select svalue from cuon where skey = '" + sKey + "'"
        result = self.xmlrpc_executeNormalQuery(sSql)
        if result:
           try:
              v = result[0]['svalue']
           except:
              v = None
        
        return v
    def saveValue(self, sKey, cKey):
        self.out('py_saveValue cKey = ' + cKey)
        sSql = "select skey from cuon where skey = '" + sKey + "'"
        result = self.xmlrpc_executeNormalQuery(sSql)
        self.out('py_saveValue result = ' + `result`)
        if result:
           sSql = "update cuon set svalue = '" + cKey +"' where skey = '" + sKey + "'"
        else:
           sSql = "insert into cuon (skey, svalue) values ('" + sKey + "','" + cKey +"')"
        self.out('py_saveValue sSql = ' + `sSql`)
        result = self.xmlrpc_executeNormalQuery(sSql)
        return result

#context.exSaveInfoOfTable(sKey, oKey )
    
    def checkUser(self, sUser, sID, userType = None):
        ok = None
        dSession = {}
        
        if userType:
           if userType == 'cuon':
               dSession['SessionID'] = self.getValue('user_' + sUser + '_Session_ID')
               dSession['endTime'] = float(self.getValue('user_' + sUser + '_Session_endTime'))
               self.out('py_checkUser dSession is found')
        
        self.out('Session = ' + `dSession`)
        if dSession:
            if sID == dSession['SessionID'] and self.checkEndTime(dSession['endTime']):
                ok = sUser
        
        self.out('end checkUser ok = ' + `ok`)
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

    def xmlrpc_logout(self, sUser):
        self.saveValue('user_' + sUser,{'SessionID':'0', 'endTime': 0})
            
