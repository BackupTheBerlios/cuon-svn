import time
from datetime import datetime
import random
import xmlrpclib
from twisted.web import xmlrpc
 
from basics import basics
import Database

class Order(xmlrpc.XMLRPC, basics):
    def __init__(self):
        basics.__init__(self)
        self.oDatabase = Database.Database()
        
        

    def xmlrpc_getDeliveryNumber(self, orderNumber, dicUser ):
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

    def xmlrpc_getPickupAddress(self, dicOrder, dicUser):

        sSql = "select orderbook.number as order_number, orderbook.designation as order_designation , "
        sSql = sSql + " to_char(orderbook.orderedat, \'" + dicUser['SQLDateFormat'] + "\')  as o_orderedat ,"
        sSql = sSql + " to_char(orderbook.deliveredat, \'" + dicUser['SQLDateFormat'] + "\') as  order_deliverdat, "
        sSql = sSql + " address.lastname as lastname, address.lastname2 as lastname2, "
        sSql = sSql + " address.street as street, (address.zip || ' ' ||  address.city)  as city "
        sSql = sSql + " from orderbook, address where orderbook.number = \'" + dicOrder['orderNumber'] +"\' " 
        sSql = sSql + "and address.id = orderbook.addressnumber" 
        
        return self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )
    def xmlrpc_getPickupData(self, dicOrder, dicUser):
        
        sSql = "select orderbook.number as order_number, orderbook.designation as order_designation  "
        sSql = sSql + " from orderbook, orderget where orderbook.number = \'" + dicOrder['orderNumber'] +"\' "
        sSql = sSql + "and orderget.ordernumber = orderbook.id  " 
        sSql = sSql + " order by orderbook.number "
        return self.executeNormalQuery(sSql, dicUser )
        
        
    def xmlrpc_getPickupNumber(self, orderNumber, dicUser):
                
        nr = 0
        sSql = 'select pickup_number from list_of_pickups where order_number = ' + `orderNumber`
        
        dicResult =  self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )
        if dicResult != 'NONE':
           sSql1 = 'insert into list_of_pickups ( id, pickup_number, order_number) '
           sSql1 = sSql1 + ' values (nextval(\'list_of_pickups_id\'),nextval(\'numerical_misc_standard_pickup\'), ' 
           sSql1 = sSql1 + `orderNumber` + ' )'
        
           self.oDatabase.xmlrpc_executeNormalQuery(sSql1, dicUser )
        
        dicResult =  self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )
        
        if dicResult != 'NONE':
           nr = dicResult[0]['pickup_number']
        return nr
               
    def xmlrpc_getStandardInvoice(self, dicOrder , dicUser):
        sSql = "select orderbook.number as order_number, orderbook.designation as order_designation , "
        sSql = sSql + " to_char(orderbook.orderedat, \'" + dicUser['SQLDateFormat'] + "\')  as order_orderedat ,"
        sSql = sSql + " to_char(orderbook.deliveredat, \'" + dicUser['SQLDateFormat'] + "\') as  order_deliverdat, "
        sSql = sSql + " orderposition.tax_vat as tax_vat, "
        sSql = sSql + " articles.number as article_id, articles.designation as article_designation,  "
        sSql = sSql + " orderposition.designation as designation, orderposition.amount as amount, "
        sSql = sSql + " orderposition.position as position, orderposition.price as price "
        sSql = sSql + " from orderposition, articles, orderbook where orderbook.number = \'" + dicOrder['orderNumber'] +"\' "
        sSql = sSql + "and orderposition.orderid = orderbook.id and articles.id = orderposition.articleid " 
        sSql = sSql + " order by orderposition.position "
        dicUser['noWhereClient'] = 'Yes'
        return self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )


    def xmlrpc_checkExistModulOrder(self, dicUser, dicOrder):
        print 'check Exist Modul Order '
        sSql = 'select * from orderbook where modul_order_number = ' + `dicOrder['ModulOrderNumber']` + ' and modul_number = ' + `dicOrder['ModulNumber']`
        sSql += self.getWhere(None,dicUser,2)
        dicResult = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )
        print 'Order99 = ', dicResult 
        return dicResult
        
        
    def xmlrpc_createNewOrder(self,dicUser,dicOrder):
        print 'create new Order'
        dicValues = {}
        dicValues['modul_order_number'] = [dicOrder['ModulOrderNumber'],'int']
        dicValues['modul_number'] = [dicOrder['ModulNumber'],'int']
        dicValues['number'] = [dicOrder['Number'],'string']
        
        
        dicResult =  self.oDatabase.xmlrpc_saveRecord('orderbook', -1, dicValues, dicUser, 'NO')
        
        return dicResult
        
        
    
