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
import SingleContact
import cuon.Addresses.addresses
import cuon.Addresses.SingleAddress
import cuon.Addresses.SinglePartner
import time


class contactwindow(chooseWindows):

    
    def __init__(self, allTables, address_nr=0, partner_nr=0, autoNew = False):
        print 'time 01 = ', time.localtime()
        print "address_nr = " ,  address_nr
        chooseWindows.__init__(self)
        #print 'time 02 = ', time.localtime()

        self.contact_address_id = address_nr
        self.contact_partner_id = partner_nr
        
        self.singleContact = SingleContact.SingleContact(allTables)
        #print 'time 03 = ', time.localtime()

        self.singleAddress = cuon.Addresses.SingleAddress.SingleAddress(allTables)
        #print 'time 04 = ', time.localtime()
        
        self.singleContact.addressId = address_nr
        
        self.singlePartner = cuon.Addresses.SinglePartner.SinglePartner(allTables)
        
        self.singleContact.partnerId = partner_nr
        #print 'time 05 = ', time.localtime()
    
        self.loadGlade('contact.xml')
        self.win1 = self.getWidget('ContactMainwindow')
        #self.setStatusBar()
        self.allTables = allTables

        self.EntriesContact = 'contact.xml'
        
        self.loadEntries(self.EntriesContact)
        #print 'time 06= ', time.localtime()
        
        self.singleContact.setEntries(self.getDataEntries(self.EntriesContact) )
        self.singleContact.setGladeXml(self.xml)
        self.singleContact.setTreeFields( ['schedul_date','schedul_time_begin','address.lastname as adr '])
        #'select address.lastname where partner_schedul.address_id = address.id) as lastname'] )
        self.singleContact.setStore( gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_UINT) ) 
        self.singleContact.setListHeader([_('date'), _('time'), _('Address')])
        self.singleContact.setTree(self.getWidget('tree1') )
        self.singleContact.sWhere = ' where address.id = address_id and process_status = 0 and contacter_id = ' +  self.singleContact.getStaffID(self.dicUser) + ' ' 
        if address_nr > 0:
            self.singleContact.sWhere += 'and address_id = ' + `address_nr`
            #self.singleContact.setTreeOrder('schedul_date')

        elif partner_nr > 0:
            self.singleContact.sWhere += 'and partner_id = ' + `partner_nr`
            #self.singleContact.setTreeOrder('schedul_date')
            
        
        #self.singleContact.setTreeOrder("to_date('schedul_date', '" + self.dicUser['DateformatString'] +"')" )
        self.singleContact.setTreeOrder("schedul_date" )


        # set values for comboBox

          

        # Menu-items
        self.initMenuItems()

        # Close Menus for Tab
        self.addEnabledMenuItems('tabs','contact1')
  

               
        # seperate Menus
        self.addEnabledMenuItems('contact','contact1')
          

        # enabledMenues for Address
        self.addEnabledMenuItems('editContact','new1', self.dicUserKeys['address_new'])
        self.addEnabledMenuItems('editContact','delete1', self.dicUserKeys['address_delete'])
        self.addEnabledMenuItems('editContact','print1')
        self.addEnabledMenuItems('editContact','edit1', self.dicUserKeys['address_edit'])

        # enabledMenues for Save 
        self.addEnabledMenuItems('editSave','save1', self.dicUserKeys['address_save'])
    
        

        # tabs from notebook
        self.tabContact = 0    
        
        

        self.tabChanged()
        
        print 'time 99 ', time.localtime()
        self.win1.add_accel_group(self.accel_group)
        if autoNew:
            self.activateClick('new1')
            
            
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

 
    def on_set_ready1_activate(self, event):
        print 'on_set_ready1_activate'
        # First set Edit-Mode
        self.activateClick('edit1')
        # now set ready
        cbeStatus = self.getWidget('cbeStatus')
        cbeStatus.set_active(1)
        # and last save and close
        self.activateClick('save1')
        self.activateClick('quit1')
        
        
    # Button  choose address
    def on_bChooseAddressOfContact_clicked(self, event):
        adr = cuon.Addresses.addresses.addresswindow(self.allTables)
        adr.setChooseEntry('chooseAddress', self.getWidget( 'eAddressID'))

    # signals from entry eAddressNumber
    
    def on_eAddressID_changed(self, event):
        print 'eAdrnbr changed'
        #s = self.getWidget( 'eAddressID').get_text()
        #print s
        try:
            iAdrNumber = self.getChangedValue('eAddressID')
            print "iAdrNumber",  iAdrNumber
            eAdrField = self.getWidget('tvAddress')
            liAdr = self.singleAddress.getAddress(iAdrNumber)
            print "liAdr",  liAdr
            self.setTextbuffer(eAdrField,liAdr)
        except:
            pass
            

    def on_bGoToAddress_clicked(self, event):
        print 'go to address'
        #adr = cuon.Addresses.addresses.addresswindow(self.allTables,addrid=self.contact_address_id, partnerid=self.contact_partner_id)
        adr = cuon.Addresses.addresses.addresswindow(self.allTables,addrid=self.singleContact.addressId)
        
    
              

        
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
        iTime = 0
        try:
            sTime = self.getWidget('eSleepingTime').get_text()
            sTime = sTime.strip()

            if sTime.find(':') > 0:
                t1 = time.time()
                print 't1 = ', t1
                t1_l = time.localtime()
                print 't1_l', t1_l
                #t2 = time.strptime(sTime,'%H:%M')
                #print 't2 = ', t2
                liTwake = sTime.split(':')
                # last value 0 or 1 ????
                timeOffset = 0
                try:
                    timeOffset = int(self.dicUser['prefLocale']['TimeOffset'])
                except:
                    timeOffset = 0
                    
                t_set = (t1_l[0],t1_l[1],t1_l[2],int(liTwake[0]) + timeOffset,int(liTwake[1]),0,0,0,0)
                print t_set
                tR = time.mktime(t_set) + time.timezone
                print tR
                
                iTime = int((tR - t1)/60)
                
                print iTime
            else:
                
                iTime = int(sTime) 
        except:
            iTime = 0
            
        if iTime > 0:
            iTime = iTime * 60000
        else:
            iTime = 300000
        print 'iTime by sleep ', iTime    
        gobject.timeout_add(iTime, self.openWindow)
        self.closeWindow()
        
    def on_bCloseWindow_clicked(self, event):
        print 'close '
        self.activateClick('set_ready1')
        
    def on_bQuit_clicked(self, event):
        self.activateClick('quit1')
        
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
        print "refresh tree at contact"
        print "sWhere = ",  self.singleContact.sWhere
        if self.tabOption == self.tabContact:
            self.singleContact.connectTree()
            self.singleContact.refreshTree()
            
            try:
                print 'read buffer'
                self.on_eAddressID_changed('NONE')
                b1 = self.readTextBuffer(self.getWidget('tvAddress'))
                print 'b1', b1
                if b1:
                    
                    self.win1.set_title(b1.replace('\n',', '))
                self.out( 'Seite 0')

            except Exception, params:
                print Exception, params
                
        
     


         
    def tabChanged(self):
        self.out( 'tab changed to :'  + str(self.tabOption))
        
        if self.tabOption == self.tabContact:
            #contact
            print "tab changed at contact"
            self.disableMenuItem('tabs')
            self.enableMenuItem('contact')

            self.actualEntries = self.singleContact.getEntries()
            self.editAction = 'editContact'
            #self.setStatusbarText([''])
          
            self.setTreeVisible(True)
            
            



        # refresh the Tree
        self.refreshTree()
        self.enableMenuItem(self.editAction)
        self.editEntries = False
        
