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
import SingleAddressBank
import SingleMisc
import SinglePartner
import SingleScheduling
import SingleNotes
import cuon.Bank.SingleBank
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
import cuon.Staff.staff
import cuon.Staff.SingleStaff
import contact
import cuon.E_Mail.sendEmail


class addresswindow(chooseWindows):

    
    def __init__(self, allTables, addrid=0, partnerid=0):

        chooseWindows.__init__(self)
        self.InitForms = True
        
        #print 'time 1 = ', time.localtime()
        self.oDocumentTools = cuon.DMS.documentTools.documentTools()
        self.ModulNumber = self.MN['Address']
        self.singleAddress = SingleAddress.SingleAddress(allTables)
        self.singleAddressBank = SingleAddressBank.SingleAddressBank(allTables)
        self.singleMisc = SingleMisc.SingleMisc(allTables)
        self.singlePartner = SinglePartner.SinglePartner(allTables)
        self.singleBank = cuon.Bank.SingleBank.SingleBank(allTables)
        self.singleSchedul = SingleScheduling.SingleScheduling(allTables)
        self.singleStaff = cuon.Staff.SingleStaff.SingleStaff(allTables)
        self.singleAddressNotes = SingleNotes.SingleNotes(allTables)
        
        self.allTables = allTables
        #print 'time 2 = ', time.localtime()
        
        
        # self.singleAddress.loadTable()

        # self.xml = gtk.glade.XML()
    
        self.loadGlade('address.xml')
        self.win1 = self.getWidget('AddressMainwindow')
        self.win1.maximize()
        
        self.setStatusBar()
        #print 'time 3 = ', time.localtime()


        self.EntriesAddresses = 'addresses.xml'
        self.EntriesAddressesMisc = 'addresses_misc.xml'
        self.EntriesAddressesBank = 'addresses_bank.xml'
        self.EntriesPartner = 'partner.xml'
        self.EntriesPartnerSchedul = 'partner_schedul.xml'
        self.EntriesNotes = 'address_notes.xml'
        
        #print 'time 4 = ', time.localtime()
        
        self.loadEntries(self.EntriesAddresses)
        
        self.singleAddress.setEntries(self.getDataEntries('addresses.xml') )
        self.singleAddress.setGladeXml(self.xml)
        self.singleAddress.setTreeFields( ['lastname', 'firstname','city'] )
        self.singleAddress.setStore( gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING,   gobject.TYPE_UINT) ) 
        self.singleAddress.setTreeOrder('lastname, firstname')
        self.singleAddress.setListHeader([_('Lastname'), _('Firstname'), _('City')])
        if addrid > 0:
            self.singleAddress.sWhere = ' where id = ' + `addrid`
            
        self.singleAddress.setTree(self.xml.get_widget('tree1') )
        #print 'time 5 = ', time.localtime()
        
        #singleAddressBank
        
        self.loadEntries(self.EntriesAddressesBank )
        self.singleAddressBank.setEntries(self.getDataEntries(self.EntriesAddressesBank) )
        self.singleAddressBank.setGladeXml(self.xml)
        self.singleAddressBank.setTreeFields( ['depositor', 'account_number','(select lastname  from address where id = (select address_id from bank where id = bank_id) )as address_name'] )
        self.singleAddressBank.setStore( gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING,   gobject.TYPE_UINT) ) 

        self.singleAddressBank.setTreeOrder('depositor, account_number')
        self.singleAddressBank.setListHeader([_('Depositor'), _('Account'), _('Bank')])

        self.singleAddressBank.sWhere  ='where address_id = ' + `self.singleAddress.ID`
        self.singleAddressBank.setTree(self.xml.get_widget('tree1') )
        #print 'time 6 = ', time.localtime()


  
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
        #print 'time 7 = ', time.localtime()

        self.loadEntries(self.EntriesPartner )
        self.singlePartner.setEntries(self.getDataEntries('partner.xml') )
        self.singlePartner.setGladeXml(self.xml)
        self.singlePartner.setTreeFields( ['lastname', 'firstname','city'] )
        self.singlePartner.setStore( gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING,   gobject.TYPE_UINT) ) 

        self.singlePartner.setTreeOrder('lastname, firstname')
        self.singlePartner.setListHeader([_('Name of partner'), _('Firstname of partner'), _('City')])

        self.singlePartner.sWhere  ='where addressid = ' + `self.singleAddress.ID`
        if partnerid > 0:
            self.singlePartner.sWhere  += ' and id = ' + `partnerid`
        self.singlePartner.setTree(self.xml.get_widget('tree1') )
        #print 'time 8 = ', time.localtime()



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
  
        #print 'time 9 = ', time.localtime()

        #singleNotes
        
        self.loadEntries(self.EntriesNotes )
        self.singleAddressNotes.setEntries(self.getDataEntries('address_notes.xml') )
        self.singleAddressNotes.setGladeXml(self.xml)
        self.singleAddressNotes.setTreeFields([])
        self.singleAddressNotes.setTreeOrder('id')
        
        self.singleAddressNotes.sWhere  ='where address_id = ' + `self.singleAddress.ID`
        self.singleAddressNotes.setTree(self.xml.get_widget('tree1') )
        # self.singleMisc.setStore(gtk.ListStore())
        # set values for comboBox

        #print 'time 10 = ', time.localtime()


        cbFashion = self.getWidget('cbFashion')
        if cbFashion:
            cbFashion.set_popdown_strings([_('Customer'),_('Vendor'),_('Authority')])
        
        


        
            
        #print 'time 11 = ', time.localtime()
        

        # Menu-items
        self.initMenuItems()

        # Close Menus for Tab
        self.addEnabledMenuItems('tabs','mi_address1')
        self.addEnabledMenuItems('tabs','mi_bank1')
        self.addEnabledMenuItems('tabs','mi_misc1')
        self.addEnabledMenuItems('tabs','mi_partner1')
        self.addEnabledMenuItems('tabs','mi_schedul1')
        self.addEnabledMenuItems('tabs','mi_notes1')
               
        # seperate Menus
        self.addEnabledMenuItems('address','mi_address1')
        self.addEnabledMenuItems('partner','mi_partner1')
        self.addEnabledMenuItems('schedul','mi_schedul1')
        self.addEnabledMenuItems('bank','mi_bank1')
        self.addEnabledMenuItems('misc','mi_misc1')
        self.addEnabledMenuItems('notes','mi_notes1')
        
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
        
        # enabledMenues for Notes
        self.addEnabledMenuItems('editNotes', 'NotesEdit1')
  
        # enabledMenues for Save 
        self.addEnabledMenuItems('editSave','mi_save1', self.dicUserKeys['address_save'])
        self.addEnabledMenuItems('editSave','mi_PartnerSave1', self.dicUserKeys['address_partner_save'])
        self.addEnabledMenuItems('editSave','NotesSave', self.dicUserKeys['address_save'])
        self.addEnabledMenuItems('editSave','mi_MiscSave1', self.dicUserKeys['address_save'])

        

        # tabs from notebook
        self.tabAddress = 0
        self.tabBank = 1
        self.tabMisc = 2
        self.tabPartner = 3
        self.tabSchedul = 4
        self.tabNotes = 5
        
        
        #print 'time 20 = ', time.localtime()

        self.tabChanged()
        
        self.win1.add_accel_group(self.accel_group)
        #print 'time 21 = ', time.localtime()
        
        
    #Menu File
              
    def on_quit1_activate(self, event):
        self.out( "exit addresses v2")
        self.closeWindow() 
    
    def fillComboboxForms(self, sName, liCBE):
        widget = self.getWidget(sName)
        
        if widget:
            print sName
       
        print liCBE
        #for value in liCBE:
            
        #    cbeNotesMisc.append_text(value)
        #cbeNotesMisc.set_text_column(liCBE)
        #treestore = cbeNotesMisc.get_model()
        #treestore = gtk.TreeStore(str)
        if liCBE and liCBE != 'NONE':
            for sColumn in liCBE:
                print sColumn
                widget.append_text(sColumn)
                #treestore.set(iter,i, sColumn )
            
            
            model = widget.get_model()
            print model
            print `model`
            
            widget.show()
            widget.set_active(0)
            #cbeNotesMisc.set_sensitive(True)
        
        

    #Menu Address
  
    def on_save1_activate(self, event):
        self.out( "save addresses v2")
        self.doEdit = self.noEdit
        self.singleAddress.save()
        self.setEntriesEditable(self.EntriesAddresses, FALSE)
        self.endEdit()
        self.tabChanged()
        
    def on_new1_activate(self, event):
        self.out( "new addresses v2")
        self.doEdit = self.tabAddress

        self.singleAddress.newRecord()
        self.setEntriesEditable(self.EntriesAddresses, TRUE)
        
        self.getWidget('eAddress').grab_focus()
        self.startEdit()

    def on_edit1_activate(self, event):
        self.out( "edit addresses v2")
        self.doEdit = self.tabAddress
        
        self.setEntriesEditable(self.EntriesAddresses, TRUE)
        self.getWidget('eAddress').grab_focus()
        self.startEdit()
        
    def on_print1_activate(self, event):
        self.out( "print addresses v2")
        p = printAddress.printAddress(self.singleAddress.getFirstRecord() )
        
    def on_delete1_activate(self, event):
        self.out( "delete addresses v2")
        self.singleAddress.deleteRecord()


    # Menu Bank
    def on_bank_new1_activate(self, event):
        
        self.doEdit = self.noEdit
        self.singleBa.addressId = self.singleAddress.ID
        self.singlePartner.save()
        self.setEntriesEditable(self.EntriesPartner, FALSE)
        #self.startEdit()
        self.tabChanged()
        

    
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
        self.endEdit()
        self.tabChanged()
        
    def on_PartnerNew1_activate(self, event):
        self.out( "new Partner addresses v2")
        self.doEdit = self.tabPartner
        
        self.singlePartner.newRecord()
        self.setEntriesEditable(self.EntriesPartner, TRUE)
        self.startEdit()

        
    def on_PartnerEdit1_activate(self, event):
        self.doEdit = self.tabPartner

        self.setEntriesEditable(self.EntriesPartner, TRUE)
        self.startEdit()


    def on_PartnerDelete1_activate(self, event):
        self.out( "delete Partner addresses v2")
        self.singlePartner.deleteRecord()


