# -*- coding: utf-8 -*-

##Copyright (C) [2005]  [Jürgen Hamel, D-32584 Löhne]

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
from cuon.Windows.chooseWindows  import chooseWindows
import cPickle
#import cuon.OpenOffice.letter
# localisation
import locale, gettext
locale.setlocale (locale.LC_NUMERIC, '')
import threading
import datetime as DateTime
import SingleContact
import cuon.Addresses.addresses
import cuon.Addresses.SingleAddress

class contactwindow(chooseWindows):

    
    def __init__(self, allTables):

        chooseWindows.__init__(self)
       
        self.singleContact = SingleContact.SingleContact(allTables)
        self.singleAddress = cuon.Addresses.SingleAddress.SingleAddress(allTables)
        
    
        self.loadGlade('contact.xml')
        self.win1 = self.getWidget('ContactMainwindow')
        #self.setStatusBar()
        self.allTables = allTables

        self.EntriesContact = 'bank.xml'
        
        self.loadEntries(self.EntriesContact)
        
        self.singleContact.setEntries(self.getDataEntries(self.EntriesContact) )
        self.singleContact.setGladeXml(self.xml)
        self.singleContact.setTreeFields( ['address.lastname as address_name', \
        'address.city as city','bcn'] )
        self.singleContact.setStore( gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING,   gobject.TYPE_UINT) ) 
        self.singleContact.setTreeOrder('bcn')
        self.singleContact.setListHeader([_('Lastname'), _('City'),_('BCN')])
        self.singleContact.setTree(self.xml.get_widget('tree1') )
        self.singleContact.sWhere = 'where address.id = address_id '
  
  

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
        self.singleContact.save()
        self.setEntriesEditable(self.EntriesContact, False)
        self.tabChanged()
        
    def on_new1_activate(self, event):
        self.out( "new addresses v2")
        self.singleContact.newRecord()
        self.setEntriesEditable(self.EntriesContact, True)

    def on_edit1_activate(self, event):
        self.out( "edit addresses v2")
        self.setEntriesEditable(self.EntriesContact, True)


    def on_delete1_activate(self, event):
        self.out( "delete addresses v2")
        self.singleContact.deleteRecord()

 
 

        
        
    # Button  choose address
    def on_bChooseAddressOfContact_clicked(self, event):
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
        sName = self.getWidget('eFindName').get_text()
        sCity = self.getWidget('eFindCity').get_text()
        self.out('Name and City = ' + sName + ', ' + sCity, self.ERROR)
        self.singleContact.sWhere = 'where lastname ~* \'.*' + sName + '.*\' and city ~* \'.*' + sCity + '.*\''
        self.out(self.singleContact.sWhere, self.ERROR)
        self.refreshTree()

    def refreshTree(self):
        self.singleContact.disconnectTree()
        
        if self.tabOption == self.tabClients:
            self.singleContact.connectTree()
            self.singleContact.refreshTree()
        elif self.tabOption == self.tabMisc:
            self.singleMisc.sWhere  ='where address_id = ' + `int(self.singleContact.ID)`
            self.singleMisc.fillEntries(self.singleMisc.findSingleId())

        elif self.tabOption == self.tabPartner:
            self.singlePartner.sWhere  ='where addressid = ' + `int(self.singleContact.ID)`
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

            self.actualEntries = self.singleContact.getEntries()
            self.editAction = 'editAddress'
            #self.setStatusbarText([''])
          
            self.setTreeVisible(True)
            

            self.out( 'Seite 0')


        elif self.tabOption == self.tabContact:
            self.out( 'Seite 2')
            self.disableMenuItem('tabs')
            self.enableMenuItem('bank')
           
            self.editAction = 'editContact'
            self.setTreeVisible(False)
            #self.setStatusbarText([self.singleContact.sStatus])


        elif self.tabOption == self.tabMisc:
            self.out( 'Seite 3')

            self.disableMenuItem('tabs')
            self.enableMenuItem('misc')
            self.editAction = 'editMisc'
            self.setTreeVisible(False)
            #self.setStatusbarText([self.singleContact.sStatus])




        elif self.tabOption == self.tabPartner:
            #Partner
            self.disableMenuItem('tabs')
            self.enableMenuItem('partner')
            
            self.out( 'Seite 1')
            self.editAction = 'editPartner'
            self.setTreeVisible(True)
            #self.setStatusbarText([self.singleContact.sStatus])

            
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
        
