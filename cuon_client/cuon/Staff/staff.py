# -*- coding: utf-8 -*-
##Copyright (C) [2003]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 

import sys
from types import *
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import gobject

from cuon.Databases.SingleData import SingleData
import SingleStaff
import SingleStaffFee
import SingleStaffMisc
import SingleStaffVacation
import SingleStaffDisease

import logging
from cuon.Windows.chooseWindows  import chooseWindows
import cuon.DMS.documentTools
import cuon.DMS.dms



class staffwindow(chooseWindows):

    
    def __init__(self, allTables):

        chooseWindows.__init__(self)

        self.loadGlade('staff.xml','StaffMainwindow' )
        self.win1 = self.getWidget('StaffMainwindow')
        self.oDocumentTools = cuon.DMS.documentTools.documentTools()
        self.ModulNumber = self.MN['Staff']        
        self.allTables = allTables
		
		
        self.singleStaff = SingleStaff.SingleStaff(allTables)
        self.singleStaffFee = SingleStaffFee.SingleStaffFee(allTables)
        self.singleStaffMisc = SingleStaffMisc.SingleStaffMisc(allTables)
        self.singleStaffVacation = SingleStaffVacation.SingleStaffVacation(allTables)
        self.singleStaffDisease = SingleStaffDisease.SingleStaffDisease(allTables)
      
        # self.singleStaff.loadTable()
              
        self.entriesStaffs = 'staff.xml'
        self.entriesStaffsFee = 'staff_fee.xml'
        self.entriesStaffsMisc = 'staff_misc.xml'
        self.entriesStaffsVacation = 'staff_vacation.xml'
        self.entriesStaffsDisease = 'staff_disease.xml'
                
        
        #singleStaff
 
 
        self.loadEntries(self.entriesStaffs)
        self.singleStaff.setEntries(self.getDataEntries( self.entriesStaffs) )
        self.singleStaff.setGladeXml(self.xml)
        self.singleStaff.setTreeFields( ['lastname','firstname'] )
        self.singleStaff.setStore( gtk.ListStore( gobject.TYPE_STRING, gobject.TYPE_STRING,gobject.TYPE_UINT) ) 
        self.singleStaff.setTreeOrder('lastname')
        self.singleStaff.setTree(self.xml.get_widget('tree1') )
        self.singleStaff.setListHeader(['lastname','firstname' ])
        print 'Widgets - win = ', `self.win1`
        print 'Widgets - tree1 = ', `self.xml.get_widget('tree1')`
        
         #singleStaffFee
        
        self.loadEntries(self.entriesStaffsFee)
        self.singleStaffFee.setEntries(self.getDataEntries( self.entriesStaffsFee) )
        self.singleStaffFee.setGladeXml(self.xml)

        self.singleStaffFee.sWhere  ='where staff_id = ' + `self.singleStaff.ID`
        self.singleStaffFee.setTree(self.xml.get_widget('tree1') )
        
   #singleStaffMisc
        
        self.loadEntries(self.entriesStaffsMisc)
        self.singleStaffMisc.setEntries(self.getDataEntries( self.entriesStaffsMisc) )
        self.singleStaffMisc.setGladeXml(self.xml)

        self.singleStaffMisc.sWhere  ='where staff_id = ' + `self.singleStaff.ID`
        self.singleStaffMisc.setTree(self.xml.get_widget('tree1') )
  
    #singleStaffVacation
        
        self.loadEntries(self.entriesStaffsVacation)
        self.singleStaffVacation.setEntries(self.getDataEntries( self.entriesStaffsVacation) )
        self.singleStaffVacation.setGladeXml(self.xml)
        self.singleStaffVacation.setTreeFields( ['name', 'designation'] )
        self.singleStaffVacation.setStore( gtk.ListStore( gobject.TYPE_STRING, gobject.TYPE_STRING,gobject.TYPE_UINT) ) 
        self.singleStaffVacation.setTreeOrder('name')
        self.singleStaffVacation.sWhere  ='where staff_id = ' + `self.singleStaff.ID`
        self.singleStaffVacation.setTree(self.xml.get_widget('tree1') )
  
      
   #singleStaffDisease
        
        self.loadEntries(self.entriesStaffsDisease)
        self.singleStaffDisease.setEntries(self.getDataEntries( self.entriesStaffsDisease) )
        self.singleStaffDisease.setGladeXml(self.xml)

        self.singleStaffDisease.sWhere  ='where staff_id = ' + `self.singleStaff.ID`
        self.singleStaffDisease.setTree(self.xml.get_widget('tree1') )
  
          

        # Menu-items
        self.initMenuItems()

        # Close Menus for Tab

        self.addEnabledMenuItems('tabs','staff1')
        self.addEnabledMenuItems('tabs','fee1')
        self.addEnabledMenuItems('tabs','misc')
        self.addEnabledMenuItems('tabs','vacation')
        self.addEnabledMenuItems('tabs','disease')


        # seperate Menus
        self.addEnabledMenuItems('staff','staff1')
        self.addEnabledMenuItems('fee','fee1')
        self.addEnabledMenuItems('misc','misc1')
        self.addEnabledMenuItems('vacation','vacation1')
        self.addEnabledMenuItems('disease','disease1')

        
        # enabledMenues for Staff
        self.addEnabledMenuItems('editStaff','new1', self.dicUserKeys['staff_new'])
        self.addEnabledMenuItems('editStaff','clear1', self.dicUserKeys['staff_delete'])
        self.addEnabledMenuItems('editStaff','print1', self.dicUserKeys['staff_print'])
        self.addEnabledMenuItems('editStaff','edit1',self.dicUserKeys['staff_edit'])

        #enabledMenues for Stafffee
        self.addEnabledMenuItems('editFee','fee_new1', self.dicUserKeys['staff_fee_new'])
        self.addEnabledMenuItems('editFee','fee_edit1', self.dicUserKeys['staff_fee_edit'])
    
		#enabledMenues for StaffMisc
        self.addEnabledMenuItems('editMisc','misc_edit1', self.dicUserKeys['staff_misc_edit'])
		
		#enabledMenues for StaffVacation
        self.addEnabledMenuItems('editVacation','vacation_new1', self.dicUserKeys['staff_vacation_new'])
        self.addEnabledMenuItems('editVacation','vacation_delete1')
        self.addEnabledMenuItems('editVacation','vacation_edit1', self.dicUserKeys['staff_vacation_edit'])
    

		#enabledMenues for StaffDisease
        self.addEnabledMenuItems('editDisease','disease_new1', self.dicUserKeys['staff_disease_new'])
        self.addEnabledMenuItems('editDisease','disease_delete1')
        self.addEnabledMenuItems('editD','disease_edit1', self.dicUserKeys['staff_disease_edit'])
		
       # enabledMenues for Save 
        self.addEnabledMenuItems('editSave','save1', self.dicUserKeys['staff_save'])
        self.addEnabledMenuItems('editSave','fee_save1', self.dicUserKeys['staff_save'])
        self.addEnabledMenuItems('editSave','misc_save1', self.dicUserKeys['staff_save'])
        self.addEnabledMenuItems('editSave','vacation_save1', self.dicUserKeys['staff_save'])
        self.addEnabledMenuItems('editSave','disease_save1', self.dicUserKeys['staff_save'])



        # tabs from notebook
        self.tabStaff = 0
        self.tabFee = 1
        self.tabMisc = 2
        self.tabVacation = 3
        self.tabDisease = 4
        

        # start
        
        self.tabChanged()

        
