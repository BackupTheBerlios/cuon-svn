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
from types import *
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import gobject

from cuon.Databases.SingleData import SingleData
import SingleStaff
import SingleStaffFee

import logging
from cuon.Windows.chooseWindows  import chooseWindows
import cuon.DMS.documentTools
import cuon.DMS.dms



class staffwindow(chooseWindows):

    
    def __init__(self, allTables):

        chooseWindows.__init__(self)

        self.loadGlade('staff.xml')
        self.win1 = self.getWidget('StaffMainwindow')
        self.oDocumentTools = cuon.DMS.documentTools.documentTools()
        self.ModulNumber = self.MN['Staff']        
        self.allTables = allTables
        self.singleStaff = SingleStaff.SingleStaff(allTables)
        self.singleStaffFee = SingleStaffFee.SingleStaffFee(allTables)
      
        # self.singleStaff.loadTable()
              
        self.entriesStaffs = 'staff.xml'
        self.entriesStaffsFee = 'staff_fee.xml'
                
        
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
        #self.singleStaffFee.setTreeFields( ['designation' ] )
        #self.singleStaffFee.setStore( gtk.ListStore(gobject.TYPE_STRING,  gobject.TYPE_UINT) ) 
        #self.singleStaffFee.setTreeOrder('designation')
#        self.singleStaffFee.setListHeader([''])

        self.singleStaffFee.sWhere  ='where staff_id = ' + `self.singleStaff.ID`
        self.singleStaffFee.setTree(self.xml.get_widget('tree1') )
  
     
        

        # Menu-items
        self.initMenuItems()

        # Close Menus for Tab

        self.addEnabledMenuItems('tabs','staff1')
        self.addEnabledMenuItems('tabs','fee1')


        # seperate Menus
        self.addEnabledMenuItems('staff','staff1')
        self.addEnabledMenuItems('fee','fee1')

        
        # enabledMenues for Staff
        self.addEnabledMenuItems('editStaff','new1', self.dicUserKeys['staff_new'])
        self.addEnabledMenuItems('editStaff','clear1', self.dicUserKeys['staff_delete'])
        self.addEnabledMenuItems('editStaff','print1', self.dicUserKeys['staff_print'])
        self.addEnabledMenuItems('editStaff','edit1',self.dicUserKeys['staff_edit'])

        #enabledMenues for Stafffee
        self.addEnabledMenuItems('editFee','fee_new1', self.dicUserKeys['staff_fee_new'])
        self.addEnabledMenuItems('editFee','fee_clear1')
        self.addEnabledMenuItems('editFee','fee_edit1', self.dicUserKeys['staff_fee_edit'])
    
       


        # tabs from notebook
        self.tabStaff = 0
        self.tabFee = 1
        

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


    #choose Manufactor button
    def on_bChooseManufactor_clicked(self, event):
        adr = cuon.Addresses.addresses.addresswindow(self.allTables)
        adr.setChooseEntry(_('chooseAddress'), self.getWidget( 'eManufactorNumber'))
        
    # signals from entry eManufactorNumber
    
    def on_eManufactorNumber_changed(self, event):
        print 'eManufactor changed'
        eAdrField = self.getWidget('eManufactorField1')
        liAdr = self.singleAddress.getAddress(self.getWidget( 'eManufactorNumber').get_text())
        eAdrField.set_text(liAdr[0] + ', ' + liAdr[4])


    def on_bShowDMS_clicked(self, event):
        print 'dms clicked'
        if self.singleStaff.ID > 0:
            print 'ModulNumber', self.ModulNumber
            Dms = cuon.DMS.dms.dmswindow(self.allTables, self.ModulNumber, {'1':self.singleStaff.ID})
        

  
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

    def refreshTree(self):
        self.singleStaff.disconnectTree()
        self.singleStaffFee.disconnectTree()
        
        if self.tabOption == self.tabStaff:
            print '-->Start Staff refresh Tree'
            self.singleStaff.connectTree()
            self.singleStaff.refreshTree()
            print '<--End Staff refresh Tree'

        elif self.tabOption == self.tabFee:
            print 'refresh Tree fpr Staff-Fee'
            self.singleStaffFee.sWhere  ='where staff_id = ' + `int(self.singleStaff.ID)`
            self.singleStaffFee.getFirstListRecord()
            self.singleStaffFee.fillEntries(self.singleStaffFee.ID)
            


         
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
  
            
        # refresh the Tree
        self.refreshTree()
        self.enableMenuItem(self.editAction)
        self.editEntries = False
