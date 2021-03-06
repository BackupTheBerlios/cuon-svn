# coding=utf-8
##Copyright (C) [2005]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 


import time
from datetime import datetime
import random
import xmlrpclib
from twisted.web import xmlrpc
import types 
from basics import basics
import Database

class Order(xmlrpc.XMLRPC, basics):
    def __init__(self):
        basics.__init__(self)
        self.oDatabase = Database.Database()
        
    def xmlrpc_getSupply_GetNumber(self, orderNumber, dicUser):    
        iGetNumber =  0
        iSupplyNumber = 0
        
        
        sSql = "select gets_number from  fct_getGet_number(" + `orderNumber` + ") as gets_number(integer) "
        
        iGetNumber =  self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )[0]['gets_number']
        sSql = "select supply_number from  fct_getSupply_number(" + `orderNumber` + ") as supply_number(integer) "
        
        iSupplyNumber =  self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )[0]['supply_number']
        
        
        return iGetNumber,  iSupplyNumber
        

    def xmlrpc_getDeliveryNumber(self, orderNumber, dicUser ):
        nr = 0
        sc = '_client_' + `dicUser['client']`
        sSql = 'select delivery_number from list_of_deliveries where order_number = ' + `orderNumber`
        sSql = sSql + self.getWhere("",dicUser,2)
        
        dicResult =  self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )
        if dicResult in self.liSQL_ERRORS:
            liFields, liValues = self.getNormalSqlData(dicUser)
            
            sSql1 = 'insert into list_of_deliveries ( id, delivery_number, order_number '
            for sFields in liFields:
                sSql1 += sFields
            sSql1 +=  " values (nextval(\'list_of_deliveries_id\'),nextval(\'numerical_misc_standard_delivery"+sc +"\'), " 
            sSql1 +=  `orderNumber` 
            for sValues in liValues:
                sSql1 += sValues
        
            self.oDatabase.xmlrpc_executeNormalQuery(sSql1, dicUser )
        
            dicResult =  self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )
    
        if dicResult not in ['NONE','ERROR']:
           nr = dicResult[0]['delivery_number']
        return nr


    def xmlrpc_getInvoiceAddress(self, dicOrder, dicUser):
        
        sSql = "select orderbook.number as order_number, orderbook.designation as order_designation , orderbook.customers_ordernumber as customers_ordernumber, "
        sSql +=  " to_char(orderbook.orderedat, \'" + dicUser['SQLDateFormat'] + "\')  as order_orderedat ,"
        sSql +=  " to_char(orderbook.deliveredat, \'" + dicUser['SQLDateFormat'] + "\') as  order_deliverdat, "
        sSql += " address.address as address , address.firstname as firstname, "
        sSql +=  " address.lastname as lastname, address.lastname2 as lastname2, "
        
        sSql  += " address.street as street, (address.zip || ' ' ||  address.city)  as city , "
        sSql += " (address.country || '-' ||  address.zip || ' ' ||  address.city)  as city_country , "
        sSql  += "address.zip as zip,  address.country as country,  address.city as city_alone "
        sSql +=  " from orderbook, address where orderbook.id = " + `dicOrder['orderid']`  
        sSql +=  " and address.id = orderbook.addressnumber " 
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
        if dicResult not in ['NONE','ERROR']:
            nr = dicResult[0]['invoice_number']
        else:
            nr = 0
        return nr
        
    def xmlrpc_changeProposal2Order(self, ProposalID, dicUser):
        ok = True 
        print "proposalID = ",  ProposalID
        #sSql = "update orderbook set process_status = 500 where id = " + `ProposalID`
        sSql = "select * from fct_changeProposal2Order(" + `ProposalID` + " )"
        dicResult =  self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )  
        return ok
        
        
    def xmlrpc_getProposalNumber(self, orderNumber, dicUser):
        
        nr = 0
        try:
            orderNumber = int(orderNumber)
        except:
            orderNumber = 0
            
        sc = '_client_' + `dicUser['client']`
        
        sSql = 'select proposal_number from orderbook  where id = ' + `orderNumber`
        sSql += self.getWhere(None, dicUser,2)
        
        dicResult =  self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )    
        if dicResult and dicResult not in ['NONE','ERROR']:
            nr = dicResult[0]['proposal_number']
        else:
            sSql = 'select max(proposal_number) from orderbook  '
            sSql += self.getWhere(None, dicUser,1)
        
            dicResult =  self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )    
            if dicResult and dicResult not in ['NONE','ERROR']:
                nr = dicResult[0]['proposal_number']
        nr = nr + 1
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
        if dicResult not in ['NONE','ERROR']:
            date = dicResult[0]['date_of_invoice']
        else:
            date = ' '
        return date
        
    def xmlrpc_getSupplyDate(self, orderNumber, dicUser):
        
        date = ' '
        
        try:
            orderNumber = int(orderNumber)
        except:
            orderNumber = 0
            
        sc = '_client_' + `dicUser['client']`
        
        sSql = "select to_char(date_of_delivery, \'" + dicUser['SQLDateFormat'] + "\')  as date_of_delivery  from list_of_delivery where order_number = " + `orderNumber`
        sSql += self.getWhere(None, dicUser,2)
        
        dicResult =  self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )    
        if dicResult not in ['NONE','ERROR']:
            date = dicResult[0]['date_of_delivery']
        else:
            date = ' '
        return date   
        
        
    def xmlrpc_getOrderValues(self, orderid, dicUser):
        liResultStaff = None
        liResultPartner = None
        print '############ get order values ####################'
        sSql = "select discount, misc_cost,  postage_cost, packing_cost, orderbook.customers_ordernumber as customers_ordernumber, "
        sSql += " orderbook.designation as order_designation , orderbook.number as order_number, staff_id as order_staff_id, "
        sSql += " orderbook.customers_partner_id as order_customers_partner_id ,  "
        sSql += " to_char(orderbook.orderedat, \'" + dicUser['SQLDateFormat'] + "\')  as order_orderedat ,"
        sSql += " to_char(orderbook.deliveredat, \'" + dicUser['SQLDateFormat'] + "\') as  order_deliverdat "
        
        sSql += " from orderbook where id = " + `orderid`
        sSql += self.getWhere(None, dicUser,2)
        liResult = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser ) 
        
        
        
        for row in liResult:
            try:
                if row['discount'] == None or row['discount'] in self.liSQL_ERRORS:
                    row['discount'] = 0.0
            except:
                pass
            try:
                if row['order_staff_id'] > 0:
                    sSql = "select *, lastname || ', ' || firstname as last_first, firstname || ' ' || lastname as first_last from staff where id = " + `row['order_staff_id']` 
                    liResultStaff = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser ) 
            except:
                pass
            
            try:
                if row['order_customers_partner_id'] > 0:
                    sSql = "select *, lastname || ', ' || firstname as last_first, firstname || ' ' || lastname as first_last from partner where id = " + `row['order_customers_partner_id']` 
                    liResultPartner = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser ) 
            except:
                pass    
            
            
                
            
        #print 'liResultStaff = ',  liResultStaff
        if liResultStaff:
            try:
                row = liResultStaff[0]
                print 'row_keys = ' ,  row.keys() 
                for key in row.keys():
                    print 'key = ',  key
                    liResult[0]['staff_' + key] = row[key]
            except Exception, params:
                print Exception, params
              
        if liResultPartner:
            try:
                row = liResultPartner[0]
                print 'row_keys = ' ,  row.keys() 
                for key in row.keys():
                    print 'key = ',  key
                    liResult[0]['partner_' + key] = row[key]
            except Exception, params:
                print Exception, params
                 
                
        print 'liResult = ',  liResult
        top_id = self .getToPID({'orderid':orderid},  dicUser)
        
