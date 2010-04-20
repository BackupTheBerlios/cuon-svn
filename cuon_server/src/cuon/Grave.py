import time
import time
from datetime import datetime
import random
import xmlrpclib
from twisted.web import xmlrpc
from basics import basics
import Database

class Grave(xmlrpc.XMLRPC, basics):
    def __init__(self):
        basics.__init__(self)
        self.oDatabase = Database.Database()
    def xmlrpc_getComboBoxEntries(self, dicUser):
        cpServer, f = self.getParser(self.CUON_FS + '/clients.ini')
        liService0 = self.getConfigOption('CLIENT_' + `dicUser['client']`,'cbGraveService', cpServer)
        liService = ['NONE']
        if liService0:
            liService = liService0.split(',')
        
        liTypeOfGrave0 = self.getConfigOption('CLIENT_' + `dicUser['client']`,'cbTypeOfGrave', cpServer)
        liTypeOfGrave = ['NONE']
        if liTypeOfGrave0:
            liTypeOfGrave = liTypeOfGrave0.split(',')
        
        liTypeOfPaying0 = self.getConfigOption('CLIENT_' + `dicUser['client']`,'cbTypeOfPaying', cpServer)
        liTypeOfPaying = ['NONE']
        if liTypeOfPaying0:
            liTypeOfPaying = liTypeOfPaying0.split(',')
            
        liPercents0 = self.getConfigOption('CLIENT_' + `dicUser['client']`,'cbPercentsGrave', cpServer)
        liPercents = ['NONE']
        if liPercents0:
            liPercents = liPercents0.split(',')
            
        
        
        
        
        
        return liService, liTypeOfGrave, liTypeOfPaying, liPercents
        

    def xmlrpc_getComboBoxEntriesPeriod(self, dicUser):
        cpServer, f = self.getParser(self.CUON_FS + '/clients.ini')
        liSpringPeriod0 = self.getConfigOption('CLIENT_' + `dicUser['client']`,'cbGraveSpringPeriod', cpServer)
        liSpringPeriod = ['NONE']
        if liSpringPeriod0:
            liSpringPeriod = liSpringPeriod0.split(',')  
            
            
            
        return liSpringPeriod

    def xmlrpc_getGravesForAddress(self, addressid, dicUser):
        sSql = "select * from fct_getGravesForAddressID(" + `addressid` +")  as Graves "
        dicResult = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )
        
        return dicResult
    def xmlrpc_createNewGrave(self,  dicUser, dicGrave):
        print 'create new Order'
        
        dicValues = {}
        
        if dicGrave.has_key( 'addressid'):   
            dicValues['addressid'] = [dicGrave['addressid'],'int']
        if dicGrave.has_key( 'graveyardid'):   
            dicValues['graveyardid'] = [dicGrave['graveyardid'],'int']
            
        newID =  self.oDatabase.xmlrpc_saveRecord('grave', -1, dicValues, dicUser, 'NO')
        
        return newID
        
        
