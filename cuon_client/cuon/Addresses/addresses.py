# -*- coding: utf-8 -*-

##Copyright (C) [2003]  [Jürgen Hamel, D-32584 Löhne]

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
from gtk import TRUE, FALSE
import string
from cuon.Databases.SingleData import SingleData
import SingleAddress
import SingleMisc
import SinglePartner
import SingleScheduling
import lists_addresses_phone1
import lists_addresses_phone11

import logging
from cuon.Windows.chooseWindows  import chooseWindows
import cPickle
#import cuon.OpenOffice.letter
# localisation
import locale, gettext
locale.setlocale (locale.LC_NUMERIC, '')
import threading
import time
import datetime as DateTime
import cuon.DMS.documentTools
import cuon.DMS.dms
import printAddress



class addresswindow(chooseWindows):

    
    def __init__(self, allTables):

        chooseWindows.__init__(self)
        self.oDocumentTools = cuon.DMS.documentTools.documentTools()
        
        self.singleAddress = SingleAddress.SingleAddress(allTables)
        self.singleMisc = SingleMisc.SingleMisc(allTables)
        self.singlePartner = SinglePartner.SinglePartner(allTables)
        self.singleSchedul = SingleScheduling.SingleScheduling(allTables)
        self.allTables = allTables
       
        
        # self.singleAddress.loadTable()

        # self.xml = gtk.glade.XML()
    
        self.loadGlade('address.xml')
        self.win1 = self.getWidget('AddressMainwindow')
        self.setStatusBar()


        self.EntriesAddresses = 'addresses.xml'
        self.EntriesAddressesMisc = 'addresses_misc.xml'
        self.EntriesAddressesBank = 'addresses_bank.xml'
        self.EntriesPartner = 'partner.xml'
        self.EntriesPartnerSchedul = 'partner_schedul.xml'
        
        self.loadEntries(self.EntriesAddresses)
        
        self.singleAddress.setEntries(self.getDataEntries('addresses.xml') )
        self.singleAddress.setGladeXml(self.xml)
        self.singleAddress.setTreeFields( ['lastname', 'firstname','city'] )
        self.singleAddress.setStore( gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING,   gobject.TYPE_UINT) ) 
        self.singleAddress.setTreeOrder('lastname, firstname')
        self.singleAddress.setListHeader([_('Lastname'), _('Firstname'), _('City')])
        self.singleAddress.setTree(self.xml.get_widget('tree1') )

  
        #singleMisc
        
        self.loadEntries(self.EntriesAddressesMisc )
        self.singleMisc.setEntries(self.getDataEntries('addresses_misc.xml') )
        self.singleMisc.setGladeXml(self.xml)
        self.singleMisc.setTreeFields([])
        self.singleMisc.setTreeOrder('id')
        
        self.singleMisc.sWhere  ='where address_id = ' + `self.singleAddress.ID`
        self.singleMisc.setTree(self.xml.get_widget('tree1') )
        # self.singleMisc.setStore(gtk.ListStore())
        #singlePartner
        
        self.loadEntries(self.EntriesPartner )
        self.singlePartner.setEntries(self.getDataEntries('partner.xml') )
        self.singlePartner.setGladeXml(self.xml)
        self.singlePartner.setTreeFields( ['lastname', 'firstname','city'] )
        self.singlePartner.setStore( gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING,   gobject.TYPE_UINT) ) 

        self.singlePartner.setTreeOrder('lastname, firstname')
        self.singlePartner.setListHeader([_('Name of partner'), _('Firstname of partner'), _('City')])

        self.singlePartner.sWhere  ='where addressid = ' + `self.singleAddress.ID`
        self.singlePartner.setTree(self.xml.get_widget('tree1') )



        #singleScheduling
        
        self.loadEntries(self.EntriesPartnerSchedul )
        self.singleSchedul.setEntries(self.getDataEntries('partner_schedul.xml') )
        self.singleSchedul.setGladeXml(self.xml)
        self.singleSchedul.setTreeFields( ['schedul_date','schedul_time_begin','short_remark','priority','process_status'] )
        self.singleSchedul.setStore( gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_UINT, gobject.TYPE_UINT,   gobject.TYPE_UINT) ) 
        #self.singleSchedul.setTreeFields( [ 'short_remark','priority','process_status'] )
        #self.singleSchedul.setStore( gtk.ListStore( gobject.TYPE_STRING, gobject.TYPE_UINT, gobject.TYPE_UINT,   gobject.TYPE_UINT) ) 
        self.singleSchedul.setTreeOrder('schedul_date, schedul_time_begin')
        self.singleSchedul.setListHeader([_('Date '),_('Time'),  _('shortRemark'), _('Priority'), _('Status')])
 

        self.singleSchedul.sWhere  ='where partnerid = ' + `self.singlePartner.ID`
        self.singleSchedul.setTree(self.xml.get_widget('tree1') )
  

        # set values for comboBox

        cbFashion = self.getWidget('cbFashion')
        if cbFashion:
            cbFashion.set_popdown_strings([_('Customer'),_('Vendor'),_('Authority')])
        
        

        # Menu-items
        self.initMenuItems()

        # Close Menus for Tab
        self.addEnabledMenuItems('tabs','mi_address1')
        self.addEnabledMenuItems('tabs','mi_bank1')
        self.addEnabledMenuItems('tabs','mi_misc1')
        self.addEnabledMenuItems('tabs','mi_partner1')
        self.addEnabledMenuItems('tabs','mi_schedul1')

               
        # seperate Menus
        self.addEnabledMenuItems('address','mi_address1')
        self.addEnabledMenuItems('partner','mi_partner1')
        self.addEnabledMenuItems('schedul','mi_schedul1')
        self.addEnabledMenuItems('bank','mi_bank1')
        self.addEnabledMenuItems('misc','mi_misc1')

        # enabledMenues for Address
        self.addEnabledMenuItems('editAddress','mi_new1' , self.dicUserKeys['address_new'])
        self.addEnabledMenuItems('editAddress','mi_clear1', self.dicUserKeys['address_delete'])
        self.addEnabledMenuItems('editAddress','mi_print1', self.dicUserKeys['address_print'])
        self.addEnabledMenuItems('editAddress','mi_edit1', self.dicUserKeys['address_edit'])


        # enabledMenues for Misc
        self.addEnabledMenuItems('editMisc', '')
  

        # enabledMenues for Partner
        self.addEnabledMenuItems('editPartner', 'mi_PartnerNew1', self.dicUserKeys['address_partner_new'])
        self.addEnabledMenuItems('editPartner','mi_PartnerDelete1', self.dicUserKeys['address_partner_delete'])
        #self.addEnabledMenuItems('editPartner','mi_PartnerPrint1', self.dicUserKeys['address_partner_print'])
        self.addEnabledMenuItems('editPartner','mi_PartnerEdit1', self.dicUserKeys['address_partner_edit'])

        # enabledMenues for Schedul
        self.addEnabledMenuItems('editSchedul', 'mi_SchedulNew1')
        self.addEnabledMenuItems('editSchedul', 'mi_SchedulEdit1')
        #self.addEnabledMenuItems('editSchedul','mi_SchedulDelete')
        #self.addEnabledMenuItems('editSchedul','mi_SchedulPrint1')

         
        

        # tabs from notebook
        self.tabAddress = 0
        self.tabBank = 1
        self.tabMisc = 2
        self.tabPartner = 3
        self.tabSchedul = 4
        
        

        self.tabChanged()
        

    #Menu File
              
    def on_quit1_activate(self, event):
        self.out( "exit addresses v2")
        self.closeWindow() 
    
    

    #Menu Address
  
    def on_save1_activate(self, event):
        self.out( "save addresses v2")
        self.doEdit = self.noEdit
        self.singleAddress.save()
        self.setEntriesEditable(self.EntriesAddresses, FALSE)
        self.tabChanged()
        
    def on_new1_activate(self, event):
        self.out( "new addresses v2")
        self.doEdit = self.tabAddress

        self.singleAddress.newRecord()
        self.setEntriesEditable(self.EntriesAddresses, TRUE)

    def on_edit1_activate(self, event):
        self.out( "edit addresses v2")
        self.doEdit = self.tabAddress

        self.setEntriesEditable(self.EntriesAddresses, TRUE)
    def on_print1_activate(self, event):
        self.out( "print addresses v2")
        p = printAddress.printAddress(self.singleAddress.getFirstRecord() )
        
    def on_delete1_activate(self, event):
        self.out( "delete addresses v2")
        self.singleAddress.deleteRecord()



    def on_bShowDMS_clicked(self, event):
        print 'dms clicked'
        if self.singleAddress.ID > 0:
            print 'ModulNumber', self.ModulNumber
            Dms = cuon.DMS.dms.dmswindow(self.allTables, self.ModulNumber, {'1':self.singleAddress.ID})
        

    def on_bShowPartnerDMS_clicked(self, event):
        print 'dms Partner clicked'
        if self.singlePartner.ID > 0:
            print 'ModulNumber', self.MN['Partner']
            Dms = cuon.DMS.dms.dmswindow(self.allTables, self.MN['Partner'], {'1':self.singlePartner.ID})
        

    # Menu misc
    def on_MiscSave1_activate(self, event):
        
        self.out( "save Misc addresses v2")
        self.doEdit = self.noEdit
        self.singleMisc.addressId = self.singleAddress.ID
        
        self.singleMisc.save()
        self.setEntriesEditable(self.EntriesAddressesMisc, FALSE)
        self.tabChanged()

    def on_MiscEdit1_activate(self, event):
        self.out( "edit addresses v2")
        self.doEdit = self.tabMisc
        
        self.setEntriesEditable(self.EntriesAddressesMisc, TRUE)

  #Menu Partner
        
   
    def on_PartnerSave1_activate(self, event):
        self.out( "save Partner addresses v2")
        self.doEdit = self.noEdit
        self.singlePartner.addressId = self.singleAddress.ID
        self.singlePartner.save()
        self.setEntriesEditable(self.EntriesPartner, FALSE)
        self.tabChanged()
        
    def on_PartnerNew1_activate(self, event):
        self.out( "new Partner addresses v2")
        self.doEdit = self.tabPartner
        
        self.singlePartner.newRecord()
        self.setEntriesEditable(self.EntriesPartner, TRUE)

        
    def on_PartnerEdit1_activate(self, event):
        self.doEdit = self.tabPartner

        self.setEntriesEditable(self.EntriesPartner, TRUE)


    def on_PartnerDelete1_activate(self, event):
        self.out( "delete Partner addresses v2")
        self.singlePartner.deleteRecord()


