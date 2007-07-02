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
        ok = self.iCal.addEvent( sName, firstRecord, dicUser)
        print ok 
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