##        # init Comboboxes
##        tax_vat =  self.rpc.callRP('src.Misc.py_getListOfTaxVat', self.dicUser)
##        cb = self.getWidget('cbVat')
##        
##        for i in range(len(tax_vat)) :
##            li = gtk.ListItem(tax_vat[i])
##            cb.list.append_items([li])
##            li.show()
    
        self.win1.add_accel_group(self.accel_group)
    #Menu File
              
    def on_quit1_activate(self, event):
        print "exit staffs v2"
        self.closeWindow()
  

    #Menu Staff
  
    def on_save1_activate(self, event):
        print "save staffs v2"
        self.singleStaff.save()
        self.setEntriesEditable(self.entriesStaffs, False)
        self.tabChanged()
         
        
    def on_new1_activate(self, event):
        print "new staffs v2"
        self.singleStaff.newRecord()
        self.setEntriesEditable(self.entriesStaffs, True)
        

    def on_edit1_activate(self, event):
        self.setEntriesEditable(self.entriesStaffs, True)

    def on_delete1_activate(self, event):
        print "delete staffs v2"
        self.singleStaff.deleteRecord()

  
    # Fee
    def on_fee_save1_activate(self, event):
        print "save staffs Fee v2"
        
        self.singleStaffFee.staffID = self.singleStaff.ID
        self.singleStaffFee.save()
        self.setEntriesEditable(self.entriesStaffsFee, False)

        self.tabChanged()
        
    def on_fee_new1_activate(self, event):
        print "new Fee staffs v2"
        self.singleStaffFee.newRecord()
        self.setEntriesEditable(self.entriesStaffsFee, True)

    def on_fee_edit1_activate(self, event):
        self.setEntriesEditable(self.entriesStaffsFee, True)

    def on_fee_clear1_activate(self, event):
        print "delete fee staffs v2"
        self.singleStaffFee.deleteRecord()


