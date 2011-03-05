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
#from gtk import True, False
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

    
    def __init__(self, allTables, graveyardid=0, graveid=0,  addressid= 0):

        chooseWindows.__init__(self)
        self.InitForms = True
        self.connectSchedulTreeId = None
        
        self.graveyardID = graveyardid
        self.graveID = graveid
        self.addressID = addressid
        #print 'time 1 = ', time.localtime()
        self.ModulNumber = self.MN['Graveyard']
        self.singleGraveyard = SingleGraveyard.SingleGraveyard(allTables)
        #self.singleGraveyardAccounts = SingleGraveyardsAccount.SingleGraveyardsAccount(allTables)
        self.singlePrefsFinanceVat = cuon.PrefsFinance.SinglePrefsFinanceVat.SinglePrefsFinanceVat(allTables)
        self.allTables = allTables
        #print 'time 2 = ', time.localtime()
        
        
        # self.singleGraveyard.loadTable()

        # self.xml = gtk.glade.XML()
    
        self.loadGlade('graveyard.xml', 'graveyardMainwindow')
        #self.win1 = self.getWidget('graveyardMainwindow')
        print "win1",  self.win1
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
        self.singleGraveyard.setTreeOrder('shortname, designation')
        self.singleGraveyard.setListHeader([_('Name'), _('Designation')])
            
        self.singleGraveyard.setTree(self.xml.get_widget('tree1') )
        #print 'time 5 = ', time.localtime()
        
      
        
        
        

       
        
            
        #print 'time 11 = ', time.localtime()
        

        # Menu-items
        self.initMenuItems()

        # Close Menus for Tab
        self.addEnabledMenuItems('tabs','graveyard1')
               
        # seperate Menus
        self.addEnabledMenuItems('graveyard','graveyard1')
        self.addEnabledMenuItems('notes','mi_notes1')
        
        # enabledMenues for group
        self.addEnabledMenuItems('editGraveyard','new1' , self.dicUserKeys['address_new'])
        self.addEnabledMenuItems('editGraveyard','clear1', self.dicUserKeys['address_delete'])
        self.addEnabledMenuItems('editGraveyard','print1', self.dicUserKeys['address_print'])
        self.addEnabledMenuItems('editGraveyard','edit1', self.dicUserKeys['address_edit'])

        
#        # enabledMenues for Notes
#        self.addEnabledMenuItems('editNotes', 'NotesEdit1')
#  
#        # enabledMenues for Save 
#        self.addEnabledMenuItems('editSave','save1', self.dicUserKeys['address_save'])
#        self.addEnabledMenuItems('editSave','save_account1', self.dicUserKeys['address_save'])

        

        # tabs from notebook
        self.tabGraveyard = 0
        #self.tabAccount = 1
      
        self.tabChanged()
        
        self.win1.add_accel_group(self.accel_group)
        #print 'time 21 = ', time.localtime()
        
        
    #Menu File
              
    def on_quit1_activate(self, event):
        self.out( "exit graveyard v2")
        self.closeWindow() 
    
    

    #Menu Address
  
    def on_save1_activate(self, event):
        self.out( "save graveyard v2")
        self.doEdit = self.noEdit
        self.singleGraveyard.save()
        self.setEntriesEditable(self.EntriesGraveyard, False)
        self.endEdit()
        self.tabChanged()
        
    def on_new1_activate(self, event):
        self.out( "new graveyard v2")
        self.doEdit = self.tabGraveyard

        self.singleGraveyard.newRecord()
        self.setEntriesEditable(self.EntriesGraveyard, True)
        
        #self.getWidget('eAddress').grab_focus()
        self.startEdit()

    def on_edit1_activate(self, event):
        self.out( "edit graveyard v2")
        self.doEdit = self.tabGraveyard
        
        self.setEntriesEditable(self.EntriesGraveyard, True)
        #self.getWidget('eAddress').grab_focus()
        self.startEdit()
        
    def on_print1_activate(self, event):
        self.out( "print graveyard v2")
        p = printAddress.printAddress(self.singleGraveyard.getFirstRecord() )
        
    def on_delete1_activate(self, event):
        self.out( "delete graveyard v2")
        self.singleGraveyard.deleteRecord()

    # Menu Notes
    def on_NotesSave_activate(self, event):
        
        self.out( "save Notes addresses v2")
        self.doEdit = self.noEdit
        self.singleGraveyardAccounts.addressId = self.singleGraveyard.ID
        
        self.singleGraveyardAccounts.save()
        self.setEntriesEditable(self.EntriesNotes, False)
        self.tabChanged()

    def on_NotesEdit1_activate(self, event):
        self.out( "edit notes v2")
        self.doEdit = self.tabAccount
        
        self.setEntriesEditable(self.EntriesNotes, True)

   
    
        
    def saveData(self):
        print 'save Graveyard'
        if self.doEdit == self.tabGraveyard:
            print 'save 1'
            self.on_save1_activate(None)
        #elif self.doEdit == self.tabBank:
        #    print 'save 2'
      
    # Tax Vat choose
    def on_bSearchTaxVat_clicked(self, event):
        print 'cbVat search'
        print event
        
        pf = cuon.PrefsFinance.prefsFinance.prefsFinancewindow(self.allTables, preparedTab = 0 )
        pf.setChooseEntry('chooseTaxVat', self.getWidget( 'eTaxVatID'))
        
    def on_eAdressID_changed(self, event):
        print 'eAddress changed'
#        iTaxVat = self.getChangedValue('eTaxVatID')
#        sTaxVat = self.singlePrefsFinanceVat.getNameAndDesignation(iTaxVat)
#        if sTaxVat:
#            self.getWidget('eTaxVat').set_text(sTaxVat)
#        else:
#            self.getWidget('eTaxVat').set_text('')
 
    def on_chooseGraveyard_activate(self, event):
        # choose Article from other Modul
        self.setChooseValue(self.singleGraveyard.ID)
        print 'Graveyard-ID = ' + `self.singleGraveyard.ID`
        self.closeWindow()
  
    def on_tree1_row_activated(self, event, data1, data2):
        print 'DoubleClick tree1'
        self.activateClick('chooseGraveyard', event)
    
    def refreshTree(self):
        self.singleGraveyard.disconnectTree()
        #self.singleGraveyardAccounts.disconnectTree()
        
        if self.tabOption == self.tabGraveyard:
            self.singleGraveyard.connectTree()
            self.singleGraveyard.refreshTree()
            
        
#        elif self.tabOption == self.tabAccount:
#            self.singleGraveyardAccounts.sWhere  ='where address_id = ' + `int(self.singleGraveyard.ID)`
#            self.singleGraveyardAccounts.fillEntries(self.singleGraveyardAccounts.findSingleId())

          
                
         
    def tabChanged(self):
        self.out( 'tab changed to :'  + str(self.tabOption))
        
        if self.tabOption == self.tabGraveyard:
            #Address
            self.disableMenuItem('tabs')
            self.enableMenuItem('address')

            self.actualEntries = self.singleGraveyard.getEntries()
            self.editAction = 'editGraveyard'
            self.setStatusbarText([''])
          
            self.setTreeVisible(True)
            

            self.out( 'Seite 0')


       

        # refresh the Tree
        self.refreshTree()

        self.enableMenuItem(self.editAction)
        self.editEntries = False
        
