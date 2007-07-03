# -*- coding: utf-8 -*-

##Copyright (C) [2005]  [Juergen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 

import sys
import os
import os.path
from types import *
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import gobject

import string
import logging
from cuon.Windows.windows import windows
import cPickle
#import cuon.OpenOffice.letter
# localisation
import locale, gettext
locale.setlocale (locale.LC_NUMERIC, '')
import threading
import datetime as DateTime
import SingleListOfInvoice
import SingleInpayment
import cuon.DMS.dms

class invoicebookwindow(windows):

    
    def __init__(self, allTables):

        windows.__init__(self)
       
        self.singleListOfInvoice = SingleListOfInvoice.SingleListOfInvoice(allTables)
        self.singleInpayment = SingleInpayment.SingleInpayment(allTables)
        self.singleResidue = SingleListOfInvoice.SingleListOfInvoice(allTables)
    
        self.loadGlade('invoiceBook.xml', 'InvoiceMainwindow')
        #self.win1 = self.getWidget('ListOfInvoiceMainwindow')
        #self.setStatusBar()
        self.allTables = allTables

        self.EntriesListOfInvoice = 'list_of_invoices.xml'
        
        self.loadEntries(self.EntriesListOfInvoice)
        
        self.singleListOfInvoice.setEntries(self.getDataEntries(self.EntriesListOfInvoice) )
        self.singleListOfInvoice.setGladeXml(self.xml)
        self.singleListOfInvoice.setTreeFields( ['invoice_number', 'order_number','date_of_invoice','total_amount'] )
        self.singleListOfInvoice.setStore( gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_UINT) ) 
        self.singleListOfInvoice.setTreeOrder('invoice_number,order_number')
        self.singleListOfInvoice.setListHeader([_('Invoice-Nr.'), _('Order-Nr.'), _('Date'),_('Amount')])
        self.singleListOfInvoice.setTree(self.xml.get_widget('tree1') )

  
        self.EntriesInpayment = 'inpayment.xml'
        
        self.loadEntries(self.EntriesInpayment)
        
        self.singleInpayment.setEntries(self.getDataEntries(self.EntriesInpayment) )
        self.singleInpayment.setGladeXml(self.xml)
        self.singleInpayment.setTreeFields( ['invoice_number', 'date_of_paid','inpayment','order_id'] )
        self.singleInpayment.setStore( gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_UINT) ) 
        self.singleInpayment.setTreeOrder('invoice_number,date_of_paid')
        self.singleInpayment.setListHeader([_('Invoice-Nr.'), _('Date'), _('Inpayment'),_('Order-ID')])
        self.singleInpayment.setTree(self.xml.get_widget('tree1') )

        self.EntriesResidue = 'residue.xml'
        
        self.loadEntries(self.EntriesResidue)
        
        self.singleResidue.setEntries(self.getDataEntries(self.EntriesResidue) )
        self.singleResidue.setGladeXml(self.xml)
        self.singleResidue.bDistinct = True
        sResidue = "list_of_invoices.total_amount -  (select sum(in_payment.inpayment) from in_payment where   to_number(in_payment.invoice_number,'999999999') = list_of_invoices.invoice_number and status != 'delete' and client = " + `self.dicUser['client']` + ") "
        self.singleResidue.setTreeFields( ['list_of_invoices.invoice_number as invoice_number', 'list_of_invoices.order_number as order_number','list_of_invoices.date_of_invoice as date_of_invoice','list_of_invoices.total_amount as total_amount', sResidue + " as residue "] )
        self.singleResidue.setStore( gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_UINT) ) 
        self.singleResidue.setTreeOrder('invoice_number')
        self.singleResidue.setListHeader([_('Invoice-Nr.'),_('Order-Nr.'), _('Date'),_('Amount'),_('Residue')])
        self.singleResidue.setTree(self.xml.get_widget('tree1') )
        self.singleResidue.sWhere = ",in_payment where to_number(in_payment.invoice_number,'999999999') = list_of_invoices.invoice_number and  " + sResidue + " > 0.01 "
  

        # set values for comboBox

          

        # Menu-items
        self.initMenuItems()

        # Close Menus for Tab
        self.addEnabledMenuItems('tabs','list_of_invoices1')
        self.addEnabledMenuItems('tabs','inpayment1')
        self.addEnabledMenuItems('tabs','residue1')
  

               
        # seperate Menus
        self.addEnabledMenuItems('ListOfInvoice','list_of_invoices1')
        self.addEnabledMenuItems('Inpayment','inpayment1')
        #self.addEnabledMenuItems('Residue','residue')
          

        # enabledMenues for ListOfInvoice
        
        self.addEnabledMenuItems('editListOfInvoice','new', self.dicUserKeys['new'])
        self.addEnabledMenuItems('editListOfInvoice','delete', self.dicUserKeys['delete'])
        self.addEnabledMenuItems('editListOfInvoice','print', self.dicUserKeys['print'])
        self.addEnabledMenuItems('editListOfInvoice','edit', self.dicUserKeys['edit'])

        # enabledMenues for Inpayment
        
        self.addEnabledMenuItems('editInpayment','inpayment_new1', self.dicUserKeys['new'])
        self.addEnabledMenuItems('editInpayment','inpayment_delete1', self.dicUserKeys['delete'])
        self.addEnabledMenuItems('editInpayment', 'inpayment_print1', self.dicUserKeys['print'])
        self.addEnabledMenuItems('editInpayment','inpayment_edit1', self.dicUserKeys['edit'])
        
        # enabledMenues for Residue
        
