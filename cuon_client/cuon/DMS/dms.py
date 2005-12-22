# -*- coding: utf-8 -*-
##Copyright (C) [2003-2005]  [Jürgen Hamel, D-32584 Löhne]

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
#import cuon.Login.User
import SingleDMS
import cuon.Misc.misc
import os
import sane
import Image
import bz2
import re
import binascii
import cuon.DMS.documentTools

class dmswindow(windows):

    
    def __init__(self, allTables, module = 0, sep_info = None):
        
        windows.__init__(self)

        self.ModulNumber = self.MN['DMS']
        
        self.openDB()
        self.oUser = self.loadObject('User')
        self.closeDB()
        print self.oUser
        print '-.............................'
        self.oDocumentTools = cuon.DMS.documentTools.documentTools()
        

        self.singleDMS = SingleDMS.SingleDMS(allTables)
       
        self.singleDMS.username = self.oUser.getUserName()
        self.loadGlade('dms.xml')
        self.win1 = self.getWidget('DMSMainwindow')
        self.scanfile = None
        

        self.EntriesPreferences = 'dms.xml'
        if module > 0:
            self.ModulNumber = module
            
        self.sWhereStandard = ' where insert_from_module = ' + `self.ModulNumber`
        if sep_info:
            self.sepInfo = sep_info
            self.sWhereStandard = self.sWhereStandard + ' and  sep_info_1 = ' +  `self.sepInfo['1']`

            
            
        
        
        self.loadEntries(self.EntriesPreferences)
        
        
        self.singleDMS.sWhere = self.sWhereStandard
        self.singleDMS.setEntries(self.getDataEntries('dms.xml') )
        self.singleDMS.setGladeXml(self.xml)
        self.singleDMS.ModulNumber = self.ModulNumber
        
        self.singleDMS.setTreeFields( ['title', 'category'] )
        self.singleDMS.setStore( gtk.ListStore(gobject.TYPE_STRING,  gobject.TYPE_STRING,   gobject.TYPE_UINT) ) 
        self.singleDMS.setTreeOrder('title')
        self.singleDMS.setListHeader([_('Title'), _('Category') ])
        self.singleDMS.setTree(self.xml.get_widget('tree1') )

        self.singleDMS.imageWidget = self.getWidget('iThumbnail')
        
        # Menu-items
        self.initMenuItems()

  
        
        # Close Menus for Tab
        self.addEnabledMenuItems('tabs','')
         
        # enabledMenues for Preferences
        #self.addEnabledMenuItems('editProfile','profile1')
        self.addEnabledMenuItems('editDMS','clear1')
        #self.addEnabledMenuItems('editProfile','save1')
        self.addEnabledMenuItems('editDMS','new1')
        self.addEnabledMenuItems('editDMS','edit1')
        

        # tabs from notebook
        self.tabDocument = 0
        
        
        self.tabOption = self.tabDocument
        self.tabChanged()

        # SANE for scan images
        
        print 'SANE version:', sane.init()
        print 'Available devices=', sane.get_devices()
        
    

    def on_save1_activate(self, event):
        print 'save1'
        self.singleDMS.sep_info_1 = self.sepInfo['1']
        self.singleDMS.ModulNumber = self.ModulNumber
        self.singleDMS.save(['document_image'])
        
        self.setEntriesEditable(self.EntriesPreferences, FALSE)
        self.tabChanged()
        
    def on_new1_activate(self, event):
        self.singleDMS.newRecord()
        self.setEntriesEditable(self.EntriesPreferences, TRUE)

    def on_edit1_activate(self, event):
        if self.tabOption == self.tabDocument:
            self.setEntriesEditable(self.EntriesPreferences, TRUE)
##        elif self.tabOption == self.tabPrinting:
##            self.setEntriesEditable(self.EntriesPreferencesPrinting, TRUE)
##        elif self.tabOption == self.tabPathToReports:
##            self.setEntriesEditable(self.EntriesPreferencesPathToReports, TRUE)
##        elif self.tabOption == self.tabPathToDocs:
##            self.setEntriesEditable(self.EntriesPreferencesPathToDocs, TRUE)


    def on_delete1_activate(self, event):
        self.singleDMS.deleteRecord()

    def on_quit1_activate(self, event):
        self.closeWindow() 

    def on_bSearch_clicked(self, event):
        print 'Search'
        dicSearchfields = self.readSearchDatafields(  {'title':'eSearchTitle', 'category':'eSearchCategory',  'sub1':'eSearchSub1',  'sub2':'eSearchSub2',  'sub3': 'eSearchSub3',  'sub4':'eSearchSub4',  'sub5':'eSearchSub5',  'search1':'eSearchSearch1',  'search2': 'eSearchSearch2',   'search3':'eSearchSearch3',  'search4': 'eSearchSearch4'})

        print dicSearchfields
        
        sWhere = ''
        if dicSearchfields:
            for key in dicSearchfields.keys():
                if dicSearchfields[key]:
                    if sWhere:
                        sWhere = sWhere + ' and ' +  key+ " ~* \'"  + dicSearchfields[key] + "\' "
                    else:
                        sWhere = 'where  ' +  key + " ~* \'"  + dicSearchfields[key] + "\' "
            sWhere = sWhere + self.sWhereStandard
            
        else:
            sWhere = self.sWhereStandard
            
        print sWhere
        
        self.singleDMS.sWhere = sWhere
        self.refreshTree()
        
        
    def on_bScan_clicked(self, event):
        self.scanDocument()
        self.singleDMS.fileFormat = self.dicUser['prefDMS']['fileformat']['scanImage']['format']

    def on_bImport_clicked(self, event):
        print 'bImport'
        self.importDocument()


    def on_bView_clicked(self, event):
        print  self.dicUser['prefDMS']['fileformat']['scanImage']['format']
        print  self.singleDMS.fileFormat

        self.oDocumentTools.viewDocument(self.singleDMS, self.dicUser)
        
            
        
    def refreshTree(self):
        self.singleDMS.disconnectTree()
    
        
        if self.tabOption == self.tabDocument:
            
            #self.singleDMS.sWhere = " where username = \'" + self.oUser.getUserName() + "\'"
            self.singleDMS.connectTree()
            self.singleDMS.refreshTree()

            
    def tabChanged(self):
        self.out( 'tab changed to :'  + str(self.tabOption))
        
        if self.tabOption == self.tabDocument:
            #Preferences
            self.disableMenuItem('tabs')
            self.enableMenuItem('editDMS')

            self.actualEntries = self.singleDMS.getEntries()
            self.editAction = 'editDMS'
            self.setTreeVisible(TRUE)
            self.out( 'Seite 0')
            self.singleDMS.setEntries(self.getDataEntries(self.EntriesPreferences) )
            # set the Entries manually, because there is no tree event
            self.singleDMS.fillEntries(self.singleDMS.ID)


        else:
            
            self.setTreeVisible(FALSE)

        # refresh the Tree
        self.refreshTree()
        self.enableMenuItem(self.editAction)
        self.editEntries = FALSE
        

    def scanDocument(self):
    
        self.oDocumentTools.scanDocument(self.singleDMS, self.dicUser)
        
    def importDocument(self):
        sFile = self.getWidget('eImportFile').get_text()
        self.oDocumentTools.importDocument(self.singleDMS, self.dicUser, sFile)                        