#Menu Schedul
        
   
    def on_SchedulSave_activate(self, event):
        self.out( "save Schedul addresses v2")
        self.singleSchedul.partnerId = self.singlePartner.ID
        self.doEdit = self.noEdit
        print 'ID = ', self.singleSchedul.ID
        
        id = self.singleSchedul.save()
        print 'save ready'
        self.singleSchedul.load(id)
        sCalendar = 'iCal_'+ self.dicUser['Name']
        self.rpc.callRP('Web.addCalendarEvent', sCalendar,self.singleSchedul.firstRecord,  self.dicUser)
        self.setEntriesEditable(self.EntriesPartnerSchedul, FALSE)
        self.endEdit()
        self.tabChanged()

    def on_SchedulEdit1_activate(self, event):
        self.doEdit = self.tabSchedul

        self.setEntriesEditable(self.EntriesPartnerSchedul, TRUE)
        self.startEdit()

    def on_SchedulNew_activate(self, event):
        self.out( "new Schedul for partner v2")
        self.doEdit = self.tabSchedul

        self.singleSchedul.newRecord()
        self.setEntriesEditable(self.EntriesPartnerSchedul, TRUE)
        self.startEdit()

    def on_SchedulDelete_activate(self, event):
        self.out( "delete Schedul addresses v2")
        self.singleSchedul.deleteRecord()

    # Menu Notes
    def on_NotesSave_activate(self, event):
        
        self.out( "save Notes addresses v2")
        self.doEdit = self.noEdit
        self.singleAddressNotes.addressId = self.singleAddress.ID
        
        self.singleAddressNotes.save()
        self.setEntriesEditable(self.EntriesNotes, FALSE)
        self.tabChanged()

    def on_NotesEdit1_activate(self, event):
        self.out( "edit notes v2")
        self.doEdit = self.tabNotes
        
        self.setEntriesEditable(self.EntriesNotes, TRUE)

    # several functions
        
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
        

    def on_bShowDMS_clicked(self, event):
        print 'dms clicked'
        if self.singleAddress.ID > 0:
            print 'ModulNumber', self.ModulNumber
            Dms = cuon.DMS.dms.dmswindow(self.allTables, self.ModulNumber, {'1':self.singleAddress.ID})
            
    def on_bGeneratePartner_clicked(self, event):
        self.activateClick('mi_PartnerNew1')
        try:
            self.getWidget('ePartnerLastname').set_text(self.singleAddress.getLastname())
            self.getWidget('ePartnerFirstname').set_text(self.singleAddress.getFirstname())
            self.getWidget('ePartnerStreet').set_text(self.singleAddress.getStreet())
            self.getWidget('ePartnerZip').set_text(self.singleAddress.getZip())
            self.getWidget('ePartnerCity').set_text(self.singleAddress.getCity())
            self.getWidget('ePartnerCountry').set_text(self.singleAddress.getCountry())
            self.getWidget('ePartnerLetterAddress').set_text(self.singleAddress.getLetterAddress())
            
        except Exception, params:
            print Exception, params
            
        self.activateClick('mi_PartnerSave1')
        
    def on_bContact_clicked(self, event):
        print 'Contact pressed'
        con1 = contact.contactwindow(self.allTables, self.singleAddress.ID,0)
        
    def on_bPartnerContact_clicked(self, event):
        con1 = contact.contactwindow(self.allTables, self.singleAddress.ID,self.singlePartner.ID)
        
    def on_bLetter_clicked(self, event):
        print 'bLetter clicked'
        if self.singleAddress.ID > 0:
            #self.singleAddress.load(self.singleAddress.ID)
            print 'firstRecord = ', self.singleAddress.firstRecord
            print 'ModulNumber', self.ModulNumber
            dicExtInfo ={'sep_info':{'1':self.singleAddress.ID},'Modul':self.ModulNumber}
            Dms = cuon.DMS.dms.dmswindow(self.allTables, self.MN['Address_info'], {'1':-101}, self.singleAddress.firstRecord,dicExtInfo)
        

    def on_bShowPartnerDMS_clicked(self, event):
        print 'dms Partner clicked'
        if self.singlePartner.ID > 0:
            print 'ModulNumber', self.MN['Partner']
            Dms = cuon.DMS.dms.dmswindow(self.allTables, self.MN['Partner'], {'1':self.singlePartner.ID})
        
    def on_bPartnerLetter_clicked(self, event):
    
        print 'bPartnerLetter clicked'
        if self.singleAddress.ID > 0:
            #self.singleAddress.load(self.singleAddress.ID)
            #self.singlePartner.load(self.singleAddress.ID)
            
            #print 'firstRecord = ', self.singleAddress.firstRecord
            #print 'ModulNumber', self.ModulNumber
            dicExtInfo = {'sep_info':{'1':self.singlePartner.ID},'Modul':self.MN['Partner']}
            dicPartner = self.singlePartner.firstRecord
            for key in self.singleAddress.firstRecord.keys():
                dicPartner['address_' + key] = self.singleAddress.firstRecord[key]
            dicInternInformation = self.rpc.callRP('Database.getInternInformation',self.dicUser)
            if dicInternInformation != 'NONE':
                for key in dicInternInformation:
                    dicPartner[key] = dicInternInformation[key]
                
            Dms = cuon.DMS.dms.dmswindow(self.allTables, self.MN['Partner_info'], {'1':-102}, dicPartner, dicExtInfo)
            
    def on_bSchedulLetter_clicked(self, event):
    
        print 'bSchulLetter clicked'
        if self.singleSchedul.ID > 0:
            dicExtInfo = {'sep_info':{'1':self.singleSchedul.ID},'Modul':self.MN['Partner_Schedul']}
            dicSchedul = self.singleSchedul.firstRecord
            for key in self.singleAddress.firstRecord.keys():
                dicSchedul['address_' + key] = self.singleAddress.firstRecord[key]
            for key in self.singlePartner.firstRecord.keys():
                dicSchedul['partner_' + key] = self.singlePartner.firstRecord[key]
            dicInternInformation = self.rpc.callRP('Database.getInternInformation',self.dicUser, dicSchedul['schedul_staff_id'])
            if dicInternInformation != 'NONE':    
                for key in dicInternInformation:
                    dicSchedul[key] = dicInternInformation[key]
            
            dicSchedul['schedul_time_begin'] = self.getTimeString(dicSchedul['schedul_time_begin'])
            print 'dicSchedul = ', dicSchedul
            print 'lastname', dicSchedul['person1_lastname']
            Dms = cuon.DMS.dms.dmswindow(self.allTables, self.MN['Partner_Schedul_info'], {'1':-103}, dicSchedul, dicExtInfo)
                    
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
        self.findAddress()
    def on_eSearch_key_press_event(self, entry, event):
        print 'eSearch_key_press_event'
        if self.checkKey(event,'NONE','Return'):
            self.findAddress()
    
    def findAddress(self):
        print 'findAddress'
        self.out( 'Searching ....', self.ERROR)
        sName = self.getWidget('eFindName').get_text()
        sCity = self.getWidget('eFindCity').get_text()
        sZip = self.getWidget('eFindZipcode').get_text()
        sFirstname = self.getWidget('eFindFirstname').get_text()
        sID = self.getWidget('eFindID').get_text()
        sStreet = self.getWidget('eFindStreet').get_text()
        sPhone = self.getWidget('eFindPhone').get_text()

        liSearch = []
        if sName:
            liSearch.append('lastname')
            liSearch.append(sName)
        if sID:
            liSearch.append('id')
            try:
                liSearch.append(int(sID))
            except:
                liSearch.append(0)
            
        if sFirstname:
            liSearch.append('firstname')
            liSearch.append(sFirstname)
        if sCity:
            liSearch.append('city')
            liSearch.append(sCity)    
             
        if sZip:
            liSearch.append('zip')
            liSearch.append(sZip)    
        if sStreet:
            liSearch.append('street')
            liSearch.append(sStreet)
            
        if sPhone:
            liSearch.append('phone')
            liSearch.append(sPhone)    
             
        self.singleAddress.sWhere = self.getWhere(liSearch) 
        
        self.out('Address sWhere = ' + `self.singleAddress.sWhere`)
        self.refreshTree()

        
        
        
        
    # Bank aussuchen
        
    def on_tree1_row_activated(self, event, data1, data2):
        print 'DoubleClick tree1'
        self.activateClick('chooseAddress', event)


    def on_bChooseBank_clicked(self, event):
        bank = cuon.Bank.bank.bankwindow(self.allTables)
        bank.setChooseEntry('chooseBank', self.getWidget( 'eBankID'))
        
    def on_eBankID_changed(self, event):
        print 'eBankID changed'
        eAdrField = self.getWidget('tvBank')
        liAdr = self.singleBank.getAddress(long(self.getWidget( 'eBankID').get_text()))
        self.setTextbuffer(eAdrField, liAdr)


    # choose Caller, Representant, Salesman ID`s
    
    def on_bChooseCaller_clicked(self, event):
        staff = cuon.Staff.staff.staffwindow(self.allTables)
        staff.setChooseEntry('chooseStaff', self.getWidget( 'eAddressCallerID'))
        
    def on_bChooseRep_clicked(self, event):
        staff = cuon.Staff.staff.staffwindow(self.allTables)
        staff.setChooseEntry('chooseStaff', self.getWidget( 'eAddressRepID'))
        
    def on_bChooseSalesman_clicked(self, event):
        staff = cuon.Staff.staff.staffwindow(self.allTables)
        staff.setChooseEntry('chooseStaff', self.getWidget( 'eAddressSalesmanID'))
        
    def on_eAddressCallerID_changed(self, event):
        print 'eCallerID changed'
        try:
            eAdrField = self.getWidget('eAddressCaller')
            cAdr = self.singleStaff.getAddressEntry(long(self.getWidget( 'eAddressCallerID').get_text()))
            eAdrField.set_text(cAdr)
        except Exception, params:
            print Exception, params
            

    def on_bSchedulFor_clicked(self, event):
        staff = cuon.Staff.staff.staffwindow(self.allTables)
        staff.setChooseEntry('chooseStaff', self.getWidget( 'eSchedulFor'))
        
    def on_eSchedulFor_changed(self, event):
        print 'eSchedulfor changed'
        try:
            # first set the lastname, firstname to the Field
            eAdrField = self.getWidget('eSchedulForName')
            cAdr = self.singleStaff.getAddressEntry(long(self.getWidget( 'eSchedulFor').get_text()))
            eAdrField.set_text(cAdr)
            # now try to set the scheduls for this staff
            ts = self.getWidget('treeSchedul')
            
        except Exception, params:
            print Exception, params    
            
    # add date and name to notes
            
    def on_bAddNameMisc_clicked(self, event):
        self.addName2Note('tvNotesMisc')

    def on_bAddNameContacter_clicked(self, event):
        self.addName2Note('tvNotesContacter')
    def on_bAddNameRep_clicked(self, event):
        self.addName2Note('tvNotesRep')
    def on_bAddNameSalesman_clicked(self, event):
        self.addName2Note('tvNotesSalesman')

    # add formular to notes
    def on_bAddFormular2NotesMisc_clicked(self, event):
        print 'AddFormular2NoticesMisc clicked'
        self.addForm2Note('cbeNotesMisc','tvNotesMisc')
        
    def on_bAddFormular2NotesContacter_clicked(self, event):
        print 'AddFormular2NoticesContacter clicked'
        self.addForm2Note('cbeNotesContacter','tvNotesContacter')
    
    def on_bAddFormular2NotesRep_clicked(self, event):
        print 'AddFormular2NoticesRep clicked'
        self.addForm2Note('cbeNotesRep','tvNotesRep')
       
    def on_bAddFormular2NotesSalesman_clicked(self, event):
        print 'AddFormular2NoticesSalesman clicked'
        self.addForm2Note('cbeNotesSalesman','tvNotesSalesman')

    # send E-mail 
    def on_bSendEmailAddress_clicked(self, event):
        em = cuon.E_Mail.sendEmail.sendEmail()
    def on_bSendEmailPartner_clicked(self, event):
        em = cuon.E_Mail.sendEmail.sendEmail()
    def on_bSendEmailSchedul_clicked(self, event):
        em = cuon.E_Mail.sendEmail.sendEmail()
        
    def addForm2Note(self, sInput, sOutput):
        
        s = self.getActiveText(self.getWidget(sInput))
        print 'ActiveText', s
        
        if s:
            iNr = 0
            try:
                iFind = s.find('###')
                iNr = int(s[iFind+3:])
            except Exception, param:
                print Exception,param
            
            if iNr:
                Formular = self.rpc.callRP('Misc.getForm',iNr, self.dicUser)
                print Formular
                if Formular  and Formular != 'NONE':
                    newForm = self.doUncompress(self.doDecode(Formular[0]['document_image']))
                    print 'newForm', newForm
                    self.add2Textbuffer(self.getWidget(sOutput),newForm,'Tail')


    def addName2Note(self, sWidget):
        t1 = self.rpc.callRP('User.getDate', self.dicUser)
        t2 = self.rpc.callRP('User.getStaffAddressString', self.dicUser)
        text = t1 + ' : ' + t2 + '\n'
        print text
        self.add2Textbuffer(self.getWidget(sWidget),text,'Tail')
        
    
    def saveData(self):
        print 'save Addresses'
        if self.doEdit == self.tabAddress:
            print 'save 1'
            self.on_save1_activate(None)
        elif self.doEdit == self.tabBank:
            print 'save 2'
            #self.on_(None)
        elif self.doEdit == self.tabMisc:
            self.on_MiscSave1_activate(None)
        elif self.doEdit == self.tabPartner:
            self.on_PartnerSave1_activate(None)
        elif self.doEdit == self.tabSchedul:
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
            
        elif self.tabOption == self.tabNotes:
            self.singleAddressNotes.sWhere  ='where address_id = ' + `int(self.singleAddress.ID)`
            self.singleAddressNotes.fillEntries(self.singleAddressNotes.findSingleId())

            if self.InitForms:
                # set popdown for forms
                
                liCBE = self.rpc.callRP('Misc.getFormsAddressNotes', self.MN['Forms_Address_Notes_Misc'], self.dicUser) 
                self.fillComboboxForms('cbeNotesMisc', liCBE)
                
                liCBE = self.rpc.callRP('Misc.getFormsAddressNotes', self.MN['Forms_Address_Notes_Contacter'], self.dicUser) 
                self.fillComboboxForms('cbeNotesContacter', liCBE)
                
                liCBE = self.rpc.callRP('Misc.getFormsAddressNotes', self.MN['Forms_Address_Notes_Rep'], self.dicUser) 
                self.fillComboboxForms('cbeNotesRep', liCBE)
                
                liCBE = self.rpc.callRP('Misc.getFormsAddressNotes', self.MN['Forms_Address_Notes_Salesman'], self.dicUser) 
                self.fillComboboxForms('cbeNotesSalesman', liCBE)
                
                self.InitForms = False
                
         
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
            
            
        elif self.tabOption == self.tabNotes:
            self.out( 'Seite 3')

            self.disableMenuItem('tabs')
            self.enableMenuItem('notes')
            self.editAction = 'editNotes'
            self.setTreeVisible(False)
            self.setStatusbarText([self.singleAddress.sStatus])

        # refresh the Tree
        self.refreshTree()

        self.enableMenuItem(self.editAction)
        self.editEntries = False
        
