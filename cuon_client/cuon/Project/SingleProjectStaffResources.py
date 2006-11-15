# -*- coding: utf-8 -*-
##Copyright (C) [2006]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

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
import gtk
import gobject

class SingleProjectStaffResources(SingleData):

    
    def __init__(self, allTables):

        SingleData.__init__(self)
        # tables.dbd and address
        self.sNameOfTable =  "project_task_staff_res"
        self.xmlTableDef = 0
        #print 'allTables = ',`allTables`
        self.loadTable(allTables)
        # self.saveTable()

        #self.athread = threading.Thread(target = self.loadTable())
        #self.athread.start()
        
        self.listHeader['size'] = [25,10,25,25,10]
        self.setTreeFields( ['(select lastname from staff where id = staff_id) as staff_name','planed_working_day', 'real_working_day'] )
        self.setTreeOrder('staff_id, planed_working_day')
        self.setListHeader([_('staff'),_('planed'), _('real')])
        self.setStore( gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_UINT) ) 

        self.statusfields = ['lastname', 'city']

        self.taskId = 0
    
    def readNonWidgetEntries(self, dicValues):
        print 'readNonWidgetEntries(self) by SingleProjectStaffResources'
        dicValues['task_id'] = [self.taskId, 'int']
        return dicValues    
        