#        sSql2 = 'select order_top as top_id from orderinvoice where orderid = ' +  `orderid`
#        sSql2 += self.getWhere(None, dicUser,2)
#        liResultTop = self.oDatabase.xmlrpc_executeNormalQuery(sSql2, dicUser )
#        if not liResultTop or liResultTop in ['NONE','ERROR']:
#            '''No term of payment found, try default from customer '''
#            sSql2 = 'select addresses_misc.top_id as top_id from addresses_misc, orderbook '
#            sSql2 += ' where addresses_misc.address_id = orderbook.addressnumber '
#            sSql2 += self.getWhere(None, dicUser,2,'orderbook.')
#            liResultTop = self.oDatabase.xmlrpc_executeNormalQuery(sSql2, dicUser )
#            if liResultTop and liResultTop not in ['NONE','ERROR']:
#                top_id = liResultTop[0]['top_id']
#            
        
        if liResult not in self.liSQL_ERRORS:
            sSql3 = ' select term_of_payment from terms_of_payment where id = ' + `top_id`
            liResultTop2 = self.oDatabase.xmlrpc_executeNormalQuery(sSql3, dicUser )
            if liResultTop2 and liResultTop2 not in self.liSQL_ERRORS:
                liResult[0]['term_of_payment'] = liResultTop2[0]['term_of_payment']
            else :
                liResult[0]['term_of_payment'] = ''
        
        liResult[0]['gets_number'],  liResult[0]['supply_number'] = self.xmlrpc_getSupply_GetNumber(orderid, dicUser)
        
        return liResult
        
        
    def xmlrpc_setInvoiceNumber(self, orderNumber, dicUser):
        
        nr = 0
        sc = '_client_' + `dicUser['client']`
        
        sSql = 'select invoice_number from list_of_invoices where order_number = ' + `orderNumber`
        sSql += self.getWhere(None, dicUser,2)
        
        dicResult =  self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )
        print 'InvoiceNumber dicResult = ', dicResult
        
        
        if dicResult in ['NONE','ERROR'] or dicResult[0]['invoice_number'] == 0:
            
            liFields, liValues = self.getNormalSqlData(dicUser)
            
            sSql1 = 'insert into list_of_invoices ( id, invoice_number, order_number, date_of_invoice, total_amount'
            for sFields in liFields:
                sSql1 += sFields
            sSql1 += " values (nextval('list_of_invoices_id'),nextval('numerical_misc_standard_invoice" + sc + "'), " 
        

            sSql1 +=  `orderNumber` + ",'today', " + `self.getTotalSum(orderNumber, dicUser)` 
            for sValues in liValues:
                sSql1 += sValues
        
            print sSql1
            self.oDatabase.xmlrpc_executeNormalQuery(sSql1, dicUser )
        
            dicResult =  self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )
        else:
            liFields, liValues = self.getNormalSqlData(dicUser, False, False)
            sSql1 = "update list_of_invoices set total_amount = " +  `self.getTotalSum(orderNumber, dicUser)` 
            
            mFields = len(liFields)
            for counter in range(mFields):
                sSql1 += ", " +  liFields[counter] + " = " + liValues[counter]
            
            
        
            sSql1 += " where order_number = " + `orderNumber` 
            
            sSql1 += self.getWhere(None,dicUser,2)
            print sSql1
            self.oDatabase.xmlrpc_executeNormalQuery(sSql1, dicUser )
        
        if dicResult not in ['NONE','ERROR']:
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
        if dicResult not in ['NONE','ERROR']:
           liFields, liValues = self.getNormalSqlData(dicUser)
           
           sSql1 = 'insert into list_of_pickups ( id, pickup_number, order_number '
           for sFields in liFields:
                sSql1 += sFields
           sSql1 +=  ' values (nextval(\'list_of_pickups_id\'),nextval(\'numerical_misc_standard_pickup\'), ' 
           sSql1 +=  `orderNumber`
            
           for sValues in liValues:
                sSql1 += sValues
        
           
           self.oDatabase.xmlrpc_executeNormalQuery(sSql1, dicUser )
        
        dicResult =  self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )
        
        if dicResult not in ['NONE','ERROR']:
           nr = dicResult[0]['pickup_number']
        return nr
               
    def xmlrpc_getStandardInvoice(self, dicOrder , dicUser):
        result2=[]
        try:
            print dicOrder
            sSql = "select orderbook.number as order_number, orderbook.designation as order_designation , "
            sSql += " to_char(orderbook.orderedat, \'" + dicUser['SQLDateFormat'] + "\')  as order_orderedat ,"
            sSql += " to_char(orderbook.deliveredat, \'" + dicUser['SQLDateFormat'] + "\') as  order_deliverdat, "
            sSql += " orderbook.discount as total_discount,  "
            sSql += "(select  tax_vat_for_all_positions from orderinvoice  where orderinvoice.orderid = " + `dicOrder['orderid']`  
            sSql += " ) as tax_vat_for_all_positions, "
            sSql += " orderposition.tax_vat as order_tax_vat_order_position_id, "
            sSql += " (select  tax_vat.vat_value from tax_vat,material_group,articles  where "
            sSql += " articles.material_group = material_group.id and material_group.tax_vat = tax_vat.id and articles.id = orderposition.articleid) as tax_vat, "
            sSql += " (select  tax_vat.vat_value from tax_vat,material_group,articles  where "
            sSql += " articles.material_group = material_group.id and material_group.tax_vat = tax_vat.id and articles.id = orderposition.articleid) as tax_vat_material_group, "
            sSql += " (select  material_group.tax_vat from material_group,articles  where "
            sSql += " articles.material_group = material_group.id and articles.id = orderposition.articleid) as tax_vat_material_group_id, "
            sSql  += "(select material_group.price_type_net from material_group, articles where  articles.material_group = material_group.id and  articles.id = orderposition.articleid) as material_group_price_type_net,  "
            sSql += " articles.number as article_id, articles.designation as article_designation, articles.tax_vat_id as tax_vat_article_id,  articles.articles_notes as articles_notes, "
            sSql += "articles.wrapping as article_wrapping, articles.quantumperwrap as article_quantumperwrap,  articles.unit as article_unit,  "
            sSql += " orderposition.designation as designation, orderposition.amount as amount, "
            sSql += " orderposition.position as position, orderposition.price as price, "
            sSql += " orderposition.discount as discount,  "
            sSql += "   case ( select material_group.price_type_net from material_group, articles where  articles.material_group = material_group.id and  articles.id = orderposition.articleid)  when true then price when false then price / (100 + (select  tax_vat.vat_value from tax_vat,material_group,articles  where  articles.material_group = material_group.id and material_group.tax_vat = tax_vat.id and articles.id = orderposition.articleid)) * 100  when NULL then 0.00 end as end_price_netto,  case ( select material_group.price_type_net from material_group, articles where  articles.material_group = material_group.id and  articles.id = orderposition.articleid)  when true then price /100 * (100 + (select  tax_vat.vat_value from tax_vat,material_group,articles  where  articles.material_group = material_group.id and material_group.tax_vat = tax_vat.id and articles.id = orderposition.articleid)) when false then price when NULL then 0.00 end as end_price_gross , "
            sSql += " case articles.associated_with when 1 then (select botany.description from botany, articles where botany.article_id = articles.id and articles.id = orderposition.articleid and orderbook.id = " + `dicOrder['orderid']` + ") when 0 then articles.designation end as pos_designation "
            sSql += " from orderposition, articles, orderbook  where orderbook.id = " + `dicOrder['orderid']` 
            sSql += " and orderposition.orderid = orderbook.id and articles.id = orderposition.articleid " 
            sSql += " order by orderposition.position "
            dicUser['noWhereClient'] = 'Yes'
            result = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )
            result2 = []
            for oneResult in result:
                try:
                    print 'oneResult = ',  oneResult
                    oneResult['MWST_ID'] =   0
                    oneResult['MWST_VALUE'] = 0
                    oneResult['MWST_NAME'] = ''
               
                    if oneResult not in self.liSQL_ERRORS :
                        if oneResult['tax_vat_for_all_positions'] not in self.liSQL_ERRORS:
                            if oneResult['tax_vat_for_all_positions']  > 0:
                                oneResult['MWST_ID'] = oneResult['tax_vat_for_all_positions'] 
                                self.writeLog( 'TAXVATNEW1 '+ `oneResult['MWST_ID']`)
                        if oneResult['MWST_ID'] ==   0:
                            if oneResult['order_tax_vat_order_position_id'] not in self.liSQL_ERRORS:
                                if oneResult['order_tax_vat_order_position_id'] > 0:
                                    oneResult['MWST_ID'] = oneResult['order_tax_vat_order_position_id']
                                    self.writeLog( 'TAXVATNEW2 '+ `oneResult['MWST_ID']`)
                            
                        
                        if oneResult['tax_vat_article_id'] not in self.liSQL_ERRORS:
                            if oneResult['tax_vat_article_id'] > 0:
                                oneResult['MWST_ID'] = oneResult['tax_vat_article_id']
                                self.writeLog( 'TAXVATNEW3 '+ `oneResult['MWST_ID']`)
        
                        if oneResult['MWST_ID'] ==   0:
                            if oneResult['tax_vat_material_group_id'] not in self.liSQL_ERRORS:
                                if oneResult['tax_vat_material_group_id'] > 0:
                                    oneResult['MWST_ID'] = oneResult['tax_vat_material_group_id']
                                    self.writeLog( 'TAXVATNEW4 '+ `oneResult['MWST_ID']`)
        
                        if oneResult['MWST_ID'] > 0:
                            sSql = "select  vat_value, vat_name, vat_designation from tax_vat where tax_vat.id = " + `oneResult['MWST_ID']`
                            mwstResult = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )
                            try:
                                oneResult['MWST_VALUE'] = mwstResult[0]['vat_value']
                                oneResult['MWST_NAME'] = mwstResult[0]['vat_name']
                                oneResult['MWST_DESIGNATION'] = mwstResult[0]['vat_designation']
                            except:
                                pass
                            self.writeLog( 'TAXVATNEWValue '+ `oneResult['MWST_VALUE']`)
    
                    result2.append(oneResult)
                except:
                    oneResult = {}
                    #print 'oneResult = ',  oneResult
                    oneResult['MWST_ID'] =   0
                    oneResult['MWST_VALUE'] = 0
                    oneResult['MWST_NAME'] = ''
                    self.writeLog( 'TAXVATRESULT ' + `result2`)
                    for i in result[2]:
                        if i['articles_notes'] in liSQL_ERRORS:
                            i['articles_notes'] = ''
        except Exception,  params:
            
            self.writeLog('Error at getStandardInvoice = ' + `Exception` + ',  ' + `params` )
        return result2
        

    def xmlrpc_checkExistModulOrder(self, dicUser, dicOrder):
        print 'check Exist Modul Order '
        sSql = 'select * from orderbook where modul_order_number = ' + `dicOrder['ModulOrderNumber']` + ' and modul_number = ' + `dicOrder['ModulNumber']`
        sSql += self.getWhere(None,dicUser,2)
        dicResult = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )
        self.writeLog( 'Order99 = ' + `dicResult`) 
        return dicResult
        
    def xmlrpc_checkExistModulProposal(self, dicUser, dicOrder):
        print 'check Exist Modul Proposal '
        sSql = 'select * from orderbook where modul_order_number = ' + `dicOrder['ModulOrderNumber']` + ' and modul_number = ' + `dicOrder['ModulNumber']`
        sSql += self.getWhere(None,dicUser,2)
        dicResult = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )
        self.writeLog( 'Order99 = ' + `dicResult`) 
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
        print dicOrder
        if dicOrder.has_key('orderedat'):
                            
            try:
                dO = time.strptime(dicOrder['orderedat'], dicUser['DateformatString'])
                dicValues['orderedat'] = [`dO[0]`+'/'+ `dO[1]` + '/'+ `dO[2]`,'date']
                print 'Orderedat = ',  dicValues['orderedat']
            except Exception,  params:
                print Exception, params
        else:
            dicValues['orderedat'] = [time.strftime('%m/%d/%Y', time.localtime()),'date']
           
        if dicOrder.has_key('deliveredat'):
            try:
                dD = time.strptime(dicOrder['deliveredat'], dicUser['DateformatString'])
                dicValues['deliveredat'] = [`dD[0]`+'/'+ `dD[1]` + '/'+ `dD[2]`,'date']
                self.writeLog('Deliveredat = ' + `dicValues['deliveredat']`)
            except Exception,  params:
                print Exception, params
            
        self.writeLog(dicValues)
        
        if dicOrder.has_key('process_status'):
            dicValues['process_status'] = [dicOrder['process_status'], 'int'] 
        newID =  self.oDatabase.xmlrpc_saveRecord('orderbook', -1, dicValues, dicUser, 'NO')
        
        if dicOrder.has_key('Positions') and newID > 0:
            for position in dicOrder['Positions']:
                position['orderid'] = [newID,'int']
                print '-----------------------------------------------'
                print 'Position = ', position
                print ':::::::::::::::::::::::::::::::::::::::::::::::'
                dicResult2 =  self.oDatabase.xmlrpc_saveRecord('orderposition', -1, position, dicUser, 'NO')
        try:
            if newID > 0:
                dicValues,  sSave  = self.checkDefaultOrder(dicUser,  newID)
                if sSave:
                    dR4 = self.oDatabase.xmlrpc_saveRecord('orderbook', newID, dicValues, dicUser, 'NO')
        except:
            pass
            
    
        
        
        return newID
        
    def checkDefaultOrder(self,  dicUser,  id) :
        print 101
        sSave = False
        print 102
        dicValues = {}
        sc = '_client_' + `dicUser['client']`
        try:
            cpServer, f = self.getParser(self.CUON_FS + '/clients.ini')
            defaultOrderNumber = self.getConfigOption('CLIENT_' + `dicUser['client']`,'orderbook_number', cpServer)
            defaultOrderDesignation = self.getConfigOption('CLIENT_' + `dicUser['client']`,'orderbook_designation', cpServer)
            print defaultOrderDesignation, defaultOrderNumber
            print 0 
            t1 = time.localtime()
            print 1
            if defaultOrderNumber:
                sSave = True
                liValues = defaultOrderNumber.split(',')
                sON = ''
                for i in liValues:
                    print 2, i
                    if i == '!id':
                        
                        sON += self.convertTo(id, 'String')
                    elif i=='!year':
                        sON += `t1.tm_year`
                    elif i=='!month':
                        sON += `t1.tm_mon`    
                    elif i=='!day':
                        sON += `t1.tm_mday`
                    elif i=='!seq':
                        sSql = "select nextval('numerical_orderbook_ordernumber" +sc +"' )"
                        print sSql
                        newSeq = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser)[0]['nextval']
                        
                        sON += `newSeq`
                    else:
                        sON += i
                    print 'sON',  sON
                dicValues['number'] = [sON, 'string']
            if defaultOrderDesignation:
                print 3
                sSave = True
                liValues = defaultOrderDesignation.split(',')
                sOD = ''
                sSql = ' select * from address where id = ( select addressnumber from orderbook where id = ' +  self.convertTo(id, 'String') + ')'
                #print sSql
                dicResult = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )
                #print dicResult
                for i in liValues:
                    #print 4, i
                    #print '4-1',i[1:]
                    if i[0] == '!':
                        try:
                            if isinstance(dicResult[0][i[1:]], types.StringType):
                                sOD += dicResult[0][i[1:]].decode('utf-8')
                            else:
                                sOD += `dicResult[0][i[1:]]`
                        except Exception, params:
                            print Exception,params
                            
                            
                    else:
                        sOD += i
                #print 'sOD',  sOD
                dicValues['designation'] = [sOD, 'string']
            #print 5    
            #print dicValues,  sSave
        except Exception, params:
            print Exception, params
            
        return dicValues, sSave
        
                    
            
        
        
    def getTotalSum(self,OrderID, dicUser):
        
        total_sum = 0
