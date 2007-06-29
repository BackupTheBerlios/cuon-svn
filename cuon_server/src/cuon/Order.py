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
        sSql = sSql + " to_char(orderbook.orderedat, \'" + dicUser['SQLDateFormat'] + "\')  as order_orderedat ,"
        sSql = sSql + " to_char(orderbook.deliveredat, \'" + dicUser['SQLDateFormat'] + "\') as  order_deliverdat, "
        sSql += " address.address as address , address.firstname as firstname, "
        sSql = sSql + " address.lastname as lastname, address.lastname2 as lastname2, "
        
        sSql = sSql + " address.street as street, (address.zip || ' ' ||  address.city)  as city "
        sSql = sSql + " from orderbook, address where orderbook.id = " + `dicOrder['orderid']`  
        sSql = sSql + " and address.id = orderbook.addressnumber " 
        liResult = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )
        try:
            if liResult :
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

    def xmlrpc_getOrderPositions(self, dicOrder, dicUser):
        sSql = 'select * from orderposition where orderid = ' + `dicOrder['orderid']`
        dicResult =  self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )
        return dicResult
    
    
    def xmlrpc_getInvoiceNumber(self, orderNumber, dicUser):
        
        nr = 0
        try:
            orderNumber = int(orderNumber)
        except:
            orderNumber = 0
            
        sc = '_client_' + `dicUser['client']`
        
        sSql = 'select invoice_number from list_of_invoices where order_number = ' + `orderNumber`
        sSql += self.getWhere(None, dicUser,2)
        
        dicResult =  self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )    
        if dicResult != 'NONE':
            nr = dicResult[0]['invoice_number']
        else:
            nr = 0
        return nr
    def xmlrpc_getInvoiceDate(self, orderNumber, dicUser):
        
        date = ' '
        try:
            orderNumber = int(orderNumber)
        except:
            orderNumber = 0
            
        sc = '_client_' + `dicUser['client']`
        
        sSql = "select to_char(date_of_invoice, \'" + dicUser['SQLDateFormat'] + "\')  as date_of_invoice  from list_of_invoices where order_number = " + `orderNumber`
        sSql += self.getWhere(None, dicUser,2)
        
        dicResult =  self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )    
        if dicResult != 'NONE':
            date = dicResult[0]['date_of_invoice']
        else:
            date = ' '
        return date
        
    def xmlrpc_getOrderValues(self, orderid, dicUser):
        sSql = "select discount, misc_cost,  postage_cost, packing_cost, "
        sSql += " orderbook.designation as order_designation , "
        sSql += " to_char(orderbook.orderedat, \'" + dicUser['SQLDateFormat'] + "\')  as order_orderedat ,"
        sSql += " to_char(orderbook.deliveredat, \'" + dicUser['SQLDateFormat'] + "\') as  order_deliverdat "
        sSql += " from orderbook where id = " + `orderid`
        sSql += self.getWhere(None, dicUser,2)
        return self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser ) 
        
        
    def xmlrpc_setInvoiceNumber(self, orderNumber, dicUser):
        
        nr = 0
        sc = '_client_' + `dicUser['client']`
        
        sSql = 'select invoice_number from list_of_invoices where order_number = ' + `orderNumber`
        sSql += self.getWhere(None, dicUser,2)
        
        dicResult =  self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )
        print 'InvoiceNumber dicResult = ', dicResult
        
        if dicResult == 'NONE' or dicResult[0]['invoice_number'] == 0:
            sSql1 = 'insert into list_of_invoices ( id, invoice_number, order_number, date_of_invoice, total_amount) '
            
            sSql1 += " values (nextval('list_of_invoices_id'),nextval('numerical_misc_standard_invoice" + sc + "'), " 
        

            sSql1 +=  `orderNumber` + ",'today', " + `self.getTotalSum(orderNumber, dicUser)` +" )"
            print sSql1
            self.oDatabase.xmlrpc_executeNormalQuery(sSql1, dicUser )
        
            dicResult =  self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )
        else:
            sSql1 = "update list_of_invoices set total_amount = " +  `self.getTotalSum(orderNumber, dicUser)` + " where order_number = " + `orderNumber` 
            sSql1 += self.getWhere(None,dicUser,2)
            print sSql1
            self.oDatabase.xmlrpc_executeNormalQuery(sSql1, dicUser )
            
        if dicResult != 'NONE':
            nr = dicResult[0]['invoice_number']
        else:
            nr = 0
        
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
        print dicOrder
        sSql = "select orderbook.number as order_number, orderbook.designation as order_designation , "
        sSql += " to_char(orderbook.orderedat, \'" + dicUser['SQLDateFormat'] + "\')  as order_orderedat ,"
        sSql += " to_char(orderbook.deliveredat, \'" + dicUser['SQLDateFormat'] + "\') as  order_deliverdat, "
        sSql += " orderposition.tax_vat as order_tax_vat, "
        sSql += " (select  tax_vat.vat_value from tax_vat,material_group,articles  where "
        sSql += " articles.material_group = material_group.id and material_group.tax_vat = tax_vat.id and articles.id = orderposition.articleid) as tax_vat, "
        sSql += " articles.number as article_id, articles.designation as article_designation,  "
        sSql += " orderposition.designation as designation, orderposition.amount as amount, "
        sSql += " orderposition.position as position, orderposition.price as price, "
        sSql += "   case ( select material_group.price_type_net from material_group, articles where  articles.material_group = material_group.id and  articles.id = orderposition.articleid)  when true then price when false then price / (100 + (select  tax_vat.vat_value from tax_vat,material_group,articles  where  articles.material_group = material_group.id and material_group.tax_vat = tax_vat.id and articles.id = orderposition.articleid)) * 100  when NULL then 0.00 end as end_price_netto,  case ( select material_group.price_type_net from material_group, articles where  articles.material_group = material_group.id and  articles.id = orderposition.articleid)  when true then price /100 * (100 + (select  tax_vat.vat_value from tax_vat,material_group,articles  where  articles.material_group = material_group.id and material_group.tax_vat = tax_vat.id and articles.id = orderposition.articleid)) when false then price when NULL then 0.00 end as end_price_gross , "
        sSql += " case articles.associated_with when 1 then (select botany.description from botany, articles where botany.article_id = articles.id and articles.id = orderposition.articleid and orderbook.id = " + `dicOrder['orderid']` + ") when 0 then articles.designation end as pos_designation "
        sSql += " from orderposition, articles, orderbook  where orderbook.id = " + `dicOrder['orderid']` 
        sSql += " and orderposition.orderid = orderbook.id and articles.id = orderposition.articleid " 
        sSql += " order by orderposition.position "
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
        print dicOrder
        dicValues = {}
        if dicOrder.has_key('ModulOrderNumber'):
            dicValues['modul_order_number'] = [dicOrder['ModulOrderNumber'],'int']
        if dicOrder.has_key('ModulNumber'):
            dicValues['modul_number'] = [dicOrder['ModulNumber'],'int']
        if dicOrder.has_key( 'Number'):   
            dicValues['number'] = [dicOrder['Number'],'string']
        dicValues['addressnumber'] = [dicOrder['addressnumber'],'int']
        print 'Locales:', dicUser['Locales']
        print 'Dateformatstring', dicUser['DateformatString']
        if dicOrder.has_key('orderedat'):
                            
            try:
                dO = time.strptime(dicOrder['orderedat'], dicUser['DateformatString'])
                dD = time.strptime(dicOrder['deliveredat'], dicUser['DateformatString'])
                dicValues['orderedat'] = [`dO[0]`+'/'+ `dO[1]` + '/'+ `dO[2]`,'date']
                dicValues['deliveredat'] = [`dD[0]`+'/'+ `dD[1]` + '/'+ `dD[2]`,'date']
            except:
                pass
        else:
            dicValues['orderedat'] = [time.strftime('%m/%d/%Y', time.localtime()),'date']
            
        print dicValues
        dicResult =  self.oDatabase.xmlrpc_saveRecord('orderbook', -1, dicValues, dicUser, 'NO')
        
        if dicOrder.has_key('Positions'):
            for position in dicOrder['Positions']:
                position['orderid'] = [dicResult[0]['last_value'],'int']
                print '-----------------------------------------------'
                print 'Position = ', position
                print ':::::::::::::::::::::::::::::::::::::::::::::::'
                dicResult2 =  self.oDatabase.xmlrpc_saveRecord('orderposition', -1, position, dicUser, 'NO')

        
        
        
        return dicResult
        
    def getTotalSum(self,OrderID, dicUser):
        total_sum = 0
        sSql = 'select sum(amount * price) as total_sum from orderposition where orderid = '
        sSql += `OrderID`
        sSql += self.getWhere(None,dicUser,2)
        dicResult = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )
        if dicResult and dicResult != 'NONE':
            total_sum = dicResult[0]['total_sum']
        
        return total_sum
        
          
    def xmlrpc_getTotalSumString(self, OrderID, dicUser):
        retValue = '0'  

        total_sum = self.getTotalSum(OrderID,dicUser)
        try:
            #"%.2f"%y 
            total_sum = ("%." + `self.CURRENCY_ROUND` + "f") % round(total_sum,self.CURRENCY_ROUND)
            retValue = total_sum + ' ' + self.CURRENCY_SIGN
        except:
            pass
            
        return retValue  
    def xmlrpc_getNextPosition(self, orderid, dicUser):
        pos = 0
        sSql = " select max(position) as max_position from orderposition where orderid = " +  `orderid`
        liResult = self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
        if liResult and liResult != 'NONE':
            try:
                pos = liResult[0]['max_position']
                pos = int(pos)
            except:
                pos = 0
            
                
        pos += 1
        return pos
        

    def getListOfInvoices( self, dicOrder, dicUser ):
        dBegin = datetime.fromtimestamp(dicOrder['dBegin'])
        dEnd = datetime.fromtimestamp(dicOrder['dEnd'])
        print  dBegin, dEnd
        
        sSql = ' select list_of_invoices.order_number as order_number,  list_of_invoices.invoice_number as invoice_number, '
        sSql += ' list_of_invoices.date_of_invoice as date_of_invoice, list_of_invoices.total_amount as total_amount, '
        sSql += ' list_of_invoices.maturity as maturity, '
        sSql += 'address.lastname as lastname, address.city as city '
        sSql += ' from list_of_invoices, orderbook,address where  orderbook.id =  list_of_invoices.order_number and address.id = orderbook.addressnumber '
        sSql += " and list_of_invoices.date_of_invoice between '" + dBegin.strftime('%Y-%m-%d') + "' and '" + dEnd.strftime('%Y-%m-%d') +"' " 
        sSql += self.getWhere(None,dicUser,2,'list_of_invoices.')
        sSql += ' order by list_of_invoices.invoice_number ' 
        return self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
        
        
        
    def getListOfInpayment( self, dicOrder, dicUser ):
        dBegin = datetime.fromtimestamp(dicOrder['dBegin'])
        dEnd = datetime.fromtimestamp(dicOrder['dEnd'])
        print  dBegin, dEnd
        
        sSql = ' select in_payment.invoice_number as invoice_number, in_payment.inpayment as inpayment, '
        sSql += 'in_payment.date_of_paid as date_of_paid, in_payment.order_id as order_id, '
        sSql += "list_of_invoices.date_of_invoice, "
        sSql += 'address.lastname as lastname, address.city as city '
        sSql += ' from in_payment, orderbook, address, list_of_invoices where  orderbook.id =  in_payment.order_id and address.id = orderbook.addressnumber '
        sSql += " and in_payment.date_of_paid between '" + dBegin.strftime('%Y-%m-%d') + "' and '" + dEnd.strftime('%Y-%m-%d') +"' " 
        sSql += " and list_of_invoices.invoice_number = to_number(in_payment.invoice_number,'999999999') "
        sSql += self.getWhere(None,dicUser,2,'in_payment.')
        sSql += ' order by in_payment.date_of_paid ' 
        return self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
        
        
    def xmlrpc_getOrderForAddress(self, address_id, dicUser):
        sSql = ' select id, number,designation, orderedat from orderbook '
        sSql += " where addressnumber = " + `address_id` + " "
        sSql += self.getWhere(None,dicUser,2)
        return self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
        
    
    
    
    def xmlrpc_getToP(self, dicOrder, dicUser):
        
        topID = 0
        sSql = "select addresses_misc.top_id as topid from addresses_misc,orderbook where addresses_misc.address_id = orderbook.addressnumber and orderbook.id = " + `dicOrder['orderid']`
        sSql += self.getWhere(None,dicUser,2)
        print 'Before ', sSql
        print dicUser['Name']
        result = self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
        print result
        if result != 'NONE':
            topID = result[0]['topid']
            
            
        print 'topID = ', topID
        if topID == 0:
            cpServer, f = self.getParser(self.CUON_FS + '/sql.ini')
            #print cpServer
            #print cpServer.sections()
            topID = int(self.getConfigOption('modul_order','default_top', cpServer))
            print 'topID from ini = ', topID
            
        if topID > 0:
            sSql = "select * from terms_of_payment where id = " + `topID`
            result = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser)
        else:
            result = 'NONE'
        print 'result by getTop: ', result
        return result
        
    def xmlrpc_getAllOrderWithoutInvoice(self, dicUser):
        liOrder = []
        sSql = " select id from orderbook "
        sSql += self.getWhere(None,dicUser,1)
        result = self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
        if result and result != 'NONE':
            for row in result:
                order_id = row['id']
                sSql = " select max(invoice_number) as max_invoice_number from list_of_invoices where order_number = " + `order_id`
                sSql += self.getWhere(None,dicUser,2)
                result2 = self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
                print 'result2', result2
                if result2 and result2 != 'NONE' and result2[0]['max_invoice_number'] != 'NONE' :
                    if result2[0]['max_invoice_number'] < 1 or result2[0]['max_invoice_number'] != None:
                        liOrder.append(order_id)
                        print 'append1 = ', order_id
                else:
                    liOrder.append(order_id)
                    print 'append2 = ', order_id
                    
        if not liOrder:
            liOrder = 'NONE'
            
        print liOrder
        
        return liOrder
        
        
                    
    
