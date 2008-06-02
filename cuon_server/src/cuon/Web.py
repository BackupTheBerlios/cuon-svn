import time
from datetime import datetime
import random
import xmlrpclib
from twisted.web import xmlrpc
 
from basics import basics
import iCal
import Database
import commands

class Web(xmlrpc.XMLRPC, basics):
    def __init__(self):
        basics.__init__(self)
        self.iCal = iCal.iCal()
        self.oDatabase = Database.Database()
        
    def xmlrpc_addCalendarEvent(self, sName, firstRecord, dicUser):
        ok = False
        self.writeLog('Automatic-Flag = ' + `self.AUTOMATIC_SCHEDUL`)
        if not self.AUTOMATIC_SCHEDUL:
            self.writeLog('create Schedul-iCal')
            ok = self.iCal.addEvent( sName, firstRecord, dicUser)
        
        return ok 
        
    def xmlrpc_updateCalendar(self, liNames, dicData, dicUser):
        sSql = 'select * from partner_schedul where partner_id = ' + `dicData['partner_id']`
        sSql = sSql + self.getWhere("",dicUser,1)
        
        dicResult =  oDatabase.xmlrpc_py_executeNormalQuery(sSql, dicUser )
        for sName in liNames:
            self.overwriteCal(sName,dicResult,dicuser)
            
    def xmlrpc_restartServerWeb2(self, dicUser):
        shellcommand = '/etc/init.d/cuonweb2 restart'
        liStatus = commands.getstatusoutput(shellcommand)
        print liStatus
        return liStatus
          
    def xmlrpc_cron_create_iCal(self, sName, fromDate = None):
            
        self.writeLog( 'cron_create_iCal, user = ' + sName)
        ok = True
        dicUser = {}
        dicUser['Name'] = sName
        sSql = 'select * from partner_schedul where schedul_time_begin > 0 '
        if not fromDate:
            sSql += " and date_part('doy', to_date(partner_schedul.schedul_date, '" + self.DIC_USER['SQLDateFormat'] +"'))  >=  date_part('doy', now()) -2 "
            sSql += " and date_part('year', to_date(partner_schedul.schedul_date, '" + self.DIC_USER['SQLDateFormat'] +"'))  >=  date_part('year', now())"
        sSql += 'and process_status != 999 order by id desc '
        self.writeLog(sSql,999)
        dicResult = self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
        #self.writeLog(dicResult)
        if fromDate == 'All':
            liStaff = self.oDatabase.xmlrpc_executeNormalQuery('select cuon_username from staff',dicUser)
            if liStaff and liStaff not in ['NONE','ERROR']:
                for j in liStaff:
                    self.iCal.delCalendar('iCal_' + j['cuon_username'])
                    
        if dicResult and dicResult not in ['NONE','ERROR']:
            z1 = len(dicResult)
            z2 = 0
            self.writeLog('Len of new icals = ' + `z1`,999)
            
            for i in dicResult:
                if fromDate == 'All':
                    self.iCal.addEvent(i['user_id'],i,dicUser, True)
                else:
                    self.iCal.addEvent(i['user_id'],i,dicUser, False)
                z2 += 1
                self.writeLog('new icals  ' + `z2` + ' from ' + `z1`,999)
                
        return ok
    
    def xmlrpc_cron_create_iCal2(self, sName):
            
        self.writeLog( 'cron_create_iCal, user = ' + sName)
        ok = True
        dicUser = {}
        dicUser['Name'] = sName
        sSql = 'select * from partner_schedul where sep_info_3 = 5 '
        self.writeLog(sSql)
        dicResult = self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
        #self.writeLog(dicResult)
        if dicResult and dicResult not in ['NONE','ERROR']:
            for i in dicResult:
                self.iCal.addEvent(i['user_id'],i,dicUser)
                sSql = 'update partner_schedul set sep_info_3 = 2 where id = ' + `i['id'] `
                dicResult2 = self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
        return ok
