import time
from datetime import datetime
import random
import xmlrpclib
from twisted.web import xmlrpc
 
from basics import basics
import Database

class Projects(xmlrpc.XMLRPC, basics):
    def __init__(self):
        basics.__init__(self)
        self.oDatabase = Database.Database()
        
        



    def xmlrpc_checkExistModulProject(self, dicUser, dicProject):
        print 'check Exist Modul Project '
        sSql = 'select * from projects where modul_project_number = ' + `dicProject['ModulProjectNumber']` + ' and modul_number = ' + `dicProject['ModulNumber']`
        sSql += self.getWhere(None,dicUser,2)
        dicResult = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser )
        self.writeLog( 'Project99 = ' + `dicResult`) 
        return dicResult
        
        
    def xmlrpc_createNewProject(self,dicUser,dicProject):
        self.writeLog( 'create new Project')
        self.writeLog(dicProject)
        dicValues = {}
        if dicProject.has_key('ModulProjectNumber'):
            dicValues['modul_project_number'] = [dicProject['ModulProjectNumber'],'int']
        if dicProject.has_key('ModulNumber'):
            dicValues['modul_number'] = [dicProject['ModulNumber'],'int']
        if dicProject.has_key( 'Number'):   
            dicValues['number'] = [dicProject['Number'],'string']
        dicValues['customer_id'] = [dicProject['addressid'],'int']
        #print 'Locales:', dicUser['Locales']
        #print 'Dateformatstring', dicUser['DateformatString']
##        if dicProject.has_key('Projectedat'):
##                            
##            try:
##                dO = time.strptime(dicProject['Projectedat'], dicUser['DateformatString'])
##                dD = time.strptime(dicProject['deliveredat'], dicUser['DateformatString'])
##                dicValues['Projectedat'] = [`dO[0]`+'/'+ `dO[1]` + '/'+ `dO[2]`,'date']
##                dicValues['deliveredat'] = [`dD[0]`+'/'+ `dD[1]` + '/'+ `dD[2]`,'date']
##            except:
##                pass
##        else:
##            dicValues['Projectedat'] = [time.strftime('%m/%d/%Y', time.localtime()),'date']
##            
        self.writeLog(dicValues)
        dicResult =  self.oDatabase.xmlrpc_saveRecord('projects', -1, dicValues, dicUser, 'NO')
        
        # todo --> convert to resources
        if dicProject.has_key('Positions'):
            for position in dicProject['Positions']:
                position['Projectid'] = [dicResult[0]['last_value'],'int']
                print '-----------------------------------------------'
                print 'Position = ', position
                print ':::::::::::::::::::::::::::::::::::::::::::::::'
                dicResult2 =  self.oDatabase.xmlrpc_saveRecord('projectposition', -1, position, dicUser, 'NO')

        
        
        
        return dicResult
        
