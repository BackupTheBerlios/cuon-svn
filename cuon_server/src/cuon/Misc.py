import time
from datetime import datetime
import random
import xmlrpclib
from twisted.web import xmlrpc
 
from basics import basics
import Database

class Misc(xmlrpc.XMLRPC, basics):
    def __init__(self):
        basics.__init__(self)
        self.oDatabase = Database.Database()
        
    def xmlrpc_getListOfTOPs (self, dicuser):
        sSql = 'select id, number from terms_of_payment'
        sSql = sSql + context.sql.py_getWhere("",dicUser,1)
        result = oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
        li = []
        if result != 'NONE':
           for i in range(len(result)):
               li.append(result[i]['id'] + '    ' + result[i]['number'])
        
        return li
   
    def xmlrpc_getListOfTaxVat(self, dicUser):
        sSql = 'select vat_name from tax_vat'
        sSql = sSql + self.getWhere("",dicUser,1)

        result = self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
        li = []
        if result != 'NONE':
           for i in range(len(result)):
               li.append(result[i]['vat_name'])
        
        return li
