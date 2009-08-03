import random
import xmlrpclib
from twisted.web import xmlrpc
 
from basics import basics
import Database

class Finances(xmlrpc.XMLRPC, basics):
    def __init__(self):
        basics.__init__(self)
        self.oDatabase = Database.Database()
        self.debugFinances = 1
        
    

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
        
        self.writeLog('getCashAcountBook sSql = ' + `sSql`,self.debugFinances)
        result_main = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser)
        
        
        sDate_begin = dicSearchfields['eYear'] + '/' + dicSearchfields['eMonth'] + '/' + '01'
        sSql = "select (sum(value_c1) - sum(value_d1)) as saldo from account_sentence"
        sW = " where accounting_date < '" + sDate_begin + "' "
        
        sSql = sSql + self.getWhere(sW, dicUser,1)
        
        result = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser)
        if result not in ['NONE','ERROR']:
           if result[0]['saldo'] >= 0:
              result[0]['saldo_debit'] =  result[0]['saldo']
           else:
              result[0]['saldo_credit'] =  result[0]['saldo']
        
        fSaldo = result[0]['saldo']
        self.writeLog('getCashAcountBook result_main = ' + `result_main`,self.debugFinances)
        for v1 in result_main:
            fSaldo = fSaldo + v1['debit'] - v1['credit']
            v1['saldo'] = fSaldo
        
        result[0]['saldo_end'] = fSaldo 
        dicResults['cab'] = result_main
        dicResults['before'] = result
        return dicResults
    def xmlrpc_get_cab_doc_number1(self, dicUser):
        
        self.writeLog('new CAB-Number for doc1')
        ret = -1
        cSql = "select nextval(\'numerical_cash_account_book_doc_number1" + "_client_" + `dicUser['client']` + "\') "
        self.writeLog('CAB1-cSql = ' + cSql,self.debugFinances)
        #context.src.logging.writeLog('User = ' + `dicUser`)
        dicNumber = self.oDatabase.xmlrpc_executeNormalQuery(cSql,dicUser)
        self.writeLog('dicNumber = ' + `dicNumber`)
        if dicNumber:
           ret = dicNumber[0]['nextval']
        return ret
        
    def xmlrpc_getLastDate(self, dicUser):
        self.writeLog('start py_get_LastDate',self.debugFinances)
        sSql = "select to_char(now(),'" + dicUser['SQLDateFormat'] + "\') as last_date"
        result = self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
        if result and result not in ['NONE','ERROR']:
            ret = result[0]['last_date']
        cSql = "select to_char(accounting_date,'" +dicUser['SQLDateFormat'] + "\') as last_date from account_sentence "
        cSql = cSql + " where id = (select max(id) as max_id from account_sentence "
        self.writeLog('get0  cSql = ' + cSql,self.debugFinances)
        cSql = cSql + self.getWhere("",dicUser,1)
        cSql = cSql + ")"
        self.writeLog('get  cSql = ' + `cSql`,self.debugFinances)
        #context.src.logging.writeLog('User = ' + `dicUser`)
        liS = self.oDatabase.xmlrpc_executeNormalQuery(cSql,dicUser)
        
        self.writeLog('liS = ' + `liS`,self.debugFinances)
        if liS and liS not in ['NONE','ERROR']:
           ret = liS[0]['last_date']
        return ret
        
    def xmlrpc_get_AccountPlanNumber(self, id, dicUser):
        
        self.writeLog('get acctPlanNumber for ' + `id`)
        ret = 'NONE'
        sSql = "select name from account_plan where id = " + `id`  
        sSql = sSql + self.getWhere("",dicUser, 2)
        self.writeLog('get AcctPlan cSql = ' + sSql)
        #context.src.logging.writeLog('User = ' + `dicUser`)
        liAcct = self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
        
        self.writeLog('liAcct = ' + `liAcct`)
        if liAcct not in ['NONE','ERROR']:
           ret = liAcct[0]['name']
        return ret
    
    def xmlrpc_get_iAcct(self,iAcct, dicUser): 
        ret = 'NONE'
        liAcct = None
        
        if iAcct and iAcct not in ['NONE','ERROR']:
            cSql = "select designation from account_info where id = " + `iAcct` 
            #self.writeLog('acct SQL ' + `sAcct` + ', ' + `cSql`)
            cSql = cSql + self.getWhere("",dicUser,2)
            #self.writeLog('get Acct cSql = ' + cSql)
            #context.src.logging.writeLog('User = ' + `dicUser`)
            liAcct = self.oDatabase.xmlrpc_executeNormalQuery(cSql,dicUser)
        
            self.writeLog('liAcct = ' + `liAcct`)
        if liAcct and liAcct not in ['NONE','ERROR']:
           ret = liAcct[0]['designation']
        return ret
        
    def xmlrpc_get_acct(self,sAcct, dicUser): 
        self.writeLog('new acct Info for ' + `sAcct`)
        ret = 'NONE'
        liAcct = None
        
        if sAcct and sAcct not in ['NONE','ERROR']:
            cSql = "select designation from account_info where account_number = '" + sAcct + "'"
            self.writeLog('acct SQL ' + `sAcct` + ', ' + `cSql`)
            cSql = cSql + self.getWhere("",dicUser,2)
            self.writeLog('get Acct cSql = ' + cSql)
            #context.src.logging.writeLog('User = ' + `dicUser`)
            liAcct = self.oDatabase.xmlrpc_executeNormalQuery(cSql,dicUser)
        
            self.writeLog('liAcct = ' + `liAcct`)
        if liAcct and liAcct not in ['NONE','ERROR']:
           ret = liAcct[0]['designation']
        return ret
        
    def xmlrpc_getAcctID(self, sAcct, dicUser):
        ret = 0
        liAcct = None
        
        if sAcct and sAcct not in ['NONE','ERROR']:
            cSql = "select id from account_info where account_number = '" + sAcct + "'"
            #self.writeLog('acct SQL ' + `sAcct` + ', ' + `cSql`)
            cSql = cSql + self.getWhere("",dicUser,2)
            #self.writeLog('get Acct cSql = ' + cSql)
            #context.src.logging.writeLog('User = ' + `dicUser`)
            liAcct = self.oDatabase.xmlrpc_executeNormalQuery(cSql,dicUser)
        
            #self.writeLog('liAcct = ' + `liAcct`)
        if liAcct and liAcct not in ['NONE','ERROR']:
           ret = liAcct[0]['id']
        return ret
        
    def xmlrpc_get_cabShortKeyValues(self, s, dicUser):
        
        self.writeLog('start py_get_cabShortKeyValues')
        ret = -1
        cSql = "select max(id) as max_id from account_sentence where short_key = '" + s + "'"
        self.writeLog('get0  cSql = ' + cSql)
        cSql = cSql + self.getWhere("",dicUser,1)
        
        self.writeLog('get  cSql = ' + cSql)
        #context.src.logging.writeLog('User = ' + `dicUser`)
        liS = self.oDatabase.xmlrpc_executeNormalQuery(cSql,dicUser)
        
        self.writeLog('liS = ' + `liS`)
        if liS not in ['NONE','ERROR']:
           ret = liS[0]['max_id']
        return ret
        
    def xmlrpc_get_cab_designation(self, id, dicUser):
        ret = 'NONE'
        cSql = "select designation from account_sentence where id = " + `id` 
        sSql = sSql + self.getWhere("",dicUser,1)
        self.writeLog('get  cSql = ' + cSql)
        #context.src.logging.writeLog('User = ' + `dicUser`)
        liS = self.oDatabase.xmlrpc_executeNormalQuery(cSql,dicUser)
        
        self.writeLog('liS = ' + `liS`)
        if liS not in ['NONE','ERROR']:
           ret = liS[0]['designation']
        return ret
    def xmlrpc_get_cab_doc_number1(self, dicUser):
        self.writeLog('new CAB-Number for doc1')
        ret = -1
        cSql = "select nextval(\'numerical_cash_account_book_doc_number1" + "_client_" + `dicUser['client']` + "\') "
        self.writeLog('CAB1-cSql = ' + cSql)
        #context.src.logging.writeLog('User = ' + `dicUser`)
        dicNumber = self.oDatabase.xmlrpc_executeNormalQuery(cSql,dicUser)
        self.writeLog('dicNumber = ' + `dicNumber`)
        if dicNumber not in ['NONE','ERROR']:
           ret = dicNumber[0]['nextval']
        return ret
    def xmlrpc_updateAccountInfo(self, dicAcct, dicUser):
        self.writeLog('Search for account_Number ' )
        sSql = "select id from account_plan where name = '" + dicAcct['account_plan_number'][0] + "'"
        sSql = sSql + self.getWhere("",dicUser,2)
        
        result = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser)
        pn = 'NONE'
        if result not in ['NONE','ERROR'] and result[0].has_key('id'):
            dicAcct['account_plan_number'] = [result[0]['id'], 'int']
            pn = result[0]['id']
            print 'pn = ', pn

        if pn not in ['NONE','ERROR']:
            sSql = "select id from account_info where account_number = '" + dicAcct['account_number'][0] + "' and account_plan_number = " + `pn` 
            sSql = sSql + self.getWhere("",dicUser,2)
            self.writeLog('Search for account_Number sSql =  ' + `sSql` )
            result = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser)
            self.writeLog('result id by finances = ' + `result`)
            if result not in ['NONE','ERROR']:
            
                id = result[0]['id']
            else:
                id = -1
            dicAcct['client'] = [dicUser['client'],'int']
            result = self.oDatabase.xmlrpc_saveRecord('account_info',id, dicAcct, dicUser)
            self.writeLog('dicAcct = ' + `dicAcct`)
        
        return result
        
        
    def xmlrpc_getTotalAmount(self, order_id, dicUser):            
        total_amount = 0
        sSql = " select total_amount from list_of_invoices where order_number = " + `order_id` 
        sSql += self.getWhere(None,dicUser,2)
        result = self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
        if result and result not in ['NONE','ERROR']:
            total_amount = result[0]['total_amount']
            #total_amount = ("%." + `self.CURRENCY_ROUND` + "f") % round(total_amount,self.CURRENCY_ROUND)  
        return total_amount
        
    def xmlrpc_getTotalAmountString(self, OrderID, dicUser):
        retValue = '0'  

        total_sum = self.xmlrpc_getTotalAmount(OrderID,dicUser)
        try:
            #"%.2f"%y 
            total_sum = ("%." + `self.CURRENCY_ROUND` + "f") % round(total_sum,self.CURRENCY_ROUND)
            retValue = total_sum + ' ' + self.CURRENCY_SIGN
        except:
            pass
            
        return retValue  
     
     
    def xmlrpc_createTicketFromInpayment(self, inpayment_id, dicUser):
        ret = True
        
        return ret
        
        
    def xmlrpc_createTicketFromInvoice(self, invoice_id, dicUser):
        ret = True
        print 'new ticket'
        
        sSql = "select orb.id,  orb.discount,  orb.packing_cost,  orb.postage_cost,  orb.misc_cost,  "
        sSql += "inv.id"
        sSql += "from orderbook as orb, list_of_invoices as inv   "
        sSql += "where orb.id = inv.ordernumber "
        
        
        sSql += self.getWhere('', dicUser, 2, 'inv.')
        result = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser)
        
        
        
        return ret    
    