##        self.addEnabledMenuItems('editInpayment','inpayment_new1', self.dicUserKeys['new'])
##        self.addEnabledMenuItems('editInpayment','inpayment_delete1', self.dicUserKeys['delete'])
##        self.addEnabledMenuItems('editInpayment', 'inpayment_print1', self.dicUserKeys['print'])
##        self.addEnabledMenuItems('editInpayment','inpayment_edit1', self.dicUserKeys['edit'])

        # enabledMenues for Save 
        self.addEnabledMenuItems('editSave','save', self.dicUserKeys['save'])
        self.addEnabledMenuItems('editSave','inpayment_save1', self.dicUserKeys['save'])
    
        

        # tabs from notebook
        self.tabListOfInvoice = 0
        self.tabInpayment = 1
        self.tabResidue = 2
    
        
        print 'self tab changed'
        

        self.tabChanged()
        

    def checkClient(self):
        pass
        
    #Menu File
              
    def on_quit1_activate(self, event):
        print "exit ListOfInvoice V1"
        self.closeWindows()        

    


    #Menu ListOfInvoice
  
    def on_save_activate(self, event):
        print  "save invoicebook v2"
        self.singleListOfInvoice.save()
        self.setEntriesEditable(self.EntriesListOfInvoice, False)
        self.tabChanged()
        
    def on_new_activate(self, event):
        self.out( "new invoicebook v2")
        self.singleListOfInvoice.newRecord()
        self.setEntriesEditable(self.EntriesListOfInvoice, True)

    def on_edit_activate(self, event):
        self.out( "edit invoicebook v2")
        self.setEntriesEditable(self.EntriesListOfInvoice, True)


    def on_delete_activate(self, event):
        self.out( "delete invoicebook v2")
        self.singleListOfInvoice.deleteRecord()




    def on_this_month_activate(self, event):
        dBegin = self.getFirstDayOfMonthAsSeconds()
        dEnd = self.getLastDayOfMonthAsSeconds()
        print dBegin,dEnd
        self.printListOfInvoices(dBegin,dEnd)
        
    def on_last_month_activate(self, event):
        dBegin,dEnd = self.getFirstLastDayOfLastMonthAsSeconds()
        print dBegin,dEnd
        self.printListOfInvoices(dBegin,dEnd)
            
        
    def printListOfInvoices(self, dBegin, dEnd):
        dicExtraData = {}
        print ' start List of Invoices printing'
        dicExtraData['dBegin'] = dBegin
        dicExtraData['dEnd'] = dEnd
        
        print 'dicOrder = ', dicExtraData
        
        Pdf = self.rpc.callRP('Report.server_list_list_of_invoices', dicExtraData, self.dicUser)
        self.showPdf(Pdf, self.dicUser)