#Menu Schedul
        
   
    def on_SchedulSave_activate(self, event):
        self.out( "save Schedul addresses v2")
        self.doEdit = self.noEdit
        self.singleSchedul.partnerId = self.singlePartner.ID
        id = self.singleSchedul.save()
        self.singleSchedul.load(id)
        sCalendar = 'iCal_'+ self.dicUser['Name']
        self.rpc.callRP('Web.addCalendarEvent', sCalendar,self.singleSchedul.firstRecord,  self.dicUser)
        self.setEntriesEditable(self.EntriesPartnerSchedul, FALSE)
        self.tabChanged()

    def on_SchedulEdit1_activate(self, event):
        self.doEdit = self.tabSchedul

        self.setEntriesEditable(self.EntriesPartnerSchedul, TRUE)
   
    def on_SchedulNew_activate(self, event):
        self.out( "new Schedul for partner v2")
        self.doEdit = self.tabSchedul

        self.singleSchedul.newRecord()
        self.setEntriesEditable(self.EntriesPartnerSchedul, TRUE)

    def on_SchedulDelete_activate(self, event):
        self.out( "delete Schedul addresses v2")
        self.singleSchedul.deleteRecord()

    
        
    def on_calendar1_day_selected_double_click(self, event):
        print event
        cal = self.getWidget('calendar1')
        if cal:
            print cal.get_date()
            t0 = cal.get_date()
            print t0
            t1 = `t0[0]`+' '+ `t0[1] +1` + ' ' + `t0[2]` 
            
            print t1
            t2 = time.localtime(time.mktime(time.strptime(t1,'%Y %m %d')))
            
            
            sTime = time.strftime(self.dicUser['DateformatString'], t2)
            print sTime
            
        
            eDate = self.getWidget('eSchedulDate')
            eDate.set_text(sTime)
            
       
    def on_eSchedulDate_changed(self, event):
        self.out(event)
        self.setDateToCalendar(event.get_text(),'calendar1')
        #cal = self.getWidget('calendar1')
        
        #cal.select_month(month, year)
        # cal.select_day(day)


