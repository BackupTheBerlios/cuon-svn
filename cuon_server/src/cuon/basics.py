import xmlrpclib
from twisted.web import xmlrpc
from twisted.internet import defer
from twisted.internet import reactor
from twisted.web import server
import time
import random
import sys





class basics(xmlrpc.XMLRPC):
    def __init__(self):
        self.CUON_FS = None  
        self.CUON_AI_SERVER = "http://84.244.7.139:8765"
        self.CUON_WEBPATH = '/var/cuon_www/'
        self.CUON_ICALPATH = '/var/cuon_www/iCal/'
        f = open('/etc/cuon/cuon_zope.ini')
        if f:
            s1 = f.readline()
            while s1:
                liIni = s1.split('=')
                if liIni[0].strip() == 'ZOPE_PYTHON':
                    sys.path.append(liIni[1].strip())
                if liIni[0].strip() == 'CUON_FS':
                    self.CUON_FS = liIni[1].strip()
                if liIni[0].strip() == 'CUON_AI_SERVER':
                    self.CUON_AI_SERVER = liIni[1].strip()
                if liIni[0].strip() == 'CUON_WEBPATH':
                    self.CUON_WEBPATH = liIni[1].strip()
                if liIni[0].strip() == 'CUON_ICALPATH':
                    self.CUON_ICALPATH = liIni[1].strip()
                s1 = f.readline()
                
            f.close()
        self.ai_server = xmlrpclib.ServerProxy(self.CUON_AI_SERVER)
    
    def out(self, s):
        print s
        
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
    
    def writeLog(self, sLogEntry):
##        file = open('cuon_sql.log','a')
##        file.write(time.ctime(time.time() ))
##        file.write('\n')
##        file.write(sLogEntry)
##        file.write('\n')
##        file.close()
        print sLogEntry
        
              
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
                
              


