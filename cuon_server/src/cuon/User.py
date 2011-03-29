
from twisted.web import xmlrpc
import os
import sys
import time
from datetime import datetime
import random   
import xmlrpclib
from basics import basics
import Database
import uuid
import urllib
import httplib
import md5


class User(xmlrpc.XMLRPC, basics):
    def __init__(self):
        basics.__init__(self)
        self.Database = Database.Database()
        self.home_url = 'www.cuon.org'
        self.headers = {'Content-type': 'application/x-www-form-urlencoded'}

    def xmlrpc_getNameOfStandardProfile(self, dicUser):
        sSql = 'select profile_name from preferences where username = \'' + dicUser['Name'] +'\' and is_standard_profile = TRUE'
        
        result = self.Database.xmlrpc_executeNormalQuery(sSql, dicUser )
        #print "Profile = ",  result
        
        if result not in ['NONE','ERROR']:
           return result[0]['profile_name']
        else:
           return result
           
    def xmlrpc_getStandardProfile(self, sProfile, dicUser):
        self.writeLog('Profile =' + `sProfile`)
        sSql = 'select * from preferences where username = \'' + dicUser['Name'] +'\' and profile_name = \'' + sProfile +'\''
        
        result = self.Database.xmlrpc_executeNormalQuery(sSql, dicUser )
        if result not in ['NONE','ERROR']:
           return result[0]
        else:
           return result

    def xmlrpc_getModulList(self, dicUser):
        #dicUser = {'Name':'jhamel'}
        cp1,f = self.getParser('/etc/cuon/menus.cfg')
        # Name of known modules
        # addresses
        # articles
        # biblio
        # account_book
        # order
        # dms
        # staff
        # expert_system
        values = ['all','addresses','articles','biblio','account_book','order','dms','staff','expert_system','forms','forms_addresses']
        dicUserModules = {}
        dicUserModules[dicUser['Name']] = []


        for key in values:
            value = self.getConfigOption(dicUser['Name'],key,cp1)
            
            if value:
                liValue = value.split('#')
                liKey = []
                for i in liValue:
                    i = i.strip()
                    liPoint = i.split(';')
                    print liPoint
                    print i
                    try:
                        
                        print 'item',liPoint
                        dicKey = {}

                        dicKey[key] = {liPoint[0]:liPoint[1]}
                        dicUserModules[dicUser['Name']].append(dicKey)
                        

                    except Exception,params:
                        print Exception,params
                
        values = ['extendet_gpl']
        
        
        dicKeys = []
        for key in values:
            value0 = self.getConfigOption(dicUser['Name'],key,cp1)
            
            if value0:
                liValue0 = value0.split('%')
                for value in liValue0:
                    liValue = value.split('#')
                    dicKey = {}
                    print 'Value', value
                    for i in liValue:
                        i = i.strip()
                        liPoint = i.split(';')
                        print 'liPoint',liPoint
                        print 'i = ', i
                        try:
                            if liPoint[1][0] == '[':
                                print 'list',liPoint
                                liList = (liPoint[1][1:len(liPoint[1])-1]).split(',')
                                print 'liList', liList
                                dicKey[liPoint[0]] = liList
                                print 'end 1'
                               
                            elif liPoint[1][0] == '{':
    
                                print 'dic',liPoint
                                liList = (liPoint[1][1:len(liPoint[1])-1]).split(',')
                                print 'liList', liList
                                liDics = {}
                                for list1 in liList:
                                    liD = list1.split(',')
                                    for dic in liD:
                                        dic_inv = dic.split(':')
                                        liDics[dic_inv[0]] = dic_inv[1]
                                        print liDics
                                dicKey[liPoint[0]] = liDics
                                print 'end 2'
                                
    
                            else:
                                print 'item',liPoint
    
                                dicKey[liPoint[0]] = liPoint[1]
                                print 'end 3'
                                
    
                        except Exception,params:
                            print Exception,params
                    
                    print 'DicKey ', dicKey
                    dicKeys.append(dicKey)
                dicUserModules[dicUser['Name']].append({key:dicKeys})
        
        dicModul = {}
        # User alle
        dicUserModules['AllUser'] = [{'all':{'Priv':'all'}},{'experimental':{'Priv':'all'}} ]
        dicUserModules['AllUser'].append({'staff':{'Priv':'all'}})
        #dicExt1 = {'extendet_gpl':[{'Priv':'all','MenuItem':{'Main':'data','Sub':'Extendet1'},'Imports':['cuon.Ext1.ext1','cuon.Ext1.ext2']}]}
        #dicExt1['extendet_gpl'][0]['MenuStart']='cuon.Ext1.ext1.ext1()'
        
        #dicUserModules['AllUser'].append(dicExt1)
        #print dicUserModules
        
        # User jhamel
