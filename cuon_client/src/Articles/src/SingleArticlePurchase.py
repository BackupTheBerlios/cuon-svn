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
from gtk import TRUE, FALSE
import cuon.Addresses.SingleAddress

class SingleArticlePurchase(SingleData):

    
    def __init__(self, allTables):

        SingleData.__init__(self)
        # tables.dbd and address
        self.sNameOfTable =  "articles_purchase"
        self.xmlTableDef = 0
        # self.loadTable()
        # self.saveTable()

        self.loadTable(allTables)
        self.setStore( gtk.ListStore(gobject.TYPE_STRING,  gobject.TYPE_UINT) )
        self.listHeader['names'] = ['designation', 'ID']
        self.listHeader['size'] = [25,10]
        print "number of Columns "
        print len(self.table.Columns)
        #
        self.articlesNumber = 9
        self.liOtherEntries = []
        self.singleAddress = cuon.Addresses.SingleAddress.SingleAddress(allTables)
        

    def readNonWidgetEntries(self, dicValues):
        print 'readNonWidgetEntries(self) by SinglePurchase'
        print 'self.articlesNumber = ' + `self.articlesNumber`
        dicValues['articles_number'] = [self.articlesNumber, 'int']
        return dicValues
       
    def fillOtherEntries(self, oneRecord):
        # name of Entry with value ( addressid )
        # which SingleData ( at this point singleAddress )
        # 
        eWidget = self.getWidget('eAddressNumber')
        lAddressID = long(eWidget.get_text())
        if lAddressID > 0:
            dicRecords = self.singleAddress.load(lAddressID)
            print dicRecords
            if dicRecords:
                dicRecord = dicRecords[0]
                sLastname = dicRecord['lastname']
                eOther = self.getWidget('eAddressField1')
                eOther.set_text(sLastname)
                
                        
