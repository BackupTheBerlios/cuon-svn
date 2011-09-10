from icalendar import Calendar, Event,UTC
import time
from datetime import datetime
import random
import xmlrpclib
import Database 
from twisted.web import xmlrpc
 
from basics import basics

class iCal(xmlrpc.XMLRPC, basics):
    def __init__(self):
        basics.__init__(self)
        self.oDatabase = Database.Database()
        

    def createUID(self):
        s = ''
    
        n = random.randint(500000,1000000000)
        for i in xrange(27):
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
    
    def createEvent(self, dicEvent, UID = None):
        event = Event()
        #print ' start create event '
        try:
            if dicEvent.has_key('summary'):
                event.add('summary', dicEvent['summary'])
                #print 'Summary', dicEvent['summary']
            if dicEvent.has_key('dtstart'):
                s = time.strptime(dicEvent['dtstart'], dicEvent['DateTimeformatString'])
                event.add('dtstart', datetime(s[0],s[1],s[2],s[3],s[4],s[5]))
                #print 'dtstart', datetime(s[0],s[1],s[2],s[3],s[4],s[5])
            if dicEvent.has_key('dtend'):
                s = time.strptime(dicEvent['dtend'], dicEvent['DateTimeformatString'])
                event.add('dtend', datetime(s[0],s[1],s[2],s[3],s[4],s[5]))
                #print 'dtend', datetime(s[0],s[1],s[2],s[3],s[4],s[5])
            if dicEvent.has_key('dtstamp'):
                event.add('dtstamp', dicEvent['dtstamp'])
                #print 'stamp',  dicEvent['dtstamp']
            if not UID:
                dicEvent['uid'] = `dicEvent['id']` + '#### ' + self.createUID()
            else:
                dicEvent['uid'] = UID
                
            event.add('uid',dicEvent['uid'])
            
            #print 'UID', dicEvent['uid']
            if dicEvent.has_key('priority'):
                event.add('priority',dicEvent['priority'] )
            if dicEvent.has_key('location'):
                event.add('location',dicEvent['location'] )
            if dicEvent.has_key('status'):
                event.add('status',dicEvent['status'] )
            if dicEvent.has_key('description'):
                event.add('description',dicEvent['description'] )    
                
        except Exception, param:
            print 'Except error 55'
            #print Exception
            #print param
            
            #event = None
        return event
        
    def delCalendar(self,sName):
        newCal = self.createCal()
        self.writeCalendar(sName, newCal)
          
    def getCalendar(self, sName):
        Cal = None
        try:
            s = self.readCalendar(sName)
            Cal = Calendar.from_string(s)
        except Exception, param:
            print 'Except error 77'
            #print Exception
            #print param
        if not Cal:
            Cal = self.createCal()
        return Cal
        
    def writeCalendar(self, sName, Cal):
        try:
            f = open(self.ICALPATH + sName,'w')
            f.write(Cal.as_string())
            f.close()
        except Exception, param:
            print 'Except error 88'
            #print Exception
            #print param  
        
        return True
        
    def readCalendar(self,sName):
        sCal = None
        f = None
        try:
            f = open(self.ICALPATH + sName)
        
            sCal = f.read()
            f.close()
        except Exception, param:
            
            print 'Except error by open iCal'
            #print Exception
            #print param
            if f:
                print 'close f'
                f.close()
            sCal = 'BEGIN:VCALENDAR\r\nPRODID:-//My calendar product//mxm.dk//\r\nVERSION:2.0\r\nBEGIN:VEVENT\r\nDTEND:20050404T100000Z\r\nDTSTAMP:20050404T001000Z\r\nDTSTART:20050404T080000Z\r\nPRIORITY:5\r\nSUMMARY:Python meeting about calendaring\r\nUID:20050115T101010/27346262376@mxm.dk\r\nEND:VEVENT\r\nEND:VCALENDAR\r\n\n'

        return sCal
     
    def setCalendarValues(self,sName,firstRecord, dicUser, sUserKey, completeNew = False):
        ok = False
        dicEvent = self.getDicCal(firstRecord, dicUser,sUserKey)
        
        if dicEvent.has_key('staff_cuon_username') and len(dicEvent['staff_cuon_username']) > 0:
            #print 'create Calendar for schedul_staff', dicEvent['staff_cuon_username']
            #print dicEvent['staff_cuon_username'], len(dicEvent['staff_cuon_username'])
            sName = 'iCal_' + dicEvent['staff_cuon_username']
            
         
        Cal = self.getCalendar(sName)
        #print 'Cal', Cal
        newEvent = self.createEvent(dicEvent)
        
        if completeNew:
            Cal.add_component(newEvent)
            ok = True
            self.writeCalendar(sName, Cal)
                 
        else:
            Cal2 = self.createCal()
            for i in Cal.walk('VEVENT'):
                #print 'i = ', i
                if i.has_key('UID'):
                    #print 'uid = ', i['UID']
                    sSearch = `firstRecord['id']` +'####'
                    #print sSearch
                    if i['UID'][0:len(sSearch)] != sSearch:
                        #print 'uid not found'
                        Cal2.add_component(i)
                else:
                    Cal2.add_component(i)
                
            #print 'newEvent = ' + `newEvent`
            if newEvent and ( (newEvent.has_key('status') and  newEvent['status'] != "CANCELLED") or not newEvent.has_key('status')) :
                Cal2.add_component(newEvent)
                ok = True
            self.writeCalendar(sName, Cal2)
                
        return ok

    def addEvent(self, sName, firstRecord, dicUser, completeNew = False):
        
        
        ok = False
        # calendar of the contakter
        ok = self.setCalendarValues(sName, firstRecord, dicUser,'User', completeNew)
        # calendar of the schedul staff
        ok = self.setCalendarValues(sName, firstRecord, dicUser,'schedul_staff', completeNew)
        
        
       
