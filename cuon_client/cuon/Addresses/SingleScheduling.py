# -*- coding: utf-8 -*-

##Copyright (C) [2003]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 
from cuon.Databases.SingleData import SingleData
import logging
import threading
import threading
import string


class SingleScheduling(SingleData):

    
    def __init__(self, allTables):

        SingleData.__init__(self)
        # tables.dbd and address
        self.sNameOfTable =  "partner_schedul"
        self.xmlTableDef = 0
        self.loadTable(allTables)
        #self.athread = threading.Thread(target = self.loadTable())
        #self.athread.start()
        
        self.listHeader['names'] = ['name', 'zip', 'city', 'Street', 'ID']
        self.listHeader['size'] = [25,10,25,25,10]
        self.out( "number of Columns ")
        self.out( len(self.table.Columns))
        #
        self.partnerId = 0
        
	

    def readNonWidgetEntries(self, dicValues):
        dicValues['partnerid'] = [self.partnerId, 'int']
        return dicValues
    def getPartnerID(self):
        id = 0
        if self.firstRecord.has_key('partnerid'):
             id = self.firstRecord['partnerid']
        return id 
        
    def getShortRemark(self):
        s = None
        if self.firstRecord.has_key('short_remark'):
             s = self.firstRecord['short_remark']
        return s
        
    def getShortRemark(self):
        s = None
        if self.firstRecord.has_key('short_remark'):
             s = self.firstRecord['short_remark']
        return s    
    
    def getNotes(self):
        s = None
        if self.firstRecord.has_key('notes'):
             s = self.firstRecord['notes']
        return s    
    


    def fillExtraEntries(self, oneRecord):
        if oneRecord.has_key('schedul_datetime'):
            print '-----------------------------------------------------'
            print 'Schedul-Time: ', oneRecord['schedul_datetime']
            liDate = string.split(oneRecord['schedul_datetime'])
            if liDate:
                try:
                    assert len(liDate) == 2
                    eDate = self.getWidget('eDate')
                    eTime = self.getWidget('eTime')
                    eDate.set_text(liDate[0])
                    eTime.set_text(liDate[1])
                    #(liDate[1])
                    
                except:
                    print 'error in Date'
                    
                
        else :
            print `oneRecord`
            
    
