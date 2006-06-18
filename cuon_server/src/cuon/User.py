
from twisted.web import xmlrpc
import os
import sys
import time
import random	
import xmlrpclib
import pg
from basics import basics
import Database

class User(xmlrpc.XMLRPC, basics):
    def __init__(self):
        basics.__init__(self)
        self.Database = Database.Database()
        
    def xmlrpc_getNameOfStandardProfile(self, dicUser):
        sSql = 'select profile_name from preferences where username = \'' + dicUser['Name'] +'\' and is_standard_profile = TRUE'
        
        result = self.Database.xmlrpc_executeNormalQuery(sSql, dicUser )
        if result != 'NONE':
           return result[0]['profile_name']
        else:
           return result
           
    def xmlrpc_getStandardProfile(self, sProfile, dicUser):
        self.writeLog('Profile =' + `sProfile`)
        sSql = 'select * from preferences where username = \'' + dicUser['Name'] +'\' and profile_name = \'' + sProfile +'\''
        
        result = self.Database.xmlrpc_executeNormalQuery(sSql, dicUser )
        if result != 'NONE':
           return result[0]
        else:
           return result

    def xmlrpc_getModulList(self, dicUser):
        dicUser = {'Name':'jhamel'}
        dicUserModules = {}
        # Name of known modules
        # addresses
        # articles
        # biblio
        # account_book
        # order
        # dms
        # staff
        # expert_system
        
        dicModul = {}
        # User alle
        dicUserModules['AllUser'] = [{'all':{'Priv':'all'}},{'experimental':{'Priv':'all'}} ]
        dicUserModules['AllUser'].append({'staff':{'Priv':'all'}})
        dicExt1 = {'extendet_gpl':[{'Priv':'all','MenuItem':{'Main':'data','Sub':'Extendet1'},'Imports':['cuon.Ext1.ext1','cuon.Ext1.ext2']}]}
        dicExt1['extendet_gpl'][0]['MenuStart']='cuon.Ext1.ext1.ext1()'
        
        dicUserModules['AllUser'].append(dicExt1)
        
        
        # User jhamel
        dicUserModules['jhamel'] = [{'all':{'Priv':'all'}},{'experimental':{'Priv':'all'}} ]
        dicUserModules['jhamel'].append({'staff':{'Priv':'all'}})
        dicUserModules['jhamel'].append({'expert_system':{'Priv':'all'}})
        dicUserModules['jhamel'].append({'project':{'Priv':'all'}})
        
        dicExt1 = {'extendet_gpl':[{'Priv':'all','MenuItem':{'Main':'data','Sub':'Extendet1', 'ExternalNumber':'ext1'},'Imports':['cuon.Ext1.ext1','cuon.Ext1.ext2']}]}
        dicExt1['extendet_gpl'][0]['MenuStart']='cuon.Ext1.ext1.ext1()'
        
        
        dicExt1['extendet_gpl'].append({'Priv':'all','MenuItem':{'Main':'action1','Sub':'hibernation1', 'ExternalNumber':'ext2'},'Imports':['cuon.Garden.hibernation','cuon.Garden.hibernation']})
        dicExt1['extendet_gpl'][1]['MenuStart']='cuon.Garden.hibernation.hibernationwindow(self.allTables)'
        
        dicExt1['extendet_gpl'].append({'Priv':'all','MenuItem':{'Main':'data','Sub':'botany1', 'ExternalNumber':'ext3'},'Imports':['cuon.Garden.botany','cuon.Garden.botany']})
        dicExt1['extendet_gpl'][2]['MenuStart']='cuon.Garden.botany.botanywindow(self.allTables)'
        
        dicUserModules['jhamel'].append(dicExt1)
        
        
        
        
        # User cuon
        dicUserModules['cuon'] = [{'all':{'Priv':'all'}},{'experimental':{'Priv':'all'}} ]
        dicUserModules['cuon'].append({'staff':{'Priv':'all'}})
        dicExt1 = {'extendet_gpl':[{'Priv':'all','MenuItem':{'Main':'data','Sub':'Extendet1'},'Imports':['cuon.Ext1.ext1','cuon.Ext1.ext2']}]}
        dicExt1['extendet_gpl'][0]['MenuStart']='cuon.Ext1.ext1.ext1()'
        
        dicUserModules['cuon'].append(dicExt1)
        
        
        
        try:
           if dicUserModules.has_key(dicUser['Name']):
              dicModul = dicUserModules[dicUser['Name']]
           else:
              dicModul = dicUserModules['AllUser']
        except:
           pass
        
        return dicModul
        
    def xmlrpc_getClientInfo(self, dicUser):
        self.writeLog('Start1 execute py_getListsOfClients')
        
        dicUserClients = {}
        
        dicUserClients['AllUser']={}
        dicUserClients['AllUser']['clientsRight']={}
        dicUserClients['AllUser']['clientsRight']['create']='NO'
        dicUserClients['AllUser']['clientsID']=[1]
        
        
        try:
           if dicUserClients.has_key(dicUser['Name']):
              dicClients = dicUserClients[dicUser['Name']]
           else:
              dicClients = dicUserClients['AllUser']
        except:
           pass
        self.writeLog('ListOfclients = ' + `dicClients`)
        
        return dicClients