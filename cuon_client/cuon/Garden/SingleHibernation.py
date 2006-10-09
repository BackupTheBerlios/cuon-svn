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
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import gobject



class SingleHibernation(SingleData):

    
    def __init__(self, allTables):

        SingleData.__init__(self)
        # tables.dbd and address
        self.sNameOfTable =  "hibernation"
        self.xmlTableDef = 0
        # self.loadTable()
        # self.saveTable()
        self.loadTable(allTables)
        self.setStore( gtk.ListStore( gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING,  gobject.TYPE_STRING, gobject.TYPE_UINT) )
        self.listHeader['size'] = [25,10,25,25,10]
        #
        self.setTreeFields( ['sequence_of_stock', 'hibernation_number', 'address.lastname as lastname', 'address.firstname as firstname'] )
        self.setTreeOrder('sequence_of_stock, hibernation_number')
        self.setListHeader([_('Stocknr'), _('Number'),_('Lastname'), _('Firstname')])
        
        #
        
    def getHibernation(self, id):
        dicRecords = self.load(id)
        liHibernation = []
        if dicRecords:
            dicRecord = dicRecords[0]
            liHibernation.append(dicRecord['number'])
            liHibernation.append(dicRecord['designation'])
            liHibernation.append (' ')
            liHibernation.append(' ')
            liHibernation.append(' ' )
        if not liHibernation:
            liHibernation.append(' ')
            liHibernation.append(' ')
            liHibernation.append(' ')
            liHibernation.append(' ')
            liHibernation.append(' ')
            
        return liHibernation

       
    def getHibernationFields(self, id):
        dicRecords = self.load(id)
        
        
    def getHibernationRecord(self, id):
        
        dicRecords = self.load(id)
        print 'dicRecords = ', dicRecords
        
        if dicRecords and len(dicRecords) >= 1:
            return dicRecords[0]
        else:
            return {}
            
        
    def getHibernationNumber(self, id):
        dicRecords = self.load(id)
        return dicRecords[0]['number']
    
