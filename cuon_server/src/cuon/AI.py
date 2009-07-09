# -*- coding: utf-8 -*-

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
 
from basics import basics
import Database

class AI(xmlrpc.XMLRPC, basics):
    def __init__(self):
        basics.__init__(self)
        self.oDatabase = Database.Database()
        print "AI now starting 1"


    def sendQuestion(self, question):
        return self.ai_server.AI.getAnswer(question)
   
    def xmlrpc_getAI(self, question, dicUser):
        import string
        answer = 'Something wrong,  perhaps your Session at the C.U.O.N. Server is expired. Try to login again.'
        self.writeLog('py_getAI question = ' + `question`,1)
        goDecode = False
        sUser = self.oDatabase.checkUser(dicUser['Name'], dicUser['SessionID'], dicUser['userType'])
        if sUser:
            #answer = context.ex_getAI(question)
            question = question.replace('.*', 'dot_star')
            answer = self.sendQuestion(question.encode('utf-7'))
            answer = answer.replace('dot_star', '.*')
            
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
                
            
        self.writeLog( "answer by AI " + answer)
        
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
              sSql = "select id, number, designation from articles "
              sSql = sSql + "where number ~* \'.*" + liAnswer[4] + '.*\''
              sSql = sSql + " or designation ~* \'.*" + liAnswer[4] + '.*\''
              sSql = sSql + self.getWhere('',dicUser,2)
              
        
              self.writeLog('article_ai1' + `sSql`)
        
              result = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser)
              if resultnot in ['NONE','ERROR']:
                 answer = ''
                 for r1 in result:
                    answer = answer + "%s \t\t %s \n" %(`r1['id']` + ' -- ' + r1['number'],r1['designation'] )
              else:
                 answer = self.sendQuestion('NO ARTICLES FOUND')
        return answer      

    def addresses(self, liAnswer, dicUser):
    
        answer = 'No Data Found'
        if liAnswer[2] == 'SEARCH':
           if liAnswer[3] == 'ALL':
              liAnswer, Firstname = self.checkAnswer(liAnswer,'Address') 
              sSql = "select id, lastname, lastname2, firstname, street, zip, city from address "
              sSql = sSql +  "where ( (lastname ~* \'.*" + liAnswer[4] + '.*\''
              sSql = sSql + " or lastname2 ~* \'.*" + liAnswer[4] + '.*\') '
              if Firstname:
                  
                  sSql = sSql + " and firstname ~* \'.*" + liAnswer[5] + '.*\''
              else:
                  sSql = sSql + " or firstname ~* \'.*" + liAnswer[4] + '.*\''
                  
              sSql +=  ') ' +  self.getWhere('',dicUser,2)
              
              self.writeLog('address_ai1' + `sSql`)
        
              result = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser)
              if result not in ['NONE','ERROR']:
                 answer = ''
                 for r1 in result:
                    answer = answer + "%s\n%s\n%s\n%s\n%s %s\n------------------------------------\n" %(`r1['id']` + ' -- ' + r1['lastname'],r1['lastname2'],r1['firstname'],r1['street'],r1['zip'],r1['city'] )
              else:
                 answer = self.sendQuestion('NO ADDRESS FOUND')
        return answer
        
    def addresses_phone(self, liAnswer, dicUser):
            
        import string
        ok = False
        answer = ''
        print 'aphone1',  `liAnswer`
        self.writeLog('address_phone_ai1 lianswer[4] = ' + `liAnswer[4]`,1)
        #liAnswer[4] = liAnswer[4].decode('latin-1').decode('utf-7')
        self.writeLog('address_phone_ai1 lianswer[4](2) = ' + `liAnswer[4]`)
        if liAnswer[2] == 'SEARCH':
             print 'aphone2'
             if liAnswer[3] == 'ALL':
              print 'aphone3'
              liAnswer, Firstname = self.checkAnswer(liAnswer,'Address')
              print 'aphone4'
                
               
              sSql = "select id, lastname, lastname2, firstname, phone from address "
              sSql = sSql +  "where (lastname ~* \'.*" + liAnswer[4] + '.*\''
              sSql = sSql + " or lastname2 ~* \'.*" + liAnswer[4] + '.*\' )'
              #print 'dicUser1', `dicUser`
              #print 'sSql1',  sSql
              #print 'Firstname',  Firstname
              
              if Firstname:
                  
                  sSql = sSql + " and firstname ~* \'.*" + liAnswer[5] + '.*\''
              else:
                  sSql = sSql + " or firstname ~* \'.*" + liAnswer[4] + '.*\''
              #print 'sSql2',  sSql
              sSql = sSql + self.getWhere('',dicUser,2)
              #print 'sSql3',  sSql
              self.writeLog('address_phone_ai1 SQL ' + `sSql`)
              #print `dicUser`
              #print sSql
              print"o-1"
              result = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser)
              print "o1"
              if result not in ['NONE','ERROR']:
                 ok = True
                 print "o2"
                 for r1 in result:
                     try:
                        answer = answer + "%s\n%s\n%s\n%s\n------------------------------------\n" %(`r1['id']` + ' -- ' +r1['lastname'],r1['lastname2'],r1['firstname'],r1['phone'] )
                     except Exception,  params:
                         print Exception,  params
                     print "o3"
              sSql = "select ad.id as ad_id, ad.lastname as ad_lastname, ad.city as ad_city, pa.lastname as pa_lastname, pa.lastname2 as pa_lastname2, pa.firstname as pa_firstname, pa.phone1 as pa_phone1, pa.phone2 as pa_phone2 from partner as pa, address as ad "
              sSql = sSql +  "where ((pa.lastname ~* \'.*" + liAnswer[4] + '.*\''
              sSql = sSql + " or pa.lastname2 ~* \'.*" + liAnswer[4] + '.*\')'
              if Firstname:
                sSql = sSql + " and pa.firstname ~* \'.*" + liAnswer[5] + '.*\''
              else:
                sSql = sSql + " or pa.firstname ~* \'.*" + liAnswer[4] + '.*\''
                
              sSql += ' )and pa.addressid = ad.id  '
                  
              sSql = sSql + self.getWhere('',dicUser,2, 'pa.')
              self.writeLog('address_phone_ai1_2 ' + `sSql`)
              print "r-1"  
              result = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser)
              print "r0"
              if result not in ['NONE','ERROR']:
                 ok = True
                 print "rstart"
                 for r1 in result:
                    print "r1"
                    try:
                        answer = answer + "%s\n%s\n%s\n%s\n%s\n%s\n------------------------------------\n" %(`r1['ad_id']`+ ' -- ' +r1['ad_lastname'] + ', ' +r1['ad_city'], r1['pa_lastname'],r1['pa_lastname2'],r1['pa_firstname'],r1['pa_phone1'], r1['pa_phone2'] )
                    except Exception,  param:
                        print Exception,  param
                        answer = "error in sql decoding"

                    print "r2"
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
                answer = "INSERT DATA SUCCESSFUL AT ID " + `result[0]['last_value']`
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
        
        

      
