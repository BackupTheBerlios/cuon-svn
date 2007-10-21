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
        
    
    def xmlrpc_getProjectsForAddress(self, address_id, dicUser):
        sSql = ' select id, name,designation, project_starts_at as date from projects '
        sSql += " where customer_id = " + `address_id` + " "
        sSql += self.getWhere(None,dicUser,2)
        return self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
        
    # Stats 
    def xmlrpc_getStatRep(self, dicUser):
        result = {}
        REP_ID = None
        WITHOUT_ID = None
        MIN_SCHEDUL_YEAR = '2003'
        try:
                       
            cpServer, f = self.getParser(self.CUON_FS + '/user.cfg')
            #print cpServer
            #print cpServer.sections()
            
            REP_ID = self.getConfigOption('STATS','REP_ID', cpServer)
            WITHOUT_ID = self.getConfigOption('STATS','WITHOUT_ID', cpServer)
        
        except:
            pass
            

        if REP_ID:
            lirep = REP_ID.split(',')
            liSql = []
            liSql.append({'id':'day','sql':'doy','logic':'='})
            liSql.append({'id':'week','sql':'week','logic':'='})
            liSql.append({'id':'month','sql':'month','logic':'='})
            liSql.append({'id':'quarter','sql':'quarter','logic':'='})
            liSql.append({'id':'year','sql':'year','logic':'='})
            liSql.append({'id':'decade','sql':'decade','logic':'='})
            liSql.append({'id':'century','sql':'century','logic':'='})

            for rep in lirep:
                rep_name = None
                sSql = 'select cuon_username from staff where staff.id = ' + rep 
                res1 = self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
                if res1 and res1 not in ['NONE','ERROR']:
                    rep_name = res1[0]['cuon_username']
                if rep_name:    
                    sSql = "select '" + rep_name + "' as rep_name_" + rep + " ,"
                    for vSql in liSql:
                        for z1 in range(-5,20):
                            if vSql['id'] == 'decade' and z1 > 4:
                                pass
                            elif vSql['id'] == 'century' and z1 > 1:
                                pass 
                            elif vSql['id'] == 'year' and z1 > 5:
                                pass 
                            elif vSql['id'] == 'quarter' and z1 > 9:
                                pass 
                            elif vSql['id'] == 'month' and z1 > 14:
                                pass     
                            elif vSql['id'] == 'week' and z1 > 9:
                                pass     
                            
                            else:
                                sSql += "(select  count(ps.id) from projects as ps, address as a,  where a.id = ps.customer_id and a.rep_id = " + rep 
                                          
                                sSql +=  " and  date_part('" + vSql['sql'] +"',ps.project_start_at) " + vSql['logic']+"  date_part('" + vSql['sql'] + "', now()) - " + `z1`
                                if WITHOUT_ID:
                                    liWithoutId = WITHOUT_ID.split(',')
                                    for no_id in liWithoutId:
                                        sSql += ' and a.id != ' + no_id
                                sSql += " and date_part('year',ps.project_start_at) >= " + MIN_SCHEDUL_YEAR
                                sSql += self.getWhere('',dicUser,2,'ps.')
                                sSql += ") as " + 'rep_' + rep +'_'+ vSql['id'] + '_count_' + `z1`.replace('-','M') + " , "
                                
                                #sSql += " group by a.rep_id "


                    sSql = sSql[0:len(sSql)-2]
                    self.writeLog(sSql)
                    tmpResult = self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
                    if tmpResult and tmpResult not in ['NONE','ERROR']:
                        oneResult = tmpResult[0]
                        for key in oneResult.keys():
                            result[key] = oneResult[key]
                                      
                 

##                                tmpResult = self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
##                                if tmpResult and tmpResult not in ['NONE','ERROR']:
##                                    oneResult = tmpResult[0]
##                                    for key in oneResult.keys():
##                                      result['rep_' + rep +'_'+ vSql['id'] + '_' + key + '_' + `z1` ] = oneResult[key]
##                                      
                    
                
                
            
        if not result:
            result = 'NONE'


        self.writeLog('rep-Result = ' + `result`)
        
        return result
    
    
