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




class basics(xmlrpc.XMLRPC):
    def __init__(self):
        self.debug = 0
        self.SSL_OFFSET = 500
        
        self.CUON_FS = '/etc/cuon'  
        
       
        self.XMLRPC_PORT = 7080
        self.XMLRPC_HOST = 'localhost'
        
        
        self.WEBPATH = '/var/cuon_www/'
        self.WEB_HOST = 'localhost'
        self.WEB_PORT = 7081
        self.ICALPATH = '/var/cuon_www/iCal/'
        
	
        
        self.AI_PORT = 7082
        self.AI_HOST = '84.244.7.139'
        self.AI_SERVER = "http://84.244.7.139:" + `self.AI_PORT`
        
        self.REPORT_PORT = 7083
        self.REPORT_HOST = 'localhost'
        self.REPORTPATH = "/usr/share/cuon/cuon_server/src/cuon/Reports/XML"
        self.DocumentPathHibernationIncoming = '/var/cuon/Documents/Hibernation/Incoming'
        self.DocumentPathListsAddresses = '/var/cuon/Documents/Lists/Addresses'
        self.DocumentPathListsArticles = '/var/cuon/Documents/Lists/Articles'
        
        self.WIKI_PORT = 7084
        self.ONLINE_BOOK = 'http://84.244.7.139:7084/?action=xmlrpc2'
        
        self.POSTGRES_HOST = 'localhost'
        self.POSTGRES_PORT = 5432
        
        
        try:
            self.cpServer = ConfigParser.ConfigParser()
            
            self.cpServer.readfp(open(self.CUON_FS + '/server.ini'))
    
            
            
            # AI
            value = self.getConfigOption('AI','AI_HOST')
            if value:
                self.AI_HOST = value
                
            value = self.getConfigOption('AI','AI_PORT')
            if value:
                self.AI_PORT = int(value)
                
            
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
    
    def getConfigOption(self, section, option):
        value = None
        if self.cpServer.has_option(section,option):
            value = self.cpServer.get(section, option)
            print 'getConfigOption', section + ', ' + option + ' = ' + value
        return value
        
    def getParser(self, sFile):
        cpParser = ConfigParser.ConfigParser()
        f = open(sFile)
        print 'f1 = ', f
        cpParser.readfp(f)
        print 'cpp', cpParser
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
        
    def createNewSessionID(self, secValue = 36000):
        
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

    def getWhere(self, sWhere, dicUser, Single = 0, Prefix=""):
        self.writeLog('Start getWhere Single = ' +`Single`)
        
        
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
        self.writeLog('getWhere = ' + `sWhere`)
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
        debugValue = 1
        #print 'debugValue', debugValue
        if debugValue > 0:
        
            file = open('/tmp/cuon_server.log','a')
            file.write(time.ctime(time.time() ))
            file.write('\n')
            file.write(sLogEntry)
            file.write('\n')
            file.close()
            #print sLogEntry
        
        
              
    def getTimeString(self, time_id):
        dicTime = []
        
        dicTime.append('0:00')
        dicTime.append('0:15')
        dicTime.append('0:30')
        dicTime.append('0:45')
        dicTime.append('1:00')
        dicTime.append('1:15')
        dicTime.append('1:30')
        dicTime.append('1:45')
        dicTime.append('2:00')
        dicTime.append('2:15')
        dicTime.append('2:30')
        dicTime.append('2:45')
        dicTime.append('3:00')
        dicTime.append('3:15')
        dicTime.append('3:30')
        dicTime.append('3:45')
        dicTime.append('4:00')
        dicTime.append('4:15')
        dicTime.append('4:30')
        dicTime.append('4:45')
        dicTime.append('5:00')
        dicTime.append('5:15')
        dicTime.append('5:30')
        dicTime.append('5:45')
        dicTime.append('6:00')
        dicTime.append('6:15')
        dicTime.append('6:30')
        dicTime.append('6:45')
        dicTime.append('7:00')
        dicTime.append('7:15')
        dicTime.append('7:30')
        dicTime.append('7:45')
        dicTime.append('8:00')
        dicTime.append('8:15')
        dicTime.append('8:30')
        dicTime.append('8:45')
        dicTime.append('9:00')
        dicTime.append('9:15')
        dicTime.append('9:30')
        dicTime.append('9:45')
        dicTime.append('10:00')
        dicTime.append('10:15')
        dicTime.append('10:30')
        dicTime.append('10:45')
        dicTime.append('11:00')
        dicTime.append('11:15')
        dicTime.append('11:30')
        dicTime.append('11:45')
        dicTime.append('12:00')
        dicTime.append('12:15')
        dicTime.append('12:30')
        dicTime.append('12:45')
        dicTime.append('13:00')
        dicTime.append('13:15')
        dicTime.append('13:30')
        dicTime.append('13:45')
        dicTime.append('14:00')
        dicTime.append('14:15')
        dicTime.append('14:30')
        dicTime.append('14:45')
        dicTime.append('15:00')
        dicTime.append('15:15')
        dicTime.append('15:30')
        dicTime.append('15:45')
        dicTime.append('16:00')
        dicTime.append('16:15')
        dicTime.append('16:30')
        dicTime.append('16:45')
        dicTime.append('17:00')
        dicTime.append('17:15')
        dicTime.append('17:30')
        dicTime.append('17:45')
        dicTime.append('18:00')
        dicTime.append('18:15')
        dicTime.append('18:30')
        dicTime.append('18:45')
        dicTime.append('19:00')
        dicTime.append('19:15')
        dicTime.append('19:30')
        dicTime.append('19:45')
        dicTime.append('20:00')
        dicTime.append('20:15')
        dicTime.append('20:30')
        dicTime.append('20:45')
        dicTime.append('21:00')
        dicTime.append('21:15')
        dicTime.append('21:30')
        dicTime.append('21:45')
        dicTime.append('22:00')
        dicTime.append('22:15')
        dicTime.append('22:30')
        dicTime.append('22:45')
        dicTime.append('23:00')
        dicTime.append('23:15')
        dicTime.append('23:30')
        dicTime.append('23:45')
        return dicTime[time_id]
                
              


