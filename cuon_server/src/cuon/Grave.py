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
import types
from copy import deepcopy
import Order

class Grave(xmlrpc.XMLRPC, basics):
    def __init__(self):
        basics.__init__(self)
        self.oDatabase = Database.Database()
    def xmlrpc_getComboBoxEntries(self, dicUser):
        liGraveyards = []
        liPercents = []
        liPeriodAutumn = []
        liPeriodHolliday = []
        liPeriodSpring = []
        liPeriodSummer = []
        liPeriodWinter = []
        liPeriodUnique = []
        liPeriodYearly = []
        liTimeTab = []
        liSorting = []
        liTypeOfGrave = []
        
        cpServer, f = self.getParser(self.CUON_FS + '/clients.ini')
        liTimeTab0 = self.getConfigOption('CLIENT_' + `dicUser['client']`,'cbGraveTypeOfTab', cpServer)
        liTimeTab = ['NONE']
        if liTimeTab0:
            liTimeTab = liTimeTab0.split(',')
        
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
            
        liSorting0 = self.getConfigOption('CLIENT_' + `dicUser['client']`,'cbGraveSorting', cpServer)
        liSorting = ['NONE']
        if liSorting0:
            liSorting = liSorting0.split(',')
        
        
        
        return liTimeTab, liTypeOfGrave, liTypeOfPaying, liPercents, liPeriodSpring, liPeriodSummer, liPeriodAutumn, liPeriodWinter, liPeriodHolliday,  liPeriodUnique, liPeriodYearly,  liSorting
        
        
    def xmlrpc_getService(self, dicUser,  timeTab):
        
        sService = None
        liTimeTab = ['NONE']
        
        if timeTab == 0:
            sService = 'cbGraveService'
        elif timeTab == 1:
             sService = 'cbGraveSpringPeriod'
        elif timeTab == 2:
             sService = 'cbGraveSummerPeriod'
        elif timeTab == 3:
             sService = 'cbGraveAutumnPeriod'
             
        elif timeTab == 4:
             sService = 'cbGraveHollidayPeriod'
             
        elif timeTab == 5:
             sService = 'cbGraveWinterPeriod'
        elif timeTab == 6:
             sService = 'cbGraveYearlyPeriod'
        elif timeTab == 7:
             sService = 'cbGraveUniquePeriod'
        
                
       
             
        if sService:     
            cpServer, f = self.getParser(self.CUON_FS + '/clients.ini')
            liTimeTab0 = self.getConfigOption('CLIENT_' + `dicUser['client']`,sService,  cpServer)
            liTimeTab = ['NONE']
            if liTimeTab0:
                liTimeTab = liTimeTab0.split(',')
            
        return liTimeTab
        
    
        
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
        
    
        
    def getGravePlantListValues(self,  liSearchfields, dicUser, nRows):
        
        sSql = "select * from fct_getGravePlantListValues( "  
        
        for sSearch in liSearchfields:
            if isinstance(sSearch,  types.IntType):
                sSql += `sSearch` + ",  " 
            else:
                sSearch = sSearch.strip().replace("'", "#!#")
                sSql += "'" + sSearch + "',  " 
            
        
        
        sSql +=  `nRows` + ", " + `dicUser['iOrderSort']` + " )  as (graveyard_id integer, grave_id integer, graveyard_shortname varchar, graveyard_designation varchar,grave_firstname varchar, grave_lastname varchar, grave_pos_number integer , grave_contract_begins_at date , grave_contract_ends_at date , grave_detachment varchar, grave_grave_number varchar) "
        
        print 'grave list sql = ',  sSql
        
        return self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )
        
    def getGravePlantListArticles(self,  liSearchfields, dicUser, nRows):
        
        sSql = "select * from fct_getGravePlantListArticles( "  
        
        for sSearch in liSearchfields:
            if isinstance(sSearch,  types.IntType):
                sSql += `sSearch` + ",  " 
            else:
                sSearch = sSearch.strip().replace("'", "#!#")
                sSql += "'" + sSearch + "',  " 
            
        
        
        sSql +=  `nRows` + ", " + `dicUser['iOrderSort']` + " )  as (graveyard_id integer, grave_id integer, graveyard_shortname varchar, graveyard_designation varchar,grave_firstname varchar, grave_lastname varchar, grave_pos_number integer , grave_contract_begins_at date , grave_contract_ends_at date , grave_detachment varchar, grave_grave_number varchar, service_article_id integer, article_number varchar(150), article_designation varchar(250),service_price float, service_count float, article_notes text, service_notes text, grave_notes text) "
        
        print 'grave list sql = ',  sSql
        
        result1 =  self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )
        self.writeLog( 'result1 = ' + `result1`)
        result2 = []
        for row1 in result1:
            found = False
            #self.writeLog('Row1 = ' +  `row1`)
            if result2:
                for iRow2 in range(len(result2)):
                    #self.writeLog('iRow2 = ' + `iRow2`)
                    if result2[iRow2]['service_article_id'] == row1['service_article_id']:
                        result2[iRow2]['service_count'] += row1['service_count']
                        found = True
                        break 
                        
            if not found:
                result2.append(deepcopy(row1))
                
        #self.writeLog( 'result2 = ' + `result2`)
        
        return result1,  result2
   
    def xmlrpc_calcAllPrices(self,  dicUser):
        bOK = False
        
        
        
        return bOK 
        
        
    def xmlrpc_createAllNewInvoice(self,  dicUser,  liValues):
        print 'All Invoices',  liValues
        bOK = False
        
        
        return bOK
        
        
    def xmlrpc_createNewInvoice(self,  dicUser,  liValues,  graveID):
        print '1 new Invoice',  liValues
        liService = liValues[0]
        print 'new Invoice = ', liService,  graveID 
        defaultOrderNumber = ''
        defaultOrderDesignation  = ''
        oOrder = Order.Order()
        
        #oOrder.checkDefaultOrder(dicUser,  id) 
        sSql = "select * from fct_createNewInvoice('" + liService[0] + "' , " + `graveID` + "  ) as order_id "
        
        allInvoices = self.oDatabase.xmlrpc_executeNormalQuery(sSql,  dicUser )
        
        for i in range(len(allInvoices)):
            newOrderID = allInvoices[i]['order_id']
            if newOrderID > 0:
                
                for sService in liService:
                    dicValues,  sSave  = oOrder.checkDefaultOrder(dicUser,  newOrderID)
                    if sSave:
                        dR4 = self.oDatabase.xmlrpc_saveRecord('orderbook', newOrderID, dicValues, dicUser, 'NO')
                    
                    if i == len(allInvoices):
                        
                        sSql = "select * from fct_addPositionToInvoice('" + sService + "' , " + `newOrderID` + ",1  ) as bOK "
                    else:
                        sSql = "select * from fct_addPositionToInvoice('" + sService + "' , " + `newOrderID` + " ,0 ) as bOK "
                        
                    self.oDatabase.xmlrpc_executeNormalQuery(sSql,  dicUser ) 
        
        
        # Now mark it as done 
        sSql = " update grave set created_order = 1 where id = " + `graveID` ;
        self.oDatabase.xmlrpc_executeNormalQuery(sSql,  dicUser ) 
        
        
        return newOrderID
        
