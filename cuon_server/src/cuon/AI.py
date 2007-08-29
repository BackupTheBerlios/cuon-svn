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
        print 'py_getAI answer = ' + `answer`
        
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
                    
                elif liAnswer[1] == 'MISC':
                    print 'MISC'
                    if liAnswer[2] == 'DATA':
                        print 'DATA'
                        if liAnswer[3] == 'INSERT':
                            print 'INSERT'
                            goDecode = False
                            answer = self.insert_data(liAnswer, dicUser, 'Misc_Data')
                    
                    
            if goDecode:
                answer = answer.encode('utf-7')
            
        except:
            self.out('No correct answer from AI = ' + `answer`)
            
        
        print "answer by AI ", answer
        
        return answer
        
    def checkAnswer(self,liAnswer,key):
        bKey = False

        if key == 'Address':
            liSearchkeys = liAnswer[4].split(',')
            if len(liSearchkeys) == 1:
                liSearchkeys = liAnswer[4].split()
            else:
                liSearchkeys[0], liSearchkeys[1] =  liSearchkeys[1], liSearchkeys[0]
          
            # lastname first
            liSearchkeys.reverse()
            if len(liSearchkeys) > 1:
                liAnswer[4] = liSearchkeys[0].strip()
                liAnswer.append('')
                for i in liSearchkeys[1:]:
                    liAnswer[5] +=  i.strip()
                    bKey = True
        elif key == 'Misc_Data':
            liSearchkeys = liAnswer[4].split(';')
            if len(liSearchkeys) > 0:
                
                bKey = True
            liAnswer[4] = liSearchkeys
                
        return liAnswer,bKey
        
        
        
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
              if resultnot in ['NONE','ERROR']:
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
              liAnswer, Firstname = self.checkAnswer(liAnswer,'Address') 
              sSql = "select lastname, lastname2, firstname, street, zip, city from address "
              sSql = sSql +  "where ( lastname ~* \'.*" + liAnswer[4] + '.*\''
              sSql = sSql + " or lastname2 ~* \'.*" + liAnswer[4] + '.*\') '
              if Firstname:
                  
                  sSql = sSql + " and firstname ~* \'.*" + liAnswer[5] + '.*\''
              else:
                  sSql = sSql + " or firstname ~* \'.*" + liAnswer[4] + '.*\''
                  
              sSql = sSql + self.getWhere('',dicUser,2)
              
              self.writeLog('address_ai1' + `sSql`)
        
              result = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser)
              if resultnot in ['NONE','ERROR']:
                 answer = ''
                 for r1 in result:
                    answer = answer + "%s\n%s\n%s\n%s\n%s %s\n\n" %(r1['lastname'],r1['lastname2'],r1['firstname'],r1['street'],r1['zip'],r1['city'] )
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
              liAnswer, Firstname = self.checkAnswer(liAnswer,'Address')
              
                
               
              sSql = "select lastname, lastname2, firstname, phone from address "
              sSql = sSql +  "where (lastname ~* \'.*" + liAnswer[4] + '.*\''
              sSql = sSql + " or lastname2 ~* \'.*" + liAnswer[4] + '.*\' )'
              if Firstname:
                  
                  sSql = sSql + " and firstname ~* \'.*" + liAnswer[5] + '.*\''
              else:
                  sSql = sSql + " or firstname ~* \'.*" + liAnswer[4] + '.*\''
                  
              sSql = sSql + self.getWhere('',dicUser,2)
              
              self.writeLog('address_phone_ai1 ' + `sSql`)
        
              result = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser)
              if result not in ['NONE','ERROR']:
                 ok = True
        
                 for r1 in result:
                    answer = answer + "%s\n%s\n%s\n%s\n\n" %(r1['lastname'],r1['lastname2'],r1['firstname'],r1['phone'] )
        
              sSql = "select lastname, lastname2, firstname, phone1, phone2 from partner "
              sSql = sSql +  "where (lastname ~* \'.*" + liAnswer[4] + '.*\''
              sSql = sSql + " or lastname2 ~* \'.*" + liAnswer[4] + '.*\')'
              if Firstname:
                sSql = sSql + " and firstname ~* \'.*" + liAnswer[5] + '.*\''
              else:
                sSql = sSql + " or firstname ~* \'.*" + liAnswer[4] + '.*\''
                  
              sSql = sSql + self.getWhere('',dicUser,2)
              self.writeLog('address_phone_ai1_2 ' + `sSql`)
        
              result = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser)
              if result not in ['NONE','ERROR']:
                 ok = True
                 
                 for r1 in result:
                    answer = answer + "%s\n%s\n%s\n%s\n%s\n\n" %(r1['lastname'],r1['lastname2'],r1['firstname'],r1['phone1'], r1['phone2'] )
        if not ok:
                 answer = self.sendQuestion('NO PHONE FOUND')
        return answer


    def insert_data(self, liAnswer, dicUser, cKey):
        print 'insert Data reached ', liAnswer
        answer = 'INSERT DATA FAILED'
        dicValues = {}
        liAnswer, bKey = self.checkAnswer(liAnswer,'Misc_Data') 
        print liAnswer, bKey
        print cKey
        
        if bKey:
            if cKey == 'Misc_Data':    
                
                for i in liAnswer[4]:
                    liData = i.split(':')
                    print 'liData = ', liData
                    dicValues[liData[0]] = [liData[1], self.getTypeOfData(liData[0])]
                
            
            print dicValues
            result = self.oDatabase.xmlrpc_saveRecord('misc_data',-1,dicValues,dicUser )
            print 'result by insertData', result
            if  result not in ['NONE','ERROR']:
                answer = "INSERT DATA SUCCESSFULL AT ID " + `result[0]['last_value']`
                print answer
                answer = self.sendQuestion(answer.encode('utf-7'))
        return answer

    def getTypeOfData(self, cData):
        cRet = 'string'
        if cData[0] == 'i':
            cRet = 'int'
        elif cData[0] == 'd':
            cRet = 'date'
        elif cData[0] == 'f':
            cRet = 'float'
        return cRet
        
        

      