#        sSql = 'select sum(amount * price) as total_sum from orderposition where orderid = '
#        sSql += `OrderID`
#        sSql += self.getWhere(None,dicUser,2)
#        dicResult = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )
#        if dicResult and dicResult not in ['NONE','ERROR']:
#        total_sum = dicResult[0]['total_sum']

        sSql = "select total_sum from fct_getOrderTotalSum(" + `OrderID` +") as total_sum(float) "
        dicResult = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )
        #print 'Total-sum = ', dicResult
        
        if dicResult and dicResult not in ['NONE','ERROR']:
            total_sum = dicResult[0]['total_sum']

        #print 'Total-sum 2= ', total_sum        
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
        
    def xmlrpc_getPaidAt(self,OrderID, dicUser):
        paidAt = ' '
        sSql = "select  to_char(date_of_paid, \'" + dicUser['SQLDateFormat'] + "\')  as paid_at from  in_payment where order_id = " + `OrderID` 
        sSql += self.getWhere(None,dicUser,2)
        liResult = self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
        if liResult and liResult not in ['NONE','ERROR']:
            try:
                paidAt = liResult[0]['paid_at']
            except:
                pass
        
        return paidAt
        
        
    def xmlrpc_getNextPosition(self, orderid, dicUser):
        pos = 0
        sSql = " select max(position) as max_position from orderposition where orderid = " +  `orderid`
        liResult = self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
        if liResult and liResult not in ['NONE','ERROR']:
            try:
                pos = liResult[0]['max_position']
                pos = int(pos)
            except:
                pos = 0
            
                
        pos += 1
        return pos
        
    def xmlrpc_getUserInfoOrder(self, dicOrder, dicUser):
        
        return None
    
        
    def xmlrpc_getUserInfoInvoice(self, dicOrder, dicUser):
        sSql = 'select * from staff, list_of_invoices as lii where cuon_username =  lii.user_id and lii.invoice_number = ' + `dicOrder['invoiceNumber'] ` 
        sSql += self.getWhere(None,dicUser,2,'list_of_invoices.')
        return self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
    
    def getListOfInvoices( self, dicOrder, dicUser ):
        dBegin = datetime.fromtimestamp(dicOrder['dBegin'])
        dEnd = datetime.fromtimestamp(dicOrder['dEnd'])
        print  dBegin, dEnd
        
        sSql = ' select list_of_invoices.order_number as order_number,  list_of_invoices.invoice_number as invoice_number, '
        sSql += ' list_of_invoices.date_of_invoice as date_of_invoice, list_of_invoices.total_amount as total_amount, '
        sSql += ' list_of_invoices.maturity as maturity, '
        sSql += 'address.lastname as lastname, address.city as city, address.id as addressid , address.zip as zip '
        sSql += ' from list_of_invoices, orderbook,address where  orderbook.id =  list_of_invoices.order_number and address.id = orderbook.addressnumber '
        sSql += " and list_of_invoices.date_of_invoice between '" + dBegin.strftime('%Y-%m-%d') + "' and '" + dEnd.strftime('%Y-%m-%d') +"' " 
        sSql += self.getWhere(None,dicUser,2,'list_of_invoices.')
        sSql += ' order by list_of_invoices.invoice_number ' 
        return self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
        
        
        
    def getListOfInpayment( self, dicOrder, dicUser ):
        self.checkMaturityDay(dicUser)
        dBegin = datetime.fromtimestamp(dicOrder['dBegin'])
        dEnd = datetime.fromtimestamp(dicOrder['dEnd'])
        print  dBegin, dEnd
        
        sSql = ' select in_payment.invoice_number as invoice_number, in_payment.inpayment as inpayment, '
        sSql += 'in_payment.date_of_paid as date_of_paid, in_payment.order_id as order_id, '
        sSql += "list_of_invoices.date_of_invoice, "
        sSql += 'address.lastname as lastname, address.city as city, address.id as addressid '
        sSql += ' from in_payment, orderbook, address, list_of_invoices where  orderbook.id =  in_payment.order_id and address.id = orderbook.addressnumber '
        sSql += " and in_payment.date_of_paid between '" + dBegin.strftime('%Y-%m-%d') + "' and '" + dEnd.strftime('%Y-%m-%d') +"' " 
        sSql += " and list_of_invoices.invoice_number = to_number(in_payment.invoice_number,'999999999') "
        sSql += self.getWhere(None,dicUser,2,'in_payment.')
        sSql += ' order by in_payment.date_of_paid ' 
        return self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
        
        
    def xmlrpc_getOrderForAddress(self, address_id, dicUser,  iBegin = 500,  iEnd = 799):
        sSql = ' select id, number,designation, orderedat from orderbook '
        sSql += " where addressnumber = " + `address_id` + " "
        sSql += " and  process_status between " + `iBegin` + " and " + `iEnd` + " "
        sSql += self.getWhere(None,dicUser,2)
        sSql += " order by id desc "
        
        return self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
    
    def xmlrpc_getOrderForProject(self, project_id, dicUser):
        sSql = ' select id, number,designation, orderedat from orderbook '
        sSql += " where project_id= " + `project_id` + " "
        
        sSql += self.getWhere(None,dicUser,2)
        sSql += " order by id desc "
        
        return self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
        
    
    def xmlrpc_getInvoicesForAddress(self, address_id, dicUser):
        sSql = ' select li.id as id , orderbook.designation,  li.invoice_number as number,li.date_of_invoice as date from orderbook, list_of_invoices as li '
        sSql += " where orderbook.addressnumber = " + `address_id` + " " 
        sSql += ' and li.order_number = orderbook.id '
        sSql += self.getWhere(None,dicUser,2,'li.')
        sSql += " order by li.id desc "
        return self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
       
    
    def getToPID(self, dicOrder, dicUser):
        
        topID = 0
        sSql = "select * from fct_getTopIDForOrder(" + `dicOrder['orderid']` + " ) as topid "   
        #print 'Before ', sSql
        #print dicUser['Name']
        result = self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
        print result
        if result not in ['NONE','ERROR']:
            try:
                topID = int(result[0]['topid'])
            except:
                topID = 0
            
            
        #print 'topID = ', topID
        if not topID or topID == 0 :
            #print 'read from INI'
            try:
                cpServer, f = self.getParser(self.CUON_FS + '/clients.ini')
                #print cpServer
                #print cpServer.sections()
                topID = self.getConfigOption('CLIENT_' + `dicUser['client']`,'modul_order_default_top', cpServer)
                #print 'topID from ini = ', topID
                topID = int(topID.strip())
                #print 'topID_zahl'
            except Exception,params:
                #print Exception,params
                topID = 0
        return topID
        
    
    def xmlrpc_getToP(self, dicOrder, dicUser):
        topID = self.getToPID(dicOrder, dicUser)
        if topID > 0:
            sSql = "select * from terms_of_payment where id = " + `topID`
            result = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser)
        else:
            result = 'NONE'
        print 'result by getTop: ', result
        return result
        
    def xmlrpc_getAllOrderWithoutInvoice(self, dicUser):
        liOrder = []
        sSql = " select id from orderbook  where process_status = 500 and ready_for_invoice = true "
        sSql += self.getWhere(None,dicUser,2)
        sSql += ' order by id '
        result = self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
        if result and result not in ['NONE','ERROR']:
            for row in result:
                order_id = row['id']
                sSql = " select max(invoice_number) as max_invoice_number from list_of_invoices where order_number = " + `order_id`
                sSql += self.getWhere(None,dicUser,2)
                result2 = self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
                #print 'result2 act.1', result2
                if result2 and result2 not in ['NONE','ERROR'] and result2[0]['max_invoice_number'] not in ['NONE','ERROR'] :
                    if result2[0]['max_invoice_number'] < 1 :
                        liOrder.append(order_id)
                        #print 'append1 = ', order_id
                else:
                    liOrder.append(order_id)
                    #print 'append2 = ', order_id
                    
        if not liOrder:
            liOrder = 'NONE'
            
        #print liOrder
        self.writeLog('liOrder all invoices')
        self.writeLog(liOrder)
        return liOrder
    def checkMaturityDay(self, dicUser):
        sSql = 'select id, order_number from list_of_invoices where maturity is null '
        sSql += self.getWhere('',dicUser,2)
        result =  self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
        if result and result not in ['NONE','ERROR']:
            for row in result:
                dicOrder = {}

                dicOrder['orderid'] = row['order_number']
                topID = self.getToPID(dicOrder, dicUser)
                sSql = 'select days from terms_of_payment where id = ' + `topID`
                result2 =  self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
                days = 0
                if  result2 and result2 not in ['NONE','ERROR']:
                    days = result2[0]['days']
                    
                sSql = ' update list_of_invoices set maturity = date_of_invoice + ' + `days`
                sSql += ' where id = ' + `row['id']`
                result3 =  self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
        
