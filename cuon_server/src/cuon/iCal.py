from icalendar import Calendar, Event,UTC
import time
from datetime import datetime
import random
import xmlrpclib
from twisted.web import xmlrpc
 
from basics import basics

class iCal(xmlrpc.XMLRPC, basics):
    def __init__(self):
        basics.__init__(self)
        
    def createUID(self):
        s = ''
    
        n = random.randint(500000,1000000000)
        for i in range(27):
            ok = True
            while ok:
                r = random.randint(65,122)
                if r < 91 or r > 96:
                    ok = False
                    s = s + chr(r)
    
        s = s + `n`
        sTime = time.asctime(time.localtime())
        uid = sTime + ' ' + s
        return uid
    
    def getParsedDate(self, sDate):
        sValue = time.strftime(sDate, '%Y.%m.%d %H:%M')
        return sValue
    
    def createEvent(self, dicEvent):
        event = Event()
        try:
            if dicEvent.has_key('summary'):
                event.add('summary', dicEvent['summary'])
            if dicEvent.has_key('dtstart'):
                s = time.strptime(dicEvent['dtstart'], dicEvent['DateTimeformatString'])
                event.add('dtstart', datetime(s[0],s[1],s[2],s[3],s[4],s[5]))
            if dicEvent.has_key('dtend'):
                s = time.strptime(dicEvent['dtend'], dicEvent['DateTimeformatString'])
                event.add('dtend', datetime(s[0],s[1],s[2],s[3],s[4],s[5]))
            if dicEvent.has_key('dtstamp'):
                event.add('dtstamp', dicEvent['dtstamp'])
        
            dicEvent['uid'] = self.createUID()
        
            if dicEvent.has_key('priority'):
                event.add('priority',dicEvent['priority'] )
        except Exception, param:
            print 'Except error'
            print Exception
            print param
            
            #event = None
        return event
        
        
    def getCalendar(self, sName):
        Cal = None
        try:
            s = self.readCalendar(sName)
            Cal = Calendar.from_string(s)
        except Exception, param:
            print 'Except error'
            print Exception
            print param
            
        return Cal
        
    def writeCalendar(self, sName, Cal):
        try:
            f = open(self.CUON_ICALPATH + sName,'w')
            f.write(Cal.as_string())
            f.close()
        except Exception, param:
            print 'Except error'
            print Exception
            print param  
        
        return True
        
    def readCalendar(self,sName):
        sCal = None
        try:
            f = open(self.CUON_ICALPATH + sName)
        
            sCal = f.read()
            f.close()
        except Exception, param:
            print 'Except error'
            print Exception
            print param
            
        return sCal
        
    def xmlrpc_addEvent(self, sName, firstRecord, dicUser):
        ok = False
        Cal = self.getCalendar(sName)
        print 'Cal', Cal
        dicEvent = self.getDicCal(firstRecord, dicUser)
        
        newEvent = self.createEvent(dicEvent)
        print 'newEvent = ' + `newEvent`
        if newEvent:
            Cal.add_component(newEvent)
            self.writeCalendar(sName, Cal)
            ok = True
                
        return ok
    
    def getDicCal(self, firstRecord, dicUser):
            
        self.writeLog('Start getDicCal')
        self.writeLog('getDicCal firstRecord = ' + `firstRecord`)
        
        dicCal = {}
        # Save TimeTransformation
        dicCal['DateTimeformatString'] = dicUser['DateTimeformatString']
        sDate =  firstRecord['schedul_date']
        
        try:
            sTime = self.getTimeString( firstRecord['schedul_time_begin'])
            dicCal['dtstart'] = sDate + ' ' + sTime
                        
        except Exception, param:
            print 'Except error getDicCal 1'
            print Exception
            print param
            
            
            self.writeLog('1 Time error by ' + `firstRecord['schedul_time_begin']`)
        try:
            sTime = self.getTimeString( firstRecord['schedul_time_end'])
            dicCal['dtend'] = sDate + ' ' + sTime
                        
        
            self.writeLog('2 Time error by ' + `firstRecord['schedul_time_end']`)
        
        except Exception, param:
            print 'Except error getDicCal 2'
            print Exception
            print param
            
        try:
            dicCal['summary'] = firstRecord['short_remark']
                        
        except Exception, param:
            print 'Except error getDicCal 3'
            print Exception
            print param
            
            self.writeLog('String error by ' + `firstRecord['short_remark']`)
        
        self.writeLog('dicCal = ' + `dicCal`)
        
        return dicCal     
        
        
        

#i=iCal()
#dicEvent={}
#s = 'BEGIN:VCALENDAR\r\nPRODID:-//My calendar product//mxm.dk//\r\nVERSION:2.0\r\nBEGIN:VEVENT\r\nDTEND:20050404T100000Z\r\nDTSTAMP:20050404T001000Z\r\nDTSTART:20050404T080000Z\r\nPRIORITY:5\r\nSUMMARY:Python meeting about calendaring\r\nUID:20050115T101010/27346262376@mxm.dk\r\nEND:VEVENT\r\nEND:VCALENDAR\r\n\n'
#dicEvent['dtstart']=datetime(2006,06,05,10,0,0)
#s2 = i.xmlrpc_addEvent(s,dicEvent)
#print 's2=', s2

