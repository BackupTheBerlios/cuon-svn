 # -*- coding: utf-8 -*-

##Copyright (C) [2003 -2007]  [Jürgen Hamel, D-32584 Löhne]

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
import commands
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
import cuon.DMS.SingleDMS

import cuon.DMS.dms
import printAddress
import cuon.Staff.staff
import cuon.Staff.SingleStaff
import contact
import cuon.E_Mail.sendEmail
import cuon.Misc.cuon_dialog
import cuon.Misc.misc
import cuon.Order.order
import cuon.PrefsFinance.prefsFinance
import cuon.PrefsFinance.SinglePrefsFinanceTop
import cuon.Project.project

class addresswindow(chooseWindows):

    
    def __init__(self, allTables, addrid=0, partnerid=0):

        chooseWindows.__init__(self)
        self.InitForms = True
        self.connectSchedulTreeId = None
        self.OrderID = 0
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
        self.singleDMS = cuon.DMS.SingleDMS.SingleDMS(allTables)
        self.singlePrefsFinanceTop = cuon.PrefsFinance.SinglePrefsFinanceTop.SinglePrefsFinanceTop(allTables)
        
       
        
        self.allTables = allTables
        #print 'time 2 = ', time.localtime()
        
        
        # self.singleAddress.loadTable()

        # self.xml = gtk.glade.XML()
    
        self.loadGlade('address.xml', 'AddressMainwindow')
        #self.win1 = self.getWidget('AddressMainwindow')
        self.win1.maximize()
        
        self.setStatusBar()
        #print 'time 3 = ', time.localtime()
 
        # Trees for Order and Invoice
        self.treeOrder = cuon.Misc.misc.Treeview()
        self.treeInvoice = cuon.Misc.misc.Treeview()
       
        self.treeOrder.start(self.getWidget('tvAddressOrder'),'Text','Order')
        self.treeInvoice.start(self.getWidget('tvAddressInvoices'),'Text','Invoice')
        

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
        self.singleAddress.setTreeFields( ['lastname', 'firstname','city','phone','status_info'] )
        self.singleAddress.setStore( gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING,  gobject.TYPE_UINT) ) 
        self.singleAddress.setTreeOrder('lastname, firstname')
        self.singleAddress.setListHeader([_('Lastname'), _('Firstname'), _('City'),_('Phone'),_('Info')])
        if addrid > 0:
            self.singleAddress.sWhere = ' where id = ' + `addrid`
            
        self.singleAddress.setTree(self.xml.get_widget('tree1') )
        #print 'time 5 = ', time.localtime()
        
        #singleAddressBank
        
        self.loadEntries(self.EntriesAddressesBank )
        self.singleAddressBank.setEntries(self.getDataEntries(self.EntriesAddressesBank) )
        self.singleAddressBank.setGladeXml(self.xml)
        self.singleAddressBank.setTreeFields( ['depositor', 'account_number','address_id'] )
        self.singleAddressBank.setStore( gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_UINT,   gobject.TYPE_UINT) ) 

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
            pass
            #self.singlePartner.sWhere  += ' and id = ' + `partnerid`
        self.singlePartner.setTree(self.xml.get_widget('tree1') )
        #print 'time 8 = ', time.localtime()



        #singleScheduling
        
        self.loadEntries(self.EntriesPartnerSchedul )
        self.singleSchedul.setEntries(self.getDataEntries('partner_schedul.xml') )
        self.singleSchedul.setGladeXml(self.xml)
        self.singleSchedul.setTreeFields( ['schedul_date',"to_char(round(schedul_time_begin/4),'99') || ':' || to_char(round(mod(schedul_time_begin,4)*15,0),'09MI') as begindate ","to_char(round(schedul_time_end/4),'99') || ':' || to_char(round(mod(schedul_time_end,4)*15,0),'09MI') as enddate ",'short_remark','priority','process_status'] )
        self.singleSchedul.setStore( gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_UINT, gobject.TYPE_UINT,   gobject.TYPE_UINT) ) 
        #self.singleSchedul.setTreeFields( [ 'short_remark','priority','process_status'] )
        #self.singleSchedul.setStore( gtk.ListStore( gobject.TYPE_STRING, gobject.TYPE_UINT, gobject.TYPE_UINT,   gobject.TYPE_UINT) ) 
        self.singleSchedul.setTreeOrder("to_date(schedul_date," + "'" + self.dicUser['SQLDateFormat'] + "')" + ',schedul_time_begin')
        self.singleSchedul.setListHeader([_('Date '),_('Begin'), _('End'), _('shortRemark'), _('Priority'), _('Status')])
 

        self.singleSchedul.sWhere  ='where partnerid = ' + `self.singlePartner.ID` + ' and process_status != 999 '
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
        self.addEnabledMenuItems('tabs','mi_order1')
               
        # seperate Menus
        self.addEnabledMenuItems('address','mi_address1')
        self.addEnabledMenuItems('partner','mi_partner1')
        self.addEnabledMenuItems('schedul','mi_schedul1')
        self.addEnabledMenuItems('bank','mi_bank1')
        self.addEnabledMenuItems('misc','mi_misc1')
        self.addEnabledMenuItems('notes','mi_notes1')
        self.addEnabledMenuItems('order','mi_order1')
        
        # enabledMenues for Address
        self.addEnabledMenuItems('editAddress','mi_new1' , self.dicUserKeys['address_new'])
        self.addEnabledMenuItems('editAddress','mi_clear1', self.dicUserKeys['address_delete'])
        self.addEnabledMenuItems('editAddress','mi_print1', self.dicUserKeys['address_print'])
        self.addEnabledMenuItems('editAddress','mi_edit1', self.dicUserKeys['address_edit'])


        # enabledMenues for Misc
        self.addEnabledMenuItems('editMisc', '')
  

        # enabledMenues for Partner
        self.addEnabledMenuItems('editPartner', 'PartnerNew1', self.dicUserKeys['address_partner_new'])
        self.addEnabledMenuItems('editPartner','PartnerDelete1', self.dicUserKeys['address_partner_delete'])
        #self.addEnabledMenuItems('editPartner','PartnerPrint1', self.dicUserKeys['address_partner_print'])
        self.addEnabledMenuItems('editPartner','PartnerEdit1', self.dicUserKeys['address_partner_edit'])

        # enabledMenues for Schedul
        self.addEnabledMenuItems('editSchedul', 'SchedulNew', self.dicUserKeys['address_new'])
        self.addEnabledMenuItems('editSchedul', 'SchedulEdit1', self.dicUserKeys['address_edit'])
        #self.addEnabledMenuItems('editSchedul','mi_SchedulDelete')
        #self.addEnabledMenuItems('editSchedul','mi_SchedulPrint1')
        
        # enabledMenues for Notes
        self.addEnabledMenuItems('editNotes', 'NotesEdit1', self.dicUserKeys['address_edit'])
  
        # enabledMenues for Save 
        self.addEnabledMenuItems('editSave','mi_save1', self.dicUserKeys['address_save'])
        self.addEnabledMenuItems('editSave','PartnerSave1', self.dicUserKeys['address_partner_save'])
        self.addEnabledMenuItems('editSave','NotesSave', self.dicUserKeys['address_save'])
        self.addEnabledMenuItems('editSave','schedulSave', self.dicUserKeys['address_save'])
        self.addEnabledMenuItems('editSave','mi_MiscSave1', self.dicUserKeys['address_save'])

        

        # tabs from notebook
        self.tabAddress = 0
        self.tabBank = 1
        self.tabMisc = 2
        self.tabPartner = 3
        self.tabSchedul = 4
        self.tabNotes = 5
        self.tabOrder = 6
        
        ts = self.getWidget('treeScheduls')
        #treeview.set_model(liststore)
 
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Scheduls", renderer, text=0)
        ts.append_column(column)
        
        #print 'time 20 = ', time.localtime()

        # some Variables
        self.notebook2 = self.getWidget('notebook2')
        self.tabChanged()
        
        self.win1.add_accel_group(self.accel_group)
        #print 'time 21 = ', time.localtime()
        
        
    
    #Menu File
              
    def on_quit1_activate(self, event):
        self.out( "exit addresses v2")
        self.closeWindow() 
        
        
    def on_newsletter_email_activate(self, event):
        dicV = {}
        dicV['From'] = self.dicUser['Email']['From']
        dicV['To'] = 'Newsletter: '
        dicV['Signatur'] = self.dicUser['Email']['Signatur']

        print dicV
        em = cuon.E_Mail.sendEmail.sendEmail(dicV)
        
    def on_newsletter_print_activate(self, event):
        
        Dms = cuon.DMS.dms.dmswindow(self.allTables, self.MN['Newsletter'])
        
