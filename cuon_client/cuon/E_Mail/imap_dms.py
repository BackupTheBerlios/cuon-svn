# -*- coding: utf-8 -*-
##Copyright (C) [2009]  [Juergen Hamel, D-32584 Loehne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 

import imaplib, string, email, getpass, sys, time
import os,  time


from email import message_from_string
from email.header import decode_header
from email import parser
import cuon.DMS.dms
import cuon.DMS.SingleDMS
import cuon.DMS.documentTools
import cuon.Misc.misc
import cuon.XMLRPC.xmlrpc
from cuon.TypeDefs.constants import constants
from cuon.Databases.dumps import dumps
from threading import Thread

class imap_dms(Thread,  constants,  dumps):
    def __init__(self, allTables,   dicUser):
        Thread.__init__(self)
        constants.__init__(self)
        dumps.__init__(self)
        
        self.dicUser = dicUser
        self.imap_server = dicUser['Email']['ImapHost']
        self.imap_port = dicUser['Email']['ImapPort']
        # imap username (if blank, you will be prompted at startup)
        self.imap_user = dicUser['Email']['ImapLoginUser']
        
        # imap password (if blank, you will be prompted at startup)
        self.imap_password = dicUser['Email']['ImapPassword']
        
        #seconds to sleep between each check
        self.sleep_time = 60
        
        # if 1 use SSL, otherwise don't
        self.use_ssl=dicUser['Email']['ImapSSL']
        self.use_crypt=dicUser['Email']['ImapCrypt']
        # number of seconds to display message
        self.display_timeout=5
        
        # if 1, print some debug info; otherwise don't
        self.debug=0
        self.rpc = cuon.XMLRPC.xmlrpc.myXmlRpc()
        # font to display message in 
        self.display_font='-adobe-helvetica-*-*-normal-*-34-*-*-*-*-*-*-*'
        
        # color of message
        self.isplay_color='black'
        
        self.singleDMS = cuon.DMS.SingleDMS.SingleDMS(allTables)
        self.documentTools = cuon.DMS.documentTools.documentTools()
        self.misc = cuon.Misc.misc.misc()
    
    def decodeMailHeader(self, sSubject1):
        noDecode = False
        sSubject = ''
        for iSub in sSubject1:
            try:
                if iSub[1]:
                    sSubject += iSub[0].decode(iSub[1]) + ' '
                else:
                    sSubject += iSub[0]+ ' '
                                               
            except:
                noDecode = True
        if noDecode:
            sSubject = sSubject1
        return sSubject
        
    
    def run(self):
        M = None
        ok = False
        print 'check imap =',  time.asctime( time.localtime(time.time()) ),  self.dicUser['Email']['check_imap'] 
        if self.dicUser['Email'].has_key('check_imap') and self.dicUser['Email']['check_imap'] == True:
            print 'Imap check is True'
            try:
                
                if self.use_ssl:
                    if  self.imap_port == 0:
                        M = imaplib.IMAP4_SSL(self.imap_server)
                    else: 
                        M = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
                        
                else:
                    if  self.imap_port == 0:
                        M = imaplib.IMAP4(self.imap_server)
                    else:
                        M = imaplib.IMAP4(self.imap_server,  self.imap_port)

                    
            except Exception, e:
                #print sys.exc_info()[0]
                print 'IMAP Server error: ', Exception, e
                M = None
                
                    
            
        try:
            if M:
                if  self.use_crypt < 1 or self.use_crypt == 2 or self.use_crypt == 3:
                    try:
                        res = M.login(self.imap_user, self.imap_password)
                    except Exception, e:
                        print 'IMAP login error 0: ', Exception, e   
                elif self.use_crypt == 4:
                    try:
                        res = M.login_cram_md5(self.imap_user, self.imap_password)
                    except Exception, e:
                        print 'IMAP login error 1: ', Exception, e   
                elif self.use_crypt == 1:   
                    try:
                        res = M.login(self.imap_user, self.imap_password)
                    except:
                        try:
                            res = M.login_cram_md5(self.imap_user, self.imap_password)
                        except Exception, e:
                            print 'IMAP login error 2: ', Exception, e   
                else:
                    try:
                        res = M.login(self.imap_user, self.imap_password)
                    except Exception, e:
                            print 'IMAP login error 2: ', Exception, e 
                    
                # Get inbox status
                #mboxes = M.list()
                #imap.SelectMailbox("Inbox")
                #print mboxes
                #status = M.status('INBOX.AUTOMATIC_CUON', '(UNDELETED)')
    
                # Parse status string
                # ie. ('OK', ['"INBOX" (UNSEEN 0)'])
                #print status
                
                #print 'msgCount = ',  status[1][0].split()[2].split(')')[0]
    
                M.select('INBOX.AUTOMATIC_CUON')
                r, data = M.search(None, '(ALL)')
                print r,  data
                if r == 'OK':
                    for singleMail in data:
                        #print 'singlemail = ',  singleMail
                        liNumbers = singleMail.split(' ')
                        for oneNumber in liNumbers:
                            oneNumber = oneNumber.strip()
                            print 'oneNumber = ',  oneNumber
                            mail = M.fetch(int(oneNumber),  '(RFC822)')
                            #print 'mail found',  mail
                            message1 = mail[1][0][1]

                            message = message_from_string(message1)
                            #message = parser.Parser().parsestr(message1)
                           
                            sFrom = self.decodeMailHeader( email.header.decode_header(message['From']))
                            print 'From = ',  sFrom
                            
                            sTo = self.decodeMailHeader( email.header.decode_header(message['To']))
                            print 'sTo = ',  sTo
                            
                            sDate = self.decodeMailHeader( email.header.decode_header(message['Date']))
                            print 'sDate = ',  sDate
                            