#Menu Inpayment
  
    def on_inpayment_save1_activate(self, event):
        print  "save invoicebook v2"
        self.singleInpayment.save()
        self.setEntriesEditable(self.EntriesInpayment, False)
        self.tabChanged()
        
    def on_inpayment_new1_activate(self, event):
        self.out( "new invoicebook v2")
        self.singleInpayment.newRecord()
        self.setEntriesEditable(self.EntriesInpayment, True)

    def on_inpayment_edit1_activate(self, event):
        self.out( "edit invoicebook v2")
        self.setEntriesEditable(self.EntriesInpayment, True)


    def on_inpayment_delete1_activate(self, event):
        self.out( "delete invoicebook v2")
        self.singleInpayment.deleteRecord()

    def on_inpayment_this_month1_activate(self, event):
        dBegin = self.getFirstDayOfMonthAsSeconds()
        dEnd = self.getLastDayOfMonthAsSeconds()
        print dBegin,dEnd
        self.printListOfInpayment(dBegin,dEnd)
    def on_inpayment_last_month1_activate(self, event):
        dBegin, dEnd = self.getFirstLastDayOfLastMonthAsSeconds()
        print dBegin,dEnd
        self.printListOfInpayment(dBegin,dEnd)
        
    def printListOfInpayment(self, dBegin, dEnd):
        print 'print list this month'
        dicExtraData = {}
        print ' start List of Invoices printing'
        dicExtraData['dBegin'] = dBegin
        dicExtraData['dEnd'] = dEnd
        
        print 'dicOrder = ', dicExtraData
        
        Pdf = self.rpc.callRP('Report.server_list_of_inpayment', dicExtraData, self.dicUser)
        self.showPdf(Pdf, self.dicUser)

    # Menu Residue
    def on_all_outstanding_accounts1_activate(self, event):
        #dBegin,dEnd = self.getFirstLastDayOfLastMonthAsSeconds()
        dicDate = self.getActualDateTime()
        dBegin = dicDate['date']
        dEnd = dicDate['date']
        self.printListOfResidue(dBegin,dEnd)
            
        
    def printListOfResidue(self, dBegin, dEnd):
        dicExtraData = {}
        print ' start List of Residue printing'
        dicExtraData['dBegin'] = dBegin
        dicExtraData['dEnd'] = dEnd
        
        print 'dicOrder = ', dicExtraData
        
        Pdf = self.rpc.callRP('Report.server_list_of_residue', dicExtraData, self.dicUser)
        self.showPdf(Pdf, self.dicUser)

    # Buttons
 
    def on_bDMS_clicked(self, event):
        print 'dms clicked'
        if self.singleListOfInvoice.ID > 0:
            print 'ModulNumber', self.ModulNumber
            Dms = cuon.DMS.dms.dmswindow(self.allTables, self.ModulNumber, {'1':self.singleListOfInvoice.ID})
        
        
        
    # search button
    def on_bSearch_clicked(self, event):
        self.out( 'Searching ....', self.ERROR)
        sTitle = self.getWidget('eFindTitle').get_text()
        sDesi = self.getWidget('eFindDesignation').get_text()
        
        self.singleListOfInvoice.sWhere = 'where title ~* \'.*' + sTitle + '.*\' and designation ~* \'.*' + sDesi + '.*\''
        #self.out(self.singleListOfInvoice.sWhere, self.ERROR)
        self.refreshTree()

    def refreshTree(self):
        print 'refresh tree '
        self.singleListOfInvoice.disconnectTree()
        self.singleInpayment.disconnectTree()
        
        if self.tabOption == self.tabListOfInvoice:
            self.singleListOfInvoice.connectTree()
            self.singleListOfInvoice.refreshTree()
        elif self.tabOption == self.tabInpayment:
            print 'refresh tree by singleInpayment'
            #self.singleInpayment.sWhere  ='where address_id = ' + `int(self.singleListOfInvoice.ID)`
            #self.singleMisc.fillEntries(self.singleMisc.findSingleId())
            self.singleInpayment.connectTree()
            self.singleInpayment.refreshTree()
        elif self.tabOption == self.tabResidue:
            print 'refresh tree by singleInpayment'
            #self.singleInpayment.sWhere  ='where address_id = ' + `int(self.singleListOfInvoice.ID)`
            #self.singleMisc.fillEntries(self.singleMisc.findSingleId())
            self.singleResidue.connectTree()
            self.singleResidue.refreshTree()    
##        elif self.tabOption == self.tabPartner:
##            self.singlePartner.sWhere  ='where addressid = ' + `int(self.singleListOfInvoice.ID)`
##            self.singlePartner.connectTree()
##            self.singlePartner.refreshTree()
##        elif self.tabOption == self.tabSchedul:
##            self.singleSchedul.sWhere  ='where partnerid = ' + `int(self.singlePartner.ID)`
##            self.singleSchedul.connectTree()
##            self.singleSchedul.refreshTree()
            
     


         
    def tabChanged(self):
        print 'tab changed to :'  + str(self.tabOption)
        
        if self.tabOption == self.tabListOfInvoice:
            #ListOfInvoice
            print 'Seite 1'
            self.disableMenuItem('tabs')
            self.enableMenuItem('ListOfInvoice')

            self.actualEntries = self.singleListOfInvoice.getEntries()
            self.editAction = 'editListOfInvoice'
            #self.setStatusbarText([''])
          
            self.setTreeVisible(True)
            

            self.out( 'Seite 0')


        elif self.tabOption == self.tabInpayment:
            print  'Seite 2'
            self.disableMenuItem('tabs')
            self.enableMenuItem('Inpayment')
           
            self.editAction = 'editInpayment'
            self.setTreeVisible(True)
            print '4'
            #self.setStatusbarText([self.singleListOfInvoice.sStatus])

        elif self.tabOption == self.tabResidue:
            print  'Seite 3'
            self.disableMenuItem('tabs')
            #self.enableMenuItem('Residue')
           
            self.editAction = 'editResidue'
            self.setTreeVisible(True)
            
            #self.setStatusbarText([self.singleListOfInvoice.sStatus])

        # refresh the Tree
        self.refreshTree()
        
        self.enableMenuItem(self.editAction)
        
        self.editEntries = False
        
