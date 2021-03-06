# -*- coding: utf-8 -*-

##Copyright (C) [2003, 2004, 2005, 2006, 2007]  [Juergen Hamel, D-32584 Loehne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 


# Import smtplib for the actual sending function
#import smtplib, sys
import xmlrpclib
from twisted.web import xmlrpc
from twisted.internet.threads import deferToThread

### Here are the email pacakge modules we'll need
##from email.MIMEImage import MIMEImage
##from email.MIMEMultipart import MIMEMultipart
##from email.MIMEText import MIMEText
from basics import basics
from Email2 import Email 
import Database
import time

class cuonemail(xmlrpc.XMLRPC, basics):

    def __init__(self):
        
        
        basics.__init__(self)
        self.oDatabase = Database.Database()
        
    def xmlrpc_getCryptCombobox(self):
        
        return self.EMAILLOGINCRYPT
      
        
    def xmlrpc_sendTheEmail(self, dicValues, liAttachments,dicUser ):
        ok = ''
            
        if dicValues.has_key('To'):
            if dicValues['To'][0:11] == 'Newsletter:':
                cNL = dicValues['To'][12 :]
                print cNL
                liNL = cNL.split(',')
                for oneNL in liNL:
                    oneNL = oneNL.strip()
                    if oneNL:
                        result = self.getNewsletterEmail(oneNL,dicUser)
                        print 'result = ', result 
                        for sm in result:
                            print 'sm = ',  sm
                            if sm.has_key('email'):
                                #print 'sm[email] = ',  sm['email']
                                dicValues['To'] = sm['email']
                                dicValues['sm'] = sm
                                ok += self.sendEmail(dicValues, liAttachments,dicUser) + '\n'
                            
                       
                        
            else:
                #ok += deferToThread(self.sendEmail, dicValues, liAttachments,dicUser) +'\n'
                ok += self.sendEmail(dicValues, liAttachments,dicUser) +'\n'
            
        return ok
                
    def sendEmail(self, dicValues, liAttachments,dicUser ):
        cuonmail = Email(smtp_server = "localhost")
        print ' send mail'
        if liAttachments:
            cuonmail.attachments = liAttachments
        else:
            cuonmail.attachments = []
            

        ok = ''
        try:
            dicValues = self.replaceValues(dicValues)
              
            if dicUser.has_key('Email'):
                dicEmail = dicUser['Email']
##                self.Email['From']='MyAddress@mail_anywhere.com'
##                self.Email['Host']='mail_anywhere.com'
##                self.Email['Port']='25'
##                self.Email['LoginUser']='login'
##                self.Email['Password']='secret'
##                self.Email['Signatur']='NONE'

                print '1'
                if dicEmail['LoginUser'] != 'login':
                    self.EMAILUSER = dicEmail['LoginUser']
                print '2'   
                if dicEmail['Password'] != 'secret':
                    self.EMAILPASSWORD = dicEmail['Password']
                print '3'    
                if dicEmail['Host'] != 'mail_anywhere.com':
                    self.EMAILSERVER = dicEmail['Host']
                      
            
            if dicValues.has_key('From'):
                cuonmail.from_address = dicValues['From']
            print '4'
            if dicValues.has_key('To'):
                print 'send mail to ',  dicValues['To']
                cuonmail.recipients.add(dicValues['To']) 
                
            print '6'   
            if dicValues.has_key('Subject'):
                cuonmail.subject = dicValues['Subject']
            print '7'
            if dicValues.has_key('Body'):
                #print 'dicValues = ',  dicValues.keys()
                cuonmail.message = dicValues['Body']  
            
            print '8'
            cuonmail.smtp_server = self.EMAILSERVER
            print '9'
            cuonmail.smtp_user = self.EMAILUSER
            print '10'
            cuonmail.smtp_password = self.EMAILPASSWORD
            print '11'
            cuonmail.smtp_crypt = dicEmail['Crypt']
            print '12'
            
        except Exception, params:
            print 'Error in Email'
            print Exception, params
        
        s = None
        try:
            s = cuonmail.send()
        except Exception, params:
            print Exception
            print ' -----------------'
            print  params
            s = params
            
        try:
            print 'return Value form Email2 ', s
            print 'Status = ', cuonmail.statusdict
            print 's = ', s
            if not s:
                s = 'Email '
                try:
                    s += 'send : ' +  dicValues['To'] + ', ' + `dicValues['Subject']`
                except:
                    s += ' wrong To or subject'
            else:
                s = `s`
            ok = s
            if  dicValues['sm'].has_key('addressid'):
                ok += ';p='
            else:
                ok += ';a='
            ok += `dicValues['sm']['id']`  
            
            f = open('/var/log/cuonmail.log','a')
            f.write(time.ctime(time.time() ))
            f.write('     ')
            f.write(ok)
            f.write('\n')
            f.close()
        except:
            pass
        
        return ok
        
    def getNewsletterEmail(self, NewsletterShortcut, dicUser):
        print NewsletterShortcut
        sSql = "select * from address where newsletter ~'.*" + NewsletterShortcut +".*'"
        sSql += self.getWhere("",dicUser,2)
        print sSql
        result = self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
        if result in ['NONE','ERROR']:
            result = []
        #print 'result 1 ', result
        sSql = "select * from partner where newsletter ~'.*" + NewsletterShortcut +".*'"
        sSql += self.getWhere("",dicUser,2)
        print sSql
        result2 = self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
        print 'result2 = ', result2
        if result2 not in ['NONE','ERROR']:
            for res in result2:
                result.append(res)
        print 'result3', result
        return result
        
    def replaceValues(self, dicValues) :
        try:
            dicVars = dicValues['sm']
            for v in ['Body','Subject']:
                s = dicValues[v]
                for key in dicVars.keys():
                    try:
                        try:
                            if self.checkType(dicVars[key], 'unicode'): 
                                
                                dicVars[key] = dicVars[key].encode('utf-8')
                        except Exception, params:
                            print Exception, params
                            
                        #print 'try to replace this ', key,  dicVars[key]
                        if dicVars[key] == 'NONE' or dicVars[key] ==None:
                            s = s.replace('##'+ key + ';;','')
                        elif self.checkType(dicVars[key], 'string') :
                            
                            #print dicVars[key],  dicVars[key].decode('utf-8'),  dicVars[key].decode('utf-8').decode('utf-8')
                            #print dicVars[key].decode('latin-1'),  dicVars[key].decode('utf-8').encode('latin-1')
                            s = s.replace('##'+ key + ';;',dicVars[key])
                        
                        else:
                            s = s.replace('##'+ key + ';;',`dicVars[key]` )
                    except Exception,  params:
                        print Exception, params
                        s = s = s.replace('##'+ '' + ';;','')
                dicValues[v] = s 
        except Exception, params:
            print Exception, params
        
        
        
        return dicValues
        
