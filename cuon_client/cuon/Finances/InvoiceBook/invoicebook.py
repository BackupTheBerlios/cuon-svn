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
import cuon.DMS.dms

class invoicebookwindow(windows):

    
    def __init__(self, allTables):

        windows.__init__(self)
       
        self.singleListOfInvoice = SingleListOfInvoice.SingleListOfInvoice(allTables)
    
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

  
  

        # set values for comboBox

          

        # Menu-items
        self.initMenuItems()

        # Close Menus for Tab
        self.addEnabledMenuItems('tabs','mi_ListOfInvoice1')
  

               
        # seperate Menus
        self.addEnabledMenuItems('ListOfInvoice','mi_ListOfInvoice1')
          

        # enabledMenues for Address
        self.addEnabledMenuItems('editListOfInvoice','mi_new1')
        self.addEnabledMenuItems('editListOfInvoice','mi_clear1')
        self.addEnabledMenuItems('editListOfInvoice','mi_print1')
        self.addEnabledMenuItems('editListOfInvoice','mi_edit1')


    
        

        # tabs from notebook
        self.tabListOfInvoice = 0
    
        
        

        self.tabChanged()
        

    def checkClient(self):
        pass
        
    #Menu File
              
    def on_quit1_activate(self, event):
        self.out( "exit ListOfInvoice V1")
        self.on_bChooseClient_clicked(event)
        

    def on_bChooseClient_clicked(self, event):
        print 'Client-ID = ', self.singleListOfInvoice.ID
        
        if self.singleListOfInvoice.ID  > 0:
            self.oUser.client = self.singleListOfInvoice.ID 
            self.oUser.refreshDicUser()
            print `self.oUser.getSqlDicUser`
            self.openDB()
            self.oUser = self.saveObject('User', self.oUser)
            self.closeDB()
            self.closeWindow() 
        else:
            print 'no client-ID'
    
        


    #Menu ListOfInvoice
  
    def on_save_activate(self, event):
        self.out( "save invoicebook v2")
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
        dicOrder = {}
        print ' start List of Invoices printing'
        dicOrder['dBegin'] = dBegin
        dicOrder['dEnd'] = dEnd
        
        print 'dicOrder = ', dicOrder
        
        Pdf = self.rpc.callRP('Report.server_order_list_of_invoices', dicOrder, self.dicUser)
        self.showPdf(Pdf, self.dicUser,'INVOICE')


 
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
        self.singleListOfInvoice.disconnectTree()
        
        if self.tabOption == self.tabListOfInvoice:
            self.singleListOfInvoice.connectTree()
            self.singleListOfInvoice.refreshTree()
  ##      elif self.tabOption == self.tabMisc:
##            self.singleMisc.sWhere  ='where address_id = ' + `int(self.singleListOfInvoice.ID)`
##            self.singleMisc.fillEntries(self.singleMisc.findSingleId())

##        elif self.tabOption == self.tabPartner:
##            self.singlePartner.sWhere  ='where addressid = ' + `int(self.singleListOfInvoice.ID)`
##            self.singlePartner.connectTree()
##            self.singlePartner.refreshTree()
##        elif self.tabOption == self.tabSchedul:
##            self.singleSchedul.sWhere  ='where partnerid = ' + `int(self.singlePartner.ID)`
##            self.singleSchedul.connectTree()
##            self.singleSchedul.refreshTree()
            
     


         
    def tabChanged(self):
        #self.out( 'tab changed to :'  + str(self.tabOption))
        
        if self.tabOption == self.tabListOfInvoice:
            #Address
            self.disableMenuItem('tabs')
            self.enableMenuItem('ListOfInvoice')

            self.actualEntries = self.singleListOfInvoice.getEntries()
            self.editAction = 'editListOfInvoice'
            #self.setStatusbarText([''])
          
            self.setTreeVisible(True)
            

            self.out( 'Seite 0')


 ##       elif self.tabOption == self.tabBank:
##            self.out( 'Seite 2')
##            self.disableMenuItem('tabs')
##            self.enableMenuItem('bank')
           
##            self.editAction = 'editBank'
##            self.setTreeVisible(False)
##            #self.setStatusbarText([self.singleListOfInvoice.sStatus])


##        elif self.tabOption == self.tabMisc:
##            self.out( 'Seite 3')

##            self.disableMenuItem('tabs')
##            self.enableMenuItem('misc')
##            self.editAction = 'editMisc'
##            self.setTreeVisible(False)
##            #self.setStatusbarText([self.singleListOfInvoice.sStatus])




##        elif self.tabOption == self.tabPartner:
##            #Partner
##            self.disableMenuItem('tabs')
##            self.enableMenuItem('partner')
            
##            self.out( 'Seite 1')
##            self.editAction = 'editPartner'
##            self.setTreeVisible(True)
##            #self.setStatusbarText([self.singleListOfInvoice.sStatus])

            
##        elif self.tabOption == self.tabSchedul:
##            #Scheduling
##            self.disableMenuItem('tabs')
##            self.enableMenuItem('schedul')
            
##            self.out( 'Seite 4')
##            self.editAction = 'editSchedul'
##            self.setTreeVisible(True)
##            self.setStatusbarText([self.singlePartner.sStatus])

        # refresh the Tree
        self.refreshTree()
        self.enableMenuItem(self.editAction)
        self.editEntries = False
        