#    def getResidue(self, dicUser):
#        self.checkMaturityDay(dicUser)
#        sNameOfView = "v_" + dicUser['Name'] + "_" + `dicUser['client']`+ "_residue"
#    
#        sDeleteResidue = "drop view " + sNameOfView
#        result = self.oDatabase.xmlrpc_executeNormalQuery(sDeleteResidue,dicUser)
#        sResidue = "create view " + sNameOfView + " as "
#        sResidue += " select list_of_invoices.total_amount -  (case when (select sum(in_payment.inpayment) from in_payment where   to_number(in_payment.invoice_number,'999999999') = list_of_invoices.invoice_number and status != 'delete' and client = " + `dicUser['client']` + ")  != 0 then (select sum(in_payment.inpayment)  + sum(in_payment.cash_discount) from in_payment where   to_number(in_payment.invoice_number,'999999999') = list_of_invoices.invoice_number and status != 'delete' and client = " + `dicUser['client']` + ") else 0 end)  as  residue, list_of_invoices.total_amount as total_amount, "
#        sResidue += " list_of_invoices.maturity as maturity,  list_of_invoices.order_number as order_number,  list_of_invoices.id as id ,  list_of_invoices.invoice_number as invoice_number, list_of_invoices.date_of_invoice as date_of_invoice from list_of_invoices "
#        sResidue += self.getWhere('',dicUser,'1','list_of_invoices.')
#        
#        result = self.oDatabase.xmlrpc_executeNormalQuery(sResidue,dicUser)
#        print "result at create residue view",  result
#        sSql = 'select distinct '
#        sSql += 'v_residue.total_amount as total_amount, '
#        sSql += 'address.lastname as lastname, address.city as city, '
#        sSql += 'orderbook.id as order_id, v_residue.maturity as maturity, '
#        sSql += " v_residue.residue as residue, "
#        sSql += ' v_residue.order_number as order_number, v_residue.id, v_residue.invoice_number as invoice_number, v_residue.date_of_invoice as date_of_invoice '
#        sSql += " from list_of_invoices , orderbook, address,  " + sNameOfView + " as v_residue "
#        sSql += " where  v_residue.residue -(case when orderbook.discount is not Null then orderbook.discount else 0.00 end)  > 0.01 and v_residue.order_number = orderbook.id"
#        sSql += " and orderbook.id =  list_of_invoices.order_number and address.id = orderbook.addressnumber"
#        sSql += " order by lastname, v_residue.date_of_invoice "
#        result = self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
#        print "result at list residue from view",  result
#        return result 

    def getResidue(self, dicUser):
        sSql = "select total_amount,lastname, city, order_id, maturity,  residue , order_number, invoice_number,date_of_invoice, this_date from fct_getResidue() as (total_amount float, lastname varchar(150),  city varchar(150),  order_id integer,  maturity date,residue float,  order_number integer, invoice_number integer, date_of_invoice date, this_date date) "
        result = self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
        return result 
            
