# -*- coding: utf-8 -*-

##Copyright (C) [2003]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 
from cuon.Databases.SingleData import SingleData
import logging
import threading

class SingleMisc(SingleData):

    
    def __init__(self, allTables):

        SingleData.__init__(self)
        # tables.dbd and address
        self.sNameOfTable =  "addresses_misc"
        self.xmlTableDef = 0
        self.loadTable(allTables)

        #self.athread = threading.Thread(target = self.loadTable())
        #self.athread.start()
        
        self.listHeader['names'] = []
        self.listHeader['size'] = []
        self.out( "number of Columns ")
        self.out( len(self.table.Columns))
        #
        self.addressId = 0
        
    def readNonWidgetEntries(self, dicValues):
        print 'readNonWidgetEntries(self) by SinglePartner'
        dicValues['address_id'] = [self.addressId, 'int']
        return dicValues

    
