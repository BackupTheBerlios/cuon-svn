# -*- coding: utf-8 -*-

##Copyright (C) [2003]  [J�rgen Hamel, D-32584 L�hne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 

##***************************************************************************
##                          cyr_load_entries.py  -  description
##                             -------------------
##    begin                : Thu Jun 19 2003
##    copyright            : (C) 2003 by jhamel
##    email                : jhamel@cyrus.de
##***************************************************************************
from cuon.XML.MyXML import MyXML
import dataEntry
import string
import cuon.XMLRPC.xmlrpc

import cPickle
import sys
import cuon.TypeDefs.typedefs
import setOfEntries 
from cuon.Databases.dumps import dumps


class cyr_load_entries(MyXML, dumps):

    def __init__(self):
        MyXML.__init__(self)
  
        self.rpc = cuon.XMLRPC.xmlrpc.myXmlRpc()
        self.openDB()
        self.td = self.loadObject('td')
        self.closeDB()
        #self.setLogLevel(self.ERROR)
        self.configPath = "/etc/cuon/"


##        self.db = ZODB.DB(ZODB.FileStorage("cuon"))
##        self.connection = self.db.open()
##        self.root = self.connection.root()



    def getListOfEntriesNames(self, sFile):
        doc = self.getEntriesDescription(sFile)
        #        cyRootNode = self.getRootNode(doc)
        allLists = doc.getElementsByTagName("table")
        return allLists
    

    def getEntriesDescription(self, sFile):
        return  self.readDocument(self.td.nameOfXmlEntriesFiles[sFile])

        
    def getEntriesDefinition(self, sFile,  sNameOfTable, sNameOfEntries):

        doc = self.getEntriesDescription(sFile)
        self.out( doc.toxml() )
        cyRootNode = self.getRootNode(doc)

        self.out( cyRootNode[0].toxml())

        self.out( 'sNameOfTable : '  + str(sNameOfTable))
        self.out( 'sNameOfentries : '  + str(sNameOfEntries))
        
        cyEntriesNode = self.getEntry(cyRootNode, sNameOfTable, sNameOfEntries)

   
        entrySet = setOfEntries.setOfEntries()

        entrySet.setName(sNameOfEntries)


        
        iNr =  self.getNumberOfEntries(cyEntriesNode)

        self.out("Number of Columns %i "  + `iNr` )
        iCol = 0
        while (iCol < iNr):
            xmlCol = self.getEntryAt(cyEntriesNode,iCol)
            
            entry =  cuon.Windows.dataEntry.dataEntry()

            entry.setName(self.getEntrySpecification(xmlCol, "name") )
            entry.setType(self.getEntrySpecification(xmlCol, "type") )
            entry.setSizeOfEntry(self.getEntrySpecification(xmlCol, "size") )
            entry.setVerifyType(self.getEntrySpecification(xmlCol, "verify_type") )
            entry.setCreateSql(self.getEntrySpecification(xmlCol, "create_sql") )
            entry.setSqlField(self.getEntrySpecification(xmlCol, "sql_field") )
            entry.setBgColor(self.getEntrySpecification(xmlCol, "bg_color") )
            entry.setFgColor(self.getEntrySpecification(xmlCol, "fg_color") )
    

            self.out( 'entry-gets = ' + str(entry.getName())  + ', ' + str(entry.getType()))
            entrySet.addEntry(entry)
            iCol += 1

        return entrySet

    def saveEntries(self, sNameOfEntries, entries ): 

        self.out( "::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
        
        self.out( sNameOfEntries)
        self.out( entries.getName())
        self.out( cPickle.dumps(entries))
        self.out( "::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
        
        self.rpc.getServer().src.Databases.py_saveInfoOfTable(sNameOfEntries, cPickle.dumps(entries) )
        


    def loadEntries(self,sNameOfEntries):

        self.out( "::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
        self.out( "load : " + sNameOfEntries)
        self.out( "::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
        
        dictEntries = self.rpc.getServer().src.Databases.py_getInfoOfTable(sNameOfEntries)

        entries = cPickle.loads(dictEntries)   

        return entries

   