# Misc
    def on_misc_save1_activate(self, event):
        print "save staffs Fee v2"
        
        self.singleStaffMisc.staffID = self.singleStaff.ID
        self.singleStaffMisc.save()
        self.setEntriesEditable(self.entriesStaffsMisc, False)

        self.tabChanged()
        
    def on_misc_new1_activate(self, event):
        print "new misc staffs v2"
        self.singleStaffMisc.newRecord()
        self.setEntriesEditable(self.entriesStaffsMisc, True)

    def on_misc_edit1_activate(self, event):
        self.setEntriesEditable(self.entriesStaffsMisc, True)

    def on_misc_delete1_activate(self, event):
        print "delete miscstaffs v2"
        self.singleStaffMisc.deleteRecord()



# Vacation
    def on_vacation_save1_activate(self, event):
        print "save vacation Fee v2"
        
        self.singleStaffVacation.staffID = self.singleStaff.ID
        self.singleStaffVacation.save()
        self.setEntriesEditable(self.entriesStaffsVacation, False)

        self.tabChanged()
        
    def on_vacation_new1_activate(self, event):
        print "new vacation staffs v2"
        self.singleStaffVacation.newRecord()
        self.setEntriesEditable(self.entriesStaffsVacation, True)

    def on_vacation_edit1_activate(self, event):
        self.setEntriesEditable(self.entriesStaffsVacation, True)

    def on_vacation_delete1_activate(self, event):
        print "delete vacation staffs v2"
        self.singleStaffVacation.deleteRecord()



# Disease
    def on_disease_save1_activate(self, event):
        print "save staff disease v2"
        
        self.singleStaffDisease.staffID = self.singleStaff.ID
        self.singleStaffDisease.save()
        self.setEntriesEditable(self.entriesStaffsDisease, False)

        self.tabChanged()
        
    def on_disease_new1_activate(self, event):
        print "new disease staffs v2"
        self.singleStaffDisease.newRecord()
        self.setEntriesEditable(self.entriesStaffsDisease, True)

    def on_disease_edit1_activate(self, event):
        self.setEntriesEditable(self.entriesStaffsDisease, True)

    def on_disease_delete1_activate(self, event):
        print "delete disease staffs v2"
        self.singleStaffDisease.deleteRecord()


    def on_chooseStaff_activate(self, event):
        # choose Staff from other Modul
        print '############### Staff choose ID ###################'
        self.setChooseValue(self.singleStaff.ID)
        self.closeWindow()
        
    # search button
    def on_bSearch_clicked(self, event):
        self.searchStaff()


    def on_eFindNumber_editing_done(self, event):
        print 'Find Number'
        self.searchStaff()

    def on_eFindNumber_key_press_event(self, entry,event):
        if self.checkKey(event,'NONE','Return'):
            self.searchStaff()
            
    def on_eFindDesignation_editing_done(self, event):
        print 'Find Designation'
        self.searchStaff()

    def on_eFindDesignation_key_press_event(self, entry,event):
        if self.checkKey(event,'NONE','Return'):
            self.searchStaff()
        
    def on_tree1_row_activated(self, event, data1, data2):
        print 'DoubleClick tree1'
        if self.tabOption == self.tabStaff:
            self.activateClick('chooseStaff', event)

    def searchStaff(self):
        self.out( 'Searching ....', self.ERROR)
        sNumber = self.getWidget('eFindNumber').get_text()
        sDesignation = self.getWidget('eFindDesignation').get_text()
        self.out('Name and City = ' + sNumber + ', ' + sDesignation, self.ERROR)
        
        #self.singleStaff.sWhere = 'where number ~* \'.*' + sNumber + '.*\' and designation ~* \'.*' + sDesignation + '.*\''
        liSearch = ['number',sNumber, 'designation', sDesignation]
        self.singleStaff.sWhere = self.getWhere(liSearch)
        self.out(self.singleStaff.sWhere, self.ERROR)
        self.refreshTree()


