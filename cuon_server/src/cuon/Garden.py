import time
from datetime import datetime
import random
import xmlrpclib
from twisted.web import xmlrpc
 
from basics import basics
import Database

class Garden(xmlrpc.XMLRPC, basics):
    def __init__(self):
        basics.__init__(self)
        self.oDatabase = Database.Database()
        

    def xmlrpc_getOutgoingNumber(self, orderNumber, dicUser ):
        nr = 0
        sc = '_client_' + `dicUser['client']`
        sSql = 'select delivery_number from list_of_deliveries where order_number = ' + `orderNumber`
        sSql = sSql + self.getWhere("",dicUser,1)
        
        dicResult =  self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )
        if dicResult == 'NONE':
            sSql1 = 'insert into list_of_deliveries ( id, delivery_number, order_number) '
            sSql1 = sSql1 + ' values (nextval(\'list_of_deliveries_id+ sc +\'),nextval(\'numerical_misc_standard_delivery +sc +\'), ' 
            sSql1 = sSql1 + `orderNumber` + ' )'
        
            self.oDatabase.xmlrpc_executeNormalQuery(sSql1, dicUser )
        
            dicResult =  self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )
        
        if dicResult != 'NONE':
           nr = dicResult[0]['delivery_number']
        return nr
        
    def xmlrpc_getNewSequenceNumber(self, year, dicUser ):
        nr = 0
        sSql = "select max(sequence_of_stock) as nr from hibernation  where date_part('year', \"begin_date\") = " + `year`
        sSql = sSql + self.getWhere("",dicUser,2)
        
        dicResult =  self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )
        if dicResult == 'NONE':
            nr = 0
        else:
            nr = dicResult[0]['nr']
        
        return nr
            

    def xmlrpc_getInvoiceAddress(self, dicOrder, dicUser):
        
        sSql = "select orderbook.number as order_number, orderbook.designation as order_designation , "
        sSql = sSql + " to_char(orderbook.orderedat, \'" + dicUser['SQLDateFormat'] + "\')  as o_orderedat ,"
        sSql = sSql + " to_char(orderbook.deliveredat, \'" + dicUser['SQLDateFormat'] + "\') as  order_deliverdat, "
        sSql = sSql + " address.lastname as lastname, address.lastname2 as lastname2, "
        sSql = sSql + " address.street as street, (address.zip || ' ' ||  address.city)  as city "
        sSql = sSql + " from orderbook, address where orderbook.number = \'" + dicOrder['orderNumber'] +"\' " 
        sSql = sSql + "and address.id = orderbook.addressnumber" 
        
        return self.oDatabase.xmlrpc_py_executeNormalQuery(sSql, dicUser )

    def xmlrpc_getInvoiceNumber(self, orderNumber, dicUser):
        
        nr = 0
        sc = '_client_' + `dicUser['client']`
        
        sSql = 'select invoice_number from list_of_invoices where order_number = ' + `orderNumber`
        
        dicResult =  self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )
        if dicResult != 'NONE':
           sSql1 = 'insert into list_of_invoices ( id, invoice_number, order_number) '
           sSql1 = sSql1 + ' values (nextval(\'list_of_invoices_id +sc +\'),nextval(\'numerical_misc_standard_invoice + sc + \'), ' 
           sSql1 = sSql1 + `orderNumber` + ' )'
           self.oDatabase.xmlrpc_executeNormalQuery(sSql1, dicUser )
        
        dicResult =  self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )
        
        if dicResult != 'NONE':
           nr = dicResult[0]['invoice_number']
        return nr

    def xmlrpc_getIncomingAddress(self, dicOrder, dicUser):
        
         
        liFields = []
        liFields.append(["hibernation.hibernation_number","order_number"])
        liFields.append(["to_char(hibernation.begin_date, \'" + dicUser['SQLDateFormat'] + "\')","begin_date"])
        liFields.append(["hibernation.begin_working_time","begin_working_time"])
        liFields.append(["hibernation.begin_notes","begin_notes"])
        liFields.append(["hibernation.ends_notes","ends_notes"])

        liFields.append(["address.address","address"])
        liFields.append(["address.lastname","lastname"])
        liFields.append(["address.lastname2","lastname2"])
        liFields.append(["address.firstname","firstname"])
        liFields.append(["address.street","street"])
        liFields.append(["(address.zip || ' ' ||  address.city)","city "])
        
        sSql = "select " + self.oDatabase.bindSql(liFields) 
        
        sSql = sSql + " from hibernation, address where hibernation.id = \'" + `dicOrder['orderNumber']` +"\' " 
        sSql = sSql + "and address.id = hibernation.addressnumber" 
        self.writeLog('xmlrpc_getIncomingAddress = ' + `sSql`)
        print sSql

        liResult = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )
        try:
            if liResult:
                dicResult = liResult[0]
                if dicResult['firstname'] == None:
                    dicResult['first_last'] = dicResult['lastname']
                    dicResult['last_first'] = dicResult['lastname']
                else:
                    dicResult['first_last'] = dicResult['firstname'] + ' ' + dicResult['lastname']
                    dicResult['last_first'] = dicResult['lastname'] + ', ' + dicResult['firstname']
                liResult[0] = dicResult
        except Exception, params:
            print Exception, params
    

        return liResult
        
        
    def xmlrpc_getPickupData(self, dicOrder, dicUser):
        
        sSql = "select orderbook.number as order_number, orderbook.designation as order_designation  "
        sSql = sSql + " from orderbook, orderget where orderbook.number = \'" + dicOrder['orderNumber'] +"\' "
        sSql = sSql + "and orderget.ordernumber = orderbook.id  " 
        sSql = sSql + " order by orderbook.number "
        return self.executeNormalQuery(sSql, dicUser )
        
        
    def xmlrpc_getIncomingNumber(self, orderNumber, dicUser):
                
        nr = 0
        sSqlSearch = 'select incoming_number from list_of_hibernation_incoming where order_number = ' \
            + `orderNumber`  + ' and client = ' + `dicUser['client']`
        dicResult =  self.oDatabase.xmlrpc_executeNormalQuery(sSqlSearch, dicUser )
        if dicResult == 'NONE':
           sSql1 = 'insert into list_of_hibernation_incoming ( id, incoming_number, order_number) '
           sSql1 = sSql1 + ' values (nextval(\'list_of_hibernation_incoming_id\'),nextval(\'numerical_hibernation_incoming_document_client_'  \
            + `dicUser['client']` +'\'), ' 
           sSql1 = sSql1 + `orderNumber` + ' )'
           self.oDatabase.xmlrpc_executeNormalQuery(sSql1, dicUser )
        
           dicResult =  self.oDatabase.xmlrpc_executeNormalQuery(sSqlSearch, dicUser )
        
        if dicResult != 'NONE':
           nr = dicResult[0]['incoming_number']
        return nr
               
    def xmlrpc_getPickupNumber(self, orderNumber, dicUser):
                
        nr = 0
        sSqlSearch = 'select pickup_number from list_of_hibernation_pickup where order_number = ' + `orderNumber`
        dicResult =  self.oDatabase.xmlrpc_executeNormalQuery(sSqlSearch, dicUser )
        if dicResult == 'NONE':
           sSql1 = 'insert into list_of_hibernation_pickup ( id, incoming_number, order_number) '
           sSql1 = sSql1 + ' values (nextval(\'list_of_hibernation_pickup_id\'),nextval(\'numerical_hibernation_pickup_document_client_' + `dicUser['client']` + '\'), ' 
           sSql1 = sSql1 + `orderNumber` + ' )'
           self.oDatabase.xmlrpc_executeNormalQuery(sSql1, dicUser )
           
           dicResult =  self.oDatabase.xmlrpc_executeNormalQuery(sSqlSearch, dicUser )
        
        if dicResult != 'NONE':
           nr = dicResult[0]['incoming_number']
        
            
        return nr   
    def xmlrpc_getNewHibernationNumber(self, dicUser):
        sSql = 'select nextval(\'numerical_hibernation_ordernumber_client_' + `dicUser['client']` + '\') as number '
        result = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )
        Number = 0
        try:
            Number = result[0]['number']
        except Exception, params:
            print Exception, params
        return Number
        
        
    def xmlrpc_getHibernationIncoming(self, dicOrder , dicUser):
        
        liFields = []
        liFields.append(['hibernation.hibernation_number','order_number'])
        liFields.append(["to_char(hibernation.begin_date, \'" + dicUser['SQLDateFormat'] + "\')","begin_date"])
        liFields.append(["hibernation.begin_working_time","begin_working_time"])
        liFields.append(["hibernation_plant.plant_number","article_id"])
        liFields.append(["hibernation_plant.price","price"])
        liFields.append(["hibernation_plant.plant_status","status"])
        liFields.append(["hibernation_plant.plant_notice","plantnotice"])
        liFields.append(["hibernation_plant.vermin","vermin"])
        liFields.append(["hibernation_plant.diameter","diameter"])

        liFields.append(["botany.botany_name","botany_name"])
        liFields.append(["botany.local_name","local_name"])
        
    
        sSql = "select " + self.oDatabase.bindSql(liFields)
        
        
            
        sSql = sSql + " from hibernation, hibernation_plant, botany where hibernation.id = \'" + `dicOrder['orderNumber']` +"\' "
        sSql = sSql + "and hibernation_plant.hibernation_number = hibernation.id "
        sSql = sSql + "and hibernation_plant.botany_number = botany.id and "
        sSql = sSql + " hibernation.client = " + `dicUser['client']` 
        sSql = sSql + " order by hibernation_plant.plant_number "
        dicUser['noWhereClient'] = 'Yes'
        print sSql
        return self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )
    def xmlrpc_getHibernationPickup(self, dicOrder , dicUser):
        
        liFields = []
        liFields.append(['hibernation.hibernation_number','order_number'])
        liFields.append(["to_char(hibernation.begin_date, \'" + dicUser['SQLDateFormat'] + "\')","begin_date"])
        liFields.append(["hibernation.begin_working_time","begin_working_time"])
        liFields.append(["hibernation_plant.plant_number","article_id"])
        liFields.append(["hibernation_plant.price","price"])
        liFields.append(["hibernation_plant.plant_status","status"])
        liFields.append(["hibernation_plant.plant_notice","plantnotice"])
        liFields.append(["hibernation_plant.vermin","vermin"])
        liFields.append(["hibernation_plant.diameter","diameter"])

        liFields.append(["botany.botany_name","botany_name"])
        liFields.append(["botany.local_name","local_name"])
        
    
        sSql = "select " + self.oDatabase.bindSql(liFields)
        
        
            
        sSql = sSql + " from hibernation, hibernation_plant, botany where hibernation.id = \'" + `dicOrder['orderNumber']` +"\' "
        sSql = sSql + "and hibernation_plant.hibernation_number = hibernation.id "
        sSql = sSql + "and hibernation_plant.botany_number = botany.id and "
        sSql = sSql + " hibernation.client = " + `dicUser['client']` 
        sSql = sSql + " order by hibernation_plant.plant_number "
        dicUser['noWhereClient'] = 'Yes'
        print sSql
        return self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )

    def xmlrpc_reorgPlantNumber(self, hib_nr, dicUser):
        print 'hib_nr', hib_nr
        ok = True
        
        sSql = 'select hibernation_plant.id as id from hibernation_plant, botany where hibernation_number = ' + `hib_nr`
        sSql += ' and hibernation_plant.botany_number = botany.id '
        
        sSql += self.getWhere("",dicUser,2,'hibernation_plant.')
        sSql += ' order by botany.botany_name'
        print sSql
        
        result = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )
        print result
        z1 = 1
        for ids in result:
            print ids
            sSql = 'update hibernation_plant set plant_number = ' + `z1` + ' where id = ' + `ids['id']`
            result = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )
            z1 += 1
            
            
        return ok

    def xmlrpc_getOrderPositions(self, hibID, dicUser):
        sSql ='select hibernation_plant.*, botany.* from hibernation_plant, botany where hibernation_plant.hibernation_number = ' + `hibID`
        sSql += ' and hibernation_plant.botany_number = botany.id '
        
        sSql += self.getWhere("",dicUser,2,'hibernation_plant.')
        result = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )
        print 'getOrderPositions.result: ', result
        result2 = []
        if result != 'NONE':
            for row in result:
                print row
                
        return result
        
     
