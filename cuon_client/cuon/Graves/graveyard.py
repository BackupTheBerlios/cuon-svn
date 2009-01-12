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
import cuon.PrefsFinance.prefsFinance
import cuon.PrefsFinance.SinglePrefsFinanceVat

class graveyardwindow(chooseWindows):

    
    def __init__(self, allTables, addrid=0, partnerid=0):

        chooseWindows.__init__(self)
        self.InitForms = True
        self.connectSchedulTreeId = None
        
        #print 'time 1 = ', time.localtime()
        self.ModulNumber = self.MN['MaterialGroups']
        self.singleGroup = SingleMaterialgroups.SingleMaterialgroups(allTables)
        self.singleGroupAccounts = SingleMaterialgroupsAccount.SingleMaterialgroupsAccount(allTables)
        self.singlePrefsFinanceVat = cuon.PrefsFinance.SinglePrefsFinanceVat.SinglePrefsFinanceVat(allTables)
        self.allTables = allTables
        #print 'time 2 = ', time.localtime()
        
        
        # self.singleGroup.loadTable()

        # self.xml = gtk.glade.XML()
    
        self.loadGlade('materialGroup.xml', 'MaterialGroupMainwindow')
        #self.win1 = self.getWidget('AddressMainwindow')
        #self.win1.maximize()
        
        self.setStatusBar()
        #print 'time 3 = ', time.localtime()


        self.EntriesGroups = 'material.xml'
        self.EntriesAccounts = 'material_group_accounts.xml'
        
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

        
        

       
        
            
        #print 'time 11 = ', time.localtime()
        

        # Menu-items
        self.initMenuItems()

        # Close Menus for Tab
        self.addEnabledMenuItems('tabs','mi_address1')
        self.addEnabledMenuItems('tabs','mi_notes1')
               
        # seperate Menus
        self.addEnabledMenuItems('address','mi_address1')
        self.addEnabledMenuItems('notes','mi_notes1')
        
        # enabledMenues for group
        self.addEnabledMenuItems('editMaterialGroup','new1' , self.dicUserKeys['address_new'])
        self.addEnabledMenuItems('editMaterialGroup','clear1', self.dicUserKeys['address_delete'])
        self.addEnabledMenuItems('editMaterialGroup','print1', self.dicUserKeys['address_print'])
        self.addEnabledMenuItems('editMaterialGroup','edit1', self.dicUserKeys['address_edit'])

        
        # enabledMenues for Notes
        self.addEnabledMenuItems('editNotes', 'NotesEdit1')
  
        # enabledMenues for Save 
        self.addEnabledMenuItems('editSave','save1', self.dicUserKeys['address_save'])
        self.addEnabledMenuItems('editSave','save_account1', self.dicUserKeys['address_save'])

        

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
        self.out( "save material_group v2")
        self.doEdit = self.noEdit
        self.singleGroup.save()
        self.setEntriesEditable(self.EntriesGroups, FALSE)
        self.endEdit()
        self.tabChanged()
        
    def on_new1_activate(self, event):
        self.out( "new materialgroup v2")
        self.doEdit = self.tabGroup

        self.singleGroup.newRecord()
        self.setEntriesEditable(self.EntriesGroups, TRUE)
        
        #self.getWidget('eAddress').grab_focus()
        self.startEdit()

    def on_edit1_activate(self, event):
        self.out( "edit material_group v2")
        self.doEdit = self.tabGroup
        
        self.setEntriesEditable(self.EntriesGroups, TRUE)
        #self.getWidget('eAddress').grab_focus()
        self.startEdit()
        
    def on_print1_activate(self, event):
        self.out( "print material_group v2")
        p = printAddress.printAddress(self.singleGroup.getFirstRecord() )
        
    def on_delete1_activate(self, event):
        self.out( "delete material_group v2")
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
        print 'save Materialgroup'
        if self.doEdit == self.tabGroup:
            print 'save 1'
            self.on_save1_activate(None)
        #elif self.doEdit == self.tabBank:
        #    print 'save 2'
      
    # Tax Vat choose
    def on_bSearchTaxVat_clicked(self, event):
        print 'cbVat search'
        print event
        
        pf = cuon.PrefsFinance.prefsFinance.prefsFinancewindow(self.allTables)
        pf.setChooseEntry('chooseTaxVat', self.getWidget( 'eTaxVatID'))
        
    def on_eTaxVatID_changed(self, event):
        print 'eCategory changed'
        iTaxVat = self.getChangedValue('eTaxVatID')
        sTaxVat = self.singlePrefsFinanceVat.getNameAndDesignation(iTaxVat)
        if sTaxVat:
            self.getWidget('eTaxVat').set_text(sTaxVat)
        else:
            self.getWidget('eTaxVat').set_text('')
 
    def on_chooseMaterialgroup_activate(self, event):
        # choose Article from other Modul
        self.setChooseValue(self.singleGroup.ID)
        print 'Group-ID = ' + `self.singleGroup.ID`
        self.closeWindow()
  
    def on_tree1_row_activated(self, event, data1, data2):
        print 'DoubleClick tree1'
        self.activateClick('chooseMaterialgroup', event)
    
    def refreshTree(self):
        self.singleGroup.disconnectTree()
        self.singleGroupAccounts.disconnectTree()
        
        if self.tabOption == self.tabGroup:
            self.singleGroup.connectTree()
            self.singleGroup.refreshTree()
            
        
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
        
