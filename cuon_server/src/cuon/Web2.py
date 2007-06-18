import time
from datetime import datetime
import random
import xmlrpclib
from twisted.web import xmlrpc
 
from basics import basics
import iCal
import Database


class Web2(xmlrpc.XMLRPC, basics):
    def __init__(self):
        basics.__init__(self)
        self.iCal = iCal.iCal()
        self.oDatabase = Database.Database()
        self.dicUser = {}
        self.dicUser['Name'] = 'zope'
    def getRootElement(self):
        tData = 'NONE'
        sSql = "select * from web2 where type = 0"
        result = self.oDatabase.xmlrpc_executeNormalQuery(sSql, self.dicUser)
        if result and result != 'NONE':
            tData = result[0]
            
        
         
        return tData
        
    
         
        return tData    
    def getAllSiteElementIDs(self,sName):
        sSql = "select id from web2 where type = 1 and root_keys = '" + sName + "'"
        result = self.oDatabase.xmlrpc_executeNormalQuery(sSql, self.dicUser)
        
        return result
            
    def getSiteElementByID(self,id):
        sSql = "select * from web2 where id = " +`id`
        result = self.oDatabase.xmlrpc_executeNormalQuery(sSql, self.dicUser)
        
        return result
         
    
         
    
        
    def xmlrpc_updateCalendar(self, liNames, dicData, dicUser):
        sSql = 'select * from partner_schedul where partner_id = ' + `dicData['partner_id']`
        sSql = sSql + self.getWhere("",dicUser,1)
        
        dicResult =  oDatabase.xmlrpc_py_executeNormalQuery(sSql, dicUser )
        for sName in liNames:
            self.overwriteCal(sName,dicResult,dicuser)
