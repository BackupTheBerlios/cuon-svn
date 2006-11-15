import time
from datetime import datetime
import random
import xmlrpclib
from twisted.web import xmlrpc
 
from basics import basics
import iCal
import Database
import string


class WebShop(xmlrpc.XMLRPC, basics):
    

    def __init__(self):
            basics.__init__(self)
            self.oDatabase = Database.Database()
            
            
    def xmlrpc_fillValues(self,sNameOfTable, ID, direction, dicUser):
        self.out('fillValues reached')
        webTable = self.getTableInformation(sNameOfTable)
        
        
        if direction == 'FromWebshop':
           dicUser['Database'] = 'osCommerce'
           cSql = 'select * from ' + webTable['name'] + ' where ' + webTable['webID'] + '  = ' + `ID`
        elif direction == 'ToWebshop':
           dicUser['Database'] = 'osCommerce'
           cSql = 'select * from ' + webTable['myName'] + ' where id = ' + `ID`
           
        dicResult = context.src.sql.py_executeNormalQuery(cSql, dicUser)
        context.logging.writeLog('dicResult = ' + `dicResult`)
        dicValues = {}
        
        # fill dicValues
        #dicValues['address_id'] = [self.addressId, 'int']
        for column in webTable['columns']:
           context.logging.writeLog('Column = ' + `column`)
           context.logging.writeLog('Column1 = ' + `column['myColumnName']`)
           context.logging.writeLog('Column2 = ' + `dicResult[0][column['name']]`)
           context.logging.writeLog('Column3 = ' + ` column['myType'][0]`)
           if column['myType'][0] == 'varchar' or column['myType'] == 'char':
              try:
                 dicResult[0][column['name']] = dicResult[0][column['name']]
                 context.logging.writeLog('Column2(decode) = ' + `dicResult[0][column['name']]`)
              except Exception, param:
                 context.logging.writeLog('decoding error : '  + `param` )
           if column['myType'][0] == 'int':
              pass
        
           if direction == 'FromWebshop':
              dicValues[column['myColumnName']] = [dicResult[0][column['name']], column['myType'][0] ]
        
           elif direction == 'ToWebshop':
              dicValues[column['name']] = [dicResult[0][column['myColumnName']], column['type'][0] ]
              
        
           context.logging.writeLog('dicValues = ' + `dicValues`)
        
        return dicValues
    def getTableInformation(self, nameOfTable):
        dicTable = {}
        liColumns = []
        
        if nameOfTable == 'address_book':
           dicTable['name'] = 'address_book'
           dicTable['webID'] = 'address_book_id'
           dicTable['myTableName'] = 'address'
           liColumns.append( {'name':'address_book_id', 'myColumnName':'webshop_address_id','type':['int','11','notNull','None'], 'myType':['int','11','notNull','None']})
           liColumns.append({'name':'customers_id', 'myColumnName':'webshop_customers_id','type':['int','11','notNull','None'],'myType':['int','11','notNull','None']})
           liColumns.append({'name':'entry_gender', 'myColumnName':'webshop_gender','type':['char','1','notNull','None'],'myType':['varchar','1','notNull','None']})
           liColumns.append({'name':'entry_firstname', 'myColumnName':'firstname','type':['varchar','32','notNull','None'],'myType':['varchar','50','notNull','None']})
           liColumns.append({'name':'entry_lastname', 'myColumnName':'lastname','type':['varchar','32','notNull','None'],'myType':['varchar','50','notNull','None']})
           liColumns.append({'name':'entry_street_address', 'myColumnName':'street','type':['varchar','64','notNull','None'],'myType':['varchar','50','notNull','None']})
           liColumns.append({'name':'entry_suburb', 'myColumnName':'suburb','type':['varchar','32','notNull','None'],'myType':['varchar','50','notNull','None']})
           liColumns.append({'name':'entry_postcode', 'myColumnName':'zip','type':['varchar','10','notNull','None'],'myType':['varchar','10','notNull','None']})
           liColumns.append({'name':'entry_city', 'myColumnName':'city','type':['varchar','32','notNull','None'],'myType':['varchar','50','notNull','None']})
           liColumns.append({'name':'entry_state', 'myColumnName':'state_full','type':['varchar','32','notNull','None'],'myType':['varchar','50','notNull','None'],'Translate':{'table':'state','field':'name', 'replace_with':'short_name'} })
           dicTable['columns'] =liColumns            
        
        elif nameOfTable == 'countries':
           dicTable['name'] = 'countries'
           dicTable['webID'] = 'countries_id'
           dicTable['myTableName'] = 'countries'
           liColumns.append({'name':'countries_id', 'myColumnName':'webshop_id','type':['int','11','notNull','None'],'myType':['int','11','notNull','None']})
           liColumns.append({'name':'countries_name', 'myColumnName':'name','type':['varchar','64','notNull','None'],'myType':['int','11','notNull','None']})
        
        elif nameOfTable == 'articles':
           dicTable['name'] = 'products'
           dicTable['webID'] = 'products_id'
           dicTable['myTableName'] = 'articles'
           liColumns.append({'name':'products_id', 'myColumnName':'webshop_id','type':['int','11','notNull','None'],'myType':['int','11','Null','None']})
           liColumns.append({'name':'products_model', 'myColumnName':'number','type':['varchar','12','Null','None'],'myType':['varchar','30','Null','None']})
           liColumns.append({'name':'products_weight', 'myColumnName':'quantumperwrap','type':['decimal','5,2','Null','None'],'myType':['float','0','Null','None']})
        
           dicTable['columns'] =liColumns            
        
        elif nameOfTable == 'articles_webshop':
           dicTable['name'] = 'products'
           dicTable['webID'] = 'products_id'
           dicTable['myTableName'] = 'articles_webshop'
           
           liColumns.append({'name':'products_image', 'myColumnName':'image','type':['varchar','64','Null','None'],'myType':['varchar','54','Null','None']})
           liColumns.append({'name':'products_price', 'myColumnName':'price','type':['decimal','15,4','Null','None'],'myType':['float','0','Null','None']})
           liColumns.append({'name':'products_status', 'myColumnName':'status','type':['tinyint','1','Null','None'],'myType':['int','0','Null','None']})
        
           
        
        return dicTable
        
    def loadCompleteIdsOfTable(self, sTable, sID, dicUser):
        cSQL = 'select ' + sID + '  from ' + sTablesTable, sID, dicUser 
    
        context.logging.writeLog('py_loadCompleteTable : ' + `cSQL`)
        result = context.src.sql.py_executeNormalQuery(cSQL, dicUser)
        
        return result

    def updateAddress(self, dicUser):

        
        sNameOfTable = 'address_book'
        sID = 'address_book_id'
        dicUser['Database'] = 'osCommerce'
        #print `dicUser`
        webTable = context.src.Databases.py_getXmlData(sNameOfTable)
        
              
        liRecords = context.src.WebShop.py_loadCompleteIdsOfTable(sNameOfTable, sID, dicUser)
        context.logging.writeLog('liRecords :' + `liRecords`)
        direction = 'FromWebshop'
        for WebshopAddressId in liRecords:
            context.logging.writeLog('WebshopAddressID :' + `WebshopAddressId`)
            
            dicValues = context.src.WebShop.py_fillValues(sNameOfTable, WebshopAddressId['address_book_id'], direction , dicUser)
            dicUser['Database'] = 'cuon'
            cSql = ' select id from address where webshop_address_id = '  + `WebshopAddressId['address_book_id']`
            liResult = context.src.sql.py_executeNormalQuery(cSql, dicUser)
            addressID = -1
            context.logging.writeLog('AddressID-Result :' + `liResult`)
            
            if liResult:
                addressID = liResult[0]['id']
                context.logging.writeLog('addressID :' + `addressID`)
            
            if addressID > 0:
                # update if update ist checked on
                dicUser['Database'] = 'cuon'
                cSql = 'select is_webshop, update_from_webshop from addresses_misc where address_id = ' + `addressID`
                liResult2 = context.src.sql.py_executeNormalQuery(cSql, dicUser)
                context.logging.writeLog('liResult2 :' + `liResult2`)
                if liResult2:
                    if liResult2[0]['is_webshop'] == True and  liResult2[0]['update_from_webshop'] == True:
                        dicUser['Encode'] = False
                        
                        context. src.sql.py_saveRecord(webTable['myTableName'], addressID, dicValues, dicUser)
                        dicUser['Encode'] = True
            else:
                # insert new Address to cuon-Database
                dicUser['Database'] = 'cuon'
                context.logging.writeLog('save new Record 1 ')
                iNewID =  - 1
        
                dicUser['Encode'] = False
                newID = context. src.sql.py_saveRecord(webTable['myTableName'], iNewID, dicValues, dicUser)
                dicUser['Encode'] = True
                       
        
                dicValues = {}
        
                dicValues['address_id'] = [newID[0]['last_value'], 'int']
        
                dicValues['is_webshop'] = [True, 'bool']
        
                dicValues['update_from_webshop'] = [True, 'bool']
        
                dicUser['Encode'] = False
                newID = context. src.sql.py_saveRecord('addresses_misc', iNewID, dicValues, dicUser)
                dicUser['Encode'] = True
        
                context.logging.writeLog('newID =   ' + `newID`)
                
                
        dicUser['Database'] = 'cuon'
        
        return dicValues
        
    def updateArticles(self,dicUser):

        
        sNameOfTable = 'products'
        sID = 'products_id'
        #print `dicUser`
        webTable = context.src.Databases.py_getXmlData(sNameOfTable)
        dicUser['Database'] = 'cuon'     
        liRecords = context.src.WebShop.py_loadCompleteIdsOfTable('articles', dicUser)
        context.logging.writeLog('liRecords :' + `liRecords`)
        direction = 'ToWebshop'
        for articlesId in liRecords:
            context.logging.writeLog('ArticlesID :' + `articlesId`)
            
            dicValues = context.src.WebShop.py_fillValues(sNameOfTable, articlesId['id'], direction , dicUser)
            
            dicUser['Database'] = 'cuon'
            cSql = ' select id from address where webshop_address_id = '  + `WebshopAddressId['address_book_id']`
            liResult = context.src.sql.py_executeNormalQuery(cSql, dicUser)
            addressID = -1
            context.logging.writeLog('AddressID-Result :' + `liResult`)
            
            if liResult:
                addressID = liResult[0]['id']
                context.logging.writeLog('addressID :' + `addressID`)
            
            if addressID > 0:
                # update if update ist checked on
                dicUser['Database'] = 'cuon'
                cSql = 'select is_webshop, update_from_webshop from addresses_misc where address_id = ' + `addressID`
                liResult2 = context.src.sql.py_executeNormalQuery(cSql, dicUser)
                context.logging.writeLog('liResult2 :' + `liResult2`)
            
                if liResult2:
                    if liResult2[0]['is_webshop'] == True and  liResult2[0]['update_from_webshop'] == True:
                        dicUser['Encode'] = False
                        context. src.sql.py_saveRecord(webTable['myTableName'], addressID, dicValues, dicUser)
                        dicUser['Encode'] = True
            else:
                # insert new Address to cuon-Database
                context.logging.writeLog('save new Record 1 ')
                iNewID =  - 1
        
                dicUser['Encode'] = False
                newID = context. src.sql.py_saveRecord(webTable['myTableName'], iNewID, dicValues, dicUser)
                dicUser['Encode'] = True
                       
        
                dicValues = {}
        
                dicValues['address_id'] = [newID[0]['last_value'], 'int']
        
                dicValues['is_webshop'] = [True, 'bool']
        
                dicValues['update_from_webshop'] = [True, 'bool']
        
                dicUser['Encode'] = False
                newID = context. src.sql.py_saveRecord('addresses_misc', iNewID, dicValues, dicUser)
                dicUser['Encode'] = True
        
                context.logging.writeLog('newID =   ' + `newID`)
                
                
        dicUser['Database'] = 'cuon'
        
        return dicValues
