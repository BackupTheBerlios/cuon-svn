# coding=utf-8
##Copyright (C) [2003]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 

import time,  glob,  os
import xmlrpclib
from twisted.web import xmlrpc
from twisted.internet import defer
from twisted.internet import reactor
from twisted.web import server
import time
import random
import sys,os  
import shelve
import ConfigParser
import bz2, base64
import types
import uuid

class basics(xmlrpc.XMLRPC):
    def __init__(self):
        self.debug = 0
        self.DEBUG = False
        self.DEBUG_MODUS = 1
        self.MN = {}
        self.MN['DMS'] = 11000
        self.MN['Forms_Address_Notes_Misc'] = 11010
        self.MN['Forms_Address_Notes_Contacter'] = 11011
        self.MN['Forms_Address_Notes_Rep'] = 11012
        self.MN['Forms_Address_Notes_Salesman'] = 11013
        
        self.SSL_OFFSET = 500
        
        self.CUON_FS = '/etc/cuon'  
        
       
        self.XMLRPC_PORT = 7080
        self.XMLRPC_HOST = 'localhost'
        self.XMLRPC_PROTO = "http"
        
        self.WEBPATH = '/var/cuon_www/'
        self.WEB_HOST = 'localhost'
        self.WEB_PORT = 7081
        self.ICALPATH = '/var/cuon_www/iCal/'
        
        self.WEB_HOST2 = 'localhost'
        self.WEB_PORT2 = 7084
        self.WEB_START2 = False
        
        self.WEB_HOST3 = 'localhost'
        self.WEB_PORT3 = 7085
        
        
        self.WEB_HOST4 = 'localhost'
        self.WEB_PORT4 = 7086
        
        self.AI_PORT = 7082
        self.AI_HOST = '84.244.7.139'
        self.AI_SERVER = "http://84.244.7.139:" + `self.AI_PORT`
        
        self.REPORT_PORT = 7083
        self.REPORT_HOST = 'localhost'
        self.REPORTPATH = "/usr/share/cuon/cuon_server/src/cuon/Reports/XML"

        self.DocumentPathOrderInvoice = '/var/cuon/Documents/Order/Invoice'
        self.DocumentPathOrderProposal = '/var/cuon/Documents/Order/Proposal'


        self.DocumentPathHibernationIncoming = '/var/cuon/Documents/Hibernation/Incoming'
        self.DocumentPathHibernationPickup = '/var/cuon/Documents/Hibernation/Pickup'
        
        
        self.DocumentPathListsAddresses = '/var/cuon/Documents/Lists/Addresses'
        self.DocumentPathListsArticles = '/var/cuon/Documents/Lists/Articles'
        self.DocumentPathTmp =  '/var/cuon/tmp'
        
        self.DocumentPathHibernationInvoice = '/var/cuon/Documents/Hibernation/Invoice'
        self.DocumentPathGravesInvoice = '/var/cuon/Documents/Graves/Invoice'
        self.DocumentPathGravesPlants = '/var/cuon/Documents/Graves/Plants'
        
        self.WIKI_PORT = 7084
        self.ONLINE_BOOK = 'http://84.244.7.139:7084/?action=xmlrpc2'
        
        self.POSTGRES_HOST = 'localhost'
        self.POSTGRES_PORT = 5432
        self.POSTGRES_DB = 'cuon'
        self.POSTGRES_USER = 'Test'
        
        
        self.OSC_HOST = 'localhost'
        self.OSC_PORT = 5432
        self.OSC_DB = 'cuon'
        self.OSC_USER = 'Test'
        self.liSQL_ERRORS =  ['NONE','ERROR']
        
        self.PdfEncoding = 'latin-2'
        
        self.EMAILSERVER = None
        self.EMAILPORT = '25'
        self.EMAILUSER = 'jhamel'
        self.EMAILPASSWORD = None
        self.EMAILENCODING = 'utf-8'
        self.EMAILLOGINCRYPT = ['No Encryption', 'Automaitic','Plain Text','Login', 'Cram-MD5','Digest-MD5'  ]
        
        self.CURRENCY_NAME = 'EUR'
        self.CURRENCY_SIGN = '€'
        self.CURRENCY_ROUND = 2

        self.DIC_USER = {}
        self.DIC_USER['SQLDateFormat'] = 'DD.MM.YYYY'
        self.DIC_USER['SQLTimeFormat'] = 'HH24:MI'
        self.DIC_USER['SQLDateTimeFormat'] = 'DD.MM.YYYY HH24:MI'
        self.DIC_USER['DateTimeFormatstring'] = '%d.%m.%Y %H:%M'
        self.DIC_USER['DateformatString'] = '%d.%m.%Y '
        self.DIC_USER['TimeformatString'] = '%H:%M'
        
        self.JABBERSERVER=None
        self.JABBERUSERNAME=None
        self.JABBERPASSWORD=None
        
        self.AUTOMATIC_SCHEDUL = False
        
        self.IMAP_HOST = 'localhost'
        self.IMAP_PORT = 143
        self.IMAP_USERNAME = 'test'
        self.IMAP_PASSWORD = 'test'
        
        self.SEND_VERSION_INFO = 'YES'
        try:
            self.cpServer = ConfigParser.ConfigParser()
            
            self.cpServer.readfp(open(self.CUON_FS + '/server.ini'))
            # Automatic schedul 

            value = self.getConfigOption('AUTOMATIC','SCHEDUL')
            if value:
                if value.upper() == 'YES':
                    self.AUTOMATIC_SCHEDUL = True
              
            # Debug
            value = self.getConfigOption('DEBUG','ACTIVATE')
            if value:
                if value.upper() == 'YES':
                    self.DEBUG = True
                
            
            # AI
            value = self.getConfigOption('AI','AI_HOST')
            if value:
                self.AI_HOST = value
                
            value = self.getConfigOption('AI','AI_PORT')
            if value:
                self.AI_PORT = int(value)
                
            # Postgres
            value = self.getConfigOption('POSTGRES','POSTGRES_HOST')
            if value:
                self.POSTGRES_HOST = value
                
            value = self.getConfigOption('POSTGRES','POSTGRES_PORT')
            if value:
                self.POSTGRES_PORT = int(value)
                
            value = self.getConfigOption('POSTGRES','POSTGRES_DB')
            if value:
                self.POSTGRES_DB = value
                
            value = self.getConfigOption('POSTGRES','POSTGRES_USER')
            if value:
                self.POSTGRES_USER = value
                
            # Web2
            value = self.getConfigOption('WEB2','HOST')
            if value:
                self.WEB_HOST2 = value
            value = self.getConfigOption('WEB2','PORT')
            if value:
                self.WEB_PORT2 = int(value)
            value = self.getConfigOption('WEB2','START')
            if value:
            
                self.WEB_START2 = self.checkBool(value)        
            # Web3
            value = self.getConfigOption('WEB3','HOST')
            if value:
                self.WEB_HOST3 = value
            value = self.getConfigOption('WEB3','PORT')
            if value:
                self.WEB_PORT3 = int(value)
            
            # Web4
            value = self.getConfigOption('WEB4','HOST')
            if value:
                self.WEB_HOST4 = value
            value = self.getConfigOption('WEB4','PORT')
            if value:
                self.WEB_PORT4 = int(value)
                    
                
            # OSCOMMERCE
            value = self.getConfigOption('OSCOMMERCE','OSC_HOST')
            if value:
                self.OSC_HOST = value
                
            value = self.getConfigOption('OSCOMMERCE','OSC_PORT')
            if value:
                self.OSC_PORT = int(value)
                
            value = self.getConfigOption('OSCOMMERCE','OSC_DB')
            if value:
                self.OSC_DB = value
                
            value = self.getConfigOption('OSCOMMERCE','OSC_USER')
            if value:
                self.OSC_USER = value
                
                
            #PDF
            value = self.getConfigOption('PDF','ENCODING')
            if value:
                self.PdfEncoding = value

            # EMAIL Config
            value = self.getConfigOption('EMAIL','DEFAULTSERVER')
            if value:
                self.EMAILSERVER = value
            
            value = self.getConfigOption('EMAIL','DEFAULTPORT')
            if value:
                self.EMAILPORT = value
                        
            value = self.getConfigOption('EMAIL','DEFAULTUSER')
            if value:
                self.EMAILUSER = value
            
            value = self.getConfigOption('EMAIL','DEFAULTPASSWORD')
            if value:
                self.EMAILPASSWORD = value
            
            value = self.getConfigOption('EMAIL','ENCODING')
            if value:
                self.EMAILENCODING = value
                
            value = self.getConfigOption('EMAIL','CRYPT')
            if value:
                self.EMAILCRYPT = value
                
            value = self.getConfigOption('CURRENCY','NAME')
            if value:
                self.CURRENCY_NAME = value
            
            value = self.getConfigOption('CURRENCY','SIGN')
            if value:
                self.CURRENCY_SIGN = value
                
            value = self.getConfigOption('CURRENCY','ROUND')
            if value:
                self.CURRENCY_ROUND = int(value)
               
            # jABBER
            value = self.getConfigOption('JABBER','SERVER')
            if value:
                self.JABBERSERVER = value
            
            value = self.getConfigOption('JABBER','USERNAME')
            if value:
                self.JABBERUSERNAME = value
            
            value = self.getConfigOption('JABBER','PASSWORD')
            if value:
                self.JABBERPASSWORD = value
            
            # IMAP
            
            value = self.getConfigOption('IMAP','SERVER')
            if value:
                self.IMAP_HOST = value
                
            value = self.getConfigOption('IMAP','PORT')
            if value:
                self.IMAP_PORT = int(value)
                
            value = self.getConfigOption('IMAP','USERNAME')
            if value:
                self.IMAP_USERNAME = value
            
            value = self.getConfigOption('IMAP','PASSWORD')
            if value:
                self.IMAP_PASSWORD = value
                
            # VERSION_INFO
            value = self.getConfigOption('VERSION','SEND_VERSION_INFO')
            if value:
                self.SEND_VERSION_INFO = value.upper()
                
                
            
        except Exception, params:
            print "Error read ini-File"
            print Exception
            print params
            
            
        AI_SERVER = "http://" + self.AI_HOST + ":" + `self.AI_PORT`
        self.ai_server = xmlrpclib.ServerProxy(AI_SERVER)
        REPORT_SERVER = "http://" + self.REPORT_HOST + ":" + `self.REPORT_PORT`
        self.report_server = xmlrpclib.ServerProxy(REPORT_SERVER)
        
        WEB_SERVER = "http://" + self.WEB_HOST + ":" + `self.WEB_PORT`
        self.web_server = xmlrpclib.ServerProxy(WEB_SERVER)
        # Limits
        self.LIMITSQL = 400000
        self.LIMITGARDEN = 400000
        self.LIMITADDRESS = 400000
        self.LIMITARTICLES = 400000
        self.LIMITPROJECT = 400000
        self.LIMITORDER = 400000
        
        # Crypt 
        
        try:
            self.cpServer = ConfigParser.ConfigParser()
            
            self.cpServer.readfp(open(self.CUON_FS + '/sql.ini'))
            
            value = self.getConfigOption('LIMIT','GARDEN')
            if value:
                self.LIMITGARDEN = value
                
            value = self.getConfigOption('LIMIT','ADDRESS')
            if value:
                self.LIMITADDRESS = value
   
            value = self.getConfigOption('LIMIT','ARTICLES')
            if value:
                self.LIMITARTICLES = value
   
            value = self.getConfigOption('LIMIT','PROJECT')
            if value:
                self.LIMITPROJECT = value
   
            value = self.getConfigOption('LIMIT','ORDER')
            if value:
                self.LIMITORDER = value
      
        except Exception, params:
            print "Error read ini-File = sql.ini" 
            print Exception
            print params        
            
    
        self.liModules = []
        self.dicLimitTables = {}
        
        # Garden
        for i in ['hibernation', 'hibernation_plant', 'botany']:
            
            self.dicLimitTables[i] = self.LIMITGARDEN
            
        for i in ['address', 'parner', 'partner_schedul']:
            
            self.dicLimitTables[i] = self.LIMITADDRESS
            
        for i in ['articles']:
            
            self.dicLimitTables[i] = self.LIMITARTICLES
        
        for i in ['projects', 'project_phases']:
            
            self.dicLimitTables[i] = self.LIMITPROJECT
        
