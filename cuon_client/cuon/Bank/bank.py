# -*- coding: utf-8 -*-

##Copyright (C) [2005]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

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
from cuon.Windows.chooseWindows  import chooseWindows
import cPickle
#import cuon.OpenOffice.letter
# localisation
import locale, gettext
locale.setlocale (locale.LC_NUMERIC, '')
import threading
import datetime as DateTime
import SingleBank
import cuon.Addresses.addresses
import cuon.Addresses.SingleAddress

class bankwindow(chooseWindows):

    
    def __init__(self, allTables):

        chooseWindows.__init__(self)
       
        self.singleBank = SingleBank.SingleBank(allTables)
        self.singleAddress = cuon.Addresses.SingleAddress.SingleAddress(allTables)
        
    
        self.loadGlade('bank.xml')
        self.win1 = self.getWidget('BankMainwindow')
        #self.setStatusBar()
        self.allTables = allTables

        self.EntriesBank = 'bank.xml'
        
        self.loadEntries(self.EntriesBank)
        
        self.singleBank.setEntries(self.getDataEntries(self.EntriesBank) )
        self.singleBank.setGladeXml(self.xml)
        self.singleBank.setTreeFields( ['address.lastname as address_name', \
        'address.city as city','bcn'] )
        self.singleBank.setStore( gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING,   gobject.TYPE_UINT) ) 
        self.singleBank.setTreeOrder('bcn')
        self.singleBank.setListHeader([_('Lastname'), _('City'),_('BCN')])
        self.singleBank.setTree(self.xml.get_widget('tree1') )
        self.singleBank.sWhere = 'where address.id = address_id '
  
  

        # set values for comboBox

          

        # Menu-items
        self.initMenuItems()

        # Close Menus for Tab
        self.addEnabledMenuItems('tabs','bank11')
  

               
        # seperate Menus
        self.addEnabledMenuItems('address','bank1')
          

        # enabledMenues for Address
        self.addEnabledMenuItems('editAddress','mi_new1')
        self.addEnabledMenuItems('editAddress','mi_clear1')
        self.addEnabledMenuItems('editAddress','mi_print1')
        self.addEnabledMenuItems('editAddress','mi_edit1')


    
        

        # tabs from notebook
        self.tabClients = 0
    
        
        

        self.tabChanged()
        
     
    def checkClient(self):
        pass
        
    #Menu File
              
    def on_quit1_activate(self, event):
        self.out( "exit clients V1")
        self.closeWindow()        

        
    def on_tree1_row_activated(self, event, data1, data2):
        print event
        print data1
        print data2
        
        self.activateClick('bChooseClient', event, 'clicked')


    
  
    def on_save1_activate(self, event):
        self.out( "save addresses v2")
        self.singleBank.save()
        self.setEntriesEditable(self.EntriesBank, False)
        self.tabChanged()
        
    def on_new1_activate(self, event):
        self.out( "new addresses v2")
        self.singleBank.newRecord()
        self.setEntriesEditable(self.EntriesBank, True)

    def on_edit1_activate(self, event):
        self.out( "edit addresses v2")
        self.setEntriesEditable(self.EntriesBank, True)


    def on_delete1_activate(self, event):
        self.out( "delete addresses v2")
        self.singleBank.deleteRecord()

 
 

        
        
    # Button  choose address
    def on_bChooseAddressOfBank_clicked(self, event):
        adr = cuon.Addresses.addresses.addresswindow(self.allTables)
        adr.setChooseEntry('chooseAddress', self.getWidget( 'eAddressID'))

    # signals from entry eAddressNumber
    
    def on_eAddressID_changed(self, event):
        print 'eAdrnbr changed'
        iAdrNumber = self.getChangedValue('eAddressID')
        eAdrField = self.getWidget('tvAddress')
        liAdr = self.singleAddress.getAddress(iAdrNumber)
        self.setTextbuffer(eAdrField,liAdr)
    


        
    
              

        
    # search button
    def on_bSearch_clicked(self, event):
        self.out( 'Searching ....', self.ERROR)
        sBCN = self.getWidget('eFindBCN').get_text()
        sShortDesignation = self.getWidget('eFindDesignation').get_text()
        self.singleBank.sWhere = 'where address.id = address_id and bcn ~* \'.*' + sBCN + '.*\' and short_designation ~* \'.*' + sShortDesignation + '.*\''
        self.refreshTree()
    
    
    # choose Bank
            
    def on_tree1_row_activated(self, event, data1, data2):
        print 'DoubleClick tree1'
        self.activateClick('chooseBank', event)


    def on_chooseBank_activate(self, event):
        # choose Bank from other Modul
        print '############### Bank choose ID ###################'
        self.setChooseValue(self.singleBank.ID)
        
    def refreshTree(self):
        self.singleBank.disconnectTree()
        
        if self.tabOption == self.tabClients:
            self.singleBank.connectTree()
            self.singleBank.refreshTree()
        elif self.tabOption == self.tabMisc:
            self.singleMisc.sWhere  ='where address_id = ' + `int(self.singleBank.ID)`
            self.singleMisc.fillEntries(self.singleMisc.findSingleId())

        elif self.tabOption == self.tabPartner:
            self.singlePartner.sWhere  ='where addressid = ' + `int(self.singleBank.ID)`
            self.singlePartner.connectTree()
            self.singlePartner.refreshTree()
        elif self.tabOption == self.tabSchedul:
            self.singleSchedul.sWhere  ='where partnerid = ' + `int(self.singlePartner.ID)`
            self.singleSchedul.connectTree()
            self.singleSchedul.refreshTree()
            
     


         
    def tabChanged(self):
        self.out( 'tab changed to :'  + str(self.tabOption))
        
        if self.tabOption == self.tabClients:
            #Address
            self.disableMenuItem('tabs')
            self.enableMenuItem('address')

            self.actualEntries = self.singleBank.getEntries()
            self.editAction = 'editAddress'
            #self.setStatusbarText([''])
          
            self.setTreeVisible(True)
            

            self.out( 'Seite 0')


        elif self.tabOption == self.tabBank:
            self.out( 'Seite 2')
            self.disableMenuItem('tabs')
            self.enableMenuItem('bank')
           
            self.editAction = 'editBank'
            self.setTreeVisible(False)
            #self.setStatusbarText([self.singleBank.sStatus])


        elif self.tabOption == self.tabMisc:
            self.out( 'Seite 3')

            self.disableMenuItem('tabs')
            self.enableMenuItem('misc')
            self.editAction = 'editMisc'
            self.setTreeVisible(False)
            #self.setStatusbarText([self.singleBank.sStatus])




        elif self.tabOption == self.tabPartner:
            #Partner
            self.disableMenuItem('tabs')
            self.enableMenuItem('partner')
            
            self.out( 'Seite 1')
            self.editAction = 'editPartner'
            self.setTreeVisible(True)
            #self.setStatusbarText([self.singleBank.sStatus])

            
        elif self.tabOption == self.tabSchedul:
            #Scheduling
            self.disableMenuItem('tabs')
            self.enableMenuItem('schedul')
            
            self.out( 'Seite 4')
            self.editAction = 'editSchedul'
            self.setTreeVisible(True)
            self.setStatusbarText([self.singlePartner.sStatus])

        # refresh the Tree
        self.refreshTree()
        self.enableMenuItem(self.editAction)
        self.editEntries = False
        