##        cd = cuon.Misc.cuon_dialog.cuon_dialog()
##        ok, res = cd.inputLine( _('Email Newsletter'), _('insert label(s) for newsletter'))
##        print ok, res
##        if ok and res:
##            ok = self.rpc.callRP('sendNewsletterEmail', res, email_text=None, acttachment=None)
##            
        

    #Menu Address
  
    def on_save1_activate(self, event):
        self.out( "save addresses v2")
        if self.singleAddress.save() == 0:
            self.errorMsg( _('saving this Address failed. Please check'))
        else:
            self.doEdit = self.noEdit
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
    
    def on_bank_save1_activate(self, event):
        self.out( "save Bank addresses v2")
        if self.singleAddressBank.save() == 0:
            self.errorMsg( _('saving this bank failed. Please check'))
        else:
        
            self.doEdit = self.noEdit
            self.singleAddressBank.addressId = self.singleAddress.ID
            self.setEntriesEditable(self.EntriesAddressesBank, FALSE)
            self.endEdit()
            self.tabChanged()
        
    
    def on_bank_new1_activate(self, event):
        print 'bank new activate'
        self.doEdit = self.tabBank
        self.singleAddressBank.newRecord()
        self.setEntriesEditable(self.EntriesAddressesBank, True)
        self.startEdit()
        
    def on_bank_edit1_activate(self, event):
        print 'bank edit activate'

        self.out( "edit addresses v2")
        self.doEdit = self.tabBank
        
        self.setEntriesEditable(self.EntriesAddressesBank, TRUE)
        self.startEdit()
        
    def on_bank_delete1_activate(self, event):
        print 'bank delete activate'
        self.out( "delete addresses v2")
        self.singleAddressBank.deleteRecord()

    
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
        self.singlePartner.addressId = self.singleAddress.ID
        if self.singlePartner.save() == 0:
        
            self.errorMsg( _('saving this partner failed. Please check'))
        else:
            self.doEdit = self.noEdit
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
        nID = 0
        id = 0
        self.out( "save Schedul addresses v2")
        self.singleSchedul.partnerId = self.singlePartner.ID
        print 'ID = ', self.singleSchedul.ID
        
        id = self.singleSchedul.save()
        if id == 0:
            self.errorMsg( _('saving this schedul failed. Please check'))
        else:
            self.doEdit = self.noEdit
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
        self.singleAddressNotes.addressId = self.singleAddress.ID
        
        if self.singleAddressNotes.save() == 0:
         
            self.errorMsg( _('save this notes failed. Please check'))
        else:
            
    
            self.doEdit = self.noEdit
    
            self.setEntriesEditable(self.EntriesNotes, FALSE)
            if self.rpc.callRP('Misc.sendNotes0', self.dicUser, self.notebook2.get_current_page() ):
            
                liEmailAddresses  = self.rpc.callRP('Misc.getAdditionalEmailAddressesNotes0',self.singleAddress.ID, self.dicUser)
                print 'liEmailAddresses = ', liEmailAddresses
                if liEmailAddresses and liEmailAddresses not in ['NONE','ERROR']:
                    self.singleDMS.loadNotes0SaveDocument()
                    dicVars, dicExtInfo = self.getAddressInfos()
                    dicVars['email_subject'] = `dicVars['id']` + ', ' + _('CUON-ID NOTES-01')
                    dicVars['Body'] = _('Notes are changed !') + '\n ID = ' + `dicVars['id']` + '\n\n ' + dicVars['lastname'] + '\n' + dicVars['lastname2'] + '\n'
                    dicVars['Body'] += '\n\n' +  dicVars['street'] +'\n' 
                    dicVars['Body'] +=  dicVars['zip'] + ' ' + dicVars['city'] +'\n\n' 
                    dicVars['Body'] += _('Infos are generated by C.U.O.N.')
                    
                    
                    self.oDocumentTools.viewDocument(self.singleDMS, self.dicUser, dicVars, 'sentAutomaticEmail', liEmailAddresses)
                    
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
            
            if self.getWidget('rbBeginDate').get_active():
                eDate = self.getWidget('eSchedulDateBegin')
            else:
                eDate = self.getWidget('eSchedulDateEnd')
                
            eDate.set_text(sTime)
            
    def on_bPartnerSip_clicked(self, event):
        print 'Sip dial startet'
        cmd1 = self.dicUser['prefApps']['SIP'] 
        #s = self.dicUser['prefApps']['SIP_PARAMS'], self.singlePartner.firstRecord['sip'] 
        print 'Address cmd1', cmd1
        print '1', self.dicUser['prefApps']['SIP_PARAMS']
        print '2',  self.singlePartner.firstRecord['sip']
        #print s
        #print '------------------------------------------'
        self.startExternalPrg(cmd1, self.dicUser['prefApps']['SIP_PARAMS'], self.singlePartner.firstRecord['sip'])
        
        #status,data = commands.getstatusoutput(s)
        
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
        self.activateClick('PartnerNew1')
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
            
        self.activateClick('PartnerSave1')
        
    def on_bContact_clicked(self, event):
        print 'Contact pressed'
        con1 = contact.contactwindow(self.allTables, self.singleAddress.ID,0)
        
    def on_bPartnerContact_clicked(self, event):
        con1 = contact.contactwindow(self.allTables, self.singleAddress.ID,self.singlePartner.ID)
        
    def on_bLetter_clicked(self, event):
        print 'bLetter clicked'
        if self.singleAddress.ID > 0:
            firstRecord, dicExtInfo = self.getAddressInfos()
            Dms = cuon.DMS.dms.dmswindow(self.allTables, self.MN['Address_info'], {'1':-101}, firstRecord,dicExtInfo)
        

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
            if dicInternInformation not in ['NONE','ERROR']:
                for key in dicInternInformation:
                    dicPartner[key] = dicInternInformation[key]
            dicNotes = self.rpc.callRP('Address.getNotes',self.singleAddress.ID, self.dicUser)
            if dicNotes and dicNotes not in ['NONE','ERROR']:
                for key in dicNotes:
                    dicPartner['notes_' + key] = dicNotes[key]    
            dicPartner = self.addDateTime(dicPartner)
            print dicPartner
            Dms = cuon.DMS.dms.dmswindow(self.allTables, self.MN['Partner_info'], {'1':-102}, dicPartner, dicExtInfo)
            
    def on_bSchedulLetter_clicked(self, event):
        print 'bSchulLetter clicked'
        if self.singleSchedul.ID > 0:
            dicSchedul, dicExtInfo = self.getSchedulInfos()
    
        #print 'lastname', dicSchedul['person1_lastname']
            Dms = cuon.DMS.dms.dmswindow(self.allTables, self.MN['Partner_Schedul_info'], {'1':-103}, dicSchedul, dicExtInfo)
    def getAddressInfos(self):
    
        firstRecord = None
        if self.singleAddress.ID > 0:
            #self.singleAddress.load(self.singleAddress.ID)
            firstRecord = self.singleAddress.firstRecord
            print 'ModulNumber', self.ModulNumber
            dicNotes = self.rpc.callRP('Address.getNotes',self.singleAddress.ID, self.dicUser)
            if dicNotes and dicNotes not in ['NONE','ERROR']:
                for key in dicNotes:
                    firstRecord['notes_' + key] = dicNotes[key]
            firstRecord = self.addDateTime(firstRecord)
            dicExtInfo ={'sep_info':{'1':self.singleAddress.ID},'Modul':self.ModulNumber}
        
        return firstRecord, dicExtInfo
    
    def getSchedulInfos(self):
        dicSchedul = {}
        dicExtInfo = {}
        if self.singleSchedul.ID > 0:
            dicExtInfo = {'sep_info':{'1':self.singleSchedul.ID},'Modul':self.MN['Partner_Schedul']}
            dicSchedul = self.singleSchedul.firstRecord
            for key in self.singleAddress.firstRecord.keys():
                dicSchedul['address_' + key] = self.singleAddress.firstRecord[key]
            for key in self.singlePartner.firstRecord.keys():
                dicSchedul['partner_' + key] = self.singlePartner.firstRecord[key]
            dicInternInformation = self.rpc.callRP('Database.getInternInformation',self.dicUser, dicSchedul['schedul_staff_id'])
            if dicInternInformation not in ['NONE','ERROR']:    
                for key in dicInternInformation:
                    dicSchedul[key] = dicInternInformation[key]

            dicNotes = self.rpc.callRP('Address.getNotes',self.singleAddress.ID, self.dicUser)
            if dicNotes and dicNotes not in ['NONE','ERROR']:
                for key in dicNotes:
                    dicSchedul['notes_' + key] = dicNotes[key]
                    
            dicSchedul['schedul_time_begin'] = self.getTimeString(dicSchedul['schedul_time_begin'])
            #print 'dicSchedul = ', dicSchedul
            dicSchedul = self.addDateTime(dicSchedul)
            
        return dicSchedul, dicExtInfo
        
    # choose Address
        
    def on_tree1_row_activated(self, event, data1, data2):
        print 'DoubleClick tree1'
        self.activateClick('chooseAddress', event)


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

    def on_set_ready1_activate(self, event):
        self.activateClick('SchedulEdit1')
        sp = self.getWidget('eSchedulProcess')
        sp.set_text('999')
        self.activateClick('schedulSave')
        
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
            liSearch.append('lastname2')
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
            liSearch.append('fax')
            liSearch.append(sPhone)    
            liSearch.append('phone_handy')
            liSearch.append(sPhone)    
             
        self.singleAddress.sWhere = self.getWhere(liSearch) 
        
        self.out('Address sWhere = ' + `self.singleAddress.sWhere`)
        self.oldTab = -1
        self.refreshTree()

        
        
        
    
    # choose Bank 

    def on_bChooseBank_clicked(self, event):
        bank = cuon.Bank.bank.bankwindow(self.allTables)
        bank.setChooseEntry('chooseBank', self.getWidget( 'eBankID'))
        
    def on_eBankID_changed(self, event):
        print 'eBankID changed'
        eAdrField = self.getWidget('tvBank')
        try:
            liAdr = self.singleBank.getAddress(long(self.getWidget( 'eBankID').get_text()))
            self.setTextbuffer(eAdrField, liAdr)
        except Exception, param:
            self.setTextbuffer(eAdrField, ' ')
            print Exception,param
            
    # choose terms of payment
    

    def on_bSearchTOP_clicked(self, event):
        top = cuon.PrefsFinance.prefsFinance.prefsFinancewindow(self.allTables)
        top.setChooseEntry('chooseTOP', self.getWidget( 'eTOPID'))
        
    def on_eTOPID_changed(self, event):
        print 'eTOPID changed'
        eTopField = self.getWidget('tvTOP')
        try:
            liTop = self.singlePrefsFinanceTop.getTOP(long(self.getWidget( 'eTOPID').get_text()))
            self.setTextbuffer(eTopField, liTop)
        except Exception,param:
            self.setTextbuffer(eTopField, ' ')
            print Exception,param

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
            eAdrField.set_text('')
    def on_eAddressRepID_changed(self, event):
        print 'eRepID changed'
        try:
        
            eAdrField = self.getWidget('eAddressRep')
            cAdr = self.singleStaff.getAddressEntry(long(self.getWidget( 'eAddressRepID').get_text()))
            eAdrField.set_text(cAdr)
        except Exception, params:
            print Exception, params
            eAdrField.set_text('')
            
    def on_eAddressSalesmanID_changed(self, event):
        print 'eSalesmanID changed'
        try:
        
            eAdrField = self.getWidget('eAddressSalesman')
            cAdr = self.singleStaff.getAddressEntry(long(self.getWidget( 'eAddressSalesmanID').get_text()))
            eAdrField.set_text(cAdr)
        except Exception, params:
            print Exception, params
            eAdrField.set_text('')
            
    def on_bSchedulFor_clicked(self, event):
        staff = cuon.Staff.staff.staffwindow(self.allTables)
        staff.setChooseEntry('chooseStaff', self.getWidget( 'eSchedulFor'))
        
    def on_new_order_activate(self, event):
        print 'new order'
        dicOrder = {}
        dicOrder['addressnumber'] = self.singleAddress.ID
        dicOrder['ModulNumber'] = self.ModulNumber
        dicDate = self.getActualDateTime()
        dicOrder['orderedat'] = dicDate['date']
        dicOrder['deliveredat'] = dicDate['date']
        
        orderwindow = cuon.Order.order.orderwindow(self.allTables,dicOrder,True)
    def on_new_project_activate(self, event):
        print 'new project'
        dicProject = {}
        dicProject['addressid'] = self.singleAddress.ID
        dicProject['ModulNumber'] = self.ModulNumber
        projectwindow = cuon.Project.project.projectwindow(self.allTables,dicProject,True)
            
    def on_tbNewOrder_clicked(self, event):
        print 'new order toolbar '
        self.activateClick('new_order')
    

    def on_tbNewProject_clicked(self, event):
        print 'new order toolbar '
        self.activateClick('new_project')
    
    def disconnectSchedulTree(self):
        try:
            
            self.getWidget('treeScheduls').get_selection().disconnect(self.connectSchedulTreeId)
        except:
            pass

    def connectSchedulTree(self):
        try:
            self.connectSchedulTreeId = self.getWidget('treeScheduls').get_selection().connect("changed", self.SchedulTree_select_callback)
        except:
            pass
   
    def SchedulTree_select_callback(self, treeSelection):
        listStore, iter = treeSelection.get_selected()
        
        print listStore,iter
        
        if listStore and len(listStore) > 0:
           row = listStore[0]
        else:
           row = -1
   
        if iter != None:
            sNewId = listStore.get_value(iter, 0)
            print sNewId
            try:
                newID = int(sNewId[sNewId.find('###')+ 3:])
                #self.setDateValues(newID)
                
            except:
                pass
                   
    def on_eSchedulFor_changed(self, event):
        print 'eSchedulfor changed'
        try:
            # first set the lastname, firstname to the Field
            eAdrField = self.getWidget('eSchedulForName')
            cAdr = self.singleStaff.getAddressEntry(long(self.getWidget( 'eSchedulFor').get_text()))
            eAdrField.set_text(cAdr)
            # now try to set the scheduls for this staff
            ts = self.getWidget('treeScheduls')
            print 'ts = ', ts
            treestore = gtk.TreeStore(object)
            treestore = gtk.TreeStore(str)
            ts.set_model(treestore)
                
            liDates = self.rpc.callRP('Address.getAllActiveSchedul',self.dicUser,'Schedul',self.getWidget( 'eSchedulFor').get_text() )
            print 'Schedul by schedul_date: ', liDates
            if liDates and liDates not in ['NONE','ERROR']:
                lastRep = None
                lastSalesman = None
                Schedulname = None
                lastSchedulname = None
                
                #iter = treestore.append(None,[_('Schedul')])
                #print 'iter = ', iter
                iter2 = None
                iter3 = None
                liDates.reverse()
                for oneDate in liDates:
                    Schedulname = oneDate['date']
                    if lastSchedulname != Schedulname:
                        lastSchedulname = Schedulname
                        iter = treestore.append(None,[lastSchedulname])   
                    sTime  = self.getTimeString(oneDate['time_begin'] )
                    sTimeEnd =     self.getTimeString(oneDate['time_end'] )
                    iter2 = treestore.insert_before(iter,None,[oneDate['a_zip'] + ' ' + oneDate['a_city'] +', ' + oneDate['a_lastname'] +', ' + sTime + ' - ' + sTimeEnd + ' ###' +  `oneDate['id']`])           
                print 'End liDates'
            ts.show()
            #self.getWidget('scrolledwindow10').show()
            self.connectSchedulTree()
            print 'ts', ts
            
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
    def on_bSendMail_clicked(self, event):
        dicV = {}
        dicV['From'] = self.dicUser['Email']['From']
        dicV['To'] = self.singleAddress.getEmail()
        dicV['Signatur'] = self.dicUser['Email']['Signatur']
        
        print dicV
        em = cuon.E_Mail.sendEmail.sendEmail(dicV)
        
    def on_bSendExternEmail_clicked(self, event):
        pass
    
    def on_bSendPartnerEmail_clicked(self, event):
            
        dicV = {}
        dicV['From'] = self.dicUser['Email']['From']
        dicV['To'] = self.singlePartner.getEmail()
        print dicV
        em = cuon.E_Mail.sendEmail.sendEmail(dicV)
        
    
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
                if Formular  and Formular not in ['NONE','ERROR']:
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
        elif self.doEdit == self.tabNotes:
            self.on_NotesSave_activate(None)
    
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
        if liCBE and liCBE not in ['NONE','ERROR']:
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
    def on_tbSave_clicked(self, event):
        print 'save Addresses'
        if self.tabOption  == self.tabAddress:
            print 'save 1'
            self.on_save1_activate(None)
        elif self.tabOption  == self.tabBank:
            print 'save 2'
            #self.on_(None)
        elif self.tabOption  == self.tabMisc:
            self.on_MiscSave1_activate(None)
        elif self.tabOption  == self.tabPartner:
            self.on_PartnerSave1_activate(None)
        elif self.tabOption  == self.tabSchedul:
            self.on_SchedulSave_activate(None)
        elif self.tabOption  == self.tabNotes:
            self.on_NotesSave_activate(None)
            
    def on_tbNew_clicked(self, event):
        print 'new Addresses'
        if self.tabOption  == self.tabAddress:
            self.on_new1_activate(None)
        elif self.tabOption  == self.tabBank:
            pass
        elif self.tabOption  == self.tabMisc:
            self.on_MiscNew1_activate(None)
        elif self.tabOption  == self.tabPartner:
            self.on_PartnerNew1_activate(None)
        elif self.tabOption  == self.tabSchedul:
            self.on_SchedulNew_activate(None)
        elif self.tabOption  == self.tabNotes:
            self.on_NotesNew_activate(None)
            
    def on_tbEdit_clicked(self, event):
        print 'edit Addresses'
        if self.tabOption  == self.tabAddress:
            self.on_edit1_activate(None)
        elif self.tabOption  == self.tabBank:
            pass
        elif self.tabOption  == self.tabMisc:
            self.on_MiscEdit1_activate(None)
        elif self.tabOption  == self.tabPartner:
            self.on_PartnerEdit1_activate(None)
        elif self.tabOption  == self.tabSchedul:
            self.on_SchedulEdit1_activate(None)
        elif self.tabOption  == self.tabNotes:
            self.on_NotesEdit1_activate(None)
    def on_tbExtendetInfo_clicked(self, event):
        if self.tabOption  == self.tabAddress:
            self.on_bShowDMS_clicked(None)
        elif self.tabOption  == self.tabPartner:
            self.on_bShowPartnerDMS_clicked(None)
           
    def on_tbLetter_clicked(self, event):
        if self.tabOption  == self.tabAddress:
            self.on_bLetter_clicked(None)
        elif self.tabOption  == self.tabPartner:
            self.on_bPartnerLetter_clicked(None)
                  
    def on_tbAllContact_clicked(self, event):
        con1 = contact.contactwindow(self.allTables, 0,0)
    def on_tbContact_clicked(self, event):        
        self.on_bContact_clicked(None)
        
    def disconnectOrderTree(self):
        try:
            
            self.getWidget('treeScheduls').get_selection().disconnect(self.connectSchedulTreeId)
        except:
            pass

    def connectOrderTree(self):
        try:
            self.connectSchedulTreeId = self.getWidget('tvAddressOrder').get_selection().connect("changed", self.OrderTree_select_callback)
        except:
            pass
   
    def OrderTree_select_callback(self, treeSelection):
        listStore, iter = treeSelection.get_selected()
        self.OrderID = 0
        print listStore,iter
        
        if listStore and len(listStore) > 0:
           row = listStore[0]
        else:
           row = -1
   
        if iter != None:
            sNewId = listStore.get_value(iter, 0)
            print sNewId
            try:
                self.OrderID = int(sNewId[sNewId.find('###')+ 3:])
                #self.setDateValues(newID)
                
            except:
                pass
                
    def on_tvAddressOrder_row_activated(self,event,data1, data2):
        if self.OrderID:
            orderwindow = cuon.Order.order.orderwindow(self.allTables,None,False,self.OrderID)
        
    def setOrderValues(self):
        liGroup = self.rpc.callRP('Order.getOrderForAddress',self.singleAddress.ID, self.dicUser)
        if liGroup and liGroup not in ['NONE','ERROR']:
            self.treeOrder.fillTree(self.getWidget('tvAddressOrder'),liGroup,['number','designation', 'orderedat'],'self.connectOrderTree()')
            self.connectOrderTree()
        else:
            self.treeOrder.fillTree(self.getWidget('tvAddressOrder'),[],['number','designation', 'orderedat'],'self.connectOrderTree()')
            self.connectOrderTree()
    # stats 
  
    
    def refreshTree(self):
        self.singleAddress.disconnectTree()
        self.singlePartner.disconnectTree()
        self.singleSchedul.disconnectTree()
        self.singleAddressBank.disconnectTree()
        
        if self.tabOption == self.tabAddress:
            self.singleAddress.connectTree()
            if self.oldTab < 1:
                self.singleAddress.refreshTree()
            else:
                self.singleAddress.refreshTree(False)
                
        elif self.tabOption == self.tabBank:
            self.singleAddressBank.sWhere  ='where address_id = ' + `self.singleAddress.ID`

            self.singleAddressBank.connectTree()
            self.singleAddressBank.refreshTree()    
            
        elif self.tabOption == self.tabMisc:
            self.singleMisc.sWhere  ='where address_id = ' + `int(self.singleAddress.ID)`
            self.singleMisc.fillEntries(self.singleMisc.findSingleId())

        elif self.tabOption == self.tabPartner:
            self.singlePartner.sWhere  ='where addressid = ' + `int(self.singleAddress.ID)`
            self.singlePartner.connectTree()
            self.singlePartner.refreshTree()
            
        elif self.tabOption == self.tabSchedul:
            self.singleSchedul.sWhere  ='where partnerid = ' + `int(self.singlePartner.ID)` + ' and process_status != 999 '
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

        self.oldTab = self.tabOption
        
 
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
            self.setTreeVisible(True)
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
            self.getWidget('rbBeginDate').set_active(True)
            
            
        elif self.tabOption == self.tabNotes:
            self.out( 'Seite 3')

            self.disableMenuItem('tabs')
            self.enableMenuItem('notes')
            self.editAction = 'editNotes'
            self.setTreeVisible(False)
            self.setStatusbarText([self.singleAddress.sStatus])

        elif self.tabOption == self.tabOrder:
            self.out( 'Seite 3')

            self.disableMenuItem('tabs')
            self.enableMenuItem('order')
            self.editAction = 'editOrder'
            self.setTreeVisible(False)
            self.setStatusbarText([self.singleAddress.sStatus])
            self.setOrderValues()

        # refresh the Tree
        self.refreshTree()

        self.enableMenuItem(self.editAction)
        self.editEntries = False
        