#    def getReminder(self, dicUser):
#        self.checkMaturityDay(dicUser)
#        iReminder = 10
#        sResidue = "list_of_invoices.total_amount -  (case when (select sum(in_payment.inpayment) from in_payment where   to_number(in_payment.invoice_number,'999999999') = list_of_invoices.invoice_number and status != 'delete' and client = " + `dicUser['client']` + ")  != 0 then (select sum(in_payment.inpayment) + sum(in_payment.cash_discount) from in_payment where   to_number(in_payment.invoice_number,'999999999') = list_of_invoices.invoice_number and status != 'delete' and client = " + `dicUser['client']` + ") else 0 end) "
#        
#        
#        sSql = 'select distinct '
#        sSql += 'list_of_invoices.total_amount as total_amount, '
#        sSql += 'address.lastname as lastname, address.city as city, '
#        sSql += "orderbook.id as order_id, to_char(list_of_invoices.maturity, \'" + dicUser['SQLDateFormat'] + "\') as maturity, "
#        sSql += sResidue + " as residue, "
#        sSql += " current_date - list_of_invoices.maturity as remind_days, "
#        sSql += " list_of_invoices.order_number as order_number, list_of_invoices.id, list_of_invoices.invoice_number as invoice_number, to_char(list_of_invoices.date_of_invoice, \'" + dicUser['SQLDateFormat'] + "\')  as date_of_invoice "
#        sSql += " from list_of_invoices ,in_payment, orderbook, address "
#        sSql += self.getWhere('',dicUser,'1','list_of_invoices.')
#        sSql += "and " + sResidue + " > 0.01"
#        sSql += " and (current_date - list_of_invoices.maturity > " + `iReminder` + ") "
#        sSql += " and orderbook.id =  list_of_invoices.order_number and address.id = orderbook.addressnumber"
#        
#        result = self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
#        return result    
    
    def getReminder(self, dicUser):
        iReminder = 10 
        sSql = "select total_amount,lastname, city, order_id, maturity,  residue , order_number, invoice_number,date_of_invoice , this_date , this_date - maturity as remind_days from fct_getReminder(" + `iReminder` + ") as (total_amount float, lastname varchar(150),  city varchar(150),  order_id integer,  maturity date,residue float,  order_number integer, invoice_number integer, date_of_invoice date, this_date date ) "
        result = self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
        return result    
    
    def getListOfInvoicesByTop(self, dicExtraData, dicUser ):
        self.checkMaturityDay(dicUser)
        #print dicExtraData
        iReminder = 10
        sResidue = "list_of_invoices.total_amount -  (case when (select sum(in_payment.inpayment) from in_payment where   to_number(in_payment.invoice_number,'999999999') = list_of_invoices.invoice_number and status != 'delete' and client = " + `dicUser['client']` + ")  != 0 then (select sum(in_payment.inpayment) from in_payment where   to_number(in_payment.invoice_number,'999999999') = list_of_invoices.invoice_number and status != 'delete' and client = " + `dicUser['client']` + ") else 0 end) "
        
        
        sSql = 'select distinct '
        sSql += 'list_of_invoices.total_amount as total_amount, '
        sSql += 'address.lastname as lastname, address.city as city, '
        sSql += "orderbook.id as order_id, to_char(list_of_invoices.maturity, \'" + dicUser['SQLDateFormat'] + "\') as maturity, "
        sSql += sResidue + " as residue, "
        sSql += " current_date - list_of_invoices.maturity as remind_days, "
        sSql += " list_of_invoices.order_number as order_number, list_of_invoices.id, list_of_invoices.invoice_number as invoice_number, to_char(list_of_invoices.date_of_invoice, \'" + dicUser['SQLDateFormat'] + "\')  as date_of_invoice "
        sSql += " from list_of_invoices ,in_payment, orderbook, address "
        sSql += self.getWhere('',dicUser,'1','list_of_invoices.')
        sSql += "and " + sResidue + " > 0.01"
        sTops = dicExtraData['Tops']
        tops = None
        try:
            cpServer, f = self.getParser(self.CUON_FS + '/clients.ini')
            if sTops == 'directDebit':
                tops = self.getConfigOption('CLIENT_' + `dicUser['client']`,'list_of_invoices_directDebit', cpServer)
                print tops
        except:
            tops = None

        if tops:
            liTops = tops.split(',')
            if liTops:
                sSql += ' and ('
                for sTop in liTops:
                    sSql += 'case when (select max(orderinvoice.order_top) = ' + sTop + ' as top from orderinvoice where orderbook.id = orderinvoice.orderid) = true then true else case when (select max(orderinvoice.order_top) isnull as top from orderinvoice where orderbook.id = orderinvoice.orderid) = true then (select top_id = ' + sTop + ' from addresses_misc where addresses_misc.address_id = address.id ) else false end end or '
                    #sSql += 'case  orderinvoice.order_top = ' + sTop + ' or'
                sSql = sSql[:len(sSql)-3]
                sSql += ' )'
                
        #sSql += " and (current_date - list_of_invoices.maturity > " + `iReminder` + ") "
        sSql += " and orderbook.id =  list_of_invoices.order_number and address.id = orderbook.addressnumber"
        #sSql += ' and orderbook.id = orderinvoice.orderid '
        #print sSql
        result = self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
        result2 = []
        
        return result    
        
    def xmlrpc_getStatsMisc(self, dicUser):
        
        return ['NONE']
    
    def xmlrpc_getStatsGlobal(self, dicUser):
        result = {}
        iCentury = 2
        iDecade = 5
        iYear = 3
        iQuarter = 6
        iMonth = 14
        iWeek = 5
        liSql = []
        liSql.append({'id':'day','sql':'doy','logic':'='})
        liSql.append({'id':'week','sql':'week','logic':'='})
        liSql.append({'id':'month','sql':'month','logic':'='})
        liSql.append({'id':'quarter','sql':'quarter','logic':'='})
        liSql.append({'id':'year','sql':'year','logic':'='})
        liSql.append({'id':'decade','sql':'decade','logic':'='})
        liSql.append({'id':'century','sql':'century','logic':'='})
        sSql = "select now(), "
        for vSql in liSql:
            for z1 in xrange(0,30):
                if vSql['id'] == 'decade' and z1 > iDecade:
                    pass
                elif vSql['id'] == 'century' and z1 > iCentury:
                    pass 
                elif vSql['id'] == 'year' and z1 > iYear:
                    pass 
                elif vSql['id'] == 'quarter' and z1 > iQuarter:
                    pass 
                elif vSql['id'] == 'month' and z1 > iMonth:
                    pass     
                elif vSql['id'] == 'week' and z1 > iWeek:
                    pass     
                
                else:
                    #print "z1 = ",  z1
                    sSql += " (select sum(po.amount * po.price)   from list_of_invoices as li, orderposition as po, orderbook as ob "
                    sSql += " where date_part('" + vSql['sql'] +"', li.date_of_invoice) " + vSql['logic'] + " " + self.getNow(vSql,  z1)[0]
                    sSql += "  and  date_part('year', li.date_of_invoice) " + vSql['logic'] + " " + self.getNow(vSql,  z1)[1]
                    sSql += " and li.order_number = ob.id and po.orderid = li.order_number "
                    sSql += self.getWhere('', dicUser, 2,'li.')
                    sSql += " ) as " + 'order_global_' + vSql['id'] + '_count_' + `z1` +", "   

                    sSql += "( select sum(inpayment) from in_payment "
                    sSql += " where date_part('" + vSql['sql'] +"',  date_of_paid) " + vSql['logic'] + " " + self.getNow(vSql,  z1)[0]  
                    sSql += " and date_part('year',  date_of_paid) " + vSql['logic'] + " " + self.getNow(vSql,  z1)[1]  
                    sSql += self.getWhere('', dicUser, 2)         
                    sSql += " ) as " + 'order_global_incoming_' + vSql['id'] + '_count_' + `z1` +", " 
        sSql = sSql[0:len(sSql)-2]
        self.writeLog(sSql)
        tmpResult = self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
        if tmpResult and tmpResult not in ['NONE','ERROR']:
