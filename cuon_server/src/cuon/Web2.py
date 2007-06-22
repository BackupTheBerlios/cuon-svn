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
        # 0 = Root-site
        # 1 = Linked-Site
        # 2 = Upload
        # 3 = download
        # 4 = Image
        # 5 = Python code
        # 6 = Directory structure
        # 7 
        self.TypeRootSite = 0
        self.TypeLinkedSite = 1
        self.TypePython = 2
        self.TypeDir = 3


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
    def getLinkedStructure(self):
        liSites = ['root']
        newSites = ['root']
        ok = True 
        while ok:
            if newSites:
                liOk = []
                for sKey in newSites:
                    liS = self.getNextSites(sKey)
                    for s in liS:
                        liSites.append(s)
                        liOk.append(s)
            if not liOk:
                ok = False
            else:
                newSites = liOk
        
        return liSites
        
                
    def getNextSites(self, sKey):
        liSites = []
        sSql = "select name from web2 where type = " + `self.TypeLinkedSite` +" and root_keys ~'" + sKey +"' and char_length(linked_keys) > 0 "
        result = self.oDatabase.xmlrpc_executeNormalQuery(sSql, self.dicUser)
        print result
        if result and result != 'NONE':
            for site in result:
                liSites.append(site['name'].strip())
        
        print liSites
        return liSites
        
        
    def getDirectoryStructure(self):
        sSql = "select * from web2 where type = " + `self.TypeDir`
        result = self.oDatabase.xmlrpc_executeNormalQuery(sSql, self.dicUser)
        
        return result
         
##    
##        
##    def xmlrpc_updateCalendar(self, liNames, dicData, dicUser):
##        sSql = 'select * from partner_schedul where partner_id = ' + `dicData['partner_id']`
##        sSql = sSql + self.getWhere("",dicUser,1)
##        
##        dicResult =  oDatabase.xmlrpc_py_executeNormalQuery(sSql, dicUser )
##        for sName in liNames:
##            self.overwriteCal(sName,dicResult,dicuser)
