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


class SingleOrderPayment(SingleData):

    
    def __init__(self, allTables):

        SingleData.__init__(self)
        # tables.dbd and address
        self.sNameOfTable =  "in_payment"
        self.xmlTableDef = 0
        # self.loadTable()
        # self.saveTable()

        self.loadTable(allTables)
        self.setStore( gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING,  gobject.TYPE_UINT) )
        self.listHeader['names'] = ['number', 'designation', 'ID']
        self.listHeader['size'] = [25,10,25,25,10]
        print "number of Columns "
        print len(self.table.Columns)
        #
        self.invoiceNumber = 0
        self.orderID = 0
        
        
    def fillOtherEntries(self, oneRecord):
        # get total sum for this orderID
        eTotalSum = self.getWidget('ePaymentInvoiceAmount')
        # all inpayments of this Order
        eTotalPayment = self.getWidget('ePaymentPayments')
        
        try:
            
            eTotalSum.set_text( self.rpc.callRP('Order.getTotalSumString', self.orderID, self.dicUser))
            self.loading = False
            eTotalPayment.set_text( self.rpc.callRP('Finances.getTotalInpaymentString', self.orderID, self.dicUser))
            
        except Exception, params:
            print Exception, params
        self.loading = False 
        
    def readNonWidgetEntries(self, dicValues):
        print 'readNonWidgetEntries(self) by SinglePayment'
        dicValues['order_id'] = [self.orderID, 'int']
        dicValues['invoice_number'] = [self.invoiceNumber,'int']
        
        return dicValues
 
    #def fillOtherEntries(self, oneRecord):
        