##        dicUserModules['jhamel'] = [{'all':{'Priv':'all'}},{'experimental':{'Priv':'all'}} ]
##        dicUserModules['jhamel'].append({'staff':{'Priv':'all'}})
##        dicUserModules['jhamel'].append({'expert_system':{'Priv':'all'}})
##        dicUserModules['jhamel'].append({'project':{'Priv':'all'}})
##        dicUserModules['jhamel'].append({'forms':{'Priv':'all'}})
       
        #dicExt1 = {'extendet_gpl':[{'Priv':'all','MenuItem':{'Main':'data','Sub':'Extendet1', 'ExternalNumber':'ext1'},'Imports':['cuon.Ext1.ext1','cuon.Ext1.ext2']}]}
        #dicExt1['extendet_gpl'][0]['MenuStart']='cuon.Ext1.ext1.ext1()'
        
        
        #dicExt1['extendet_gpl'].append({'Priv':'all','MenuItem':{'Main':'action1','Sub':'hibernation1', 'ExternalNumber':'ext2'},'Imports':['cuon.Garden.hibernation','cuon.Garden.hibernation']})
       
        #dicExt1['extendet_gpl'][1]['MenuStart']='cuon.Garden.hibernation.hibernationwindow(self.allTables)'
        
        #dicExt1['extendet_gpl'].append({'Priv':'all','MenuItem':{'Main':'data','Sub':'botany1', 'ExternalNumber':'ext3'},'Imports':['cuon.Garden.botany','cuon.Garden.botany']})
        #dicExt1['extendet_gpl'][2]['MenuStart']='cuon.Garden.botany.botanywindow(self.allTables)'
        
        #dicUserModules[dicUser['Name']].append(dicExt1)
        
        
        
        
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
        print 'ModulesTest', dicUserModules
        return dicModul
        
    def xmlrpc_getClientInfo(self, dicUser):
        self.writeLog('Start1 execute py_getListsOfClients')
        
        dicUserClients = {}
        
        try:
            cpClients, f = self.getParser(self.CUON_FS + '/clients.ini')
            print 'f = ', f
            assert cpClients.get(dicUser['Name'], 'clientsRightCreate')
            assert cpClients.get(dicUser['Name'], 'clientsIDs')
            
            dicUserClients[dicUser['Name']]= {}
            dicUserClients[dicUser['Name']]['clientsRight']={}
            dicUserClients[dicUser['Name']]['clientsRight']['create']=cpClients.get(dicUser['Name'], 'clientsRightCreate')
            dicUserClients[dicUser['Name']]['clientsID']=cpClients.get(dicUser['Name'], 'clientsIDs').split(',')
            print 'dicUserClients-1', dicUserClients
        except Exception, params:
            print Exception, params
            dicUserClients['AllUser']={}
            dicUserClients['AllUser']['clientsRight']={}
            dicUserClients['AllUser']['clientsRight']['create']='NO'
            dicUserClients['AllUser']['clientsID']=[1]
            print 'dicUserClients-except', dicUserClients
        
        
        try:
           if dicUserClients.has_key(dicUser['Name']):
              dicClients = dicUserClients[dicUser['Name']]
           else:
              dicClients = dicUserClients['AllUser']
        except:
           pass
        self.writeLog('ListOfclients = ' + `dicClients`)
        
        return dicClients
    def xmlrpc_getDate(self, dicUser):
        #currentDate = time.localtime()
        #print currentDate
        #nD2 = datetime(currentDate[0], currentDate[1],currentDate[2],currentDate[3],currentDate[4], currentDate[5])
        dt = time.strftime(dicUser['DateformatString'])
        print dt
        return dt
        
    def xmlrpc_getStaffAddressString(self, dicUser):
        sSql = "select staff.lastname || ', ' || staff.firstname as address_string from staff where staff.cuon_username = '"
        sSql += dicUser['Name']  + "' " 
        sSql += self.getWhere('', dicUser, Single = 2)
        result = self.Database.xmlrpc_executeNormalQuery(sSql, dicUser )
        if result not in ['NONE','ERROR']:
            return result[0]['address_string']
        else:
            return result
        
    def xmlrpc_setUserData(self,  dicUser): 
        # first check uuid 
        try:
            if self.SEND_VERSION_INFO == 'YES':
                sSql = "select client_uuid from clients where id = " + `dicUser['client']`
                clientUUID =  self.Database.xmlrpc_executeNormalQuery(sSql, dicUser )[0]['client_uuid']
                id, dicVersion = self.Database.xmlrpc_getLastVersion()
                print 'db client UUID ',  clientUUID,  len(clientUUID)
                if clientUUID and clientUUID not in self.liSQL_ERRORS and len(clientUUID) == 36:
                    pass
                else:
                    clientUUID = str(uuid.uuid4())
                    sSql = "update clients set client_uuid = '" + clientUUID +"' where  id = " + `dicUser['client']`
                    self.Database.xmlrpc_executeNormalQuery(sSql, dicUser )
                #response, content = http.request(self.home_url + clientUUID, 'GET', headers=headers)   
                sInfo = clientUUID +'###' +  md5.new(dicUser['Name']).hexdigest() + '###' + `dicVersion['Major']` +'.' + `dicVersion['Minor']` + '-' + `dicVersion['Rev']` + '###' + `dicUser['client']`
                
                try:
                    conn = httplib.HTTPConnection(self.home_url, 6080)
                    conn.request("GET", '/sayVersion/' +sInfo)
                    #r2 = conn.getresponse()
                    conn.close()
                except:
                    pass
        except:
            pass
            
        sSql = "select * from fct_setUserData( array " +`self.getUserInfo(dicUser)` + " )"
        print sSql
        return self.Database.xmlrpc_executeNormalQuery(sSql, dicUser )
        
