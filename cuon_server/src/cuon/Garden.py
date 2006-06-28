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
        
        dicResult =  oDatabase.xmlrpc_py_executeNormalQuery(sSql, dicUser )
        if dicResult == 'NONE':
            sSql1 = 'insert into list_of_deliveries ( id, delivery_number, order_number) '
            sSql1 = sSql1 + ' values (nextval(\'list_of_deliveries_id+ sc +\'),nextval(\'numerical_misc_standard_delivery +sc +\'), ' 
            sSql1 = sSql1 + `orderNumber` + ' )'
        
            oDatabase.xmlrpc_executeNormalQuery(sSql1, dicUser )
        
            dicResult =  oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )
        
        if dicResult != 'NONE':
           nr = dicResult[0]['delivery_number']
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

        sSql = "select hibernation.hibernation_number as order_number,  "
        Sql = sSql + " to_char(hibernation.begin_date, \'" + dicUser['SQLDateFormat'] + "\')  as begin_date ,"
        sSql = sSql + " hibernation.begin_working_time as  begin_working_time, "
   
        sSql = sSql + " address.lastname as lastname, address.lastname2 as lastname2, "
        sSql = sSql + " address.firstname as firstname, "

        sSql = sSql + " address.street as street, (address.zip || ' ' ||  address.city)  as city "
        sSql = sSql + " from hibernation, address where hibernation.id = \'" + `dicOrder['orderNumber']` +"\' " 
        sSql = sSql + "and address.id = hibernation.addressnumber" 
        self.writeLog('xmlrpc_getIncomingAddress = ' + `sSql`)
        return self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )
        
        
    def xmlrpc_getPickupData(self, dicOrder, dicUser):
        
        sSql = "select orderbook.number as order_number, orderbook.designation as order_designation  "
        sSql = sSql + " from orderbook, orderget where orderbook.number = \'" + dicOrder['orderNumber'] +"\' "
        sSql = sSql + "and orderget.ordernumber = orderbook.id  " 
        sSql = sSql + " order by orderbook.number "
        return self.executeNormalQuery(sSql, dicUser )
        
        
    def xmlrpc_getIncomingNumber(self, orderNumber, dicUser):
                
        nr = 0
        sSql = 'select incoming_number from list_of_hibernation_incoming where order_number = ' + `orderNumber`
        print sSql 
        dicResult =  self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )
        if dicResult != 'NONE':
           sSql1 = 'insert into list_of_hibernation_incoming ( id, incoming_number, order_number) '
           sSql1 = sSql1 + ' values (nextval(\'list_of_hibernation_incoming_id\'),nextval(\'numerical_garden_incoming_document\'), ' 
           sSql1 = sSql1 + `orderNumber` + ' )'
        
           self.oDatabase.xmlrpc_executeNormalQuery(sSql1, dicUser )
        
        dicResult =  self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )
        
        if dicResult != 'NONE':
           nr = dicResult[0]['incoming_number']
        return nr
               
    def xmlrpc_getHibernationIncoming(self, dicOrder , dicUser):
        sSql = "select hibernation.hibernation_number as order_number,  "
        sSql = sSql + " to_char(hibernation.begin_date, \'" + dicUser['SQLDateFormat'] + "\')  as begin_date ,"
        sSql = sSql + " hibernation.begin_working_time as  begin_working_time, "
        #sSql = sSql + " orderposition.tax_vat as tax_vat, "
        sSql = sSql + " hibernation_plant.plant_number as article_id,  "
        #sSql = sSql + " hibernation_plant.amount as amount, "
        sSql = sSql + " hibernation_plant.price as price, "
	sSql = sSql + " botany.botany_name as botany_name "
        sSql = sSql + " from hibernation, hibernation_plant, botany where hibernation.id = \'" + `dicOrder['orderNumber']` +"\' "
        sSql = sSql + "and hibernation_plant.hibernation_number = hibernation.id "
	sSql = sSql + "and hibernation_plant.botany_number = botany.id and "
	sSql = sSql + " hibernation.client = " + `dicUser['client']` 
        sSql = sSql + " order by hibernation_plant.plant_number "
        dicUser['noWhereClient'] = 'Yes'
        print sSql
        return self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )
