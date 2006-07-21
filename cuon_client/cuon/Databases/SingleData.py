# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

##Copyright (C) [2003]  [JÃ¼rgen Hamel, D-32584 LÃ¶hne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 

import sys
import os 
sys.path.append(os.environ['CUON_PATH'])


import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import types
import string
import datetime as DateTime
from cuon.Logging.logs import logs
from cuon.Databases.cyr_table import cyr_table
from cuon.Databases.cyr_load_table import cyr_load_table
import cuon.Databases.SingleDataTreeModel
from cuon.Windows.gladeXml import gladeXml

from cuon.XML.MyXML import MyXML
import cuon.TypeDefs.typedefs
import cuon.XMLRPC.xmlrpc
import cuon.Windows
import time
import base64
import re


class SingleData(gladeXml, logs):

    def __init__(self):
        gladeXml.__init__(self)
        logs.__init__(self)
        self.table = cyr_table()
        self.xmlTableDef = 1
        self.sNameOfTable = "EMPTY"
        self.openDB()
        self.td = self.loadObject('td')
        self.oUser = self.loadObject('User')
        self.closeDB()
        #print '##############################################################'
        #print `self.oUser.getSqlDicUser()`
        #print '**************************************************************'
        self.rpc = cuon.XMLRPC.xmlrpc.myXmlRpc()
        self.listHeader = {}
        self.dicEntries =  cuon.Windows.setOfEntries.setOfEntries()
        self.ID = 0
        self.sWhere = ''
        self.liFields = []
        self.sSort = ''
        self.store = None
        self.connectTreeId = 0
        self.sCoding = 'utf-8'
        self.sDateFormat = "%d.%m.%Y"
        self.dicUser = self.oUser.getDicUser()
        self.sqlDicUser = self.oUser.getSqlDicUser()
        
        self.path = None
        self.statusfields = []
        self.sStatus = ''
        self.firstRecord = None
        self.p1 = re.compile('\(select .*\) as')
        
    def load(self, record, dicDetail = None):
        '''
        @param record: id of the record
        @param dicDetail: details for statusbar
        @return: list of records
        '''
        try:
            assert record >= 0 and  (isinstance(record, types.IntType) or isinstance(record, types.LongType))

            if dicDetail:
                dicColumns = dicDetail
            else:
                dicColumns = {}

                for i in self.table.getColumns():
                    dicColumns[str(i.getName())] = str(i.getType())

            # self.out( '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++***')
            # self.out( self.table.getName())
            # self.out( str(self.table))
            # self.out( 'len von dicUser' + str(len(self.dicUser)) + ' --> ' + str(self.dicUser))
            # self.out( 'diccolumns = ')
            # self.out( `dicColumns`)


            liRecords = self.rpc.callRP('Database.loadRecord', self.sNameOfTable, record, self.sqlDicUser, dicColumns )
            # print liRecords
            firstRecord = {}
            if liRecords:
                for r in range(len(liRecords)) :
                     record =  liRecords[r]
                     for key in record.keys():
                         if  isinstance(record[key], types.StringType):
                             pass
                             #record[key] =  unicode(record[key], 'utf-7')
                         if isinstance(record[key], types.UnicodeType):
                             record[key] = record[key].encode(self.oUser.userEncoding)
                     liRecords[r] = record


                firstRecord = liRecords[0]
                #print ('nach user-encoding')
                #print firstRecord
                self.ID = firstRecord['id']
                self.sStatus = ''
                try:
                    if self.statusfields:
                        for i in range(len(self.statusfields)):
                            self.sStatus = self.sStatus + firstRecord[self.statusfields[i]] + ', '
                except:
                    self.printOut( 'no statusfield')
                    
            self.firstRecord = firstRecord
        except AssertionError:
            self.printOut( 'assert error')
            liRecords = None
        except Exception, param:
            self.printOut( 'Error by save Data')
            self.printOut( Exception)
            self.printOut( param)
            
        #self.printOut( liRecords    )
        return liRecords

    def getFirstRecord(self):
        return  self.firstRecord
    
   
    def findSingleId(self):
        liItems = self.getListEntries()
        if liItems:
            # self.out('---> liItems = ' + str(liItems))
            self.ID = liItems[0][0]
        else:
            self.newRecord()
        
        return self.ID
    
            

        
    def save(self, liBigEntries='NO'):
        dicValues = self.readEntries()
        id = self.saveValues(dicValues, liBigEntries)
        return id
        
    def saveExternalData(self, dicValues, liBigEntries='NO'):
        id = self.saveValues(dicValues, liBigEntries)        
        return id
    
    def saveValues(self, dicValues, liBigEntries='NO'):
        id = 0
        if liBigEntries != 'NO':
            
            for lb in liBigEntries:
                #self.printOut( 'lb = '
                #self.printOut( lb
                j = 0
                k = 2048*30
                en =  base64.encodestring(dicValues[lb][0])

                endFile = len(en)
                #self.printOut( endFile)
                while j < endFile:
                    ok = self.rpc.callRP('Database.createBigRow',lb, en[j:k] , j,  self.sqlDicUser)
                    #self.printOut( ok)
                    j = k
                    k = k + 2048*30
                    #self.printOut( j)
                    #self.printOut( k)
                dicValues[lb][0] = ' '
        else:
            self.printOut( "saveValues - self.id = ", self.ID)
            liResult = self.rpc.callRP('Database.saveRecord',self.sNameOfTable, self.ID, dicValues, self.sqlDicUser, liBigEntries)
        if self.ID < 0 and liResult:
            try:
                id = liResult[0]['last_value']
            except:
                pass

        return id
                
                
        
        self.refreshTree()

 
    def deleteRecord(self):
        self.rpc.callRP('Database.deleteRecord',self.sNameOfTable, self.ID, self.sqlDicUser )
        self.refreshTree()
         

    def loadCompleteTable(self):
        return self.rpc.callRP('Database.loadCompleteTable',self.sNameOfTable, self.sqlDicUser)
        


    def saveTable(self):
        clt = cyr_load_table()
        self.table = clt.getTableDefinition(self.xmlTableDef, self.sNameOfTable)
        clt.saveTable(self.sNameOfTable, self.table)
      #  clt.loadTable(self.sNameOfTable)


    def loadTable(self, allTables = None):
        self.printOut( 'allTables (SD)  = ',`allTables`)
        if allTables:
            self.table = allTables[self.sNameOfTable]
        else:
            clt = cuon.Databases.cyr_load_table.cyr_load_table()
            self.table =  clt.loadTable(self.sNameOfTable)
  
     
        

    # Tree-functions

    def setTree(self, tree01):
        self.tree1 = tree01
        self.fillTree(self.tree1, self.getListEntries() )
        
    def disconnectTree(self):
        self.tree1.get_selection().disconnect(self.connectTreeId)

    def connectTree(self):
        self.connectTreeId = self.tree1.get_selection().connect("changed", self.tree_select_callback)
   
    def tree_select_callback(self, treeSelection):
        # self.out( 'tree_select entered')
        listStore, self.iter = treeSelection.get_selected()
        # self.out('liststore = ' + str(listStore), self.INFO)
        # self.out('iter = ' + str(iter), self.INFO)
        
        
        if listStore and len(listStore) > 0:
           # [0] = gtk.listStore , [1] = treeiter , int = column
           #self.path = listStore[0].get_path(listStore[1])
           ## self.out('path in callback',self.INFO)
           ## self.out(str(self.path), self.INFO)
           self.row = listStore[0]
        else:
            self.row = -1
   
        if self.iter != None:
            # self.fillEntries(listStore[0].get_value(listStore[1], self.listboxId) )
            self.path = listStore.get_path(self.iter)
            newId = listStore.get_value(self.iter, self.listboxId)
            
            self.fillEntries(newId)
            
            
    def treeSelectRowById(self):
        pass
        # self.out( self.ID, self.INFO)
        
        
    def treeSelectRow(self):
        ## self.out( 'Iter: ' + str(self.listIter))
        #self.treeSelection.select_iter(self.listIter)
        #model = self.treeSelection.get_tree_view().get_model()
        #rootIter = model.get_iter_root()
        #while rootIter != None:
        #    # self.out( str(rootIter))
        #    rootIter = model.iter_next(rootIter)
        #self.treeSelection.select_path(self.ID)
        #self.treeSelection = self.tree1.get_selection()
        # self.out( 'tree selected', self.INFO)
        # self.out( str(self.tree1.get_selection()), self.INFO )
        # self.out( str(self.path) , self.INFO)
                  
        if self.tree1.get_selection() != None and self.path != None:
            # self.out('select tree by path',self.INFO)
            self.tree1.get_selection().select_path(self.path)
        
            

    def treeSelectRowByIter(self):
        if self.iter:
            self.tree1.get_selection().select_iter(self.iter)
           
    def setStore(self, store01):
        self.store = store01 

    def fillTree(self, tree1, listEntries):
        model = self.getTreeModel(listEntries)
        model.setColumns(tree1, self.listHeader)
        #iter = model.get_iter_first()
        #selection = tree1.get_selection()
        #selection.set_selection(iter)
        
    
    def refreshTree(self):
        self.setEmptyEntries()
        try:
            assert self.tree1
            self.fillTree(self.tree1, self.getListEntries() )
            self.treeSelectRow()
        except:
            self.printOut( 'no Tree exist')

    def getTreeModel(self, listEntries):
        model = cuon.Databases.SingleDataTreeModel.SingleDataTreeModel()
        if self.store:
            model.setStore(self.store)
            self.tree1.set_model(model.createModel(listEntries))
        return model

    # Entries

      # NEU (abstract), dient nur dazu, -AÃ¼berschrieben zu werden-b
    def fillExternalWidget(self, value, id):
        # self.out( "SingleData.fillExternalWidget()")
        # self.out( "Value: " + str(value))
        # self.out( "ID: " + str(id))
        return ''


    def getFirstListRecord(self):
        
        liEntries = self.rpc.callRP('Database.getListEntries',{'id': 'int'}, self.table.getName() , "id" , self.sWhere, self.sqlDicUser)
        try:
            dicEntry = liEntries[0]
            id  = dicEntry['id']
            self.load(id)
            
        except:
            self.ID = 0
            
        self.printOut( "getFirstentry", liEntries)
        
        
        
    def clearAllFields(self):
        #self.printOut( 'clear all widgets ')
        nCount = self.dicEntries.getCountOfEntries()
        
        
        for n in range(nCount):
            oneEntry = self.dicEntries.getEntryAtIndex(n)
            widget = self.getWidget(oneEntry.getName())                   
            if string.count(str(widget), "GtkEntry") > 0:
                # self.out( "GtkEntry:")
                # self.out( "Name: " + str(widget.get_name()))
                widget.set_text('')
            elif string.count(str(widget), "GtkTextView") > 0:
                buffer = gtk.TextBuffer(None)
                buffer.set_text('')
                widget.set_buffer(buffer)
            elif string.count(str(widget), "GtkCheckButton") > 0:
                widget.set_active(False)
            elif string.count(str(widget), "GtkRadioButton") > 0:
                widget.set_active(False)
                  
            elif string.count(str(widget), "GnomeDateEdit") > 0:
                newDate = time.strptime('0001/01/01', 'Y/m/d') 
                self.printOut( newDate)
                widget.set_time(int(time.mktime(newDate)))
                                           
            elif string.count(str(widget), "GtkComboBoxEntry") > 0:
                self.printOut( "Cbe", 'löschen')
                self.printOut( widget.get_name())
                
                widget.set_active(0)
    
    def fillEntries(self, id):
        self.printOut( 'id by fillentries: ',  id)
        self.ID = id
        if id < 1:
            self.clearAllFields()
        else:
            oneRecord = []
            dicRecord = self.load(id)
            self.printOut(  'Record by fillEntries: ', dicRecord)
            if dicRecord:
                oneRecord = dicRecord[0]
            if not oneRecord:
                self.clearAllFields()
            for i in range(len(oneRecord)):
                sValue = oneRecord[oneRecord.keys()[i]]
                #self.printOut( 'sValue = ', sValue)
                
                if self.dicEntries.getEntryByName(oneRecord.keys()[i]) == None:
                    #self.fillExternalWidget(oneRecord[sValue], id)
                    # self.out( "sValue: " + str(sValue))
                    # self.out( "id: " + str(id))
                    #self.fillExternalWidget(sValue, id)
                    self.fillExternalWidget(sValue, oneRecord)
                elif self.dicEntries.getEntryByName(oneRecord.keys()[i]).getCreateSql() == '0'  :
                    self.printOut( 'createSql 0= ', self.dicEntries.getEntryByName(oneRecord.keys()[i]).getCreateSql())
                    self.fillExtraEntries(oneRecord)
                else :
                    self.printOut( 'createSql 1= ', self.dicEntries.getEntryByName(oneRecord.keys()[i]).getCreateSql())
                    entry = self.dicEntries.getEntryByName(oneRecord.keys()[i])
                    # self.out( type(sValue))
                    self.printOut( sValue, type(sValue))
                    if isinstance(sValue, types.ClassType) or isinstance(sValue, types.InstanceType):
                        sValue = `sValue`
                    if entry.getVerifyType() == 'string' and isinstance(sValue, types.StringType):
                        #sValue = sValue.encode(self.sCoding)
                        pass
                    elif entry.getVerifyType() == 'int' and isinstance(sValue, types.IntType):
                        sValue = `sValue`
                    
                    elif entry.getVerifyType() == 'float' and isinstance(sValue, types.FloatType):
                        iR = entry.getRound()
                        if iR == -1:
                            iR = 2
                        sValue = "%0.*f" % (iR, sValue)
                        self.printOut( sValue)

                    elif entry.getVerifyType() == 'numeric' and isinstance(sValue, types.FloatType):
                        sValue = `round(sValue,entry.getRound())`
                       
                    elif entry.getVerifyType() == 'date' and isinstance(sValue, types.StringType):
                        #sValue = sValue.encode(self.sCoding)
                        self.printOut( 'date string = ', sValue)
                        #dt = time.strptime(sValue, "YYYY-MM-DD HH:MM:SS.ss")
                        #self.printOut( dt
                        #dt = DateTime.strptime(sValue, self.sqlDicUser['DateFormatString'])
                        #self.printOut( dt
                        #self.printOut( self.sqlDicUser['DateTimeformatString']
                        #sValue = time.strptime(sValue, self.sqlDicUser['DateFormatString'] )
                        #self.printOut( newDate
                        
                    #elif entry.getVerifyType() == 'date' and isinstance(sValue, types.StringType):
                    #    dt = DateTime.DateTimeFrom(sValue)
                    #dt = DateTime.strptime(sValue, "YYYY-MM-DD HH:MM:SS.ss")
                    #dt = DateTime.DateTime(1999)
                    #    # self.out( dt)
                    #    sValue = dt.strftime(self.sDateFormat)
                    elif entry.getVerifyType() == 'bool' :
                           pass
                    else:
                        #sValue = sValue.decode(self.sCoding)
                        sValue = str(sValue)

                    widget = self.getWidget(entry.getName())
                    # self.out( "widget: " + str(widget))
                    if string.count(str(widget), "GtkEntry") > 0:
                        # self.out( "GtkEntry:")
                        # self.out( "Name: " + str(widget.get_name()))
                        widget.set_text(sValue)
                    elif string.count(str(widget), "GtkTextView") > 0:
                        buffer = gtk.TextBuffer(None)
                        buffer.set_text(sValue)
                        widget.set_buffer(buffer)
                    elif string.count(str(widget), "GtkComboBoxEntry") > 0:
                        if sValue and int(sValue) > -1:
                            widget.set_active(int(sValue))
                        else:
                            # -1 don`t function -- proof later
                            widget.set_active(0)
                    elif string.count(str(widget), "GtkCheckButton") > 0 :
                        self.printOut( 'Bool-Value from Database', sValue)
                        self.printOut( "GtkCheckButton ", entry.getName())
                        
                        
                        if sValue == 1 or sValue == 't' or sValue == 'True': 
                            sValue = True
                            self.printOut( 'is true !')
                        else:
                            sValue = False
                            self.printOut( 'is false')
                        self.printOut( 'Widget set to ', sValue)
                        widget.set_active(sValue)
                        self.printOut( widget, widget.get_active())
                            
                    elif string.count(str(widget), "GtkRadioButton") > 0:
                        self.printOut( 'Bool-Value from Database', sValue)
                        self.printOut( "GtkCheckButton ", entry.getName())
                        
                        
                        if sValue == 1 or sValue == 't' or sValue == 'True': 
                            sValue = True
                            self.printOut( 'is true !')
                        else:
                            sValue = False
                            self.printOut( 'is false')
                            
                        self.printOut( 'Widget set to ', sValue)
                        if sValue:
                            widget.set_active(sValue)
                            
                        self.printOut( widget, widget.get_active())
                    elif string.count(str(widget), "GnomeDateEdit") > 0:
                        try:
                            self.printOut( self.sqlDicUser['DateTimeformatString'])
                            newDate = time.strptime(sValue, self.sqlDicUser['DateTimeformatString'] )
                            self.printOut( newDate)
                            widget.set_time(int(time.mktime(newDate)))
                        except:
                            self.printOut( 'ERORR - Time not match')
                            
                    elif string.count(str(widget), "GtkFileChooserButton") > 0:
                        widget.set_filename(sValue)

            self.fillOtherEntries(oneRecord)

    def fillOtherEntries(self, oneRecord):
        pass

    def fillExtraEntries(self, oneRecord):
        pass


    def readEntries(self):
        try:
            assert self.dicEntries != None 
            dicValues = {}
            # self.out("Count of Entries: " + `self.dicEntries.getCountOfEntries()`)
            for i in range(self.dicEntries.getCountOfEntries() ):
                entry =  self.dicEntries.getEntryAtIndex(i)
                try:
                    
                    # self.out('Name of entry: ' + ` entry.getName()`,  self.DEBUG)
                    self.printOut( entry.getName())
                    widget = self.getWidget(entry.getName())
                    if string.count(str(widget), "GtkEntry") > 0:
                        sValue = widget.get_text()
                    elif string.count(str(widget), "GtkTextView") > 0:
                        buffer = widget.get_buffer()
                        sValue = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), 1)
                    #elif string.count(str(widget), "GtkCombo") > 0:
                    elif string.count(str(widget), "GtkCheckButton") > 0:
                        sValue = `widget.get_active()`
                    elif string.count(str(widget), "GtkRadioButton") > 0:
                        sValue = `widget.get_active()`
                    elif string.count(str(widget), "GnomeDateEdit") > 0:
                        newTime = time.localtime(widget.get_time())
        #                self.printOut( "Datum und Zeit"
        #                self.printOut( newTime
                        #if entry.getVerifyType() == 'date':
                         #   sValue = time.strftime(self.sqlDicUser['DateformatString'], newTime)
                        #else:
                        sValue = time.strftime(self.sqlDicUser['DateTimeformatString'], newTime)
        #                self.printOut( sValue
                    elif string.count(str(widget), "GtkComboBoxEntry") > 0:
                        sValue = widget.get_active()
                        self.printOut( "GtkComboEntry", sValue)
                        self.printOut( "Text = ", widget.get_active_text())

                    elif string.count(str(widget), "GtkFileChooserButton") > 0:
                        self.printOut( "  GtkFileChooserButton ")
                        sValue =  widget.get_filename()
                        self.printOut( sValue)
                        
                    else:
                        sValue = widget.get_text()
                except Exception, param:
                        self.printOut( 'Exception Error:', param )
                        sValue = ''


                try:
                    assert entry.getCreateSql() == '1'
                    dicValues[entry.getSqlField()] = [sValue , entry.getVerifyType() ]
                except Exception, param:
                    self.printOut( 'no SQL-Field')
                    
                    
                # self.out( 'Value by sql = ' + `dicValues[entry.getSqlField()]`)

            # self.out( 'dicValue by readEntries = ')
            # self.out(  dicValues)
            #self.printOut(  'read-Entries' , dicValues )
            dicValues = self.readNonWidgetEntries(dicValues)
        except AssertionError:
            self.printOut( 'assert error')
            dicValues = None
        
        dicValues['client'] = [self.sqlDicUser['client'], 'int']
        dicValues = self.readExtraEntries(dicValues)
        dicValues = self.verifyValues(dicValues)
        #self.printOut(  'after Verify' , `dicValues`)
        return dicValues
 
    def readExtraEntries(self, dicValues):
        return dicValues
        
    def verifyValues(self, dicValues):
        try:
            assert dicValues != None
            #self.printOut( dicValues)
            for i in dicValues.keys():
                oValue = dicValues[i][0]
                sVerify = dicValues[i][1]
                
                if sVerify  == 'string':
                    # self.out( oValue)
                    if oValue:
                        pass