##    def on_calendar1_day_selected(self, cal):
##        print cal
##        date  = cal.get_date()
##        print date
##        print date[0]
##        print date[1]
##        print date[2]
##        eSchedulDate = self.getWidget('eSchedulDate')
##        newDate = mx.DateTime.DateTime(date[0], date[1] + 1, date[2])
##        sDate = newDate.strftime(self.oUser.userDateTimeFormatString)
##        eSchedulDate.set_text(sDate)
        
##    def on_eSchedulDate_changed(self, event):
##        pass

##    def on_hscale1_value_changed(self, hScale):
##        tTime = None
##        hourValue =  hScale.get_value()
##        eSchedulTime = self.getWidget('eSchedulTime')
##        sTime = eSchedulTime.get_text()
##        if sTime:
##            tTime = mx.DateTime.strptime(sTime,self.oUser.userTimeFormatString)
##            oldHour = tTime.hour
##            oldMinute = tTime.minute
            
##            print 'oldHour = ' + `oldHour`
            
##            tTime = mx.DateTime.today(hourValue, oldMinute)
##        else:
##            tTime = mx.DateTime.today(hourValue, 0)
            
##        sTime = tTime.strftime(self.oUser.userTimeFormatString)
##        eSchedulTime.set_text(sTime)
            
