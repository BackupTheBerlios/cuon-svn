# -*- coding: utf-8 -*-
##Copyright (C) [2005]  [Juergen Hamel, D-32584 Loehne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 
import sys
import os
#sys.path.append(os.environ['CUON_PATH'])

from cuon.Databases.SingleData import SingleData
import logging
import threading
import SingleGraveServiceNotes

class SingleGraveWinter(SingleData):

    
    def __init__(self, allTables):

        SingleData.__init__(self)
        # tables.dbd and address
        self.sNameOfTable =  "grave_work_winter"
        self.xmlTableDef = 0
        self.loadTable(allTables)
        # self.saveTable()

        #self.athread = threading.Thread(target = self.loadTable())
        #self.athread.start()
        
        self.listHeader['names'] = ['name', 'zip', 'city', 'Street', 'ID']
        self.listHeader['size'] = [25,10,25,25,10]
        self.out( "number of Columns ")
        self.out( len(self.table.Columns))
        #
        self.statusfields = ['lastname', 'city']
        self.graveID = 0
     
  
        self.singleGrave = None
        self.graveServiceID = None
        self.singleGraveNotes = SingleGraveServiceNotes.SingleGraveServiceNotes(allTables)
        
    
           
    def readNonWidgetEntries(self, dicValues):
        
        dicValues['grave_id'] = [self.graveID, 'int']
        return dicValues
        
    def saveOtherDatatable(self, id):
        text = self.readTextBuffer(self.getWidget('tvGrave'))
        self.singleGrave.save()
        self.singleGraveNotes.graveID = self.graveID
        self.singleGraveNotes.graveServiceID = self.graveServiceID 
        self.singleGraveNotes.saveSpecial(self.getWidget('tvDescriptionWinter'))
        
    def loadOtherDatatable(self, id):
        self.singleGraveNotes.graveID = self.graveID
        self.singleGraveNotes.graveServiceID = self.graveServiceID 
        self.singleGraveNotes.loadSpecial(self.getWidget('tvDescriptionWinter'))
    

        
        
