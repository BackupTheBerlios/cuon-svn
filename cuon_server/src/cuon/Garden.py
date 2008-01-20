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
        
        if dicResult not in ['NONE','ERROR']:
           nr = dicResult[0]['delivery_number']
        return nr
        
    def xmlrpc_getNewSequenceNumber(self, year, dicUser ):
        nr = 0
        sSql = "select max(sequence_of_stock) as nr from hibernation  where date_part('year', \"begin_date\") = " + `year`
        sSql = sSql + self.getWhere("",dicUser,2)
        
        dicResult =  self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )
        if dicResult in [ 'NONE', 'ERROR']:
            nr = 0
        else:
            nr = dicResult[0]['nr']
        if not self.checkType(nr, 'int'):
            nr = 0
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
        if dicResult not in ['NONE','ERROR']:
           sSql1 = 'insert into list_of_invoices ( id, invoice_number, order_number) '
           sSql1 = sSql1 + ' values (nextval(\'list_of_invoices_id +sc +\'),nextval(\'numerical_misc_standard_invoice + sc + \'), ' 
           sSql1 = sSql1 + `orderNumber` + ' )'
           self.oDatabase.xmlrpc_executeNormalQuery(sSql1, dicUser )
        
        dicResult =  self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )
        
        if dicResult not in ['NONE','ERROR']:
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
        
        if dicResult not in ['NONE','ERROR']:
           nr = dicResult[0]['incoming_number']
        return nr
               
    def xmlrpc_getPickupNumber(self, orderNumber, dicUser):
                
        nr = 0
        sSqlSearch = 'select pickup_number from list_of_hibernation_pickup where order_number = ' + `orderNumber`
        dicResult =  self.oDatabase.xmlrpc_executeNormalQuery(sSqlSearch, dicUser )
        if dicResult == 'NONE':
           sSql1 = 'insert into list_of_hibernation_pickup ( id, pickup_number, order_number) '
           sSql1 = sSql1 + ' values (nextval(\'list_of_hibernation_pickup_id\'),nextval(\'numerical_hibernation_pickup_document_client_' + `dicUser['client']` + '\'), ' 
           sSql1 = sSql1 + `orderNumber` + ' )'
           self.oDatabase.xmlrpc_executeNormalQuery(sSql1, dicUser )
           
           dicResult =  self.oDatabase.xmlrpc_executeNormalQuery(sSqlSearch, dicUser )
        
        if dicResult not in ['NONE','ERROR']:
           nr = dicResult[0]['pickup_number']
        
            
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
        liFields.append(["hibernation.sequence_of_stock","sequence_of_stock"])
        liFields.append(["hibernation.begin_notes","begin_notes"])
        liFields.append(["hibernation.ends_notes","ends_notes"])

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
        liFields.append(["hibernation.sequence_of_stock","sequence_of_stock"])
        liFields.append(["hibernation.begin_notes","begin_notes"])
        liFields.append(["hibernation.ends_notes","ends_notes"])

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
        
        iPosition = 1
        result2 = []
        
        try:
            cpServer, f = self.getParser(self.CUON_FS + '/sql.ini')
            #print cpServer
            #print cpServer.sections()
            replace_staff_pickup = self.getConfigOption('modul_hibernation','replace_staff_pickup', cpServer)
            replace_staff_supply = self.getConfigOption('modul_hibernation','replace_staff_supply', cpServer)

            
            replace_plant_hibertion = self.getConfigOption('modul_hibernation','replace_plant_hibertion', cpServer)
           
            replace_plant_add_earth = self.getConfigOption('modul_hibernation','replace_plant_add_earth', cpServer)
            replace_plant_add_pot = self.getConfigOption('modul_hibernation','replace_plant_add_pot', cpServer)
            replace_plant_add_material = self.getConfigOption('modul_hibernation','replace_plant_add_material', cpServer)
            replace_plant_add_misc = self.getConfigOption('modul_hibernation','replace_plant_add_misc', cpServer)
            

            translate_price_staff_pickup_for = self.getConfigOption('modul_hibernation','translate_price_staff_pickup_for', cpServer)
            translate_price_staff_supply_for = self.getConfigOption('modul_hibernation','translate_price_staff_supply_for', cpServer)

            translate_price_hibernation_for = self.getConfigOption('modul_hibernation','translate_price_hibernation_for', cpServer)
            translate_price_add_earth_for = self.getConfigOption('modul_hibernation','translate_price_add_earth_for', cpServer)
            translate_price_add_pot_for = self.getConfigOption('modul_hibernation','translate_price_add_pot_for', cpServer)
            translate_price_add_material_for = self.getConfigOption('modul_hibernation','translate_price_add_material_for', cpServer)
            translate_price_add_misc_for = self.getConfigOption('modul_hibernation','translate_price_add_misc_for', cpServer)
            
            
            
            sSql ='select begin_working_time, ends_working_time, begin_staff_number, ends_staff_number from hibernation where id = ' + `hibID`
            
            
            sSql += self.getWhere("",dicUser,2)
            print sSql
            result = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )

            if result not in ['NONE','ERROR']:
                row = result[0]
                print 'row=', row
                if row['begin_working_time'] > 0.0001:
                    sSql = 'select fee_per_hour_invoice from staff_fee where staff_id = ' + `row['begin_staff_number']`
                    sSql += self.getWhere("",dicUser,2)
                    print sSql
                    result_2 = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )
                    print result_2
                    if result_2 not in ['NONE','ERROR']:
                        dicPos = {}
                        dicPos['position'] = [ iPosition,'int']
                        iPosition += 1
                        dicPos['price'] = [result_2[0]['fee_per_hour_invoice'] * row['begin_working_time'],'float']
                        dicPos['articleid'] = [int(replace_staff_pickup),'int']
                        dicPos['designation'] = [translate_price_staff_pickup_for + ' ','string']
                        dicPos['amount'] = [1.00,'float']

                        result2.append(dicPos)
                        
                if row['ends_working_time'] > 0.0001:
                    sSql = 'select fee_per_hour_invoice from staff_fee where staff_id = ' + `row['ends_staff_number']`
                    sSql += self.getWhere("",dicUser,2)
                    result_2 = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )
                    if result_2 not in ['NONE','ERROR']:
                        dicPos = {}
                        dicPos['position'] = [ iPosition,'int']
                        iPosition += 1
                        dicPos['price'] =  [result_2[0]['fee_per_hour_invoice'] * row['ends_working_time'],'float']
                        dicPos['articleid'] = [int(replace_staff_supply),'int']
                        dicPos['designation'] = [translate_price_staff_supply_for + ' ','string']
                        dicPos['amount'] = [1.00,'float']

                        result2.append(dicPos)
            
            # TODO search for staff --> fee
