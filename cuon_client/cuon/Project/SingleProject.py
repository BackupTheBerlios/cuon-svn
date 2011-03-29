# -*- coding: utf-8 -*-
##Copyright (C) [2006]  [Jürgen Hamel, D-32584 Löhne]

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

class SingleProject(SingleData):

    
    def __init__(self, allTables):

        SingleData.__init__(self)
        # tables.dbd and address
        self.sNameOfTable =  "projects"
        self.xmlTableDef = 0
        #print 'allTables = ',`allTables`
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

    def getInfoForID(self,  projectID):
        liProject = []
        
        if projectID > 0:
            try:
                projectID = long(projectID)
                
                dicRecords = self.load(projectID)
        
            except:
                id = 0
                dicRecords = {}
          
            if dicRecords and dicRecords not in ['ERROR', 'NONE']:
                dicRecord = dicRecords[0]
                try:
                    liProject.append(dicRecord['name'])
                    liProject.append(dicRecord['designation'])
                    liProject.append(_('starts at: ') + `dicRecord['project_starts_at']`)
                    liProject.append(_('ends at: ') + `dicRecord['project_ends_at']`)
                    liProject.append(_('Time in days: ') + `dicRecord['time_in_days']`)
                  
                except:
                    pass
                    
            if not liProject:
                liProject.append(' ')
                liProject.append(' ')
                liProject.append(' ')
                liProject.append(' ')
                liProject.append(' ')
            
        return liProject
        
    def fillOtherEntries(self, oneRecord):
        try:
            self.getWidget('eCreatedBy').set_text(oneRecord['user_id'])
            self.getWidget('eCreatedAt').set_text(oneRecord['insert_time'])
            self.getWidget('eLastModifyBy').set_text(oneRecord['update_user_id'])
            self.getWidget('eLastModifyAt').set_text(oneRecord['update_time'])
        except Exception, params:
            print Exception, params
         
    def getCustomerID(self):
        return self.firstRecord['customer_id'] 
 
 
