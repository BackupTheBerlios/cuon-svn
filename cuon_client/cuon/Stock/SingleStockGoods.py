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
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import gobject
#from gtk import TRUE, FALSE


class SingleStockGoods(SingleData):
    """
    @author: Jürgen Hamel
    @organization: Cyrus-Computer GmbH, D-32584 Löhne
    @copyright: by Jürgen Hamel
    @license: GPL ( GNU GENERAL PUBLIC LICENSE )
    @contact: jh@cyrus.de
    """

    
    def __init__(self, allTables):

        SingleData.__init__(self)
        # tables.dbd and address
        self.sNameOfTable =  "stock_goods"
        self.xmlTableDef = 0
        # self.loadTable()
        # self.saveTable()

        self.loadTable(allTables)
        self.setStore( gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING,  gobject.TYPE_UINT) )
        self.listHeader['names'] = ['number', 'designation', 'ID']
        self.listHeader['size'] = [25,10,25,25,10]
        print "number of Columns "
        print len(self.table.Columns)
        self.stock_id = 0
        self.article_id = 0
        
 
    def readNonWidgetEntries(self, dicValues):
        print 'readNonWidgetEntries(self) by SingleStockGoods'
        dicValues['stock_id'] = [self.stock_id, 'int']
        #dicValues['article_id'] = [self.article_id, 'int']
        return dicValues