##        Email(
##557           from_address = "server@gp-server.gp",
##558           smtp_server = "gp-server.gp",
##559           to_address = "gerold@gp-server.gp",
##560           subject = "Einfaches Beispiel (öäüß)",
##561           message = "Das ist der Nachrichtentext mit Umlauten (öäüß)"
##562       ).send()


        
##        COMMASPACE = ', '
## 
##        # Create the container (outer) email message.
##        self.msg = MIMEMultipart('related')
##        
##        # Guarantees the message ends in a newline
##        self.msg.epilogue = ''
##
##        self.mFiles = []
##        
##        
##
##    def setSubject(self, s):
##        if s:
##            self.msg['Subject'] = s
##        else:
##            self.msg['Subject'] = 'No Subject'
##            
##
##    def setFrom(self,s):
##        self.msg['From'] = s
##        
##
##    def setTo(self,s):
##        self.msg['To'] = s
##        
## 
##    def addAttachments(self, *maFiles):
##        for j in range(0, len(maFiles)):
##            self.mFiles.append( maFiles[j])
##
##    def setBody(self,body=None ):
##        if body:
##            self.msg.preamble =  body 
##        else:
##            self.msg.preamble = 'No Text' 
##            
##            
##                                                                                
##    def xmlrpc_sendTheEmail(self, dicValues, liAttachments,dicUser ):
##        ok = False
##        
##        if dicValues:
##            
##            try:
##                if dicValues.has_key('Username'):
##                    self.EMAILUSER = dicValues['Username']
##                if dicValues.has_key('Password'):
##                    self.EMAILPASSWORD = dicValues['Password']
##                if dicValues.has_key('To'):
##                    self.setTo(dicValues['To'])
####                if dicValues.has_key('From'):
####                    self.setFrom(dicValues['From'])
##                if dicValues.has_key('Subject'):
##                    self.setSubject(dicValues['Subject'])
##                if dicValues.has_key('Body'):
##                    self.setBody(dicValues['Body'])
##            except:
##                pass
##                    
##        # Assume we know that the txt files are all in ascii format
##        if liAttachments:
##            for file in self.mFiles:
##                # Open the files in binary mode.  Let the MIMEText class automatically
##                # guess the specific image type.
##                fp = open(file, 'rb')
##                txt = MIMEText(fp.read())
##                fp.close()
##                self.msg.attach(txt)
##                 # Send the email via our own SMTP server.
##            try:
##                
##                print ' start send email'
##         replaceValues(dicValues)       server = smtplib.SMTP(self.EMAILSERVER)
##                #print 'Email-Server = ', server
##                #print self.EMAILUSER, self.EMAILPASSWORD
##                
##                server.login(self.EMAILUSER, self.EMAILPASSWORD)
##                #print 'login'
##                #print self.msg.as_string()
##                
##                server.sendmail(dicValues['From'], dicValues['To'], 'To: ' + dicValues['To'] + '\nSubject: cuon 7 \n\n ' + dicValues['Body'] + '\n')
##                print 'send'
##                server.quit()
##                ok = True
##            except Exception, param:
##                print Exception
##                print param
##            
##        # Normal Email without Attachment    
##        else:
##                # Send the email via our own SMTP server.
##            try:
##                
##                print ' start send email'
##                server = smtplib.SMTP(self.EMAILSERVER)
##                #print 'Email-Server = ', server
##                #print self.EMAILUSER, self.EMAILPASSWORD
##                msgText = MIMEText(dicValues['Body'])
##                server.login(self.EMAILUSER, self.EMAILPASSWORD)
##                #print 'login'
##                #print self.msg.as_string()
##                print dicValues
##                s = server.sendmail(dicValues['From'], dicValues['To'], 'To: ' + dicValues['To'] + '\nSubject: ' + dicValues['Subject'] +' \n\n ' + msgText + '\n')
##                print 'send', s
##                server.quit()
##                ok = True
##            except Exception, param:
##                print Exception
##                print param
##            
##        return ok
##            
##            
##        
