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

from cuon.Databases.SingleData import SingleData

import logging
from cuon.Windows.chooseWindows  import chooseWindows
import cuon.Addresses.addresses
import cuon.Addresses.SingleAddress
import cuon.DMS.documentTools
import cuon.DMS.dms

import SingleBotany



class botanywindow(chooseWindows):

    
    def __init__(self, allTables):

        chooseWindows.__init__(self)

        self.loadGlade('botany.xml')
        self.win1 = self.getWidget('BotanyMainwindow')
        self.oDocumentTools = cuon.DMS.documentTools.documentTools()
        self.ModulNumber = self.MN['Botany']        
        self.allTables = allTables
        self.singleBotany = SingleBotany.SingleBotany(allTables)
        self.singleAddress = cuon.Addresses.SingleAddress.SingleAddress(allTables)
        
        # self.singleBotany.loadTable()
              
        self.EntriesBotany = 'botany.xml'
                
        
        #singleBotany
 
 
        self.loadEntries(self.EntriesBotany)
        self.singleBotany.setEntries(self.getDataEntries( self.EntriesBotany) )
        self.singleBotany.setGladeXml(self.xml)
        self.singleBotany.setTreeFields( ['botany_name', 'botany_family'] )
#        self.singleBotany.setStore( gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING,   gobject.TYPE_UINT) ) 
        self.singleBotany.setTreeOrder('botany_name')
        self.singleBotany.setTree(self.xml.get_widget('tree1') )
        self.singleBotany.setListHeader(['botany_name', 'botany_family', ])
        
   
        

        # Menu-items
        self.initMenuItems()

        # Close Menus for Tab

        self.addEnabledMenuItems('tabs','botany1')


        # seperate Menus
        self.addEnabledMenuItems('botany','botany1')

        
        # enabledMenues for Article
        self.addEnabledMenuItems('editBotany','new1', self.dicUserKeys['articles_new'])
        self.addEnabledMenuItems('editBotany','clear1', self.dicUserKeys['articles_delete'])
        self.addEnabledMenuItems('editBotany','print1', self.dicUserKeys['articles_print'])
        self.addEnabledMenuItems('editBotany','edit1',self.dicUserKeys['articles_edit'])

      


        # tabs from notebook
        self.tabBotany = 0
        

        # start
        
        self.tabChanged()

        # enabled menus for article
        self.addEnabledMenuItems('editBotany','new1')
        self.addEnabledMenuItems('editBotany','clear1')
        self.addEnabledMenuItems('editBotany','print1')

        
       
    
        self.win1.add_accel_group(self.accel_group)
    #Menu File
              
    def on_quit1_activate(self, event):
        print "exit botany v2"
        self.closeWindow()
  

    #Menu Botany
  
    def on_save1_activate(self, event):
        print "save articles v2"
        self.singleBotany.save()
        self.setEntriesEditable(self.EntriesBotany, False)
        self.tabChanged()
         
        
    def on_new1_activate(self, event):
        print "new articles v2"
        self.singleBotany.newRecord()
        self.setEntriesEditable(self.EntriesBotany, True)
        

    def on_edit1_activate(self, event):
        self.setEntriesEditable(self.EntriesBotany, True)

    def on_delete1_activate(self, event):
        print "delete articles v2"
        self.singleBotany.deleteRecord()


   
    # search button
    def on_bSearch_clicked(self, event):
        self.searchBotany()


    def on_eFindNumber_editing_done(self, event):
        print 'Find Number'
        self.searchArticle()

    def on_eFindNumber_key_press_event(self, entry,event):
        if self.checkKey(event,'NONE','Return'):
            self.searchArticle()
            
    def on_eFindDesignation_editing_done(self, event):
        print 'Find Designation'
        self.searchArticle()

    def on_eFindDesignation_key_press_event(self, entry,event):
        if self.checkKey(event,'NONE','Return'):
            self.searchArticle()
    def on_bBotanyDMS_clicked(self, event):
        print 'dms clicked'
        if self.singleBotany.ID > 0:
            print 'ModulNumber', self.ModulNumber
            Dms = cuon.DMS.dms.dmswindow(self.allTables, self.ModulNumber, {'1':self.singleBotany.ID})
        


    def searchBotany(self):
        self.out( 'Searching ....', self.ERROR)
        sNumber = self.getWidget('eFindNumber').get_text()
        sDesignation = self.getWidget('eFindDesignation').get_text()
        self.out('Name and City = ' + sNumber + ', ' + sDesignation, self.ERROR)
        
        #self.singleBotany.sWhere = 'where number ~* \'.*' + sNumber + '.*\' and designation ~* \'.*' + sDesignation + '.*\''
        liSearch = ['number',sNumber, 'designation', sDesignation]
        self.singleBotany.sWhere = self.getWhere(liSearch)
        self.out(self.singleBotany.sWhere, self.ERROR)
        self.refreshTree()

    def refreshTree(self):
        self.singleBotany.disconnectTree()
        
        if self.tabOption == self.tabBotany:
            self.singleBotany.connectTree()
            self.singleBotany.refreshTree()

  


         
    def tabChanged(self):
        print 'tab changed to :'  + str(self.tabOption)
        self.setTreeVisible(True)
        if self.tabOption == self.tabBotany:
            #Address
            self.disableMenuItem('tabs')
            self.enableMenuItem('botany')
            print 'Seite 0'
            self.editAction = 'editBotany'
   
        # refresh the Tree
        self.refreshTree()
        self.enableMenuItem(self.editAction)
        self.editEntries = False
