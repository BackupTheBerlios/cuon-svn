import random
import xmlrpclib
from twisted.web import xmlrpc
 
from basics import basics
import Database

class Finances(xmlrpc.XMLRPC, basics):
    def __init__(self):
        basics.__init__(self)
        self.oDatabase = Database.Database()
        
        


    def getCashAccountBook(self, dicSearchfields, dicUser):
    
        dicUser['NoWhereClient'] = 'YES'
        client = dicUser['client']
        dicResults = {}
        sSql = " select a.designation as designation, a.document_number1 as nr1, a.document_number2 as nr2, "
        sSql = sSql + " to_char(a.accounting_date, \'" + dicUser['SQLDateFormat'] + "\') as date, "
        sSql = sSql + " a.account_1 as account, a.value_c1 as credit, a.value_d1 as debit "
        #sSql = sSql + " account_2, value_c2, value_d2 "
        #sSql = sSql + " account_3, value_c3, value_d3 "
        #sSql = sSql + " account_4, value_c4, value_d4 "
        
        sSql = sSql + "from account_sentence as a "
        
        sSql = sSql + "where date_part('year', a.accounting_date) = " + dicSearchfields['eYear'] +" "
        sSql = sSql + "and  date_part('month', a.accounting_date) = " + dicSearchfields['eMonth'] +" "
        sSql = sSql + self.getWhere("",dicUser,2,'a.')
        sSql = sSql + " order by a.accounting_date "
        
        self.writeLog('getCashAcountBook sSql = ' + `sSql`)
        result_main = oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser)
        
        
        sDate_begin = dicSearchfields['eYear'] + '/' + dicSearchfields['eMonth'] + '/' + '01'
        sSql = "select (sum(value_c1) - sum(value_d1)) as saldo from account_sentence"
        sW = " where accounting_date < '" + sDate_begin + "' "
        
        sSql = sSql + self.getWhere(sW, dicUser,1)
        
        result = oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser)
        if result:
           if result[0]['saldo'] >= 0:
              result[0]['saldo_debit'] =  result[0]['saldo']
           else:
              result[0]['saldo_credit'] =  result[0]['saldo']
        
        fSaldo = result[0]['saldo']
        self.writeLog('getCashAcountBook result_main = ' + `result_main`)
        for v1 in result_main:
            fSaldo = fSaldo + v1['debit'] - v1['credit']
            v1['saldo'] = fSaldo
        
        result[0]['saldo_end'] = fSaldo 
        dicResults['cab'] = result_main
        dicResults['before'] = result
        return dicResults