#    #choose Manufactor button
#    def on_bChooseManufactor_clicked(self, event):
#        adr = cuon.Addresses.addresses.addresswindow(self.allTables)
#        adr.setChooseEntry(_('chooseAddress'), self.getWidget( 'eManufactorNumber'))
#        
#    # signals from entry eManufactorNumber
#    
#    def on_eManufactorNumber_changed(self, event):
#        print 'eManufactor changed'
#        eAdrField = self.getWidget('eManufactorField1')
#        liAdr = self.singleAddress.getAddress(self.getWidget( 'eManufactorNumber').get_text())
#        eAdrField.set_text(liAdr[0] + ', ' + liAdr[4])

    def on_bShowStaffDMS_clicked(self, event):
        print 'dms clicked'
        if self.singleStaff.ID > 0:
            print 'ModulNumber', self.ModulNumber
            Dms = cuon.DMS.dms.dmswindow(self.allTables, self.ModulNumber, {'1':self.singleStaff.ID})
        

    def refreshTree(self):
        self.singleStaff.disconnectTree()
        self.singleStaffFee.disconnectTree()
        self.singleStaffMisc.disconnectTree()
        self.singleStaffVacation.disconnectTree()
        self.singleStaffDisease.disconnectTree()

        if self.tabOption == self.tabStaff:
            self.singleStaff.connectTree()
            self.singleStaff.refreshTree()

        elif self.tabOption == self.tabFee:
            self.singleStaffFee.sWhere  ='where staff_id = ' + `int(self.singleStaff.ID)`
            self.singleStaffFee.getFirstListRecord()
            self.singleStaffFee.fillEntries(self.singleStaffFee.ID)
            
        elif self.tabOption == self.tabMisc:
            self.singleStaffMisc.sWhere  ='where staff_id = ' + `int(self.singleStaff.ID)`
            self.singleStaffMisc.getFirstListRecord()
            self.singleStaffMisc.fillEntries(self.singleStaffFee.ID)
            
        elif self.tabOption == self.tabVacation:
            self.singleStaffVacation.sWhere  ='where staff_id = ' + `int(self.singleStaff.ID)`
            self.singleStaffVacation.connectTree()
            self.singleStaffVacation.refreshTree()
        
        elif self.tabOption == self.tabDisease:
            self.singleStaffDisease.sWhere  ='where staff_id = ' + `int(self.singleStaff.ID)`
            self.singleStaffDisease.connectTree()
            self.singleStaffDisease.refreshTree()


         
    def tabChanged(self):
        print 'tab changed to :'  + str(self.tabOption)
        self.setTreeVisible(True)
        if self.tabOption == self.tabStaff:
            #Staff
            self.disableMenuItem('tabs')
            self.enableMenuItem('staff')
            print 'Seite 0'
            self.editAction = 'editStaff'
            
        elif self.tabOption == self.tabFee:
            #Fee
            self.disableMenuItem('tabs')
            self.enableMenuItem('fee')
            self.editAction = 'editFee'
            print 'Seite 1'
        elif self.tabOption == self.tabMisc:
            #Misc
            self.disableMenuItem('tabs')
            self.enableMenuItem('misc')
            self.editAction = 'editMisc'
            
        elif self.tabOption == self.tabVacation:
            #Misc
            self.disableMenuItem('tabs')
            self.enableMenuItem('vacation')
            self.editAction = 'editVacation'
               
        elif self.tabOption == self.tabDisease:
            #Misc
            self.disableMenuItem('tabs')
            self.enableMenuItem('disease')
            self.editAction = 'editDisease'
               
            
        # refresh the Tree
        self.refreshTree()
        self.enableMenuItem(self.editAction)
        self.editEntries = False
