##Copyright (C) [2003]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 
# -*- coding: utf-8 -*-

import sys
from types import *
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import SingleData, cyr_load_table, cyr_table, cyr_column
import SingleImportZip
from cuon.Windows.windows import windows
import cuon.Windows.cyr_load_entries
import cuon.TypeDefs.typedefs_server
import cuon.XMLRPC.xmlrpc
import string
import cPickle
import sys
import cuon.Databases.import_generic1
import cuon.Databases.import_generic2
import  cuon.Databases.SingleCuon


class databaseswindow(windows):
    """
    @author: Jürgen Hamel
    @organization: Cyrus-Computer GmbH, D-32584 Löhne
    @copyright: by Jürgen Hamel
    @license: GPL ( GNU GENERAL PUBLIC LICENSE )
    @contact: jh@cyrus.de
    """
    
    def __init__(self):
        windows.__init__(self)
        self.openDB()
        self.td = self.loadObject('td')
        self.closeDB()
        
        self.gladeName = self.td.databases_glade_name

        # self.setLogLevel(self.INFO)
        self.allTables = {}
        
        self.xml = gtk.glade.XML(self.gladeName)
        self.setXmlAutoconnect()

#        self.xml.signal_autoconnect({ 'on_close1_activate' : self.on_close1_activate} )
#        self.xml.signal_autoconnect({ 'on_dbcheck1_activate' : self.on_dbcheck1_activate} )
#        self.xml.signal_autoconnect({ 'on_load_defaults1_activate' : self.on_load_defaults1_activate} )

        self.rpc = cuon.XMLRPC.xmlrpc.myXmlRpc()
        self.rpc.td = self.td
        
        self.ta = self.xml.get_widget('tableImportSQLStructure')
        self.ta.hide()

        self.fd = self.xml.get_widget('zip_fileselection1')
        self.fd.hide()
        
        # User auf zope setzen
        #self.oUser.setUserName('zope')
        #self.oUser.setUserPassword('test')
        
        self.dicUser = self.oUser.getSqlDicUser()
        # set to 0 for disable 'where client =  '
        self.dicUser['client'] = 0
     
     
     
    def checkClient(self):
        pass
           

    def on_save_client1_activate(self,event):

        liAllTables = cPickle.loads(eval(self.doDecode(self.rpc.callRP('Database.getInfo', 'allTables'))))

        print `liAllTables`
        
        try:
            clt = cuon.Databases.cyr_load_table.cyr_load_table()
            for lt in liAllTables:
                self.allTables[lt] =  clt.loadTable(lt)
        except Exception, param:
            print 'ERROR '
            print Exception
            print param
            
            
        sc = cuon.Databases.SingleCuon.SingleCuon(self.allTables)
        f = file('version','r')
        s = f.readline()
        s1 = s.split()
        n1 = s1[0].strip()
        v1 = s1[1].strip()
        sFile = s1[2].strip()
        f.close()
        print s1
        
        try:
            f = file(sFile,'rb')
            b = f.read()
            f.close()
            print 'Read by saveClient f = ', sFile
            print 'len = ', len(b)
            
            dicValues = {'name':[n1,'string'],'version' : [v1,'string'], 'clientdata':[b,'app']}
            sc.newRecord()
            sc.saveExternalData(dicValues,['clientdata'])

        except Exception, param:
            print "Error open Versionsfile"
            print Exception
            print param
 
                                
                            
        
    
    def on_close1_activate(self, event):
        win1 = self.xml.get_widget('DatabasesMainwindow')
        win1.hide()


    def on_dbcheck1_activate(self, event):
        clt = cyr_load_table.cyr_load_table()
        ### for Server-functions set the td-object
        clt.td = self.td
        tableList = []
        for key in self.td.nameOfXmlTableFiles.keys():
            print  "start check for : " + `key`
  
            lTable = clt.getListOfTableNames(key)
            tableList = self.startCheck(key,lTable, tableList)
            print 'check finished - now create sequences'
            lSequences = clt.getListOfSequenceNames(key)
            print 'Sequences'
            print `lSequences`
            
            liClients = self.rpc.callRP('Database.getListOfClients', self.dicUser)
            print `liClients`
            for cli in liClients:
                for s in range(len(lSequences)):
                    seq = lSequences[s]
                    print 'seq 1 ' + seq
                    seq = seq + '_client_' + `cli`
                    lSequences[s] = seq
                    print 'seq 2 ' + seq
            print `lSequences`        
            self.startCheckSequences(key,lSequences)

        print 'allTables = '
        print tableList    
        self.rpc.callRP('Database.saveInfo', 'allTables', self.doEncode(repr(cPickle.dumps(tableList) )))
        
        
    def on_trigger1_activate(self, event):
         print 'create procedures and trigger'
         
         self.createProcedureAndTrigger()
       
    def on_load_defaults1_activate(self, event):
        cle = cuon.Windows.cyr_load_entries.cyr_load_entries()
        self.out( 'before Key ')
        ### for Server-functions set the td-object
        cle.td = self.td
        for key in self.td.nameOfXmlEntriesFiles.keys():
            print 'xml = ' + key
            lEntry = cle.getListOfEntriesNames(key)
            for i in lEntry:
                self.out( i.toxml())
                sNameOfTable = key[6:(len(`key`) -7)]
                print  "sNameOfTable" , sNameOfTable 
                self.startXMLCheck(key,i , sNameOfTable)        


        print '----------------------------------------------- Glade-Files -------------------------------------------------------------------------'
        print '------------------------------------------------------------------------------------------------------------------------------------------'
        print '------------------------------------------------------------------------------------------------------------------------------------------'
        
        #save glade-files
        self.saveGladeFiles()       

        #save report-files
        self.saveReportFiles()       

        print '----------------------------------------------- Report files -------------------------------------------------------------------------'
        print '------------------------------------------------------------------------------------------------------------------------------------------'
        print '------------------------------------------------------------------------------------------------------------------------------------------'


    def on_grants1_activate(self, event):
        self.setGrants()


    def on_import_zipcode1_activate(self, event):
        self.fd.show()
        

    def on_fd_ok_button1_clicked(self,event):
        filename = self.fd.get_filename()
        self.out( filename)
        self.fd.hide()
        self.importZip(filename)
        
    def on_fd_cancel_button1_clicked(self,event):
        self.fd.hide()
            
    def on_import_generic1_activate(self,event):
        imf = cuon.Databases.import_generic1.import_generic1()

    def on_import_generic2_activate(self,event):
        imf = cuon.Databases.import_generic2.import_generic2()
       
        
    def startCheck(self, key, lTable, tableList):
 
        clt = cyr_load_table.cyr_load_table()
       ### for Server-functions set the td-object
        clt.td = self.td
        # first - the infotable cuon must be setup
        #print 'User:', self.dicUser
        ok =  self.rpc.callRP('Database.createCuon', self.dicUser)

        # now check the rest
        
        for i in lTable:
            self.out( i)
            print 'tableDefinition = ' ,key,i
            table = clt.getTableDefinition(key,i)
            print '1---clt.savetable', table.getName()
            clt.saveTable(i,table )
            print '1+++++++++++++++++++++++++++++++++++++++++++++++++++'
            
            print '2---dbcheck', table.getName()
            self.dbcheck(table)
            print '2+++++++++++++++++++++++++++++++++++++++++++++++++++'
            
            print '3---List of tables', `tableList`
            tableList.append(table.getName())
            print '3--------------------------------------------------------------------------------------'
        return tableList

    def startCheckSequences(self, key, lSequences):
        print 'start check Sequences'
        clt = cyr_load_table.cyr_load_table()
       ### for Server-functions set the td-object
        clt.td = self.td
 
        for i in lSequences:
            print 'Check this Sequence = ' , `i`
            ok =  self.rpc.callRP('Database.checkExistSequence',i, self.dicUser)
            if not ok:
                print 'create Sequence'
                iSeq = i.upper().find('_CLIENT_')
                if iSeq > 0:
                    seqname =i[0:iSeq]
                else:
                    seqname = i
                dicSeq = clt.getSequenceDefinition(key, seqname)
                print dicSeq
                sSql = "create sequence " + i
                if dicSeq['increment']:
                    sSql = sSql + ' INCREMENT ' + dicSeq['increment']
                if dicSeq['minvalue']:
                    sSql = sSql + ' MINVALUE ' + dicSeq['minvalue']
                if dicSeq['maxvalue']:
                    sSql = sSql + ' MAXVALUE ' + dicSeq['maxvalue']
                if dicSeq['start']:
                    sSql = sSql + ' START ' + dicSeq['start']
                if dicSeq['cache'] != '0':
                    sSql = sSql + ' CACHE ' + dicSeq['cache']
                if dicSeq['cycle'] == 'Yes':
                    sSql = sSql + ' CYCLE ' 


                    
                self.out( sSql)
                print 'Sql Sequence = ', sSql
                self.rpc.callRP('Database.xml_executeNormalQuery', sSql, self.dicUser)
        


    def dbcheck(self, table):
        self.out("check Databases")
        #ok = self.rpc.callRP('src.Databases.py_packCuonFS')
        ok = self.rpc.callRP('Database.checkExistTable',table.getName(), self.dicUser)
        self.out("ok = " + `ok`,1)
        
        if ok == 0:
            # create table
            self.createTable(table)
        
        self.checkColumn(table)
        

    def createTable(self, table):
        self.out( table.getName())
        self.out( table.getSpecials())

        sSql = 'create table ' + str(table.getName()) + ' () ' 
        
        if  table.getSpecials() :
               sSql = sSql + str(table.getSpecials())

        sSql1 = string.replace(sSql,';',' ')    
        self.out( sSql1)
        
        self.rpc.callRP('Database.executeNormalQuery',sSql1, self.dicUser)

        # create the sequence
        
        sSql1 = "create sequence " + str(table.getName()) +"_id " 
        self.out( sSql1)
   
        self.rpc.callRP('Database.executeNormalQuery',sSql1, self.dicUser)

 


    def checkColumn(self, table):
        
        for i in range(len(table.Columns)):
            co = table.Columns[i]
            self.out( ('Name OfColumn : ' + str(co.getName() ) ) )
            #print `self.dicUser`
            ok = self.rpc.callRP('Database.checkExistColumn',table.getName(), co.getName() , self.dicUser)
            self.out("column-ok = " + str(ok),1)
            
            if ok == 0:
                print "column-ok = " + str(ok) + ' , Column must be created' 

                # create Column
                print 'create Column ' + str(co.getName())
                self.createColumn(table, co)
            else:
                print 'Column exist, now check Column Type'
                ok = self.rpc.callRP('Database.checkTypeOfColumn',table.getName(), co.getName(), co.getType(), co.getSizeOfDatafield() , self.dicUser )

                
                self.out("column-ok = " +`co.getType()` + ', ' + ` co.getSizeOfDatafield()` + ', -- ' +  str(ok),1)
                print "column-ok = " +`co.getType()` + ', ' + ` co.getSizeOfDatafield()` + ', -- ' +  str(ok) 
                if ok == 0:
                    print 'Column Type false, modify !'
                    # change column
                    self.modifyColumn(table, co)
                
        
            
    def createColumn(self, table, co):
        self.out( co.getName())

        
        sSql = 'alter table ' + str(table.getName()) + ' add column  ' + co.getName() + ' ' + co.getType()
        if (string.find(co.getType(), 'char' )>= 0 ) :
            # find char, so take size to it
            sSql = sSql + '(' + str(co.getSizeOfDatafield()) +') '
        if (string.find(co.getType(), 'numeric' )>= 0 ) :
            # find numeric, so take size to it
            print '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
            sSql = sSql + '(' + str(co.getSizeOfDatafield()) +') '
            print sSql
            print '----------------------------------------------------------------'
        if  co.isAllowNull()  == 0 :
            self.out( co.isAllowNull())
            sSql = sSql + ' not null '

        if co.getPrimaryKey() == 1:
            sSql = sSql + ' PRIMARY KEY '
            
        print sSql
        
        self.rpc.callRP('Database.executeNormalQuery',sSql, self.dicUser)

        if co.getDefaultValue():
            sSql = 'alter table ' + str(table.getName()) + ' alter column  ' + co.getName()
            sSql = sSql + " SET DEFAULT " + co.getDefaultValue()

        self.rpc.callRP('Database.executeNormalQuery',sSql, self.dicUser)
    
    #
    # start xml defaults, entries, etc.
    #

    def modifyColumn(self, table, co):
        pass
    
 
 
    def startXMLCheck(self, key, lEntry, sNameOfTable):
        self.out( 'XML-Check')
        self.out( key)
        self.out( lEntry)
        self.out( '------------------------------------------------------------------------------------')
        
        cle = cuon.Windows.cyr_load_entries.cyr_load_entries()
        ### for Server-functions set the td-object
        cle.td = self.td
         
        entrySet = cle.getEntriesDefinition(key,lEntry, sNameOfTable)
        self.out( 'entry-Set = ' + str(entrySet.getName()))
        cle.saveEntries('entry_' + entrySet.getName() + '.xml', entrySet )
        self.out( 'end startXMLCheck')
        #ok = self.rpc.callRP('src.Databases.py_packCuonFS')    

       
    def saveGladeFiles(self):

        self.out( 'start save glade-files to zodb')
        self.out( self.td.nameOfGladeFiles, self.INFO)
        nameOfGladeFiles = []
        for key in self.td.nameOfGladeFiles.keys():
            self.out( 'xml = ' + key, self.INFO)
            print  'glade-xml = ' + key
            
            gladeName = self.td.nameOfGladeFiles[key]
            self.out( 'gladename = ' + `gladeName`, self.INFO)
            print 'gladename = ' + `gladeName`
            f1 = open(gladeName)
            xml1 = f1.read()
            f1.close()
            self.rpc.callRP('Database.saveInfo',key, self.doEncode(repr(cPickle.dumps(xml1) )))
            nameOfGladeFiles.append(key)

        self.rpc.callRP('Database.saveInfo', 'nameOfGladeFiles', self.doEncode(repr(cPickle.dumps(nameOfGladeFiles) )))