#        self.dicLimitTables['GARDEN'] = {'list':['hibernation', 'hibernation_plant', 'botany'],'limit':self.LIMITGARDEN}
#        self.liModules.append('GARDEN')
#        
#        self.dicLimitTables['ADDRESS'] = {'list':['address'], 'limit':self.LIMITADDRESS}
#        self.liModules.append('ADDRESS')
#        
#        self.dicLimitTables['PROJECTS'] = {'list':['projects', 'project_phases'], 'limit':self.LIMITPROJECT}
#        self.liModules.append('PROJECTS')
#        
        
        
        
        self.OrderStatus  = {}
        self.OrderStatus['OrderStart'] = 0
        self.OrderStatus['OrderEnd'] = 299
        self.OrderStatus['ProposalStart'] = 300
        self.OrderStatus['ProposalEnd'] = 399
            
        self.liTime = []
        
        self.liTime.append('0:00')
        self.liTime.append('0:15')
        self.liTime.append('0:30')
        self.liTime.append('0:45')
        self.liTime.append('1:00')
        self.liTime.append('1:15')
        self.liTime.append('1:30')
        self.liTime.append('1:45')
        self.liTime.append('2:00')
        self.liTime.append('2:15')
        self.liTime.append('2:30')
        self.liTime.append('2:45')
        self.liTime.append('3:00')
        self.liTime.append('3:15')
        self.liTime.append('3:30')
        self.liTime.append('3:45')
        self.liTime.append('4:00')
        self.liTime.append('4:15')
        self.liTime.append('4:30')
        self.liTime.append('4:45')
        self.liTime.append('5:00')
        self.liTime.append('5:15')
        self.liTime.append('5:30')
        self.liTime.append('5:45')
        self.liTime.append('6:00')
        self.liTime.append('6:15')
        self.liTime.append('6:30')
        self.liTime.append('6:45')
        self.liTime.append('7:00')
        self.liTime.append('7:15')
        self.liTime.append('7:30')
        self.liTime.append('7:45')
        self.liTime.append('8:00')
        self.liTime.append('8:15')
        self.liTime.append('8:30')
        self.liTime.append('8:45')
        self.liTime.append('9:00')
        self.liTime.append('9:15')
        self.liTime.append('9:30')
        self.liTime.append('9:45')
        self.liTime.append('10:00')
        self.liTime.append('10:15')
        self.liTime.append('10:30')
        self.liTime.append('10:45')
        self.liTime.append('11:00')
        self.liTime.append('11:15')
        self.liTime.append('11:30')
        self.liTime.append('11:45')
        self.liTime.append('12:00')
        self.liTime.append('12:15')
        self.liTime.append('12:30')
        self.liTime.append('12:45')
        self.liTime.append('13:00')
        self.liTime.append('13:15')
        self.liTime.append('13:30')
        self.liTime.append('13:45')
        self.liTime.append('14:00')
        self.liTime.append('14:15')
        self.liTime.append('14:30')
        self.liTime.append('14:45')
        self.liTime.append('15:00')
        self.liTime.append('15:15')
        self.liTime.append('15:30')
        self.liTime.append('15:45')
        self.liTime.append('16:00')
        self.liTime.append('16:15')
        self.liTime.append('16:30')
        self.liTime.append('16:45')
        self.liTime.append('17:00')
        self.liTime.append('17:15')
        self.liTime.append('17:30')
        self.liTime.append('17:45')
        self.liTime.append('18:00')
        self.liTime.append('18:15')
        self.liTime.append('18:30')
        self.liTime.append('18:45')
        self.liTime.append('19:00')
        self.liTime.append('19:15')
        self.liTime.append('19:30')
        self.liTime.append('19:45')
        self.liTime.append('20:00')
        self.liTime.append('20:15')
        self.liTime.append('20:30')
        self.liTime.append('20:45')
        self.liTime.append('21:00')
        self.liTime.append('21:15')
        self.liTime.append('21:30')
        self.liTime.append('21:45')
        self.liTime.append('22:00')
        self.liTime.append('22:15')
        self.liTime.append('22:30')
        self.liTime.append('22:45')
        self.liTime.append('23:00')
        self.liTime.append('23:15')
        self.liTime.append('23:30')
        self.liTime.append('23:45')
        
        
    def getConfigOption(self, section, option, configParser = None):
        value = None
        if configParser:
            cps = configParser
        else:
           cps = self.cpServer
           
        if cps.has_option(section,option):
            value = cps.get(section, option)
            #print 'getConfigOption', section + ', ' + option + ' = ' + value
        return value
    
      
        
    def getParser(self, sFile):
        cpParser = ConfigParser.ConfigParser()
        f = open(sFile)
        #print 'f1 = ', f
        cpParser.readfp(f)
        #print 'cpp', cpParser
        return cpParser, f
        
    def out(self, s):
        self.writeLog(s,self.debug)
        
    def checkEndTime(self, fTime):
        ok = 0
        try:
            if time.time() < fTime:
                ok = 1
        except:
            self.out('Error in time-routine')
                    
        return ok
        
    def createNewSessionID(self, secValue = 42000):
        
        s = ''
        
        n = random.randint(0,1000000000)
        for i in range(27):
            ok = True
            while ok:
                r = random.randint(65,122)
                if r < 91 or r > 96:
                    ok = False
                    s = s + chr(r)
    
        s = s + `n`
        #writeLog(s)
        return {'SessionID':s, 'endTime': time.time() + secValue}

    def getUserInfo(self, dicUser):
        liUser = []
        liUser.append(dicUser['Name'])
        liUser.append(`dicUser['client']`)
        if  dicUser.has_key('noWhereClient') and dicUser['noWhereClient'].upper() == 'YES':
            liUser.append('1')
        elif dicUser.has_key('noWhereClient') and dicUser['noWhereClient'].upper() == 'NO':
             liUser.append('0')
        else:
            liUser.append('1')
        
             
        
        
        return liUser
        
    def getWhere(self, sWhere, dicUser, Single = 0, Prefix=""):
        #self.writeLog('Start getWhere Single = ' +`Single`)
        
        
        if not dicUser.has_key('noWhereClient'):
            if sWhere and len(sWhere) > 0 and Single == 0:
               iFind = sWhere.upper().find('WHERE' )
               if iFind >= 0:
                  sWhere = sWhere[0:iFind + 5] + " "+ Prefix + "client = " + `dicUser['client']` + " and "+ Prefix + "status != 'delete' and " + sWhere[iFind +5:] 
            elif Single == 1:
               sWhere = " Where "+ Prefix + "client = " + `dicUser['client']` + " and " + Prefix + "status != 'delete' "
        
            elif Single == 2:
               sWhere = " and "+ Prefix + "client = " + `dicUser['client']` + " and "+ Prefix + "status != 'delete' "
        
            else:
               sWhere = " where "+ Prefix + "client = " + `dicUser['client']` + " and "+ Prefix + "status != 'delete' "
        
        #self.writeLog('getWhere = ' + `sWhere`)
        if not sWhere:
            sWhere = ' '
        return sWhere       
    def openDB(self):
        self.dbase = shelve.open(os.path.normpath(self.CUON_FS + '/' + 'cuonData'))

    def closeDB(self):
        self.dbase.close()
        
    def saveObject(self, key, oValue):

        self.dbase[key] = oValue

    def loadObject(self, key):
        oValue = None
        try:
            oValue = self.dbase[key]
        except:
            oValue = None
            
        return oValue
    def writeLog(self, sLogEntry, debugValue = 1):
        
        if debugValue > 100 or self.DEBUG:
            try:
                #print 'debugValue', debugValue
                if debugValue == 1 or self.DEBUG_MODUS > 0:
                    
                    file = open('/var/log/cuon_allserver.log','a')
                    file.write(time.ctime(time.time() ))
                    file.write('\n')
                    file.write(sLogEntry)
                    file.write('\n')
                    file.close()
                    #print sLogEntry
            except:
                pass
                
            
    def getStaffID(self, dicUser):
        return "(select id from staff where staff.cuon_username = '" +  dicUser['Name'] + "') "
    
    
    def getTimeString(self, time_id):
        
        return self.liTime[time_id]
                
              
    def getTime(self,s ):
        Hour,Minute = divmod(s,4)
        Minute = Minute * 15
        
        return Hour, Minute
    
    def rebuild(self, data):
        s = self.doDecode64(data)
        Data = self.decompress(s)
        return Data
        
    
    def decompress(self, data):
        Data = None
        try:
            Data = bz2.decompress(data)
                 
        except Exception, param:
            print Exception, param
        #print 'data', data
        #print 'Data', Data
        return Data
        
    def doDecode64(self, data):
        Data = None
        try:
            Data = base64.decodestring(data)
                 
        except Exception, param:
            print Exception, param
        #print 'data', data
        #print 'Data', Data
        return Data
        
    def xmlrpc_testXmlrpc(self, iA = None, iB=None):
        print 'test xmlrpc', iA, iB
        if iA and iB:
            return iA * iB
        else:
            return 'Test without Values'
    
    
    def getBeforeYears(self, datepart,z1):
            beforeYears = 0
            newTime = time.localtime()
        
            if datepart == 'month' and z1 > 0:
                if (newTime.tm_mon - z1) <= 0:
                    beforeYears = 1
            if datepart == 'quarter' and z1 > 0:
                if (newTime.tm_mon - z1)*3 <= 0:
                    beforeYears = 1
                
            return newTime.tm_year - beforeYears       
            
    def getNow(self, vSql, z1,  year=2010):
        newTime = time.localtime()
        datepart = vSql['id']
        now = 0
            
        if datepart == 'month' :
            now = newTime.tm_mon - z1
            if now < 1:
                now += 12
                year -= 1
                
        elif datepart == 'quarter' :
            if newTime.tm_mon in [1, 2, 3]:
                now = 1
            elif newTime.tm_mon in [4, 5, 6]:
                now = 2
            elif newTime.tm_mon in [7, 8, 9]:
                now = 3
            elif newTime.tm_mon in [10, 11, 12]:
                now = 4
            now -= z1
            
            if now < 1:
                now += 4
                year -= 1
                
        elif datepart == 'week' :
           now =  "  date_part('" + vSql['sql'] + "', now()) - " + `z1`
        elif datepart == 'day' :
           now =  "  date_part('" + vSql['sql'] + "', now()) - " + `z1`
            
        else:
            now = z1
        if isinstance(now, types.IntType):
            now = `now`
            
        return now,  `year`
        
        
    def getActualDateTime(self):
        newTime = time.localtime()
        tDate =  time.strftime(self.DIC_USER['DateformatString'], newTime)
        tTime =  time.strftime(self.DIC_USER['TimeformatString'], newTime)
        tStamp = time.strftime(self.DIC_USER['DateTimeFormatstring'], newTime)
        dicTime = {'date':tDate, 'time':tTime, 'timestamp':tStamp }
        
        return dicTime
    def addDateTime(self, firstRecord):
        dicTime = self.getActualDateTime()
        if dicTime:
            for key in dicTime:
                firstRecord['date_' + key] = dicTime[key]
        return firstRecord       




    def getTime(self,s ):
        try:
            if isinstance(s,types.StringType):
                iS = int(s)
            else:
                iS = s
                
            Hour,Minute = divmod(iS,4)
            Minute = Minute * 15
        except:
            Hour = 0
            Minute = 0
            
        
        return Hour, Minute
        
    def getTimeString(self, s):
        Hour, Minute = self.getTime(s)
        #print Hour, Minute
        sHour = `Hour`
        if Minute == 0:
            sMinute = '00'
        else:
            sMinute = `Minute`
        
        s = sHour + ':' + sMinute
        return s
        
        
    def getActualDateTime(self):
        dicTime = {}
        try:
            newTime = time.localtime()
            tDate =  time.strftime(self.DIC_USER['DateformatString'], newTime)
            tTime =  time.strftime(self.DIC_USER['TimeformatString'], newTime)
            tStamp = time.strftime(self.DIC_USER['DateTimeFormatstring'], newTime)
            dicTime = {'date':tDate, 'time':tTime, 'timestamp':tStamp }
        except Exception,  params:
            print Exception, params
            dicTime = {'date':' ', 'time':' ', 'timestamp':' ' }
            
        
        return dicTime
        
    
       
        
    
    def getDateTime(self,dateString,strFormat="%Y-%m-%d"):
        # Expects "YYYY-MM-DD" string
        # returns a datetime object
        eSeconds = time.mktime(time.strptime(dateString,strFormat))
        return datetime.datetime.fromtimestamp(eSeconds)
    
    def formatDate(self,dtDateTime,strFormat="%Y-%m-%d"):
        # format a datetiself, me object as YYYY-MM-DD string and return
        return dtDateTime.strftime(strFormat)
    
    def getFirstOfMonth2(self, dtDateTime):
        #what is the first day of the current month
        ddays = int(dtDateTime.strftime("%d"))-1 #days to subtract to get to the 1st
        delta = datetime.timedelta(days= ddays)  #create a delta datetime object
        return dtDateTime - delta                #Subtract delta and return
    
    def getFirstOfMonth(self, dtDateTime):
        #what is the first day of the current month
        #format the year and month + 01 for the current datetime, then form it back
        #into a datetime object
        return self.getDateTime(self.formatDate(dtDateTime,"%Y-%m-01"))
        
    def getFirstOfYear(self, dtDateTime):
        #what is the first day of the current month
        #format the year and month + 01 for the current datetime, then form it back
        #into a datetime object
        return self.getDateTime(self.formatDate(dtDateTime,"%Y-01-01"))
    
    def getLastOfMonth(self, dtDateTime):
        dYear = dtDateTime.strftime("%Y")        #get the year
        dMonth = str(int(dtDateTime.strftime("%m"))%12+1)#get next month, watch rollover
        if int(dMonth) == 1:
            iYear = int(dYear)
            iYear += 1
            dYear = `iYear`
        print dMonth, len(dMonth)
        print dYear, len(dYear)
        
        dDay = "1"                               #first day of next month
        nextMonth = self.getDateTime("%s-%s-%s"%(dYear,dMonth,dDay))#make a datetime obj for 1st of next month
        delta = datetime.timedelta(seconds=1)    #create a delta of 1 second
        return nextMonth - delta                 #subtract from nextMonth and return
        
    def getLastOfYear(self, dtDateTime):
        dYear = dtDateTime.strftime("%Y")        #get the year
        
        return self.getDateTime(self.formatDate(dtDateTime,"%Y-12-31"))
    
    
    def getFirstDayOfMonth(self,sdate=None):
        if sdate == None:
            dDate = datetime.date.today()   
        else:
            dDate = sdate
            
        return self.getFirstOfMonth(dDate)
        
    def getLastDayOfMonth(self,sdate=None):
        if sdate == None:
            dDate = datetime.date.today()   
        else:
            dDate = sdate
            
        return self.getLastOfMonth(dDate)
        
        
    def getSeconds(self, dt):
        eSeconds = time.mktime( dt.timetuple())
        return eSeconds

    
    def getFirstDayOfMonthAsSeconds(self,sdate=None):
        return self.getSeconds(self.getFirstDayOfMonth(sdate))
        
    def getLastDayOfMonthAsSeconds(self,sdate=None):
        return self.getSeconds(self.getLastDayOfMonth(sdate))
        
        
    def getFirstLastDayOfLastMonthAsSeconds(self,sdate=None):
        currentFirstDay = self.getFirstDayOfMonth(sdate)
        secs = self.getSeconds(currentFirstDay) - 10
        print 'secs' , secs
        ddate = datetime.datetime.fromtimestamp(secs)
        
        dBegin = self.getFirstDayOfMonthAsSeconds(ddate)
        dEnd = self.getLastDayOfMonthAsSeconds(ddate)
        print dBegin,dEnd
        return dBegin,dEnd
        
        
    def checkType(self, oType, sType):
        bRet = False
        if sType == 'string':
            if isinstance(oType, types.StringType):
                bRet = True
        elif sType == 'int':
            if isinstance(oType, types.IntType):
                bRet = True
        elif sType == 'float':
            if isinstance(oType, types.FloatType):
                bRet = True
                                              
        return bRet
        
    def convertTo(self, value, sType):
        s = None
        if sType == "String":
            s = `value`
            s = s.strip()
            sL = len(s)
            if s[0] == 'L':
                s = s[1:]
            if s[sL-1]=='L':
                s = s[:sL-1]
        
        return s
                
        
    def getAssociatedTable(self, iNumber):
        sTable = None
        iDMS = 0
        
        if iNumber:
            if iNumber == 1:
                sTable = 'botany'
                iDMS = 110500
                
        return sTable, iDMS
        
        
    def  getNormalSqlData(self,  dicUser, braces=True,  coma=True):
        print `dicUser`
        liFields = []
        liValues = []
        
        sF = 'client '
        sV = `dicUser['client']` + ' '
        
        #set to every sf,sv the coma
        if coma:
            sF =  ', ' + sF
            sV =  ', ' + sV
            
        # set at last sf, sv the braces
        if braces:
            sF +=  ' )'
            sV +=  ')'
        
        liFields.append( sF)
        liValues.append( sV)
        
        return liFields,  liValues
        
    def checkBool(self,  value) :
        if value.upper() in ['YES', 'Y', 'JA', 'J', 'SI']:
            return True
        else:
            return False
            
        
    def xmlrpc_getComboReportLists(self, dicUser,  sPattern):
       
        
        liReport = []
        liReport1 = []
        liReport2 = []
        liReport3 = []
        liReportS = []
        liReportS2 = []
        
        repPath = "/usr/share/cuon/cuon_server/src/cuon/Reports/"
        # check user
        
        if os.path.isdir(repPath + 'user_' + dicUser['Name']):
            liReport1 = glob.glob(repPath + 'user_' + dicUser['Name'] + "/" + sPattern)
                                                                       
        # check to client id 
        if dicUser['client'] == -7:
            for clientID in range(50):
                if os.path.isdir(repPath + 'client_' + `clientID`):
                    liReport2 += glob.glob(repPath + 'client_' + `clientID` + "/" + sPattern)
        else:
            if os.path.isdir(repPath + 'client_' + `dicUser['client']`):
                liReport2 = glob.glob(repPath + 'client_' + `dicUser['client']` + "/" + sPattern)
                    
            #check last the XML
        liReport3 = glob.glob(repPath + 'XML' + "/" + sPattern)
        liReportS = liReport1 + liReport2 + liReport3
        if liReportS:
            liReportS2 = []
            for sFile in liReportS:
                print "sfile = ",  sFile
                liFile = sFile.split('/')
                liReportS2.append(liFile[len(liFile)-1])
                #print 'liReport = ',  liReportS2
                
                        
            for item in liReportS2:
                if not item in liReport:
                    liReport.append(item)
                #liReport.append(sFile[1])
                    
                
        return liReport
         
    def getNullUUID(self):
        return '00000000-0000-0000-0000-000000000000'
           
    def make64BitInt(self, x, y):
        return   (long(x) << 32) + long(y)


    def getIRandom(self, iValue):
        
        return  int(random.random()*iValue)
     
     
 
    def  normalizeXML(self,  sValue):
        if sValue:
            sValue = sValue.replace('&', '&amp;')
      
            sValue = sValue.replace('\'', '&apos;')
            sValue = sValue.replace('\"', '&quot; ')
            sValue = sValue.replace('<', '&lt;')
            sValue = sValue.replace('>', '&gt;')
            # for testing:
            #sValue = sValue.replace('/', '')
        return sValue
    def getNewUUID(self):
        return str(uuid.uuid4())
        
