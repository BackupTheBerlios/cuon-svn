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

import SingleGraveyard

import cuon.PrefsFinance.prefsFinance
import cuon.PrefsFinance.SinglePrefsFinanceVat

class graveyardMainwindow(chooseWindows):

    
    def __init__(self, allTables, addrid=0, partnerid=0):

        chooseWindows.__init__(self)
        self.InitForms = True
        self.connectSchedulTreeId = None
        
        #print 'time 1 = ', time.localtime()
        self.ModulNumber = self.MN['Graveyard']
        self.singleGraveyard = SingleGraveyard.SingleGraveyard(allTables)
        #self.singleGraveyardAccounts = SingleMaterialgroupsAccount.SingleMaterialgroupsAccount(allTables)
        self.singlePrefsFinanceVat = cuon.PrefsFinance.SinglePrefsFinanceVat.SinglePrefsFinanceVat(allTables)
        self.allTables = allTables
        #print 'time 2 = ', time.localtime()
        
        
        # self.singleGraveyard.loadTable()

        # self.xml = gtk.glade.XML()
    
        self.loadGlade('graveyard.xml', 'graveyardMainwindow')
        #self.win1 = self.getWidget('AddressMainwindow')
        #self.win1.maximize()
        
        self.setStatusBar()
        #print 'time 3 = ', time.localtime()


        self.EntriesGraveyard = 'graveyard.xml'
        
        #print 'time 4 = ', time.localtime()
        
        self.loadEntries(self.EntriesGraveyard)
        
        self.singleGraveyard.setEntries(self.getDataEntries(self.EntriesGraveyard) )
        self.singleGraveyard.setGladeXml(self.xml)
        self.singleGraveyard.setTreeFields( ['shortname', 'designation'] )
        self.singleGraveyard.setStore( gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING,   gobject.TYPE_UINT) ) 
        self.singleGraveyard.setTreeOrder('sortname, designation')
        self.singleGraveyard.setListHeader([_('Name'), _('Designation')])
            
        self.singleGraveyard.setTree(self.xml.get_widget('tree1') )
        #print 'time 5 = ', time.localtime()
        
      
        
        
        

       
        
            
        #print 'time 11 = ', time.localtime()
        

        # Menu-items
        self.initMenuItems()

        # Close Menus for Tab
        self.addEnabledMenuItems('tabs','graveyard1')
               
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
        self.singleGraveyard.save()
        self.setEntriesEditable(self.EntriesGraveyard, FALSE)
        self.endEdit()
        self.tabChanged()
        
    def on_new1_activate(self, event):
        self.out( "new materialgroup v2")
        self.doEdit = self.tabGroup

        self.singleGraveyard.newRecord()
        self.setEntriesEditable(self.EntriesGraveyard, TRUE)
        
        #self.getWidget('eAddress').grab_focus()
        self.startEdit()

    def on_edit1_activate(self, event):
        self.out( "edit material_group v2")
        self.doEdit = self.tabGroup
        
        self.setEntriesEditable(self.EntriesGraveyard, TRUE)
        #self.getWidget('eAddress').grab_focus()
        self.startEdit()
        
    def on_print1_activate(self, event):
        self.out( "print material_group v2")
        p = printAddress.printAddress(self.singleGraveyard.getFirstRecord() )
        
    def on_delete1_activate(self, event):
        self.out( "delete material_group v2")
        self.singleGraveyard.deleteRecord()

    # Menu Notes
    def on_NotesSave_activate(self, event):
        
        self.out( "save Notes addresses v2")
        self.doEdit = self.noEdit
        self.singleGraveyardAccounts.addressId = self.singleGraveyard.ID
        
        self.singleGraveyardAccounts.save()
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
        self.setChooseValue(self.singleGraveyard.ID)
        print 'Group-ID = ' + `self.singleGraveyard.ID`
        self.closeWindow()
  
    def on_tree1_row_activated(self, event, data1, data2):
        print 'DoubleClick tree1'
        self.activateClick('chooseMaterialgroup', event)
    
    def refreshTree(self):
        self.singleGraveyard.disconnectTree()
        self.singleGraveyardAccounts.disconnectTree()
        
        if self.tabOption == self.tabGroup:
            self.singleGraveyard.connectTree()
            self.singleGraveyard.refreshTree()
            
        
        elif self.tabOption == self.tabAccount:
            self.singleGraveyardAccounts.sWhere  ='where address_id = ' + `int(self.singleGraveyard.ID)`
            self.singleGraveyardAccounts.fillEntries(self.singleGraveyardAccounts.findSingleId())

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

            self.actualEntries = self.singleGraveyard.getEntries()
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
            self.setStatusbarText([self.singleGraveyard.sStatus])


        elif self.tabOption == self.tabMisc:
            self.out( 'Seite 3')

            self.disableMenuItem('tabs')
            self.enableMenuItem('misc')
            self.editAction = 'editMisc'
            self.setTreeVisible(False)
            self.setStatusbarText([self.singleGraveyard.sStatus])




        elif self.tabOption == self.tabPartner:
            #Partner
            self.disableMenuItem('tabs')
            self.enableMenuItem('partner')
            
            self.out( 'Seite 1')
            self.editAction = 'editPartner'
            self.setTreeVisible(True)
            self.setStatusbarText([self.singleGraveyard.sStatus])

            
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
            self.setStatusbarText([self.singleGraveyard.sStatus])

        # refresh the Tree
        self.refreshTree()

        self.enableMenuItem(self.editAction)
        self.editEntries = False
        