##            print 'Cal', Cal
##            Cal2 = self.createCal()
##            for i in Cal.walk('VEVENT'):
##                print 'i = ', i
##                if i.has_key('UID'):
##                    print 'uid = ', i['UID']
##                    sSearch = `firstRecord['id']` +'####'
##                    print  '--->' + i['UID'][0:len(sSearch)] + '<---', '+++' + sSearch + '+++'
##
##                    print sSearch
##                    if i['UID'][0:len(sSearch)] != sSearch:
##                        print 'uid not found'
##                        Cal2.add_component(i)
##                    else:
##                        print 'UID foiCal.pyund'
##                        print  i['UID'][0:len(sSearch)-1], sSearch
##                else:
##                    Cal2.add_component(i)
##                
##            newEvent = self.createEvent(dicEvent)
##            print 'newEvent = ' + `newEvent`
##            if newEvent:
##                Cal2.add_component(newEvent)
##                self.writeCalendar('iCal_' + dicEvent['staff_cuon_username'], Cal2)
##                ok = True
                            
        return ok
    
    def getDicCal(self, firstRecord, dicUser, sUser):
        result = None
        self.writeLog('Start getDicCal')
        self.writeLog('getDicCal firstRecord = ' + `firstRecord`)
        if sUser == 'User':
            try:
                sSql = " select partner_schedul.id as sch_id,staff.cuon_username as staff_cuon_username, staff.lastname as st_lastname, staff.firstname as st_firstname, address.id as adr_id, address.lastname as adr_lastname, address.firstname as adr_firstname, address.zip as adr_zip, address.country as adr_country, address.city as adr_city from address, partner, partner_schedul, staff where partner.id = " 
                sSql += `firstRecord['partnerid']` + " and address.id = partner.addressid and partner.id = partner_schedul.partnerid and staff.cuon_username = partner_schedul.user_id and partner_schedul.id = " + `firstRecord['id']`
                result = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser)
            except Exception, params:
                print ' Exception getDicCal sql'
                #print Exception, params
                
        elif sUser == 'schedul_staff':
            try:
                sSql = " select partner_schedul.id as sch_id,staff.cuon_username as staff_cuon_username, staff.lastname as st_lastname, staff.firstname as st_firstname, address.id as adr_id, address.lastname as adr_lastname, address.firstname as adr_firstname, address.zip as adr_zip, address.country as adr_country, address.city as adr_city from address, partner, partner_schedul, staff where partner.id = " 
                sSql += `firstRecord['partnerid']` + " and address.id = partner.addressid and partner.id = partner_schedul.partnerid and staff.id = partner_schedul.schedul_staff_id and partner_schedul.id = " + `firstRecord['id']`
                result = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser)
            except Exception, params:
                print 'Exception 2 getDicCal sql'
                #print Exception, params
                
                        
            
        dicCal = {}
        #print 'firstRecord = ', firstRecord
        # Save TimeTransformation
        #dicCal['DateTimeformatString'] = dicUser['DateTimeformatString']
        dicCal['DateTimeformatString'] = self.DIC_USER['DateTimeFormatstring']
        sDate =  firstRecord['schedul_date']
        sDateEnd = firstRecord['schedul_date_end']
        #print 'result = ', result
        if result and result == 'NONE':
            result = None
        
        try:
            sTime = self.getTimeString( firstRecord['schedul_time_begin'])
            dicCal['dtstart'] = sDate + ' ' + sTime
                
                        
        except Exception, param:
            print 'Except error getDicCal 1'
            #print Exception
            #print param
            
            
            self.writeLog('1 Time error by ' + `firstRecord['schedul_time_begin']`)
        try:
            sTime = self.getTimeString( firstRecord['schedul_time_end'])
            if len(sDateEnd) > 0:
                
                dicCal['dtend'] = sDateEnd + ' ' + sTime
            else:
                dicCal['dtend'] = sDate + ' ' + sTime
                        
        
        
        except Exception, param:
            print 'Except error getDicCal 2'
            #print Exception
            #print param
            
        try:
            dicCal['summary'] = ''

            if result:
                dicCal['summary'] += '>> ' + result[0]['adr_zip'] + ' ' + self.tryDecode(result[0]['adr_city']) + ' <<, '

                dicCal['summary'] += firstRecord['short_remark'] + ', ID = ' + `result[0]['adr_id']` + ', '
                
            if result and result[0].has_key('st_lastname'):
                dicCal['summary'] += self.tryDecode(result[0]['st_lastname']) + ', ' 
                
            
            if result and result[0].has_key('st_firstname'):
                dicCal['summary'] += self.tryDecode(result[0]['st_firstname']) + ' ' 
                
            
            #dicCal['summary'] = self.tryDecode(dicCal['summary'] )
            #print 'Summary', dicCal['summary']

            #dicCal['summary'] = dicCal['summary'].decode('utf-8')
        except Exception, param:
            dicCal['summary'] = ' '
            print 'Except error getDicCal 3'
            #print Exception
            #print param
            
            self.writeLog('String error by ' + `firstRecord['short_remark']`)
        try:
            dicCal['id'] = firstRecord['id']
            if result and result not in ['NONE','ERROR']:
                

                dicCal['location'] = result[0]['adr_lastname']+ ','+ result[0]['adr_country'] + '-' + result[0]['adr_zip'] + ' ' + result[0]['adr_city']
                dicCal['location'] = self.tryDecode(dicCal['location'])
            #print 'location', dicCal['location']
                
        except Exception, params:
            print 'Error by location'
            #print Exception, params
            
        try:
            
            dicCal['description'] = firstRecord['notes']
                
            dicCal['description'] = self.tryDecode(dicCal['description'])
            print 'description', dicCal['description']
                
        except Exception, params:
            print 'Error by notes'
            print Exception, params
        try:
            
            if result and result not in ['NONE','ERROR']:
                if firstRecord['process_status'] >= 0 and firstRecord['process_status'] <= 99:
                    dicCal['status'] = "TENTATIVE"
                elif firstRecord['process_status'] >= 100 and  firstRecord['process_status'] <= 800:
                #dicCal['status'] = `firstRecord['process_status']`
                    dicCal['status'] = "CONFIRMED"
                elif firstRecord['process_status'] >= 801:
                    dicCal['status'] = "CANCELLED" 
                    
                    
                
                
                
        except Exception, params:
            print 'Error by status'
            print Exception, params
                
        #self.writeLog('dicCal = ' + `dicCal`)
            
        try:
            if result:
                dicCal['staff_cuon_username'] = result[0]['staff_cuon_username'] 
        except Exception, param:
            print 'Except error getDicCal 4'
            #print Exception
            #print param
        return dicCal     
    
    def createCal(self):
        s ='BEGIN:VCALENDAR\r\nPRODID:-//CUON\r\nVERSION:2.0\r\nEND:VCALENDAR\r\n\n'
       #'BEGIN:VCALENDAR\r\nPRODID:-//CUON\r\nVERSION:2.0\r\nBEGIN:VEVENT\r\nDTEND:20050404T100000Z\r\nDTSTAMP:20050404T001000Z\r\nDTSTART:20050404T080000Z\r\nPRIORITY:5\r\nSUMMARY:Python meeting about calendaring\r\nUID:20050115T101010/27346262376@mxm.dk\r\nEND:VEVENT\r\nEND:VCALENDAR\r\n\n'
       
        Cal = Calendar.from_string(s)
        return Cal
        
    def overwriteCal(self, sName, liRecords, dicUser):
        Cal = self.createCal()
        for record in liRecords:
            dicEvent = self.getDicCal(record, dicUser)
        
            newEvent = self.createEvent(dicEvent)
            print 'newEvent = ' + `newEvent`
            if newEvent:
                Cal.add_component(newEvent)
                
        self.writeCalendar(sName, Cal)
        
        

    def tryDecode(self, s):
        #print 'before:', s

        try:
            s = s.decode('utf-8')
        except:
            try:
                s = s.decode('latin-1')
            except:
                try:
                    s = s.decode('latin-2')
                except:
                    try:
                        s = s.decode('iso-8859-15')
                    except:
                        try:
                            s = s.decode('utf-7')
                        except:
                            try:
                                s = s.decode('CP-1250')
                            except:
                                try:
                                    v = s.encode('utf-8')
                                except Exception, params:
                                    print '-----> no decode method is functional, clean s '
                                    s = ''
                                    #print Exception, params

        #print len(s)
        #try:
        #    print 'after1:', s
        #except:
        #    pass

                                
##        try:
##            s = s.encode('utf-8')
##        except Exception, params:
##            print 'Error by encode'
##            print Exception,params
##        try:    
##            print 'after2:', s
##        except:
##            pass
##            
        return s
        
                
#i=iCal()
#dicEvent={}
#s = 'BEGIN:VCALENDAR\r\nPRODID:-//My calendar product//mxm.dk//\r\nVERSION:2.0\r\nBEGIN:VEVENT\r\nDTEND:20050404T100000Z\r\nDTSTAMP:20050404T001000Z\r\nDTSTART:20050404T080000Z\r\nPRIORITY:5\r\nSUMMARY:Python meeting about calendaring\r\nUID:20050115T101010/27346262376@mxm.dk\r\nEND:VEVENT\r\nEND:VCALENDAR\r\n\n'
#dicEvent['dtstart']=datetime(2006,06,05,10,0,0)
#s2 = i.xmlrpc_addEvent(s,dicEvent)
#print 's2=', s2

