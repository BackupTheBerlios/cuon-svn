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


import logging
from cuon.Windows.chooseWindows  import chooseWindows

#import cuon.OpenOffice.letter
# localisation
import locale, gettext
locale.setlocale (locale.LC_NUMERIC, '')

import SingleMaterialgroups
import SingleMaterialgroupsAccount

class materialgroupwindow(chooseWindows):

    
    def __init__(self, allTables, addrid=0, partnerid=0):

        chooseWindows.__init__(self)
        self.InitForms = True
        self.connectSchedulTreeId = None
        
        #print 'time 1 = ', time.localtime()
        self.ModulNumber = self.MN['MaterialGroups']
        self.singleGroup = SingleMaterialgroups.SingleMaterialgroups(allTables)
        self.singleGroupAccounts = SingleMaterialgroupsAccount.SingleMaterialgroupsAccount(allTables)
        
        self.allTables = allTables
        #print 'time 2 = ', time.localtime()
        
        
        # self.singleGroup.loadTable()

        # self.xml = gtk.glade.XML()
    
        self.loadGlade('material_group.xml', 'MaterialgroupsMainwindow')
        #self.win1 = self.getWidget('AddressMainwindow')
        #self.win1.maximize()
        
        self.setStatusBar()
        #print 'time 3 = ', time.localtime()


        self.EntriesGroups = 'material_groups.xml'
        self.EntriesAccounts = 'material_groups_accounts.xml'
        
        #print 'time 4 = ', time.localtime()
        
        self.loadEntries(self.EntriesGroups)
        
        self.singleGroup.setEntries(self.getDataEntries(self.EntriesGroups) )
        self.singleGroup.setGladeXml(self.xml)
        self.singleGroup.setTreeFields( ['name', 'designation'] )
        self.singleGroup.setStore( gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING,   gobject.TYPE_UINT) ) 
        self.singleGroup.setTreeOrder('name, designation')
        self.singleGroup.setListHeader([_('Name'), _('Designation')])
            
        self.singleGroup.setTree(self.xml.get_widget('tree1') )
        #print 'time 5 = ', time.localtime()
        
      
        #Groupaccounts
        
        self.loadEntries(self.EntriesAccounts )
        self.singleGroupAccounts.setEntries(self.getDataEntries(self.EntriesAccounts) )
        self.singleGroupAccounts.setGladeXml(self.xml)
        self.singleGroupAccounts.setTreeFields([])
        self.singleGroupAccounts.setTreeOrder('id')
        
        self.singleGroupAccounts.sWhere  ='where material_group_id = ' + `self.singleGroup.ID`
        self.singleGroupAccounts.setTree(self.xml.get_widget('tree1') )
        # self.singleMisc.setStore(gtk.ListStore())
        # set values for comboBox

        
        

        # init Comboboxes 
        
        # Tax-Vat
        tax_vat =  self.rpc.callRP('Misc.getListOfTaxVat', self.dicUser)
        cb = self.getWidget('cbVat')
        
        for i in range(len(tax_vat)) :
            li = gtk.ListItem(tax_vat[i])
            cb.list.append_items([li])
            li.show()
    
        
            
        #print 'time 11 = ', time.localtime()
        

        # Menu-items
        self.initMenuItems()

        # Close Menus for Tab
        self.addEnabledMenuItems('tabs','mi_address1')
        self.addEnabledMenuItems('tabs','mi_notes1')
               
        # seperate Menus
        self.addEnabledMenuItems('address','mi_address1')
        self.addEnabledMenuItems('notes','mi_notes1')
        
        # enabledMenues for Address
        self.addEnabledMenuItems('editMaterialGroup','mi_new1' , self.dicUserKeys['address_new'])
        self.addEnabledMenuItems('editMaterialGroup','mi_clear1', self.dicUserKeys['address_delete'])
        self.addEnabledMenuItems('editMaterialGroup','mi_print1', self.dicUserKeys['address_print'])
        self.addEnabledMenuItems('editMaterialGroup','mi_edit1', self.dicUserKeys['address_edit'])

        
        # enabledMenues for Notes
        self.addEnabledMenuItems('editNotes', 'NotesEdit1')
  
        # enabledMenues for Save 
        self.addEnabledMenuItems('editSave','mi_save1', self.dicUserKeys['address_save'])
        self.addEnabledMenuItems('editSave','NotesSave', self.dicUserKeys['address_save'])

        

        # tabs from notebook
        self.tabGroup = 0
        self.tabAccount = 1
      
        self.tabChanged()
        
        self.win1.add_accel_group(self.accel_group)
        #print 'time 21 = ', time.localtime()
        
        
    #Menu File
              
    def on_quit1_activate(self, event):
        self.out( "exit addresses v2")
        self.closeWindow() 
    
    

    #Menu Address
  
    def on_save1_activate(self, event):
        self.out( "save addresses v2")
        self.doEdit = self.noEdit
        self.singleGroup.save()
        self.setEntriesEditable(self.EntriesGroups, FALSE)
        self.endEdit()
        self.tabChanged()
        
    def on_new1_activate(self, event):
        self.out( "new addresses v2")
        self.doEdit = self.tabGroup

        self.singleGroup.newRecord()
        self.setEntriesEditable(self.EntriesGroups, TRUE)
        
        self.getWidget('eAddress').grab_focus()
        self.startEdit()

    def on_edit1_activate(self, event):
        self.out( "edit addresses v2")
        self.doEdit = self.tabGroup
        
        self.setEntriesEditable(self.EntriesGroups, TRUE)
        self.getWidget('eAddress').grab_focus()
        self.startEdit()
        
    def on_print1_activate(self, event):
        self.out( "print addresses v2")
        p = printAddress.printAddress(self.singleGroup.getFirstRecord() )
        
    def on_delete1_activate(self, event):
        self.out( "delete addresses v2")
        self.singleGroup.deleteRecord()

    # Menu Notes
    def on_NotesSave_activate(self, event):
        
        self.out( "save Notes addresses v2")
        self.doEdit = self.noEdit
        self.singleGroupAccounts.addressId = self.singleGroup.ID
        
        self.singleGroupAccounts.save()
        self.setEntriesEditable(self.EntriesNotes, FALSE)
        self.tabChanged()

    def on_NotesEdit1_activate(self, event):
        self.out( "edit notes v2")
        self.doEdit = self.tabAccount
        
        self.setEntriesEditable(self.EntriesNotes, TRUE)

   
    def saveData(self):
        print 'save Addresses'
        if self.doEdit == self.tabGroup:
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
        self.single.disconnectTree()
        self.singlePartner.disconnectTree()
        self.singleSchedul.disconnectTree()
        
        if self.tabOption == self.tabGroup:
            self.singleGroup.connectTree()
            self.singleGroup.refreshTree()
            
        elif self.tabOption == self.tabMisc:
            self.singleMisc.sWhere  ='where address_id = ' + `int(self.singleGroup.ID)`
            self.singleMisc.fillEntries(self.singleMisc.findSingleId())

        elif self.tabOption == self.tabPartner:
            self.singlePartner.sWhere  ='where addressid = ' + `int(self.singleGroup.ID)`
            self.singlePartner.connectTree()
            self.singlePartner.refreshTree()
            
        elif self.tabOption == self.tabSchedul:
            self.singleSchedul.sWhere  ='where partnerid = ' + `int(self.singlePartner.ID)` + ' and process_status != 999 '
            self.singleSchedul.connectTree()
            self.singleSchedul.refreshTree()
            
        elif self.tabOption == self.tabAccount:
            self.singleGroupAccounts.sWhere  ='where address_id = ' + `int(self.singleGroup.ID)`
            self.singleGroupAccounts.fillEntries(self.singleGroupAccounts.findSingleId())

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
        
        if self.tabOption == self.tabGroup:
            #Address
            self.disableMenuItem('tabs')
            self.enableMenuItem('address')

            self.actualEntries = self.singleGroup.getEntries()
            self.editAction = 'editMaterialGroup'
            self.setStatusbarText([''])
          
            self.setTreeVisible(True)
            

            self.out( 'Seite 0')


        elif self.tabOption == self.tabBank:
            self.out( 'Seite 2')
            self.disableMenuItem('tabs')
            self.enableMenuItem('bank')
           
            self.editAction = 'editBank'
            self.setTreeVisible(False)
            self.setStatusbarText([self.singleGroup.sStatus])


        elif self.tabOption == self.tabMisc:
            self.out( 'Seite 3')

            self.disableMenuItem('tabs')
            self.enableMenuItem('misc')
            self.editAction = 'editMisc'
            self.setTreeVisible(False)
            self.setStatusbarText([self.singleGroup.sStatus])




        elif self.tabOption == self.tabPartner:
            #Partner
            self.disableMenuItem('tabs')
            self.enableMenuItem('partner')
            
            self.out( 'Seite 1')
            self.editAction = 'editPartner'
            self.setTreeVisible(True)
            self.setStatusbarText([self.singleGroup.sStatus])

            
        elif self.tabOption == self.tabSchedul:
            #Scheduling
            self.disableMenuItem('tabs')
            self.enableMenuItem('schedul')
            
            self.out( 'Seite 4')
            self.editAction = 'editSchedul'
            self.setTreeVisible(True)
            self.setStatusbarText([self.singlePartner.sStatus])
            
            
        elif self.tabOption == self.tabAccount:
            self.out( 'Seite 3')

            self.disableMenuItem('tabs')
            self.enableMenuItem('notes')
            self.editAction = 'editNotes'
            self.setTreeVisible(False)
            self.setStatusbarText([self.singleGroup.sStatus])

        # refresh the Tree
        self.refreshTree()

        self.enableMenuItem(self.editAction)
        self.editEntries = False
        
