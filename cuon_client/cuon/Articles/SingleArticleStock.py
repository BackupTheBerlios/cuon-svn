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



class SingleArticleStock(SingleData):

    
    def __init__(self, allTables):

        SingleData.__init__(self)
        # tables.dbd and address
        self.sNameOfTable =  "articles_stock"
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

        

    def readNonWidgetEntries(self, dicValues):
        print 'readNonWidgetEntries(self) by SinglePurchase'
        print 'self.articlesNumber = ' + `self.articlesNumber`
        dicValues['articles_number'] = [self.articlesNumber, 'int']
        return dicValues
       
    def fillOtherEntries(self, oneRecord):
        """ Fill in the separate stock informations in various fields
        @type    oneRecord: list
        @param   oneRecord: the actual record-data
        """
        print "fillOtherentries",  oneRecord
        try:
            dicStock =self.rpc.callRP('src.Stock.py_getArticleStockInfo', oneRecord['articles_number'], self.sqlDicUser)
            print dicStock
            eActual =  self.getWidget('eArticleStockActual')
            eReserved =  self.getWidget('eArticleStockReserved')
            eOffer =  self.getWidget('eArticleStockOffer')
            eFree =  self.getWidget('eArticleStockFree')

            eActual.set_text(`dicStock['actual']`)
            eReserved.set_text(`dicStock['reserved']`)
            eOffer.set_text(`dicStock['offer']`)
            eFree.set_text(`dicStock['free']`)
        except  Exception, param:
            print 'Error - fillOtherentries Article'
            print param


    def setOtherEmptyEntries(self):
        
        try:

            eActual =  self.getWidget('eArticleStockActual')
            eReserved =  self.getWidget('eArticleStockReserved')
            eOffer =  self.getWidget('eArticleStockOffer')
            eFree =  self.getWidget('eArticleStockFree')

            eActual.set_text('0')
            eReserved.set_text('0')
            eOffer.set_text('0')
            eFree.set_text('0')
        except  Exception, param:
            print 'Error - fillOtherentries Article'
            print param
                  
