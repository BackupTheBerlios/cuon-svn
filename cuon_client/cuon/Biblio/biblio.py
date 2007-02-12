# -*- coding: utf-8 -*-

##Copyright (C) [2005]  [Juergen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

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
import SingleBiblio
import cuon.DMS.dms

class bibliowindow(chooseWindows):

    
    def __init__(self, allTables):

        chooseWindows.__init__(self)
       
        self.singleBiblio = SingleBiblio.SingleBiblio(allTables)

    
        self.loadGlade('biblio.xml', 'BiblioMainwindow')
        #self.win1 = self.getWidget('BiblioMainwindow')
        #self.setStatusBar()
        self.allTables = allTables

        self.EntriesBiblio = 'biblio.xml'
        
        self.loadEntries(self.EntriesBiblio)
        
        self.singleBiblio.setEntries(self.getDataEntries('biblio.xml') )
        self.singleBiblio.setGladeXml(self.xml)
        self.singleBiblio.setTreeFields( ['title', 'designation','year','month'] )
        self.singleBiblio.setStore( gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_UINT, gobject.TYPE_UINT, gobject.TYPE_UINT) ) 
        self.singleBiblio.setTreeOrder('title,year,month')
        self.singleBiblio.setListHeader([_('Title'), _('Designation'), _('Year'),_('Month')])
        self.singleBiblio.setTree(self.xml.get_widget('tree1') )

  
  

        # set values for comboBox

          

        # Menu-items
        self.initMenuItems()

        # Close Menus for Tab
        self.addEnabledMenuItems('tabs','mi_biblio1')
  

               
        # seperate Menus
        self.addEnabledMenuItems('biblio','mi_biblio1')
          

        # enabledMenues for Address
        self.addEnabledMenuItems('editBiblio','mi_new1')
        self.addEnabledMenuItems('editBiblio','mi_clear1')
        self.addEnabledMenuItems('editBiblio','mi_print1')
        self.addEnabledMenuItems('editBiblio','mi_edit1')


    
        

        # tabs from notebook
        self.tabBiblio = 0
    
        
        

        self.tabChanged()
        

    def checkClient(self):
        pass
        
    #Menu File
              
    def on_quit1_activate(self, event):
        self.out( "exit biblio V1")
        self.on_bChooseClient_clicked(event)
        

    def on_bChooseClient_clicked(self, event):
        print 'Client-ID = ', self.singleBiblio.ID
        
        if self.singleBiblio.ID  > 0:
            self.oUser.client = self.singleBiblio.ID 
            self.oUser.refreshDicUser()
            print `self.oUser.getSqlDicUser`
            self.openDB()
            self.oUser = self.saveObject('User', self.oUser)
            self.closeDB()
            self.closeWindow() 
        else:
            print 'no client-ID'
    
        


    #Menu Biblio
  
    def on_save1_activate(self, event):
        self.out( "save addresses v2")
        self.singleBiblio.save()
        self.setEntriesEditable(self.EntriesBiblio, False)
        self.tabChanged()
        
    def on_new1_activate(self, event):
        self.out( "new addresses v2")
        self.singleBiblio.newRecord()
        self.setEntriesEditable(self.EntriesBiblio, True)

    def on_edit1_activate(self, event):
        self.out( "edit addresses v2")
        self.setEntriesEditable(self.EntriesBiblio, True)


    def on_delete1_activate(self, event):
        self.out( "delete addresses v2")
        self.singleBiblio.deleteRecord()

 
    def on_bDMS_clicked(self, event):
        print 'dms clicked'
        if self.singleBiblio.ID > 0:
            print 'ModulNumber', self.ModulNumber
            Dms = cuon.DMS.dms.dmswindow(self.allTables, self.ModulNumber, {'1':self.singleBiblio.ID})
        
    # search button
    def on_bSearch_clicked(self, event):
        self.out( 'Searching ....', self.ERROR)
        sTitle = self.getWidget('eFindTitle').get_text()
        sDesi = self.getWidget('eFindDesignation').get_text()
        
        self.singleBiblio.sWhere = 'where title ~* \'.*' + sTitle + '.*\' and designation ~* \'.*' + sDesi + '.*\''
        #self.out(self.singleBiblio.sWhere, self.ERROR)
        self.refreshTree()

    def refreshTree(self):
        self.singleBiblio.disconnectTree()
        
        if self.tabOption == self.tabBiblio:
            self.singleBiblio.connectTree()
            self.singleBiblio.refreshTree()
  ##      elif self.tabOption == self.tabMisc:
##            self.singleMisc.sWhere  ='where address_id = ' + `int(self.singleBiblio.ID)`
##            self.singleMisc.fillEntries(self.singleMisc.findSingleId())

##        elif self.tabOption == self.tabPartner:
##            self.singlePartner.sWhere  ='where addressid = ' + `int(self.singleBiblio.ID)`
##            self.singlePartner.connectTree()
##            self.singlePartner.refreshTree()
##        elif self.tabOption == self.tabSchedul:
##            self.singleSchedul.sWhere  ='where partnerid = ' + `int(self.singlePartner.ID)`
##            self.singleSchedul.connectTree()
##            self.singleSchedul.refreshTree()
            
     


         
    def tabChanged(self):
        #self.out( 'tab changed to :'  + str(self.tabOption))
        
        if self.tabOption == self.tabBiblio:
            #Address
            self.disableMenuItem('tabs')
            self.enableMenuItem('biblio')

            self.actualEntries = self.singleBiblio.getEntries()
            self.editAction = 'editBiblio'
            #self.setStatusbarText([''])
          
            self.setTreeVisible(True)
            

            self.out( 'Seite 0')


 ##       elif self.tabOption == self.tabBank:
##            self.out( 'Seite 2')
##            self.disableMenuItem('tabs')
##            self.enableMenuItem('bank')
           
##            self.editAction = 'editBank'
##            self.setTreeVisible(False)
##            #self.setStatusbarText([self.singleBiblio.sStatus])


##        elif self.tabOption == self.tabMisc:
##            self.out( 'Seite 3')

##            self.disableMenuItem('tabs')
##            self.enableMenuItem('misc')
##            self.editAction = 'editMisc'
##            self.setTreeVisible(False)
##            #self.setStatusbarText([self.singleBiblio.sStatus])




##        elif self.tabOption == self.tabPartner:
##            #Partner
##            self.disableMenuItem('tabs')
##            self.enableMenuItem('partner')
            
##            self.out( 'Seite 1')
##            self.editAction = 'editPartner'
##            self.setTreeVisible(True)
##            #self.setStatusbarText([self.singleBiblio.sStatus])

            
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
        
