import time
from datetime import datetime
import random
import xmlrpclib
from twisted.web import xmlrpc
 
from basics import basics
import Database

class Stock(xmlrpc.XMLRPC, basics):
    def __init__(self):
        basics.__init__(self)
        self.oDatabase = Database.Database()
        
        
    def xmlrpc_getArticleStockInfo (self, id, dicUser):
    
        act1 = self.getStockAmount(id, dicUser)
        res1 = 0
        offer1 = 0
        dicStock = {}
        dicStock['actual'] = act1
        dicStock['reserved'] = res1
        dicStock['offer'] = offer1
        dicStock['free'] = act1 - res1 -offer1
        return dicStock

    def getStockAmount(self, ar_id, dicUser):
        self.writeLog('start stock amount')
        act = 0
        client = dicUser['client']
        id1 = ar_id
        
        sSql =  "select  b.number as article_number, "
        sSql = sSql + " sum(a.to_embed) as amount " 
        sSql = sSql + "from stock_goods as a, articles as b where "
        sSql = sSql + "a.article_id = " + `id1` + "and b.id = " + `id1` + " "
        sSql = sSql + "and a.client = " + `client` 
        sSql = sSql + "and b.client = " + `client` 
        sSql = sSql + "and b.status != 'delete' and a.status != 'delete' " 
        sSql = sSql + "group by  b.number, b.designation order by b.number "
        self.writeLog('goods-List1 Sql = ' + `sSql` )
        dicUser['noWhereClient'] = 'YES'
        result = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser)
        try:
           act = result[0]['amount']
        except:
           pass
        
        return act
    def xmlrpc_getGoodsList1 (self, dicSearchlists, dicUser):
        
        context.logging.writeLog('start goods list 1')
        client = dicUser['client']
        sSql =  "select  b.number as article_number, b.designation as article_designation,"
        sSql = sSql + " sum(a.to_embed) as amount " 
        sSql = sSql + "from stock_goods as a, articles as b where a.article_id = b.id "
        sSql = sSql + "and a.client = " + `client` 
        sSql = sSql + "and b.client = " + `client` 
        sSql = sSql + "and b.status != 'delete' and a.status != 'delete' " 
        sSql = sSql + "group by b.number, b.designation order by b.number "
        context.logging.writeLog('goods-List1 Sql = ' + `sSql` )
        dicUser['noWhereClient'] = 'YES'
        result = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser)
        
        return result
