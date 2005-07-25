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
from gtk import TRUE, FALSE
import string

import logging
from cuon.Windows.windows  import windows
import cuon.Login.User
import SinglePreferences
import _sane as sane


class preferenceswindow(windows):

    
    def __init__(self, allTables):

        windows.__init__(self)
        self.openDB()
        self.oUser = self.loadObject('User')
        self.closeDB()
        print self.oUser
        print '-.............................'
        

        self.singlePreferences = SinglePreferences.SinglePreferences(allTables)
       
        self.singlePreferences.username = self.oUser.getUserName()
        self.loadGlade('preferences.xml')
        self.win1 = self.getWidget('PreferencesMainwindow')



        self.EntriesPreferences = 'preferences.xml'
        self.EntriesPreferencesPrinting = 'preferences_printing.xml'
        self.EntriesPreferencesPathToReports = 'preferences_path_to_reports.xml'
        self.EntriesPreferencesPathToDocs = 'preferences_path_to_docs.xml'
        self.EntriesPreferencesScanner = 'preferences_scanner.xml'

        
        self.loadEntries(self.EntriesPreferences)
        self.loadEntries(self.EntriesPreferencesPrinting)
        self.loadEntries(self.EntriesPreferencesPathToReports)
        self.loadEntries(self.EntriesPreferencesPathToDocs)
        self.loadEntries(self.EntriesPreferencesScanner)
        
        
        self.singlePreferences.sWhere = " where username = \'" + self.oUser.getUserName() + "\'"
        self.singlePreferences.setEntries(self.getDataEntries('preferences.xml') )
        self.singlePreferences.setGladeXml(self.xml)
        self.singlePreferences.setTreeFields( ['profile_name', 'description'] )
        self.singlePreferences.setStore( gtk.ListStore(gobject.TYPE_STRING,  gobject.TYPE_STRING,   gobject.TYPE_UINT) ) 
        self.singlePreferences.setTreeOrder('profile_name')
        self.singlePreferences.setListHeader([_('Profile'), _('Description') ])
        self.singlePreferences.setTree(self.xml.get_widget('tree1') )


        # Menu-items
        self.initMenuItems()

  
        
        # Close Menus for Tab
        self.addEnabledMenuItems('tabs','')
         
        # enabledMenues for Preferences
        #self.addEnabledMenuItems('editProfile','profile1')
        self.addEnabledMenuItems('editProfile','clear1')
        #self.addEnabledMenuItems('editProfile','save1')
        self.addEnabledMenuItems('editProfile','new1')
        self.addEnabledMenuItems('editProfile','edit1')
        

        # tabs from notebook
        self.tabProfile = 0
        self.tabPrinting = 1
        self.tabPathToReports = 2
        self.tabPathToDocs = 3
        self.tabScanner = 4
        
        
        self.tabOption = self.tabProfile
        self.tabChanged()
        print 'SANE version:', sane.init()
 


    def on_save1_activate(self, event):
        print 'save1'
        self.singlePreferences.save()
        self.setEntriesEditable(self.EntriesPreferences, FALSE)
        self.tabChanged()
        
    def on_new1_activate(self, event):
        self.singlePreferences.newRecord()
        self.setEntriesEditable(self.EntriesPreferences, TRUE)

    def on_choose_profile1_activate(self, event):
        print 'choose Profil'
        self.loadProfile(self.singlePreferences.profileName)

        
    def on_edit1_activate(self, event):
        if self.tabOption == self.tabProfile:
            self.setEntriesEditable(self.EntriesPreferences, TRUE)
        elif self.tabOption == self.tabPrinting:
            self.setEntriesEditable(self.EntriesPreferencesPrinting, TRUE)
        elif self.tabOption == self.tabPathToReports:
            self.setEntriesEditable(self.EntriesPreferencesPathToReports, TRUE)
        elif self.tabOption == self.tabPathToDocs:
            self.setEntriesEditable(self.EntriesPreferencesPathToDocs, TRUE)
        elif self.tabOption == self.tabScanner:
            self.setEntriesEditable(self.EntriesPreferencesScanner, TRUE)

    
    def on_delete1_activate(self, event):
        self.singlePreferences.deleteRecord()

    def on_quit1_activate(self, event):
        self.closeWindow() 

    # Buttons
    def on_bListScanDevices_clicked(self, event):
        liDevs = sane.get_devices()
        print 'Available devices=', liDevs
        cb = self.getWidget('cbScanDevice')
        for devs in liDevs:
            listItem_a = gtk.ListItem(devs[0])
            cb.list.append_items([listItem_a])
            
   
    def refreshTree(self):
        self.singlePreferences.disconnectTree()
    
        
        if self.tabOption == self.tabProfile:
            
            self.singlePreferences.sWhere = " where username = \'" + self.oUser.getUserName() + "\'"
            self.singlePreferences.connectTree()
            self.singlePreferences.refreshTree()

            
    def tabChanged(self):
        self.out( 'tab changed to :'  + str(self.tabOption))
        
        if self.tabOption == self.tabProfile:
            #Preferences
            self.disableMenuItem('tabs')
            self.enableMenuItem('editProfile')

            self.actualEntries = self.singlePreferences.getEntries()
            self.editAction = 'editProfile'
            self.setTreeVisible(TRUE)
            self.out( 'Seite 0')
            self.singlePreferences.setEntries(self.getDataEntries(self.EntriesPreferences) )
            # set the Entries manually, because there is no tree event
            self.singlePreferences.fillEntries(self.singlePreferences.ID)

        elif self.tabOption == self.tabPrinting:
            self.editAction = 'editProfile'
            self.setTreeVisible(FALSE)
            self.singlePreferences.setEntries(self.getDataEntries(self.EntriesPreferencesPrinting) )
            # set the Entries manually, because there is no tree event
            self.singlePreferences.fillEntries(self.singlePreferences.ID)
            
        elif self.tabOption == self.tabPathToReports:
            self.editAction = 'editProfile'
            self.setTreeVisible(FALSE)
            self.singlePreferences.setEntries(self.getDataEntries(self.EntriesPreferencesPathToReports) )
            # set the Entries manually, because there is no tree event
            self.singlePreferences.fillEntries(self.singlePreferences.ID)

        elif self.tabOption == self.tabPathToDocs:
            self.editAction = 'editProfile'
            self.setTreeVisible(FALSE)
            self.singlePreferences.setEntries(self.getDataEntries(self.EntriesPreferencesPathToDocs) )
            # set the Entries manually, because there is no tree event
            self.singlePreferences.fillEntries(self.singlePreferences.ID)

        elif self.tabOption == self.tabScanner:
            self.editAction = 'editProfile'
            self.setTreeVisible(FALSE)
            self.singlePreferences.setEntries(self.getDataEntries(self.EntriesPreferencesScanner) )
            # set the Entries manually, because there is no tree event
            self.singlePreferences.fillEntries(self.singlePreferences.ID)
           
 

        else:
            
            self.setTreeVisible(FALSE)

        # refresh the Tree
        self.refreshTree()
        self.enableMenuItem(self.editAction)
        self.editEntries = FALSE
        
