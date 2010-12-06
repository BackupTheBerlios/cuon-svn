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
import SingleClient
import cuon.Addresses.addresses

class clientswindow(chooseWindows):

    
    def __init__(self, allTables, ClientID = 0):

        chooseWindows.__init__(self)
       
        self.singleClients = SingleClient.SingleClient(allTables)

    
        self.loadGlade('clients.xml')
        self.win1 = self.getWidget('ClientMainwindow')
        #self.setStatusBar()
        if ClientID > 0:
            self.singleClients.ID = ClientID
            
            self.activateClick("bChooseClient")

        else:
            self.EntriesClients = 'clients.xml'
            
            self.loadEntries(self.EntriesClients)
            
            self.singleClients.setEntries(self.getDataEntries('clients.xml') )
            self.singleClients.setGladeXml(self.xml)
            self.singleClients.setTreeFields( ['name', 'designation','client_number'] )
            self.singleClients.setStore( gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING,   gobject.TYPE_UINT) ) 
            self.singleClients.setTreeOrder('name, designation')
            self.singleClients.setListHeader([_('Lastname'), _('Firstname'), _('City')])
            self.singleClients.setTree(self.getWidget('tree1') )
        

      
    
            # set values for comboBox
    
              
    
            # Menu-items
            self.initMenuItems()
    
            # Close Menus for Tab
            self.addEnabledMenuItems('tabs','mi_address1')
      
    
                   
            # seperate Menus
            self.addEnabledMenuItems('address','mi_address1')
              
    
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
        self.on_bChooseClient_clicked(event)
        

    def on_bChooseClient_clicked(self, event):
        print 'Client-ID = ', self.singleClients.ID
        
        if self.singleClients.ID  > 0:
            self.oUser.client = self.singleClients.ID 
            self.oUser.refreshDicUser()
            print `self.oUser.getSqlDicUser`
            self.openDB()
            self.oUser = self.saveObject('User', self.oUser)
            self.closeDB()
            self.closeWindow() 
            self.rpc.callRP('User.setUserData',self.dicUser)
        else:
            print 'no client-ID'
    
    def on_tree1_row_activated(self, event, data1, data2):
        print event
        print data1
        print data2
        
        self.activateClick('bChooseClient', event, 'clicked')



  
    def on_save1_activate(self, event):
        self.out( "save client v2")
        self.singleClients.save()
        self.setEntriesEditable(self.EntriesClients, False)
        self.tabChanged()
        
    def on_new1_activate(self, event):
        self.out( "new client v2")
        self.singleClients.newRecord()
        self.setEntriesEditable(self.EntriesClients, True)

    def on_edit1_activate(self, event):
        self.out( "edit client v2")
        self.setEntriesEditable(self.EntriesClients, True)


    def on_delete1_activate(self, event):
        self.out( "delete client v2")
        self.singleClients.deleteRecord()

 
 

        
        
    # Button  choose address
    def on_bChooseAddress_clicked(self, event):
        adr = cuon.Addresses.addresses.addresswindow(self.allTables)
        adr.setChooseEntry('chooseAddress', self.getWidget( 'eAddressID'))

    # signals from entry eAddressNumber
    
    def on_eAddressID_changed(self, event):
        print 'eAdrnbr changed'
        iAdrNumber = self.getChangedValue('eAddressID')
        eAdrField = self.getWidget('tvAddress')
        liAdr = self.singleAddress.getAddress(iAdrNumber)
        self.setTextbuffer(eAdrField,liAdr)
    


        
    def on_chooseAddress_activate(self, event):
        # choose Address from other Modul
        if self.tabOption == self.tabClients:
            print '############### Address choose ID ###################'
            self.setChooseValue(self.singleClients.ID)
            self.closeWindow()
        elif self.tabOption == self.tabPartner:
            print '############### Address choose ID ###################'
            self.setChooseValue(self.singlePartner.ID)
            self.closeWindow()

        else:
            print '############### No ID found,  choose ID -1 ###################'
            self.setChooseValue('-1')
            self.closeWindow()
 
              

        
    # search button
    def on_bSearch_clicked(self, event):
        self.out( 'Searching ....', self.ERROR)
        sName = self.getWidget('eFindName').get_text()
        sCity = self.getWidget('eFindCity').get_text()
        self.out('Name and City = ' + sName + ', ' + sCity, self.ERROR)
        self.singleClients.sWhere = 'where lastname ~* \'.*' + sName + '.*\' and city ~* \'.*' + sCity + '.*\''
        self.out(self.singleClients.sWhere, self.ERROR)
        self.refreshTree()

    def refreshTree(self):
        self.singleClients.disconnectTree()
        
        if self.tabOption == self.tabClients:
            self.singleClients.connectTree()
            self.singleClients.refreshTree()
        
     


         
    def tabChanged(self):
        self.out( 'tab changed to :'  + str(self.tabOption))
        
        if self.tabOption == self.tabClients:
            #Address
            self.disableMenuItem('tabs')
            self.enableMenuItem('address')

            self.actualEntries = self.singleClients.getEntries()
            self.editAction = 'editAddress'
            #self.setStatusbarText([''])
          
            self.setTreeVisible(True)
            

            self.out( 'Seite 0')


        # refresh the Tree
        self.refreshTree()
        self.enableMenuItem(self.editAction)
        self.editEntries = False
        