##                        try:
##                            oValue = oValue.encode('utf-8')
##                            
##                        except:
##                            self.out('No encoding')
                    # self.out( oValue)
                    # self.out( '++++++++++++++++++++++++++++++++++')

                elif sVerify  == 'int':
                    # self.out( oValue,self.INFO)
                    if oValue == '':
                        oValue = 0
                    # self.out( oValue, self.INFO)
                    # self.out( '++++++++++++++++++++++++++++++++++',self.INFO)
                    self.printOut( oValue)
                    if (not isinstance(oValue, types.IntType)) and isinstance(oValue, types.StringType):
                        if oValue.isdigit():
                            oValue = int(oValue)
                        else:
                            oValue = string.strip(oValue)
                            oValue = long(oValue[0:len(oValue) -1])

                    elif isinstance(oValue, types.IntType):
                        pass
                    elif isinstance(oValue, types.LongType):
                        pass

                    else:
                        oValue = 0

                elif sVerify  == 'float':
                    # self.out( oValue)
                    if oValue == '':
                        oValue = 0.0
                    # self.out( oValue)
                    # self.out( '++++++++++++++++++++++++++++++++++')
                    self.printOut( oValue)
                    if (not isinstance(oValue, types.FloatType)) and isinstance(oValue, types.StringType) :
                        oValue = string.replace(oValue,',','.')
                        oValue = float(oValue)
                    elif isinstance(oValue, types.FloatType):
                        pass
                    elif isinstance(oValue, types.IntType):
                        oValue = float(oValue)

                    else:
                        oValue = 0.0

                elif sVerify == 'date' :
                    if oValue == '':
                        oValue = '01.01.1900'
                    else:
                        self.printOut('Date by Verify:', oValue)
                        oDate =  time.strptime(oValue, self.sqlDicUser['DateformatString'])
                        oValue = time.strftime("%Y/%m/%d",oDate)
                        self.printOut('Date by Verify 2:', oValue)

                dicValues[i][0] = oValue
                dicValues[i][1] = sVerify

        except AssertionError:
            self.printOut( 'assert error')
            dicValues = None
     
        self.out("DicValues by readEntries = " + `dicValues`)
        
        return dicValues

    def readNonWidgetEntries(self, dicValues):
        # self.out( 'readNonWidgetEntries(self) by SingleData')
        return dicValues


    def setEntries(self, dicEntries01):
        # self.out( 'singleData - set Entries ++++++++++++++++++++++++++++++++++++++++++++++++++ ')
        # self.out( dicEntries01)
        self.dicEntries = dicEntries01




    
    def getEntries(self):
        # self.out( 'singleData - get Entries ++++++++++++++++++++++++++++++++++++++++++++++++++ ')
        return self.dicEntries 
      
  

            
        
    def setGladeXml(self, xml01):
        self.setXml(xml01)
            
    def setTreeFields(self, liFields01):
        self.liFields = liFields01
        self.listboxId = len(liFields01)
        self.liFields.append('id')
        # self.out( 'lifield = ' + `self.liFields`)

    def setTreeOrder(self, sSort01):
        self.sSort = sSort01

    def setListHeader(self, liNames01):
        if liNames01:
            liNames01.append('id')
            self.listHeader['names'] = liNames01
        
        
    def getListEntries(self):
        liItems = []
        dicFields = {}
        self.printOut('liFields',self.liFields)
        for i in self.liFields:
            entry = self.dicEntries.getEntryByName(i)
            self.printOut('entry = ', `entry`)
            if entry:
                dicFields[i] = entry.getVerifyType()
            elif i == 'id':
                dicFields[i] = 'int'
            else:
                dicFields[i] = 'string'

        ## self.out('dicFields = ')
        ## self.out(dicFields)
        
        if dicFields:
            self.printOut( 'SingleData - dicFields = ', `dicFields`)
            
            
            dicLists = self.rpc.callRP('Database.getListEntries',dicFields, self.table.getName() , self.sSort, self.sWhere, self.sqlDicUser)
        else:
            dicLists = {}
            
        # self.out( dicLists)
        self.printOut( 'dicLists =',  dicLists)
        
        try:
            for i in dicLists:
                liSubItems =[]
                for j in self.liFields:
                    m = self.p1.match(j)
                    self.printOut('m = ', m)
                    if m:
                        m1 = j[m.end():]
                        self.printOut('m1 = ', m1)    
                        j = m1.strip()
                        self.printOut('j = ',j)    
                    sValue = i[j]
                    self.printOut('sValue = ',sValue)
                    #if isinstance(sValue, types.StringType):
                    #    sValue = unicode(sValue, 'utf-7')
                    if isinstance(sValue, types.UnicodeType):
                        sValue = sValue.encode(self.sCoding)     
                    self.printOut( ( 'name of j = ' + `j` + 'Value = ' + `sValue`))
                    if j != 'id':
                        entry = self.dicEntries.getEntryByName(j)
                        if entry:
                            pass
                            # self.out( entry.getName())

                        else:
                            self.printOut( 'no entry with this  name found')
                            #sValue = None


                    liSubItems.append(sValue)
                liItems.append(liSubItems)
        except Exception, param:
            self.printOut( 'Error ')
            self.printOut( Exception,param)
            
                
        # self.out( '-----------------------------------------------------------------------------------------------------------------------------------')
        # self.out( liItems)
        # self.out( '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        self.printOut( 'liItems ---', `liItems`)
        return liItems
    

    def newRecord(self):
        self.ID = -1
        self.setEmptyEntries()

    def isNewRecord(self):
        ok = False
        if self.ID == -1:
            ok = True
        return ok 
        
        
        
    
    def setEmptyEntries(self):
        for i in range(self.dicEntries.getCountOfEntries() ):
            entry =  self.dicEntries.getEntryAtIndex(i)
            widget = self.getWidget(entry.getName())
            
            # self.out( "index : " + str(i))
            # self.out( "entry : " + str(entry))
            # self.out( "name  : " + str(entry.getName()))
            
            # self.out( "widget: " + str(widget))
            
            if string.count(str(widget), "GtkEntry") > 0:
                widget.set_text('')
            elif string.count(str(widget), "GtkTextView") > 0:
                # self.out( "GtkTextView")
                buffer = gtk.TextBuffer(None)
                buffer.set_text('')
                widget.set_buffer(buffer)
        self.setOtherEmptyEntries()

    def setOtherEmptyEntries(self):
        pass

        

