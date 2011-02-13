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

import string

import logging
from cuon.Windows.windows  import windows
#import cuon.User.user
import SinglePreferences
try:
    import _sane as sane
except:
    pass
    


class preferenceswindow(windows):

    
    def __init__(self, allTables):
        print 'start preferences'
        windows.__init__(self)
        self.openDB()
        self.oUser = self.loadObject('User')
        self.closeDB()
        print self.oUser
        print '-.............................'
        

        self.singlePreferences = SinglePreferences.SinglePreferences(allTables)
       
        self.singlePreferences.username = self.oUser.getUserName()
        print 'load glade-file'
        self.loadGlade('preferences.xml')
        print 'windows started'
        self.win1 = self.getWidget('PreferencesMainwindow')
        print 'set Entries'

        self.EntriesPreferences = 'preferences.xml'
        self.EntriesPreferencesCommunication = 'preferences_com.xml'
        self.EntriesPreferencesExecutables = 'preferencesExecutables.xml'
        #self.EntriesPreferencesPathToDocs = 'preferences_path_to_docs.xml'
        self.EntriesPreferencesScanner = 'preferences_scanner.xml'
        self.EntriesPreferencesDMS = 'preferences_dms.xml'
        self.EntriesPreferencesEmail = 'preferences_email.xml'

        print 'load entries'
        self.loadEntries(self.EntriesPreferences)
        self.loadEntries(self.EntriesPreferencesCommunication)
        self.loadEntries(self.EntriesPreferencesExecutables)
        #self.loadEntries(self.EntriesPreferencesPathToDocs)
        self.loadEntries(self.EntriesPreferencesScanner)
        self.loadEntries(self.EntriesPreferencesDMS)
        self.loadEntries(self.EntriesPreferencesEmail)
        
        print 'set databases'
        
        self.singlePreferences.sWhere = " where username = \'" + self.oUser.getUserName() + "\'"
        self.singlePreferences.setEntries(self.getDataEntries('preferences.xml') )
        self.singlePreferences.setGladeXml(self.xml)
        self.singlePreferences.setTreeFields( ['profile_name', 'description'] )
        self.singlePreferences.setStore( gtk.ListStore(gobject.TYPE_STRING,  gobject.TYPE_STRING,   gobject.TYPE_UINT) ) 
        self.singlePreferences.setTreeOrder('profile_name')
        self.singlePreferences.setListHeader([_('Profile'), _('Description') ])
        self.singlePreferences.setTree(self.getWidget('tree1') )


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
        
        liCrypt = self.rpc.callRP('Email.getCryptCombobox')
        cbCrypt = self.getWidget('cbCrypt')
        cbImapCrypt = self.getWidget('cbImapCrypt')
        
    
        liststore = gtk.ListStore(str)
        for crypt in liCrypt:
            liststore.append([crypt])
        if cbCrypt:
            cbCrypt.set_model(liststore)
            cbCrypt.set_text_column(0)
            cbCrypt.show()
        if cbImapCrypt:
            cbImapCrypt.set_model(liststore)
            cbImapCrypt.set_text_column(0)
            cbImapCrypt.show()

        # tabs from notebook
        self.tabProfile = 0
        self.tabCommunication = 1
        self.tabPathToExecutables = 2
        self.tabEmail = 3
        self.tabScanner = 4
        self.tabDMS = 5
        
        
        self.tabOption = self.tabProfile
        self.tabChanged()
        print 'starting sane'
        try:
            print 'SANE version:', sane.init()
        except:
            pass
 


    def on_save1_activate(self, event):
        print 'save1'
        self.singlePreferences.save()
        self.setEntriesEditable(self.EntriesPreferences, False)
        self.loadProfile(self.singlePreferences.profileName)
        self.tabChanged()
        
    def on_new1_activate(self, event):
        self.singlePreferences.newRecord()
        self.setEntriesEditable(self.EntriesPreferences, True)

    def on_choose_profile1_activate(self, event):
        print 'choose Profil'
        self.loadProfile(self.singlePreferences.profileName)

        
    def on_edit1_activate(self, event):
        print "tabOption = ",  self.tabOption
        if self.tabOption == self.tabProfile:
            self.setEntriesEditable(self.EntriesPreferences, True)
        elif self.tabOption == self.tabCommunication:
            self.setEntriesEditable(self.EntriesPreferencesCommunication, True)
        elif self.tabOption == self.tabPathToExecutables:
            self.setEntriesEditable(self.EntriesPreferencesExecutables, True)
        elif self.tabOption == self.tabEmail:
            self.setEntriesEditable(self.EntriesPreferencesEmail, True)
        elif self.tabOption == self.tabScanner:
            self.setEntriesEditable(self.EntriesPreferencesScanner, True)
        elif self.tabOption == self.tabDMS:
            self.setEntriesEditable(self.EntriesPreferencesDMS, True)

    
    def on_delete1_activate(self, event):
        self.singlePreferences.deleteRecord()

    def on_quit1_activate(self, event):
        self.closeWindow() 

    # Buttons
    def on_bListScanDevices_clicked(self, event):
        try:
            
            liDevs = sane.get_devices()
            print 'Available devices=', liDevs
            cb = self.getWidget('cbScanDevice')
            for devs in liDevs:
                listItem_a = gtk.ListItem(devs[0])
                cb.list.append_items([listItem_a])
        except:
            pass
            
            
    def on_colorBG_color_set(self, event):
        self.setColor2Text(event, 'eBG')
        
    def on_colorFG_color_set(self, event):
        self.setColor2Text(event, 'eFG')
    def on_colorDutyBG_color_set(self, event):
        self.setColor2Text(event, 'eDutyBG')
    def on_colorDutyFG_color_set(self, event):
        self.setColor2Text(event, 'eDutyFG')
        
   
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
            self.setTreeVisible(True)
            self.out( 'Seite 0')
            self.singlePreferences.setEntries(self.getDataEntries(self.EntriesPreferences) )
            # set the Entries manually, because there is no tree event
            self.singlePreferences.fillEntries(self.singlePreferences.ID)

        elif self.tabOption == self.tabCommunication:
            self.editAction = 'editProfile'
            self.setTreeVisible(False)
            self.singlePreferences.setEntries(self.getDataEntries(self.EntriesPreferencesCommunication) )
            # set the Entries manually, because there is no tree event
            self.singlePreferences.fillEntries(self.singlePreferences.ID)
            
        elif self.tabOption == self.tabPathToExecutables:
            self.editAction = 'editProfile'
            self.setTreeVisible(False)
            self.singlePreferences.setEntries(self.getDataEntries(self.EntriesPreferencesExecutables) )
            # set the Entries manually, because there is no tree event
            self.singlePreferences.fillEntries(self.singlePreferences.ID)

        elif self.tabOption == self.tabEmail:
            self.editAction = 'editProfile'
            self.setTreeVisible(False)
            self.singlePreferences.setEntries(self.getDataEntries(self.EntriesPreferencesEmail) )
            # set the Entries manually, because there is no tree event
            self.singlePreferences.fillEntries(self.singlePreferences.ID)

        elif self.tabOption == self.tabScanner:
            self.editAction = 'editProfile'
            self.setTreeVisible(False)
            self.singlePreferences.setEntries(self.getDataEntries(self.EntriesPreferencesScanner) )
            # set the Entries manually, because there is no tree event
            self.singlePreferences.fillEntries(self.singlePreferences.ID)
        elif self.tabOption == self.tabDMS:
            self.editAction = 'editProfileDMS'
            self.setTreeVisible(False)
            self.singlePreferences.setEntries(self.getDataEntries(self.EntriesPreferencesDMS) )
            # set the Entries manually, because there is no tree event
            self.singlePreferences.fillEntries(self.singlePreferences.ID)
           
 

        else:
            
            self.setTreeVisible(False)

        # refresh the Tree
        self.refreshTree()
        self.enableMenuItem(self.editAction)
        self.editEntries = False
        