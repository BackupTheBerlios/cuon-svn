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
import cuon.Addresses.SinglePartner

class contactwindow(chooseWindows):

    
    def __init__(self, allTables, address_nr=0, partner_nr=0):

        chooseWindows.__init__(self)
       
        self.singleContact = SingleContact.SingleContact(allTables)
        self.singleAddress = cuon.Addresses.SingleAddress.SingleAddress(allTables)
        
        self.singleContact.addressId = address_nr
        
        self.singlePartner = cuon.Addresses.SinglePartner.SinglePartner(allTables)
        
        self.singleContact.partnerId = partner_nr
    
        self.loadGlade('contact.xml')
        self.win1 = self.getWidget('ContactMainwindow')
        #self.setStatusBar()
        self.allTables = allTables

        self.EntriesContact = 'contact.xml'
        
        self.loadEntries(self.EntriesContact)
        
        self.singleContact.setEntries(self.getDataEntries(self.EntriesContact) )
        self.singleContact.setGladeXml(self.xml)
        self.singleContact.setTreeFields( ['schedul_date','schedul_time_begin', \
        'address.lastname as lastname'] )
        self.singleContact.setStore( gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_UINT) ) 
        self.singleContact.setTreeOrder('schedul_date')
        self.singleContact.setListHeader([_('date'), _('time'), _('Address')])
        self.singleContact.setTree(self.xml.get_widget('tree1') )
        self.singleContact.sWhere = 'where address.id = address_id and process_status != 1 and contacter_id = ' +  self.singleContact.getStaffID(self.dicUser) + ' ' 
        if address_nr > 0:
            self.singleContact.sWhere += 'and address_id = ' + `address_nr`
  
  

        # set values for comboBox

          

        # Menu-items
        self.initMenuItems()

        # Close Menus for Tab
        self.addEnabledMenuItems('tabs','contact1')
  

               
        # seperate Menus
        self.addEnabledMenuItems('contact','contact1')
          

        # enabledMenues for Address
        self.addEnabledMenuItems('editContact','new1')
        self.addEnabledMenuItems('editContact','clear1')
        self.addEnabledMenuItems('editContact','print1')
        self.addEnabledMenuItems('editContact','edit1')


    
        

        # tabs from notebook
        self.tabContact = 0
    
        
        

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
        print 'save contact'
        print 'Address-ID = ', self.singleContact.addressId 
        self.singleContact.save()
        self.setEntriesEditable(self.EntriesContact, False)
        self.tabChanged()
        
    def on_new1_activate(self, event):
        print 'new contact'
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


    # sleeping 
    def on_bSleeping_clicked(self, event):
        print 'sleeps'
        try:
            sTime = int(self.getWidget('eSleepingTime').get_text()) 
        except:
            sTime = 0
            
        if sTime > 0:
            sTime = sTime * 60000
        else:
            stime = 300000
        print 'sTime by sleep ', sTime    
        gobject.timeout_add(sTime, self.openWindow)
        self.closeWindow()
        
    def on_calendar1_day_selected_double_click(self, event):
        self.setDateToEntry(event,'eDate')
        
        
    def on_rbDay_clicked(self, event):
        print event
        print event.get_name()
        sDay = event.get_name()
        nDay = '0'
        try:
            nDay = sDay[len(sDay)-1]
        except:
            nDay = '0'
        self.getWidget('eAlarmDay').set_text(nDay)
        
        
    def on_rbHour_clicked(self, event):
        print event
        print event.get_name()
        sHour = event.get_name()
        nHour = '0'
        try:
            nHour = sHour[len(sHour)-1]
        except:
            nHour = '0'
        self.getWidget('eAlarmHour').set_text(nHour)
        
        
    def on_rbMinute_clicked(self, event):
        print event
        print event.get_name()
        sMinute = event.get_name()
        nMinute = '00'
        try:
            nMinute = sMinute[len(sMinute)-2:]
        except:
            nMinute = '00'
        self.getWidget('eAlarmMinutes').set_text(nMinute)
        
    def refreshTree(self):
        self.singleContact.disconnectTree()
        
        if self.tabOption == self.tabContact:
            self.singleContact.connectTree()
            self.singleContact.refreshTree()
        
     


         
    def tabChanged(self):
        self.out( 'tab changed to :'  + str(self.tabOption))
        
        if self.tabOption == self.tabContact:
            #Address
            self.disableMenuItem('tabs')
            self.enableMenuItem('contact')

            self.actualEntries = self.singleContact.getEntries()
            self.editAction = 'editContact'
            #self.setStatusbarText([''])
          
            self.setTreeVisible(True)
            

            self.out( 'Seite 0')


        

        elif self.tabOption == self.tabMisc:
            self.out( 'Seite 3')

            self.disableMenuItem('tabs')
            self.enableMenuItem('misc')
            self.editAction = 'editMisc'
            self.setTreeVisible(False)
            #self.setStatusbarText([self.singleContact.sStatus])



        # refresh the Tree
        self.refreshTree()
        self.enableMenuItem(self.editAction)
        self.editEntries = False
        