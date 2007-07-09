# -*- coding: utf-8 -*-

##Copyright (C) [2005]  [Juergen Hamel, D-32584 Löhne]

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

import string

import logging
from cuon.Windows.chooseWindows  import chooseWindows
import cPickle
#import cuon.OpenOffice.letter
# localisation
import locale, gettext
locale.setlocale (locale.LC_NUMERIC, '')
import threading
import datetime as DateTime
import SingleWeb2
import cuon.DMS.dms
import cuon.Misc.misc


class web2window(chooseWindows):

    
    def __init__(self, allTables):

        chooseWindows.__init__(self)
       
        self.singleWeb2 = SingleWeb2.SingleWeb2(allTables)
        self.singleWebImages = SingleWeb2.SingleWeb2(allTables)
        self.singleWebDownload = SingleWeb2.SingleWeb2(allTables)

    
        self.loadGlade('web2.xml', 'Web2Mainwindow')
        #self.win1 = self.getWidget('Web2Mainwindow')
        #self.setStatusBar()
        #self.win1.maximize()
        self.allTables = allTables
        self.ModulNumber = self.MN['Web2']
        self.EntriesWeb2 = 'web2.xml'
        
        self.loadEntries(self.EntriesWeb2)
        
        self.singleWeb2.setEntries(self.getDataEntries('web2.xml') )
        self.singleWeb2.setGladeXml(self.xml)
        self.singleWeb2.setTreeFields( ['name', 'designation'] )
        self.singleWeb2.setStore( gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_UINT) ) 
        self.singleWeb2.setTreeOrder('type,name')
        self.singleWeb2.setListHeader([_('Name'), _('Designation')])
        self.singleWeb2.setTree(self.xml.get_widget('tree1') )
  

        # set values for comboBox

        self.mi = cuon.Misc.misc.misc()
  

        # Menu-items
        self.initMenuItems()

        # Close Menus for Tab
        self.addEnabledMenuItems('tabs','websites')
  

               
        # seperate Menus
        self.addEnabledMenuItems('Web2','websites')
          

        # enabledMenues for Address
        self.addEnabledMenuItems('editWeb2','new1')
        self.addEnabledMenuItems('editWeb2','delete1')
        self.addEnabledMenuItems('editWeb2','print1')
        self.addEnabledMenuItems('editWeb2','edit1')


        self.editFilename = None
        
        

        # tabs from notebook
        self.tabWeb2 = 0
        self.tabWebImages = 1
        self.tabWebDownload = 2
        
    
        
        

        self.tabChanged()
        

    def checkClient(self):
        pass
        
    #Menu File
    
    def on_server_restart1_activate(self, event):
        print 'server restart'
        liStatus = self.rpc.callRP('Web.restartServerWeb2',self.dicUser)
    
              
    def on_quit_activate(self, event):
        self.out( "exit Web2 V1")
        self.closeWindow()
        


    #Menu Web2
  
    def on_save1_activate(self, event):
        self.out( "save web2 v2")
        
        if self.editFilename:
            try:
                f = open(self.editFilename)
                s = f.read()
                self.add2Textbuffer(self.getWidget('tvData'),s,'Overwrite')
                f.close()
                
            except Exception, params:
                print Exception,params
                
        self.singleWeb2.save()
        self.setEntriesEditable(self.EntriesWeb2, False)
        self.tabChanged()        
                
    def on_new1_activate(self, event):
        self.out( "new web2 v2")
        self.singleWeb2.newRecord()
        self.setEntriesEditable(self.EntriesWeb2, True)

    def on_edit1_activate(self, event):
        self.out( "edit web2 v2")
        self.setEntriesEditable(self.EntriesWeb2, True)
        self.editFilename = None

    def on_delete1_activate(self, event):
        self.out( "delete web2 v2")
        self.singleWeb2.deleteRecord()

 
    def on_bDMS_clicked(self, event):
        print 'dms clicked'
        if self.singleWeb2.ID > 0:
            print 'ModulNumber', self.ModulNumber
            Dms = cuon.DMS.dms.dmswindow(self.allTables, self.ModulNumber, {'1':self.singleWeb2.ID})
        
    # search button
    def on_bSearch_clicked(self, event):
        self.out( 'Searching ....', self.ERROR)
        sTitle = self.getWidget('eFindTitle').get_text()
        sDesi = self.getWidget('eFindDesignation').get_text()
        
        self.singleWeb2.sWhere = 'where title ~* \'.*' + sTitle + '.*\' and designation ~* \'.*' + sDesi + '.*\''
        #self.out(self.singleWeb2.sWhere, self.ERROR)
        self.refreshTree()
   
        
    def on_bDMS_clicked(self, event):
        print 'dms clicked'
        if self.singleWeb2.ID > 0:
            print 'ModulNumber', self.ModulNumber
            Dms = cuon.DMS.dms.dmswindow(self.allTables, self.ModulNumber, {'1':self.singleWeb2.ID})
                
    
    def refreshTree(self):
        self.singleWeb2.disconnectTree()
        
        if self.tabOption == self.tabWeb2:
            
            self.singleWeb2.connectTree()
            self.singleWeb2.refreshTree()
      
            #self.singleWeb2.fillEntries(self.singleMisc.findSingleId())

##        elif self.tabOption == self.tabPartner:
##            self.singlePartner.sWhere  ='where addressid = ' + `int(self.singleWeb2.ID)`
##            self.singlePartner.connectTree()
##            self.singlePartner.refreshTree()
##        elif self.tabOption == self.tabSchedul:
##            self.singleSchedul.sWhere  ='where partnerid = ' + `int(self.singlePartner.ID)`
##            self.singleSchedul.connectTree()
##            self.singleSchedul.refreshTree()
            
     


         
    def tabChanged(self):
        #self.out( 'tab changed to :'  + str(self.tabOption))
        
        if self.tabOption == self.tabWeb2:
            #Address
            self.disableMenuItem('tabs')
            self.enableMenuItem('Web2')

            self.actualEntries = self.singleWeb2.getEntries()
            self.editAction = 'editWeb2'
            #self.setStatusbarText([''])
          
            self.setTreeVisible(True)
            

            self.out( 'Seite 0')


        elif self.tabOption == self.tabWebImages:
            self.out( 'Seite 2')
            #self.disableMenuItem('tabs')
            #self.enableMenuItem('bank')
           
            #self.editAction = 'editBank'
            self.setTreeVisible(False)
            
            #self.setStatusbarText([self.singleWeb2.sStatus])


##        elif self.tabOption == self.tabMisc:
##            self.out( 'Seite 3')

##            self.disableMenuItem('tabs')
##            self.enableMenuItem('misc')
##            self.editAction = 'editMisc'
##            self.setTreeVisible(False)
##            #self.setStatusbarText([self.singleWeb2.sStatus])




##        elif self.tabOption == self.tabPartner:
##            #Partner
##            self.disableMenuItem('tabs')
##            self.enableMenuItem('partner')
            
##            self.out( 'Seite 1')
##            self.editAction = 'editPartner'
##            self.setTreeVisible(True)
##            #self.setStatusbarText([self.singleWeb2.sStatus])

            
##        elif self.tabOption == self.tabSchedul:
##            #Scheduling
##            self.disableMenuItem('tabs')
##            self.enableMenuItem('schedul')
            
##            self.out( 'Seite 4')
##            self.editAction = 'editSchedul'
##            self.setTreeVisible(True)
##            self.setStatusbarText([self.singlePartner.sStatus])

        # refresh the Tree
        self.refreshTree()
        self.enableMenuItem(self.editAction)
        self.editEntries = False
        