##    def on_vscale1_value_changed(self, vScale):
##        tTime = None
##        minuteValue =  vScale.get_value()
##        eSchedulTime = self.getWidget('eSchedulTime')
##        sTime = eSchedulTime.get_text()
##        if sTime:
##            tTime = mx.DateTime.strptime(sTime,self.oUser.userTimeFormatString)
##            oldHour = tTime.hour
##            oldMinute = tTime.minute
            
##            tTime = mx.DateTime.today(oldHour, minuteValue)
##        else:
##            tTime = mx.DateTime.today(0, minuteValue)
            
##        sTime = tTime.strftime(self.oUser.userTimeFormatString)
##        eSchedulTime.set_text(sTime)
            
        
        
    


    # Menu Lists

    def on_liAddressesPhone1_activate(self, event):
        #self.out( "lists startet")
        Pdf = lists_addresses_phone1.lists_addresses_phone1()
        

    def on_liAddressesPhone11_activate(self, event):
        self.out( "lists startet")
        Pdf = lists_addresses_phone11.lists_addresses_phone11()



    #Menu Writer
    def on_newletter1_activate(self, event):
        self.out("writer startet ")

        fkey = 'cuonAddress' + `self.singleAddress.ID`
        self.out( fkey)
        self.pickleObject(fkey , self.singleAddress.getAddress(self.singleAddress.ID))

        sExec = os.environ['CUON_OOEXEC']
        os.system(sExec + ' cuon/OpenOffice/ooMain.py ' + fkey )
        #letter1 = cuon.OpenOffice.letter.letter()
        #letter1.createAddress(singleAddress.ID)


        
    def on_chooseAddress_activate(self, event):
        # choose Address from other Modul
        if self.tabOption == self.tabAddress:
            print '############### Address choose ID ###################'
            self.setChooseValue(self.singleAddress.ID)
            self.closeWindow()
        elif self.tabOption == self.tabPartner:
            print '############### Address choose ID ###################'
            self.setChooseValue(self.singlePartner.ID)
            self.closeWindow()