#                            sTo = self.decodeMailHeader( email.header.decode_header(message['To']))
#                            print 'sTo = ',  sTo
# 
 
                            sSubject = self.decodeMailHeader( email.header.decode_header(message['Subject']))
                            print 'sSubject = ',  sSubject
                            #sSubject = self.decodeMailHeader(sSubject1)
                                    
                            print 'sSubject = ',  sSubject
                            print 'keys : ',  message.keys()
                            sMessageID = message['Message-ID'].strip('<').strip('>')
                            print sMessageID
                                    # check if an address has this email address
                            liAddressID = self.rpc.callRP('Address.getAddressEmailID','address',  sFrom.split(','),self.dicUser)
                            if liAddressID == [0]:
                                liAddressID = []
                            liAddressID += self.rpc.callRP('Address.getAddressEmailID','address',sTo.split(','),self.dicUser)
                            if liAddressID == [0]:
                                liAddressID = []
                                
                            liPartnerID = self.rpc.callRP('Address.getAddressEmailID','partner',sFrom.split(','),self.dicUser)
                            if liPartnerID == [0]:
                                liPartnerID = []
                            liPartnerID += self.rpc.callRP('Address.getAddressEmailID','partner',  sTo.split(','),self.dicUser)
                            if liPartnerID == [0]:
                                liPartnerID = []
                            print 'Address ID`s: ',  liAddressID
                            iSearch = sSubject.find('AUTOMATIC_CUON ADDRESS ID:')
                            if iSearch != -1:
                                iSearch += 26
                                liStr = sSubject[iSearch:sSubject.find(';') -1].split(',')
                                print 'liStr = ',  liStr
                                for iID in liStr:
                                    try:
                                        nID = int(iID.strip())
                                        print 'nID = ',  nID
                                        liAddressID.append(nID)
                                    except:
                                        pass
                                sSubject = sSubject[sSubject.find(';')+1:]      
                                print 'new sSubject = ',  sSubject
                            iSearch = sSubject.find('AUTOMATIC_CUON PARTNER ID:')
                            if iSearch != -1:
                                iSearch += 26
                                liStr = sSubject[iSearch:sSubject.find(';')].split(',')
                                for iID in liStr:
                                    try:
                                        nID = int(iID.strip())
                                        liPartnerID.append(nID)       
                                    except:
                                        pass
                                sSubject = sSubject[sSubject.find(';')+1:]        
                            for part in message.walk():
                                print 'email part = ',  part.get_content_type() 
                            # each part is a either non-multipart, or another multipart message
                            # that contains further parts... Message is organized like a tree
                                sType = None
                                sExtension = None
                                if part.get_content_type() == 'multipart/mixed':
                                    print 'mixed'
                                    # solve later, try to find all 
                                elif part.get_content_type() == 'application/octet-stream':
                                    sType = 'Stream'    
                                else:
                                    try:
                                        sType = self.MimeType[part.get_content_type()][0]
                                    except:
                                        print 'error to find part type = ',  part.get_content_type()
                                        sType = None
                                print 'sType = ',  sType        
                                if sType:
                                    self.save(part,sType,  liAddressID,  liPartnerID,sSubject,   sFrom,  sTo ,  sDate )
                                    if sType and (liAddressID or liPartnerID):
                                        success = M.store(oneNumber, '+FLAGS', '\\Deleted')
                                        print 'Success 1 : ',  success
                success = M.expunge()
                print 'success 20 = ',  success   
                        
        except Exception, e:
            #print sys.exc_info()
            print 'IMAP read error: ', Exception,  e
            success = M.expunge()
            print 'success 30 = ',  success
    
        try:
            if M:
                M.logout()
        except e,  params: 
            print e,  params
        
        
        return ok
            
    def save(self, part , sType,  liAddressID,  liPartnerID, sSubject,   sFrom,  sTo,  sDate):
        print 'save it',  sType
        doSave = True
        if sType == 'Stream':
            sType = 'pdf'
            sFile = part.get_filename()
            print 'sFile = ',  sFile
            if sFile:
                iFileExt = sFile.rfind('.')
                if iFileExt > -1:
                    sType = sFile[iFileExt +1:]
            else:
                sType = 'bin'
            print 'new sType = ',  sType
        
        sExtension = '___dms.' + sType
        fname = self.misc.getRandomFilename(sExtension)
        print fname
        cwd = os.getcwd() 
        print cwd
        fname = cwd + '/' +fname
        f1 = open(fname , 'w')
        try:
            f1.write(part.get_payload(decode=True))
        except:
             f1.write(part.get_payload())
        f1.close()
        #print 'fname = ',  fname
        #print 'sType = ',  sType
        #print 'sTo = ',  sTo
        #print 'sFrom = ',  sFrom
        #print 'sSubject = ',  sSubject
        dms_id = 0
        #print part.get_payload() # prints the raw text
        if liAddressID and liAddressID not in ['NONE', 'ERROR']:
            for id in liAddressID:
                if id > 0:
                    print ' ID = ',  id
                    dms_id = self.save2DMS(fname, sType, 'Address',  id,  sSubject,  sFrom,  sTo,  sDate)    
        if liPartnerID and liPartnerID not in ['NONE', 'ERROR']:
            for id in liPartnerID:
                if id > 0:
                    print ' ID Partner = ',  id
                    dms_id = self.save2DMS(fname, sType, 'Partner',  id,  sSubject,  sFrom,  sTo, sDate)         
        print 'dms_id = ', dms_id
            
        if dms_id:
            print 'dms stuff = ', dms_id,  sType
            
            s = self.rpc.callRP('Misc.getTextExtract',  dms_id, sType,  self.dicUser)
            
            #print 'extract = ',  s
            
        
            
    def save2DMS(self,  fname, sType, Modul , id,  sSubject,  sFrom,  sTo,  sDate):
        print'load = ',   fname
        
        self.documentTools.importDocument(self.singleDMS,self.dicUser, fname)
        self.singleDMS.ModulNumber = self.MN[Modul]
        self.singleDMS.sep_info_1 = id    
        self.singleDMS.newRecord()
        self.singleDMS.newDate = self.getActualDateTime()['date']
        self.singleDMS.newTitle = sSubject
        print self.singleDMS.newDate
        self.singleDMS.newCategory = _('email')
        self.singleDMS.Rights = 'EMAIL'
        self.singleDMS.sub1 = _('From: ') + sFrom
        self.singleDMS.sub2 = _('To: ') + sTo
        if sType == 'txt':
            self.singleDMS.sub3 = _('Plain Text') 
        else:
            self.singleDMS.sub3 = _('Attachment Type: ') + sType
        
        newID = self.singleDMS.save(['document_image'])
        self.singleDMS.sub4 = _('Email Date: ') + sDate

        return newID
        