##            if result not in ['NONE','ERROR']:
##                if result['hib_price'] > 0:
##                        dicPos = {}
##                        dicPos['position'] = iPosition
##                        iPosition += 1
##                        dicPos['price'] = row['hib_price']
##                        dicPos['article_id'] = int(replace_plant_hibertion)
##                        dicPos['designation'] = row['bot_name']
##                        result2.append(dicPos) 
        
            sSql ='select hibernation_plant.id as hib_id, hibernation_plant.add_earth as hib_add_earth, '
            sSql +='hibernation_plant.add_material as hib_add_material, hibernation_plant.add_pot as hib_add_pot, '
            sSql +='hibernation_plant.add_misc as hib_add_misc, hibernation_plant.price as hib_price, '
            sSql += ' botany.botany_name as bot_name from hibernation_plant, botany where hibernation_plant.hibernation_number = ' + `hibID`
            sSql += ' and hibernation_plant.botany_number = botany.id '
            
            sSql += self.getWhere("",dicUser,2,'hibernation_plant.')
            print sSql
            
            result = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )
            print 'getOrderPositions.result: ', result
            
            if result not in ['NONE','ERROR']:
                for row in result:
                    print row
                    
                    if row['hib_price'] > 0:
                        dicPos = {}
                        dicPos['position'] = [ iPosition,'int']
                        iPosition += 1
                        dicPos['price'] = [row['hib_price'],'float']
                        dicPos['articleid'] = [int(replace_plant_hibertion),'int']
                        dicPos['designation'] = [translate_price_hibernation_for + ' ' + row['bot_name'],'string']
                        dicPos['amount'] = [1.00,'float']

                        result2.append(dicPos)
                    
                    if row['hib_add_earth'] > 0:
                        dicPos = {}
                        dicPos['position'] = [iPosition,'int']
                        iPosition += 1
                        dicPos['price'] = [row['hib_add_earth'],'float']
                        dicPos['articleid'] = [int(replace_plant_add_earth),'int']
                        dicPos['designation'] = [translate_price_add_earth_for +' ' + row['bot_name'],'string']
                        dicPos['amount'] = [1.00,'float']
                        result2.append(dicPos)
                    
                    
                    if row['hib_add_material'] > 0:
                        dicPos = {}
                        dicPos['position'] = [iPosition,'int']
                        iPosition += 1
                        dicPos['price'] = [row['hib_add_material'],'float']
                        dicPos['articleid'] = [int(replace_plant_add_material),'int']
                        dicPos['designation'] = [ translate_price_add_material_for + ' '  + row['bot_name'],'string']
                        dicPos['amount'] = [1.00,'float']
                        result2.append(dicPos)
                        
                        
                        
                      
                    if row['hib_add_pot'] > 0:
                        dicPos = {}
                        dicPos['position'] = [iPosition,'int']
                        iPosition += 1
                        dicPos['price'] = [row['hib_add_pot'],'float']
                        dicPos['articleid'] = [int(replace_plant_add_pot),'int']
                        dicPos['designation'] = [translate_price_add_pot_for + ' ' + row['bot_name'],'string']
                        dicPos['amount'] = [1.00,'float']
                        result2.append(dicPos)  
                        
                    
                    if row['hib_add_misc'] > 0:
                        dicPos = {}
                        dicPos['position'] = [iPosition,'int']
                        iPosition += 1
                        dicPos['price'] = [row['hib_add_misc'],'float']
                        dicPos['articleid'] = [int(replace_plant_add_misc),'int']
                        dicPos['designation'] = [translate_price_add_misc_for + ' ' + row['bot_name'],'string']
                        dicPos['amount'] = [1.00,'float']
                        result2.append(dicPos)    
                    print result2
                    
        except Exception, params:
            print 'Error'
            print Exception, params  
        if not result2:
            resutl2 = 'NONE'
            
        return result2
        
     
    def xmlrpc_getSum(self, hibID, dicUser):
        total_sum = 0
        retValue = '0'
        try:
            dicPos = self.xmlrpc_getOrderPositions(hibID,dicUser)
            
            for i in dicPos:
                if i.has_key('price') and i.has_key('amount'):
                    try:
                        print i['price'] , i['amount']
                        total_sum += i['price'][0] * i['amount'][0]
                        
                    except:
                        pass
        except:
            pass
        try:
            
            total_sum = ("%." + `self.CURRENCY_ROUND` + "f") % round(total_sum,self.CURRENCY_ROUND)
            
            #total_sum = round(total_sum,self.CURRENCY_ROUND)
            retValue = `total_sum` + ' ' + self.CURRENCY_SIGN
        except:
            pass
            
        return retValue
        
            
        
    def xmlrpc_getArticleAssociatedID(self, article_id, dicUser):
        id = 0
        sSql = "select id from botany where article_id = " + `article_id`
        sSql += self.getWhere(None,dicUser,2)
        
        liResult = self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
        if liResult and liResult not in ['NONE','ERROR']:
            id = liResult[0]['id']
        return id 
        