#            oneResult = tmpResult[0]
#            for key in oneResult.keys():
#                result[key] = oneResult[key]
            result = tmpResult[0]
        return result
        
    def xmlrpc_getStatsCaller(self, dicUser):
        result = {}
        CALLER_ID = None
        WITHOUT_ID = None
        MIN_SCHEDUL_YEAR = '2005'
        SCHEDUL_PROCESS_STATUS = None
        liCaller = None
        liSchedulProcessStatus = None
        iCentury = 2
        iDecade = 5
        iYear = 3
        iQuarter = 6
        iMonth = 14
        iWeek = 5
        
        try:
                       
            cpServer, f = self.getParser(self.CUON_FS + '/user.cfg')
            #print cpServer
            #print cpServer.sections()
            
            CALLER_ID = self.getConfigOption('STATS','CALLER_ID', cpServer)
            WITHOUT_ID = self.getConfigOption('STATS','WITHOUT_ID', cpServer)
        
        except:
            pass
        try:
                       
            cpServer, f = self.getParser(self.CUON_FS + '/clients.ini')
            #print cpServer
            #print cpServer.sections()
            
            SCHEDUL_PROCESS_STATUS = self.getConfigOption('CLIENT_' + `dicUser['client']`,'SchedulProcessStatus', cpServer)
            iValue = self.getConfigOption('CLIENT_' + `dicUser['client']`,'StatsCallerCentury', cpServer)
            if iValue:
                iCentury = int(iValue)
            
            iValue = self.getConfigOption('CLIENT_' + `dicUser['client']`,'StatsCallerDecade', cpServer)
            if iValue:
                iDecade = int(iValue)
            
            iValue = self.getConfigOption('CLIENT_' + `dicUser['client']`,'StatsCallerYear', cpServer)
            if iValue:
                iYear = int(iValue)
            
            iValue = self.getConfigOption('CLIENT_' + `dicUser['client']`,'StatsCallerQuarter', cpServer)
            if iValue:
                iQuarter = int(iValue)
            
            iValue = self.getConfigOption('CLIENT_' + `dicUser['client']`,'StatsCallerMonth', cpServer)
            if iValue:
                iMonth = int(iValue)
                
            iValue = self.getConfigOption('CLIENT_' + `dicUser['client']`,'StatsCallerWeek', cpServer)
            if iValue:
                iWeek = int(iValue)
                
                    
                
        except:
            pass    
        print "SCHEDUL_PROCESS_STATUS",   SCHEDUL_PROCESS_STATUS
        
        if SCHEDUL_PROCESS_STATUS:
            liSPS = SCHEDUL_PROCESS_STATUS.split(',')
            print "liSPS",  liSPS
            liSchedulProcessStatus = []
            for st in liSPS:
                print st
                liSchedulProcessStatus.append(int(st.strip()))
            
       
            
        if CALLER_ID:
            liCaller = CALLER_ID.split(',')
            print 'liCaller = ',  liCaller
            liSql = []
            liSql.append({'id':'day','sql':'doy','logic':'='})
            liSql.append({'id':'week','sql':'week','logic':'='})
            liSql.append({'id':'month','sql':'month','logic':'='})
            liSql.append({'id':'quarter','sql':'quarter','logic':'='})
            liSql.append({'id':'year','sql':'year','logic':'='})
            liSql.append({'id':'decade','sql':'decade','logic':'='})
            liSql.append({'id':'century','sql':'century','logic':'='})
        
            for caller in liCaller:
                caller_name = None
                sSql = 'select cuon_username from staff where staff.id = ' + caller
                res1 = self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
                print 'dicUser' , dicUser
                if res1 and res1 not in ['NONE','ERROR']:
                    caller_name = res1[0]['cuon_username']
                if caller_name:    
                    sSql = "select '" + caller_name + "' as caller_name_" + caller + " ,"
                    print sSql
                    for vSql in liSql:
                        for z1 in xrange(0,30):
                            if vSql['id'] == 'decade' and z1 > iDecade:
                                pass
                            elif vSql['id'] == 'century' and z1 > iCentury:
                                pass 
                            elif vSql['id'] == 'year' and z1 > iYear:
                                pass 
                            elif vSql['id'] == 'quarter' and z1 > iQuarter:
                                pass 
                            elif vSql['id'] == 'month' and z1 > iMonth:
                                pass     
                            elif vSql['id'] == 'week' and z1 > iWeek:
                                pass     
                            
                            else:
                                sSql += " (select sum(po.amount * po.price)   from list_of_invoices as li, orderposition as po, orderbook as ob, address as ad  "
                                sSql += " where date_part('" + vSql['sql'] +"', li.date_of_invoice) " + vSql['logic'] + " " + self.getNow(vSql,  z1)[0]
                                sSql += "  and  date_part('year', li.date_of_invoice) " + vSql['logic'] + " " + self.getNow(vSql,  z1)[1]
                                sSql += " and li.order_number = ob.id and po.orderid = li.order_number "
                                sSql += " and ad.id = ob.addressnumber and ad.caller_id = " + `caller` + " "
                                sSql += self.getWhere('', dicUser, 2,'li.')
                                sSql += " ) as " + 'order_caller_'+caller +'_' + vSql['id'] + '_count_' + `z1` +", "   
            
                                sSql += "( select sum(inpayment) from in_payment , orderbook as ob, address as ad "
                                sSql += " where date_part('" + vSql['sql'] +"',  date_of_paid) " + vSql['logic'] + " " + self.getNow(vSql,  z1)  [0]
                                sSql += " and date_part('year' ,  date_of_paid) " + vSql['logic'] + " " + self.getNow(vSql,  z1)[1]
                                sSql += " and in_payment.order_id = ob.id  "
                                sSql += " and ad.id = ob.addressnumber and ad.caller_id = " + `caller` + " "
                                
                                sSql += self.getWhere('', dicUser, 2, 'in_payment.')         
                                sSql += " ) as " + 'order_incoming_caller_' + caller +'_' + vSql['id'] + '_count_' + `z1` +", " 
                                print "sSql 2 = ",  sSql
                                
                sSql = sSql[0:len(sSql)-2]
                print "Caller = ",  caller
                if caller == 4:
                    print sSql
                    
                #print "len sql = ",  len(sSql)
                self.writeLog(sSql)
                tmpResult = self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
                if tmpResult and tmpResult not in ['NONE','ERROR']:
                    oneResult = tmpResult[0]
                    for key in oneResult.keys():
                        if oneResult[key] and  oneResult[key] not in ['NONE','ERROR']:
                            result[key] = oneResult[key]
                        else:
                            result[key] =0
                        #result[key] = oneResult[key]
        return result
        
    def xmlrpc_getStatsReps(self, dicUser):
        
        return ['NONE']
    def xmlrpc_getStatsSalesman(self, dicUser):
        
        return ['NONE']

    def xmlrpc_getStatTaxVat1(self, dicUser):
        self.writeLog('start tax vat stats')
        
        sSql = " select * from fct_getStatTaxVat() as (id int, vat_value float , vat_name varchar(20), vat_designation varchar(60), tax_vatSum numeric, sum_price_netto numeric, z1 int) "
        
        res1 = self.oDatabase.xmlrpc_executeNormalQuery(sSql,  dicUser)
        #print 'Data from sql = ' ,  res1
        result = {}
        for row in res1:
         
            #print row['id'],  row['z1'], row['tax_vatsum'], row['vat_value'] , row['vat_name']   
            result['TaxVat_month_tax_vatSum_taxvatID_' + `row['id']` + '_taxvatMonth_' + `row['z1']`] =  float(row['tax_vatsum'] )
            result['TaxVat_month_tax_vatValue_taxvatID_' + `row['id']` + '_taxvatMonth_' + `row['z1']`] =  row['vat_value']               
            result['TaxVat_month_tax_vatName_taxvatID_' + `row['id']` + '_taxvatMonth_' + `row['z1']`] =    row['vat_name']         
            result['TaxVat_month_tax_NetSum_taxvatID_' + `row['id']` + '_taxvatMonth_' + `row['z1']`] =  float(row['sum_price_netto'] )
          
        
        
        #self.writeLog('STATS-RESULT = ' + `result`)
        
                
        return result
        

    def xmlrpc_dup_order(self, iOrderID, dicUser, iType = 0):
        sSql = "select * from  fct_duplicateOrder(" + `iOrderID` + ", " + `iType` + ")" 
        result = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser)
        
        return result

    def xmlrpc_getArticleParts(self, dicOrder, dicUser):
        sSql = "select article_id from  fct_getArticlePartsListForOrder(" + `dicOrder['orderid']` + ") as (article_id int) " 
        result = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser)
        
        return result
        
