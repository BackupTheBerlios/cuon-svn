# coding=utf-8
##Copyright (C) [2009]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 


import time,  glob,  os
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
            for i in range(len(liTypeOfGrave)):
                liTypeOfGrave[i] = liTypeOfGrave[i] + '###'+`i`
        
        liTypeOfPaying0 = self.getConfigOption('CLIENT_' + `dicUser['client']`,'cbTypeOfPaying', cpServer)
        liTypeOfPaying = ['NONE']
        if liTypeOfPaying0:
            liTypeOfPaying = liTypeOfPaying0.split(',')
            for i in range(len(liTypeOfPaying)):
                liTypeOfPaying[i] = liTypeOfPaying[i] + '###'+`i`
                
                
        liPercents0 = self.getConfigOption('CLIENT_' + `dicUser['client']`,'cbPercentsGrave', cpServer)
        liPercents = ['NONE']
        if liPercents0:
            liPercents = liPercents0.split(',')
            
        liPeriodSpring0 = self.getConfigOption('CLIENT_' + `dicUser['client']`,'cbGraveSpringPeriod', cpServer)
        liPeriodSpring = ['NONE']
        if liPeriodSpring0:
            liPeriodSpring = liPeriodSpring0.split(',')
            
        liPeriodSummer0 = self.getConfigOption('CLIENT_' + `dicUser['client']`,'cbGraveSummerPeriod', cpServer)
        liPeriodSummer = ['NONE']
        if liPeriodSummer0:
            liPeriodSummer = liPeriodSummer0.split(',')
            
        liPeriodAutumn0 = self.getConfigOption('CLIENT_' + `dicUser['client']`,'cbGraveAutumnPeriod', cpServer)
        liPeriodAutumn = ['NONE']
        if liPeriodAutumn0:
            liPeriodAutumn = liPeriodAutumn0.split(',')
            
        liPeriodWinter0 = self.getConfigOption('CLIENT_' + `dicUser['client']`,'cbGraveWinterPeriod', cpServer)
        liPeriodWinter = ['NONE']
        if liPeriodWinter0:
            liPeriodWinter = liPeriodWinter0.split(',')
        
        liPeriodHolliday0 = self.getConfigOption('CLIENT_' + `dicUser['client']`,'cbGraveHollidayPeriod', cpServer)
        liPeriodHolliday = ['NONE']
        if liPeriodHolliday0:
            liPeriodHolliday = liPeriodHolliday0.split(',')
            
        liPeriodUnique0 = self.getConfigOption('CLIENT_' + `dicUser['client']`,'cbGraveUniquePeriod', cpServer)
        liPeriodUnique = ['NONE']
        if liPeriodUnique0:
            liPeriodUnique = liPeriodUnique0.split(',')
            
        liPeriodYearly0 = self.getConfigOption('CLIENT_' + `dicUser['client']`,'cbGraveYearlyPeriod', cpServer)
        liPeriodYearly = ['NONE']
        if liPeriodYearly0:
            liPeriodYearly = liPeriodYearly0.split(',')
            
  
        
        
        
        return liService, liTypeOfGrave, liTypeOfPaying, liPercents, liPeriodSpring, liPeriodSummer, liPeriodAutumn, liPeriodWinter, liPeriodHolliday,  liPeriodUnique, liPeriodYearly
        

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
        
    def xmlrpc_getGraveyards(self, dicUser):
        sSql = "select id,  shortname from graveyard "
        sSql += self.getWhere("", dicUser, 1)
        liGraveyards = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )
        print 'gr_list = ',  liGraveyards
    
        return liGraveyards


    def xmlrpc_getComboGraveyards(self, dicUser):
        liGraveyards = self.xmlrpc_getGraveyards(dicUser)
        print 'liGraveyards = ',  liGraveyards
        liReturn = []
        if liGraveyards and liGraveyards not in self.liSQL_ERRORS:
            for graveyard in liGraveyards:
                liReturn.append(graveyard['shortname'] + '###' + `graveyard['id']`)
        
        if not liReturn:
            liReturn = ['NONE']
        return liReturn
        
    
        
    def getGravePlantListValues(self,  dicSearchfields, dicUser, nRows):
        
        sSql = "select * from fct_getGravePlantListValues( array "  + `self.getListOfSearchFields(dicSearchfields)` +":: char[] ,  " + `nRows` + ")  as (graveyard_shortname varchar, graveyard_designation varchar,grave_firstname varchar, grave_lastname varchar ) "
        
        
        return self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )
        
    def getListOfSearchFields(self, dicSearchfields):
        liReturn = []
        liReturn.append('test')
        
        return liReturn
