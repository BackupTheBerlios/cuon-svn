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
import SingleDMS
import cuon.Misc.misc
import os
import sane
import Image
import bz2

class dmswindow(windows):

    
    def __init__(self, allTables):

        windows.__init__(self)
        self.openDB()
        self.oUser = self.loadObject('User')
        self.closeDB()
        print self.oUser
        print '-.............................'
        

        self.singleDMS = SingleDMS.SingleDMS(allTables)
       
        self.singleDMS.username = self.oUser.getUserName()
        self.loadGlade('dms.xml')
        self.win1 = self.getWidget('DMSMainwindow')
        self.scanfile = None


        self.EntriesPreferences = 'dms.xml'

        
        self.loadEntries(self.EntriesPreferences)
        
        
        #self.singleDMS.sWhere = " where username = \'" + self.oUser.getUserName() + "\'"
        self.singleDMS.setEntries(self.getDataEntries('dms.xml') )
        self.singleDMS.setGladeXml(self.xml)
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


    def on_bScan_clicked(self, event):
        self.scanDocument()
   
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
 ##       misc = cuon.Misc.misc.misc()
        
##        sc = self.dicUser['prefDMS']['scan_program']
##        sc = sc + ' --mode ' + self.dicUser['prefDMS']['scan_mode']
##        sc = sc + ' --resolution ' + self.dicUser['prefDMS']['scan_resolution']
        
##        print sc
##        self.scanfile = self.dicUser['prefPath']['tmp'] +  misc.getRandomFilename('_scan.tmp')
##        print self.scanfile
##        sc = sc + ' >> ' + self.scanfile

##        print sc
##        ok = os.system(sc)
##        print ok
        
        scanner=sane.open(self.dicUser['prefDMS']['scan_device'])
        print 'SaneDev object=', scanner
        print 'Device parameters:', scanner.get_parameters()
        
        # Set scan parameters
        scanner.mode = 'Color'
        #scanner.contrast=170.0
        #scanner.brightness=150.0
        #scanner.white_level=190.0
        scanner.depth=24
        scanner.br_x=1024.0
        scanner.br_y=768.0
        scanner.resolution = 150
        
        print 'Device parameters after setting:', scanner.get_parameters()
   
        # Initiate the scan
        scanner.start()
        
        # Get an Image object
        # (For my B&W QuickCam, this is a grey-scale image.  Other scanning devices
        #  may return a
        im=scanner.snap()
        print 'Device parameters after snap:', scanner.get_parameters()

        # Write the image out as a GIF file
        #im.save('/home/jhamel/foo.png')
        
        im.show()
        if (im.mode != "RGB"):
            im = im.convert("RGB")

        self.singleDMS.size_x = im.size[0]
        self.singleDMS.size_y = im.size[1]
        
        s = im.tostring('raw','RGB')
        print len(s)
        s2 = bz2.compress(s)
        print len(s2)
        self.singleDMS.imageData = s2
        

        #newIm = Image.fromstring('RGB',[1024.0,768.0], s)
        #newIm.show()
        

        
