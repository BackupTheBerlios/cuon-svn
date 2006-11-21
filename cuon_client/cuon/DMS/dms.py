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
sys.path.append('/usr/lib/python/')
sys.path.append('/usr/lib/python/site-packages/PIL')

from types import *
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import gobject
import string

import logging
from cuon.Windows.windows  import windows
#import cuon.Login.User
import SingleDMS
import dms 

import cuon.Misc.misc
import os

try:
    import Image
except:
    print "no package Image found"
    print ""
    
import bz2
import re
import binascii
import cuon.DMS.documentTools

class dmswindow(windows):

    
    def __init__(self, allTables, module = 0, sep_info = None, dicVars={}, dicExtInfo={}):
        
        windows.__init__(self)

        self.ModulNumber = self.MN['DMS']
        self.dicVars = dicVars
        self.dicExtInfo = dicExtInfo
        
            
        self.allTables = allTables
        
        self.openDB()
        self.oUser = self.loadObject('User')
        self.closeDB()
        #print self.oUser
        #print '-.............................'
        self.oDocumentTools = cuon.DMS.documentTools.documentTools()
        

        self.singleDMS = SingleDMS.SingleDMS(allTables)
       
        self.singleDMS.username = self.oUser.getUserName()
        self.loadGlade('dms.xml')
        self.win1 = self.getWidget('DMSMainwindow')
        self.diaLink = self.getWidget('diaLink')
        self.diaLink.hide()
        
        self.scanfile = None
        

        self.EntriesPreferences = 'dms.xml'
        
        if sep_info:
            try:
                if sep_info.has_key('1'):
                    self.sepInfo['1'] = sep_info['1']
                if sep_info.has_key('2'):
                    self.sepInfo['2'] = sep_info['2']
                if sep_info.has_key('3'):
                    self.sepInfo['3'] = sep_info['3']
            except:
                print 'Error by sep-info'
        else:
            self.sepInfo['1'] = self.MN['DMS']

        print "Sep-Info 1 ",  self.sepInfo['1']
           
        if module > 0:
            self.ModulNumber = module
        if   self.ModulNumber != self.MN['DMS'] :
            self.sWhereStandard = ' where insert_from_module = ' + `self.ModulNumber`
            self.sWhereStandard = self.sWhereStandard + ' and  sep_info_1 = ' +  `self.sepInfo['1']`            
        else:
            self.sWhereStandard = ''
            
        
            
        
        
        self.loadEntries(self.EntriesPreferences)
        
        
        self.singleDMS.sWhere = self.sWhereStandard
        self.singleDMS.setEntries(self.getDataEntries('dms.xml') )
        self.singleDMS.setGladeXml(self.xml)
        self.singleDMS.ModulNumber = self.ModulNumber
        print 'self.singleDMS.ModulNumber', self.singleDMS.ModulNumber
        self.singleDMS.setTreeFields( ['title', 'category','insert_time','update_time'] )
        self.singleDMS.setStore( gtk.ListStore(gobject.TYPE_STRING,  gobject.TYPE_STRING, gobject.TYPE_STRING,  gobject.TYPE_STRING,    gobject.TYPE_UINT) ) 
        self.singleDMS.setTreeOrder('title')
        self.singleDMS.setListHeader([_('Title'), _('Category'), _('Insert at'), _('update at') ])
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
        
        #Now check for automatic-Actions
        self.LastDoc = None
        if self.dicExtInfo and self.dicExtInfo.has_key('LastDoc'):
            print 'lastdoc found'
            self.activateClick('new1')
            self.LastDoc =self.dicExtInfo['LastDoc']
            self.activateClick('bImport',None,'clicked')
            

        

    def on_save1_activate(self, event):
        print 'save1'
        self.singleDMS.sep_info_1 = self.sepInfo['1']
        self.singleDMS.ModulNumber = self.ModulNumber
        self.singleDMS.save(['document_image'])
        
        self.setEntriesEditable(self.EntriesPreferences, False)
        self.tabChanged()
        
    def on_new1_activate(self, event):
        self.singleDMS.newRecord()
        self.setEntriesEditable(self.EntriesPreferences, True)
        

    def on_edit1_activate(self, event):
        if self.tabOption == self.tabDocument:
            self.setEntriesEditable(self.EntriesPreferences, True)
##        elif self.tabOption == self.tabPrinting:
##            self.setEntriesEditable(self.EntriesPreferencesPrinting, True)
##        elif self.tabOption == self.tabPathToReports:
##            self.setEntriesEditable(self.EntriesPreferencesPathToReports, True)
##        elif self.tabOption == self.tabPathToDocs:
##            self.setEntriesEditable(self.EntriesPreferencesPathToDocs, True)


    def on_clear1_activate(self, event):
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
        if self.LastDoc:
            filename = self.LastDoc
            self.LastDoc = None
        else:
            filename = self.getWidget("gfcb_ImportFile").get_filename()
            
        self.oDocumentTools.importDocument( self.singleDMS, self.dicUser, filename )
        

    def on_bLink_clicked(self, event):
        print 'bLink'
        self.diaLink.show()
    def on_okbutton1_clicked(self, event):
        print 'ok clicked'
        sLink = self.getWidget('eLink').get_text()
        print sLink
        self.diaLink.hide()
        self.singleDMS.imageData = sLink
        self.singleDMS.fileFormat = self.dicUser['prefDMS']['fileformat']['LINK']['format']

    def on_cancelbutton1_clicked(self, event):
        print 'cancel clicked'
        self.diaLink.hide()
    
    def on_bWriteLastDocument_clicked(self, event):
        if self.dicExtInfo:
            self.dicExtInfo['LastDoc'] = self.singleDMS.tmpFile
            dm2 = cuon.DMS.dms.dmswindow(self.allTables, self.dicExtInfo['Modul'], self.dicExtInfo['sep_info'],None,self.dicExtInfo)
            
    def on_bView_clicked(self, event):
        print  self.dicUser['prefDMS']['fileformat']['scanImage']['format']
        print  self.singleDMS.fileFormat

        self.oDocumentTools.viewDocument(self.singleDMS, self.dicUser, self.dicVars)
        
            
        
    def refreshTree(self):
        self.singleDMS.disconnectTree()
    
        
        if self.tabOption == self.tabDocument:
            
            #self.singleDMS.sWhere = " where username = \'" + self.oUser.getUserName() + "\'"
            self.singleDMS.connectTree()
            self.singleDMS.refreshTree()
            #self.ModulNumber = self.MN['DMS']
            
    def tabChanged(self):
        self.out( 'tab changed to :'  + str(self.tabOption))
        
        if self.tabOption == self.tabDocument:
            #Preferences
            self.disableMenuItem('tabs')
            self.enableMenuItem('editDMS')

            self.actualEntries = self.singleDMS.getEntries()
            self.editAction = 'editDMS'
            self.setTreeVisible(True)
            self.out( 'Seite 0')
            self.singleDMS.setEntries(self.getDataEntries(self.EntriesPreferences) )
            # set the Entries manually, because there is no tree event
            self.singleDMS.fillEntries(self.singleDMS.ID)


        else:
            
            self.setTreeVisible(False)

        # refresh the Tree
        self.refreshTree()
        self.enableMenuItem(self.editAction)
        self.editEntries = False
        

    def scanDocument(self):
    
        self.oDocumentTools.scanDocument(self.singleDMS, self.dicUser)
        
   
                        
