import time
from datetime import datetime
import random
import xmlrpclib
from twisted.web import xmlrpc
 
from basics import basics
import Database

class Address(xmlrpc.XMLRPC, basics):
    def __init__(self):
        basics.__init__(self)
        self.oDatabase = Database.Database()
        
    def xmlrpc_getAddress(self,id, dicUser ):
    
        sSql = 'select address, lastname, lastname2,firstname, street, zip, city, ' 
        sSql = sSql + ' trim(country) || \'-\' || trim(zip) || \' \' || trim(city) as cityfield, state, country from address '
        sWhere = 'where id = ' + `id`
        sWhere = self.getWhere(sWhere, dicUser)
        sSql = sSql + sWhere
        
        return self.xmlrpc_executeNormalQuery(sSql, dicUser)
