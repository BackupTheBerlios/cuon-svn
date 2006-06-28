import time
from datetime import datetime
import random
import xmlrpclib
from twisted.web import xmlrpc
 
from basics import basics
import Database

class AI(xmlrpc.XMLRPC, basics):
    def __init__(self):
        basics.__init__(self)
        self.oDatabase = Database.Database()
        


    def sendQuestion(self, question):
        return self.ai_server.AI.getAnswer(question)
   
    def xmlrpc_getAI(self, question, dicUser):
        import string
        self.writeLog('py_getAI question = ' + `question`,1)
        goDecode = False
        #answer = context.ex_getAI(question)
        answer = self.sendQuestion(question.encode('utf-7'))
        
        self.writeLog('py_getAI answer = ' + `answer`,1)
##        try:
##           answer = answer.decode('utf-7').encode('utf-8')
##        except:
##           pass
##        
        answer = answer.strip()
        liAnswer = answer.split()
        try:
            assert liAnswer
            if liAnswer[0] == "ENDPROGRAM":
               answer = sendQuestion('ENDPROGRAM')
            elif liAnswer[0] == 'CUON':
               goDecode = True
               if liAnswer[1] == 'ARTICLES':
                  answer = self.articles(liAnswer, dicUser)
               elif liAnswer[1] == 'ADDRESS':
                  answer = self.addresses(liAnswer, dicUser)
               elif liAnswer[1] == 'PHONE':
                  answer = self.addresses_phone(liAnswer, dicUser)
            
            if goDecode:
               answer = answer.encode('utf-7')
            
        except:
            self.out('No correct answer from AI = ' + `answer`)
            
        
        #return printed
        
        return answer

    def articles(self, liAnswer, dicUser):
        import string
        
        answer = 'No Data Found'
        if liAnswer[2] == 'SEARCH':
           if liAnswer[3] == 'ALL':
              sSql = "select number, designation from articles "
              sSql = sSql + "where number ~* \'.*" + liAnswer[4] + '.*\''
              sSql = sSql + " or designation ~* \'.*" + liAnswer[4] + '.*\''
              sSql = sSql + self.getWhere('',dicUser,2)
              
        
              self.writeLog('article_ai1' + `sSql`)
        
              result = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser)
              if result!= 'NONE':
                 answer = ''
                 for r1 in result:
                    answer = answer + "%s \t\t %s \n" %(r1['number'],r1['designation'] )
              else:
                 answer = self.sendQuestion('NO ARTICLES FOUND')
        return answer      

    def addresses(self, liAnswer, dicUser):
    
        answer = 'No Data Found'
        if liAnswer[2] == 'SEARCH':
           if liAnswer[3] == 'ALL':
              sSql = "select lastname, lastname2, firstname, street, zip, city from address "
              sSql = sSql +  "where lastname ~* \'.*" + liAnswer[4] + '.*\''
              sSql = sSql + " or lastname2 ~* \'.*" + liAnswer[4] + '.*\''
              sSql = sSql + self.getWhere('',dicUser,2)
              
              self.writeLog('address_ai1' + `sSql`)
        
              result = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser)
              if result!= 'NONE':
                 answer = ''
                 for r1 in result:
                    answer = answer + "%s\n%s\n%s\n%s\n%s %s\n" %(r1['lastname'],r1['lastname2'],r1['firstname'],r1['street'],r1['zip'],r1['city'] )
              else:
                 answer = answer = self.sendQuestion('NO ADDRESS FOUND')
        return answer
        
    def addresses_phone(self, liAnswer, dicUser):
            
        import string
        ok = False
        answer = ''
        self.writeLog('address_phone_ai1 lianswer[4] = ' + `liAnswer[4]`,1)
        #liAnswer[4] = liAnswer[4].decode('latin-1').decode('utf-7')
        self.writeLog('address_phone_ai1 lianswer[4](2) = ' + `liAnswer[4]`)
        if liAnswer[2] == 'SEARCH':
           if liAnswer[3] == 'ALL':
              sSql = "select lastname, lastname2, firstname, phone from address "
              sSql = sSql +  "where (lastname ~* \'.*" + liAnswer[4] + '.*\''
              sSql = sSql + " or lastname2 ~* \'.*" + liAnswer[4] + '.*\''
              sSql = sSql + " or firstname ~* \'.*" + liAnswer[4] + '.*\')'
              sSql = sSql + self.getWhere('',dicUser,2)
              
              self.writeLog('address_phone_ai1 ' + `sSql`)
        
              result = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser)
              if result != 'NONE':
                 ok = True
        
                 for r1 in result:
                    answer = answer + "%s\n%s\n%s\n%s\n\n" %(r1['lastname'],r1['lastname2'],r1['firstname'],r1['phone'] )
        
              sSql = "select lastname, lastname2, firstname, phone1, phone2 from partner "
              sSql = sSql +  "where (lastname ~* \'.*" + liAnswer[4] + '.*\''
              sSql = sSql + " or lastname2 ~* \'.*" + liAnswer[4] + '.*\''
              sSql = sSql + " or firstname ~* \'.*" + liAnswer[4] + '.*\')'
              sSql = sSql + self.getWhere('',dicUser,2)
              self.writeLog('address_phone_ai1_2 ' + `sSql`)
        
              result = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser)
              if result != 'NONE':
                 ok = True
                 
                 for r1 in result:
                    answer = answer + "%s\n%s\n%s\n%s\n%s\n\n" %(r1['lastname'],r1['lastname2'],r1['firstname'],r1['phone1'], r1['phone2'] )
        if not ok:
                 answer = self.sendQuestion('NO PHONE FOUND')
        return answer