#        ok = self.rpc.callRP('src.Databases.py_packCuonFS')

    def saveReportFiles(self):

        self.out( 'start save report-files to zodb')
        self.out( self.td.nameOfReportFiles, self.INFO)
        nameOfReportFiles = []
        for key in self.td.nameOfReportFiles.keys():
            self.out( 'xml = ' + key, self.INFO)
            reportName = self.td.nameOfReportFiles[key]
            self.out( 'reportname = ' + `reportName`, self.INFO)
            f1 = open(reportName)
            xml1 = f1.read()
            f1.close()
            self.rpc.callRP('Database.saveInfo', key, self.doEncode(repr(cPickle.dumps(xml1) )))
            nameOfReportFiles.append(key)

        self.rpc.callRP('Database.saveInfo', 'nameOfReportFiles', self.doEncode(repr( cPickle.dumps(nameOfReportFiles) )))
   
#        ok = self.rpc.callRP('src.Databases.py_packCuonFS')
   
    def importZip(self, filename):
        zip = open(filename)
        line = zip.readline()
        singleImportZip = SingleImportZip.SingleImportZip()
        sTypes1 = u'string'
        sTypes2 = u'float'
        
        while line:
            if line[0] != '#' and line[0] != ' ':
                line = line.decode("latin-1")
                line = line.encode("utf-7")
                
                zips = {}
                self.out( line)
                iStart = 0
                iEnd = 0
                iEnd = string.find(line, ';')
                zips['Country'] = [string.strip(line[iStart:iEnd]), sTypes1]

                iStart = iEnd +1 
                iEnd = string.find(line, ';', iStart )
                zips['State'] = [string.strip(line[iStart:iEnd]), sTypes1]

                iStart = iEnd +1 
                iEnd = string.find(line, ';', iStart )
                zips['AdministrativeDistrict'] = [string.strip(line[iStart:iEnd]), sTypes1]

                iStart = iEnd +1 
                iEnd = string.find(line, ';', iStart )
                zips['County'] = [string.strip(line[iStart:iEnd]), sTypes1]

                iStart = iEnd +1 
                iEnd = string.find(line, ';', iStart )
                zips['Management'] = [string.strip(line[iStart:iEnd]), sTypes1]

                iStart = iEnd +1 
                iEnd = string.find(line, ';', iStart )
                zips['City'] = [string.strip(line[iStart:iEnd]), sTypes1]

                iStart = iEnd +1 
                iEnd = string.find(line, ';', iStart )
                zips['District'] = [string.strip(line[iStart:iEnd]), sTypes1]

                iStart = iEnd +1 
                iEnd = string.find(line, ';', iStart )
                zips['Longitude'] = [string.strip(line[iStart:iEnd]), sTypes2]
                zips['Longitude'] = [ string.replace(zips['Longitude'][0],',','.'), zips['Longitude'][1] ]
                
                iStart = iEnd +1 
                iEnd = string.find(line, ';', iStart )
                zips['Latitude'] = [string.strip(line[iStart:iEnd]), sTypes2]
                zips['Latitude'] =  [string.replace(zips['Latitude'][0],',','.'), zips['Latitude'][1] ]
                
                iStart = iEnd +1 
                iEnd = string.find(line, ';', iStart )
                # zips['Car'] = [string.strip(line[iStart:iEnd]), sTypes1]

                iStart = iEnd +1 
                zips['Zipcode'] = [string.strip(line[iStart:len(line)-2]), sTypes1]

                self.out( zips)
                singleImportZip.Zips = zips
                singleImportZip.newRecord()
                singleImportZip.save()
                
                
                
            line = zip.readline()


        
    
    def setGrants(self):
        self.out("set grants")
        self.out(self.td.nameOfXmlGrantFiles)
        for key in self.td.nameOfXmlGrantFiles.keys():
            print 'xml = ' + key
            doc = self.readDocument(self.td.nameOfXmlGrantFiles[key])
            # groups
            if doc:
                cyRootNode = self.getRootNode(doc)
                cyNode = self.getNode(cyRootNode,'groups')
                cyNodes = self.getNodes(cyNode[0],'group')
                if cyNodes:
                    for i in cyNodes:
                        groupNode = self.getNodes(i,'nameOfGroup')
                        group = self.getData(groupNode[0])
                        self.out(group)
                        print 'group = ' + `group`
                        print `self.dicUser`
                        ok = self.rpc.callRP('Database.createGroup', group, self.dicUser)       
                        self.out(ok)

            # user
            if doc:
                cyRootNode = self.getRootNode(doc)
                cyNode = self.getNode(cyRootNode,'users')
                cyNodes = self.getNodes(cyNode[0],'user')
                self.out('CyNodes' + `cyNodes`) 
                if cyNodes:
                    for i in cyNodes:
                        userNode = self.getNodes(i,'nameOfUser')
                        user = self.getData(userNode[0])
                        self.out('User = ' + `user`)
                        print 'User = ' + `user`
                        ok = self.rpc.callRP('Database.createUser', user,'None', self.dicUser, 1)       
                        self.out(ok)


            # add user to group
            if doc:
                cyRootNode = self.getRootNode(doc)
                cyNode = self.getNode(cyRootNode,'addgroups')
                cyNodes = self.getNodes(cyNode[0],'addgroup')
                self.out('CyNodes' + `cyNodes`) 
                if cyNodes:
                    for i in cyNodes:
                        userNode = self.getNodes(i,'this_user')
                        user = self.getData(userNode[0])
                        groupNode = self.getNodes(i,'this_group')
                        group = self.getData(groupNode[0])
                        self.out('User = ' + `user` + ' , Group = ' + group)
                        ok = self.rpc.callRP('Database.addUserToGroup', user, group, self.dicUser)       
                        self.out(ok)

            # add grants to group
            if doc:
                cyRootNode = self.getRootNode(doc)
                cyNode = self.getNode(cyRootNode,'setGrants')
                cyNodes = self.getNodes(cyNode[0],'grant')
                self.out('CyNodes' + `cyNodes`) 
                if cyNodes:
                    for i in cyNodes:
                        grantNode = self.getNodes(i,'this_grants')
                        grants = self.getData(grantNode[0])
                        tableNode = self.getNodes(i,'this_tables')
                        tables = self.getData(tableNode[0])
                        groupNode = self.getNodes(i,'this_group')
                        group = self.getData(groupNode[0])
                        print'Grants = ' + `grants` + ' , Group = ' + group + ', Tables = ' + tables
                        ok = self.rpc.callRP('Database.addGrantToGroup', grants, group, tables, self.dicUser)       
                        self.out(ok)
                                                                    
                        

    def createProcedureAndTrigger(self):
        self.setLogLevel(0)
        self.out("set procedures and trigger")
        self.out(self.td.nameOfXmlSQLFiles)
        for key in self.td.nameOfXmlSQLFiles.keys():
            self.out( 'xml = ' + key)
            doc = self.readDocument(self.td.nameOfXmlSQLFiles[key])
            # procedures
            if doc:
                cyRootNode = self.getRootNode(doc)
                cyNode = self.getNode(cyRootNode,'postgre_sql')
                cyNodes = self.getNodes(cyNode[0],'function')
                if cyNodes:
                    for i in cyNodes:
                        self.out("Werte in xml")
                                                
                        funcNode = self.getNodes(i,'nameOfFunction')
                        newName = self.getData(funcNode[0])
                        self.out(newName)

                        funcNode = self.getNodes(i,'old_name')
                        oldName = self.getData(funcNode[0])
                        self.out(oldName)

                        funcNode = self.getNodes(i,'language')
                        sql_lang = self.getData(funcNode[0])
                        self.out(sql_lang)

                        funcNode = self.getNodes(i,'textOfFunction')
                        func = self.getData(funcNode[0])
                        self.out(func)
                        # first delete the function ( specified in Old_name )
                        sSql = 'DROP FUNCTION ' + oldName + ' CASCADE'
                        #ok = self.rpc.callRP('Database.createPsql', 'cuon','sat1','5432','jhamel', sSql)
                        self.out("td-values")
                        self.out(self.td.SQL_DB)
                        self.out(self.td.SQL_HOST)
                        self.out(self.td.SQL_PORT)
                        self.out(self.td.SQL_USER)
                        self.out(sSql)
                        
                        ok = self.rpc.callRP('Database.createPsql', self.td.SQL_DB,self.td.SQL_HOST,self.td.SQL_PORT, self.td.SQL_USER, sSql)       
                        self.out(ok)
                        print sSql                       
                        print ok

                        
                        sSql = 'CREATE FUNCTION ' + newName + ' AS \'  '  
                        sSql = sSql + func
                        sSql = sSql + ' \''
                        sSql = sSql + ' LANGUAGE \'' + sql_lang + '\'; '
                        self.out('sql = ' + sSql)
                        sSql = string.replace(sSql,';', '\\;')
                        ok = self.rpc.callRP('Database.createPsql', self.td.SQL_DB,self.td.SQL_HOST,self.td.SQL_PORT, self.td.SQL_USER, sSql)
                        self.out(ok)
                        print sSql                       
                        print ok


                # Trigger
                cyNodes = self.getNodes(cyNode[0],'trigger')
                if cyNodes:
                    for i in cyNodes:
                        self.out("Werte in xml")
                                                
                        triggerNode = self.getNodes(i,'nameOfTrigger')
                        newName = self.getData(triggerNode[0])
                        self.out(newName)

                        triggerNode = self.getNodes(i,'table')
                        table = self.getData(triggerNode[0])
                        self.out(table)

                        triggerNode = self.getNodes(i,'action')
                        action = self.getData(triggerNode[0])
                        self.out(action)

                        triggerNode = self.getNodes(i,'cursor')
                        cursor = self.getData(triggerNode[0])
                        self.out(cursor)

                        triggerNode = self.getNodes(i,'textOfTrigger')
                        triggerText = self.getData(triggerNode[0])
                        self.out(triggerText)

                        
                        # first delete the trigger called newName
                        sSql = 'DROP TRIGGER ' + newName
                        
                        ok = self.rpc.callRP('Database.createPsql', self.td.SQL_DB,self.td.SQL_HOST,self.td.SQL_PORT, self.td.SQL_USER, sSql)       
                        self.out(ok) 
                        print sSql                       
                        print ok

                        #then create the trigger called newName
                        sSql = 'CREATE TRIGGER ' + newName + ' '
                        sSql = sSql + action + ' ON ' + table
                        sSql = sSql + ' ' + cursor + ' ' + triggerText 
                        
                        ok = self.rpc.callRP('Database.createPsql', self.td.SQL_DB,self.td.SQL_HOST,self.td.SQL_PORT, self.td.SQL_USER, sSql)       
                        self.out(ok)
                        print sSql                       
                        print ok