##        else:
##            print '############### No ID found,  choose ID -1 ###################'
##            self.setChooseValue('-1')
##            self.closeWindow()
## 
##              

        
    # search button
    def on_bSearch_clicked(self, event):
        self.out( 'Searching ....', self.ERROR)
        sName = self.getWidget('eFindName').get_text()
        sCity = self.getWidget('eFindCity').get_text()
        self.out('Name and City = ' + sName + ', ' + sCity, self.ERROR)
        self.singleAddress.sWhere = 'where lastname ~* \'.*' + sName + '.*\' and city ~* \'.*' + sCity + '.*\''
        self.out(self.singleAddress.sWhere, self.ERROR)
        self.refreshTree()
    def on_tree1_row_activated(self, event, data1, data2):
        print 'DoubleClick tree1'
        self.activateClick('chooseAddress', event)


    def saveData(self):
        print 'save Addresses'
        if self.doEdit == tabAddress:
            print 'save 1'
            self.on_save1_activate(None)
        elif self.doEdit == tabBank:
            print 'save 2'
            #self.on_(None)
        elif self.doEdit == tabMisc:
            self.on_MiscSave1_activate(None)
        elif self.doEdit == tabPartner:
            self.on_PartnerSave1_activate(None)
        elif self.doEdit == tabSchedul:
            self.on_SchedulSave_activate(None)
     
    def refreshTree(self):
        self.singleAddress.disconnectTree()
        self.singlePartner.disconnectTree()
        
        if self.tabOption == self.tabAddress:
            self.singleAddress.connectTree()
            self.singleAddress.refreshTree()
        elif self.tabOption == self.tabMisc:
            self.singleMisc.sWhere  ='where address_id = ' + `int(self.singleAddress.ID)`
            self.singleMisc.fillEntries(self.singleMisc.findSingleId())

        elif self.tabOption == self.tabPartner:
            self.singlePartner.sWhere  ='where addressid = ' + `int(self.singleAddress.ID)`
            self.singlePartner.connectTree()
            self.singlePartner.refreshTree()
        elif self.tabOption == self.tabSchedul:
            self.singleSchedul.sWhere  ='where partnerid = ' + `int(self.singlePartner.ID)`
            self.singleSchedul.connectTree()
            self.singleSchedul.refreshTree()
            
     


         
    def tabChanged(self):
        self.out( 'tab changed to :'  + str(self.tabOption))
        
        if self.tabOption == self.tabAddress:
            #Address
            self.disableMenuItem('tabs')
            self.enableMenuItem('address')

            self.actualEntries = self.singleAddress.getEntries()
            self.editAction = 'editAddress'
            self.setStatusbarText([''])
          
            self.setTreeVisible(True)
            

            self.out( 'Seite 0')


        elif self.tabOption == self.tabBank:
            self.out( 'Seite 2')
            self.disableMenuItem('tabs')
            self.enableMenuItem('bank')
           
            self.editAction = 'editBank'
            self.setTreeVisible(False)
            self.setStatusbarText([self.singleAddress.sStatus])


        elif self.tabOption == self.tabMisc:
            self.out( 'Seite 3')

            self.disableMenuItem('tabs')
            self.enableMenuItem('misc')
            self.editAction = 'editMisc'
            self.setTreeVisible(False)
            self.setStatusbarText([self.singleAddress.sStatus])




        elif self.tabOption == self.tabPartner:
            #Partner
            self.disableMenuItem('tabs')
            self.enableMenuItem('partner')
            
            self.out( 'Seite 1')
            self.editAction = 'editPartner'
            self.setTreeVisible(True)
            self.setStatusbarText([self.singleAddress.sStatus])

            
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
        
