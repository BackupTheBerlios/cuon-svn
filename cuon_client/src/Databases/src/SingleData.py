# -*- coding: utf-8 -*-

##Copyright (C) [2003]  [Jürgen Hamel, D-32584 Löhne]

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
from gtk import TRUE, FALSE
from mx import DateTime
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
import gnome.ui
import base64


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
        self.path = None
        self.statusfields = []
        self.sStatus = ''
        self.firstRecord = None
        
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


            #liRecords = self.rpc.getServer().src.sql.py_loadRecord(self.sNameOfTable, record, self.dicUser, dicColumns)
            liRecords = self.rpc.callRP('src.sql.py_loadRecord', self.sNameOfTable, record, self.dicUser, dicColumns )
            # print liRecords

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

                if self.statusfields:
                    for i in range(len(self.statusfields)):
                        print i
                        self.sStatus = self.sStatus + firstRecord[self.statusfields[i]] + ', '

            self.firstRecord = firstRecord
        except AssertionError:
            print 'assert error'
            liRecords = None
            
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
        if liBigEntries != 'NO':
            for lb in liBigEntries:
                print 'lb = '
                print lb
                j = 0
                k = 2048*30
                en =  base64.encodestring(dicValues[lb][0])

                endFile = len(en)
                print endFile
                while j < endFile:
                    ok = self.rpc.callRP('src.sql.py_createBigRow',lb, en[j:k] , j,  self.dicUser)
                    print ok
                    j = k
                    k = k + 2048*30
                    print j
                    print k
                dicValues[lb][0] = ' '

        self.rpc.callRP('src.sql.py_saveRecord',self.sNameOfTable, self.ID, dicValues, self.dicUser, liBigEntries)
        
        self.refreshTree()

 
    def deleteRecord(self):
        self.rpc.callRP('src.sql.py_deleteRecord',self.sNameOfTable, self.ID, self.dicUser )
        self.refreshTree()
         

    def loadCompleteTable(self):
        return self.rpc.callRP('src.sql.py_loadCompleteTable',self.sNameOfTable, self.dicUser)
        


    def saveTable(self):
        clt = cyr_load_table()
        self.table = clt.getTableDefinition(self.xmlTableDef, self.sNameOfTable)
        clt.saveTable(self.sNameOfTable, self.table)
      #  clt.loadTable(self.sNameOfTable)


    def loadTable(self, allTables):
        
        self.table = allTables[self.sNameOfTable]
     
        

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
        
        
        if listStore:
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
        self.fillTree(self.tree1, self.getListEntries() )
        self.treeSelectRow()

    def getTreeModel(self, listEntries):
        model = cuon.Databases.SingleDataTreeModel.SingleDataTreeModel()
        if self.store:
            model.setStore(self.store)
            self.tree1.set_model(model.createModel(listEntries))
        return model

    # Entries

      # NEU (abstract), dient nur dazu, -Aüberschrieben zu werden-b
    def fillExternalWidget(self, value, id):
        # self.out( "SingleData.fillExternalWidget()")
        # self.out( "Value: " + str(value))
        # self.out( "ID: " + str(id))
        return ''

    
    def fillEntries(self, id):
        # self.out( id)
        self.ID = id
        if id > 0:
            dicRecord = self.load(id)
            # # self.out( dicRecord)
            oneRecord = dicRecord[0]
            for i in range(len(oneRecord)):

    
                # self.out( "dicEntries-getEntryByName: " + str(self.dicEntries.getEntryByName(oneRecord.keys()[i])))
      
                if self.dicEntries.getEntryByName(oneRecord.keys()[i]) == None:
                    #sValue = self.getEntrySqlField(oneRecord.keys()[i], id)
                    ## self.out( "oneRecord: " + str(oneRecord))
                    ## self.out( "keys: " + str(oneRecord.keys()))
                    ## self.out( "values: " + str(oneRecord.values()))
                    sValue = oneRecord.keys()[i]
                    # self.out( "#################################")
                    # self.out( "DICENTRIES: " + str(self.dicEntries.EntrySet))
                    # self.out( "#################################")
                    ## self.out( "key: " + `sValue`)
                else:
                    #entry =  self.dicEntries.getEntryAtIndex(i)
                    entry = self.dicEntries.getEntryByName(oneRecord.keys()[i])
                    # self.out( "entry: " + str(entry))
                    # self.out( "name : " + str(entry.getName()))
                    # self.out( "sql  : " + str(entry.getSqlField()))
                    # self.out( "wert : " + str(oneRecord[entry.getSqlField()]))
                    # self.out( "typ  : " + str(entry.getVerifyType()))
                    sValue = oneRecord[entry.getSqlField()]

                # NEU, s.o.
                #if i >= self.dicEntries.getCountOfEntries():
                if self.dicEntries.getEntryByName(oneRecord.keys()[i]) == None:
                    #self.fillExternalWidget(oneRecord[sValue], id)
                    # self.out( "sValue: " + str(sValue))
                    # self.out( "id: " + str(id))
                    #self.fillExternalWidget(sValue, id)
                    self.fillExternalWidget(sValue, oneRecord[sValue])
                else:
                    # Wenn nichts drin steht (eigenart von PostgreSQL)
                    # self.out( type(sValue))
                    if isinstance(sValue, types.ClassType) or isinstance(sValue, types.InstanceType):
                        sValue = `sValue`
                    if entry.getVerifyType() == 'string' and isinstance(sValue, types.StringType):
                        #sValue = sValue.encode(self.sCoding)
                        pass
                    elif entry.getVerifyType() == 'int' and isinstance(sValue, types.IntType):
                        sValue = `sValue`
                    elif entry.getVerifyType() == 'float' and isinstance(sValue, types.FloatType):
                        sValue = `sValue`
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
                    elif string.count(str(widget), "GtkCheckButton") > 0:
                        print 'Bool-Value from Database'
                        #print sValue
                        
                        if sValue :
                            print 'is true !'
                            
                        widget.set_active(sValue)
                            
                    elif string.count(str(widget), "GnomeDateEdit") > 0:
                        newDate = time.strptime(sValue, self.dicUser['DateTimeformatString'] )
                        print newDate
                        widget.set_time(int(time.mktime(newDate)))
                                           

            self.fillOtherEntries(oneRecord)

    def fillOtherEntries(self, oneRecord):
        pass

    def readEntries(self):
        try:
            assert self.dicEntries != None
            dicValues = {}
            # self.out("Count of Entries: " + `self.dicEntries.getCountOfEntries()`)
            for i in range(self.dicEntries.getCountOfEntries() ):
                entry =  self.dicEntries.getEntryAtIndex(i)
                # self.out('Name of entry: ' + ` entry.getName()`,  self.DEBUG)
                print entry.getName()
                widget = self.getWidget(entry.getName())
                if string.count(str(widget), "GtkEntry") > 0:
                    sValue = widget.get_text()
                elif string.count(str(widget), "GtkTextView") > 0:
                    buffer = widget.get_buffer()
                    sValue = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), 1)
                #elif string.count(str(widget), "GtkCombo") > 0:
                elif string.count(str(widget), "GtkCheckButton") > 0:
                    sValue = `widget.get_active()`
                elif string.count(str(widget), "GnomeDateEdit") > 0:
                    newTime = time.localtime(widget.get_time())
    #                print "Datum und Zeit"
    #                print newTime
                    sValue = time.strftime(self.dicUser['DateTimeformatString'], newTime)
    #                print sValue
                else:
                    sValue = widget.get_text()



                dicValues[entry.getSqlField()] = [sValue , entry.getVerifyType() ]
                # self.out( 'Value by sql = ' + `dicValues[entry.getSqlField()]`)

            # self.out( 'dicValue by readEntries = ')
            # self.out(  dicValues)
            print  dicValues 
            dicValues = self.readNonWidgetEntries(dicValues)

            for i in dicValues.keys():
                oValue = dicValues[i][0]
                sVerify = dicValues[i][1]

                if sVerify  == 'string':
                    # self.out( oValue)
                    oValue = oValue.encode('utf-8')
                    # self.out( oValue)
                    # self.out( '++++++++++++++++++++++++++++++++++')

                if sVerify  == 'int':
                    # self.out( oValue,self.INFO)
                    if oValue == '':
                        oValue = 0
                    # self.out( oValue, self.INFO)
                    # self.out( '++++++++++++++++++++++++++++++++++',self.INFO)
                    print oValue
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

                if sVerify  == 'float':
                    # self.out( oValue)
                    if oValue == '':
                        oValue = 0.0
                    # self.out( oValue)
                    # self.out( '++++++++++++++++++++++++++++++++++')
                    print oValue
                    if (not isinstance(oValue, types.FloatType)) and isinstance(oValue, types.StringType) :
                        oValue = string.replace(oValue,',','.')
                        oValue = float(oValue)
                    elif isinstance(oValue, types.FloatType):
                        pass
                    elif isinstance(oValue, types.IntType):
                        oValue = float(oValue)

                    else:
                        oValue = 0.0




                dicValues[i][0] = oValue
                dicValues[i][1] = sVerify

            except AssertionError:
                print 'assert error'
                dicValues = None
     
        
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
        for i in self.liFields:
            entry = self.dicEntries.getEntryByName(i)
            if entry:
                dicFields[i] = entry.getVerifyType()
            elif i == 'id':
                dicFields[i] = 'int'
            else:
                dicFields[i] = 'string'

        ## self.out('dicFields = ')
        ## self.out(dicFields)
        
        if dicFields:        
            dicLists = self.rpc.callRP('src.sql.py_getListEntries',dicFields, self.table.getName() , self.sSort, self.sWhere, self.dicUser)
        else:
            dicLists = {}
            
        # self.out( dicLists)
        print  dicLists
        try:
            for i in dicLists:
                liSubItems =[]
                for j in self.liFields:
                    sValue = i[j]
                    #if isinstance(sValue, types.StringType):
                    #    sValue = unicode(sValue, 'utf-7')
                    if isinstance(sValue, types.UnicodeType):
                        sValue = sValue.encode(self.sCoding)     
                    # print ( 'name of j = ' + `j` + 'Value = ' + `sValue`)
                    if j != 'id':
                        entry = self.dicEntries.getEntryByName(j)
                        if entry:
                            pass
                            # self.out( entry.getName())

                        else:
                            print 'no entry with this  name found'
                            sValue = None


                    liSubItems.append(sValue)
                liItems.append(liSubItems)
        except:
            print 'Error '
                
        # self.out( '-----------------------------------------------------------------------------------------------------------------------------------')
        # self.out( liItems)
        # self.out( '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        return liItems
    

    def newRecord(self):
        self.ID = -1
        self.setEmptyEntries()

        
    
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


