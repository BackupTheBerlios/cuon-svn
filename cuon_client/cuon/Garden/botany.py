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

import SingleBotanyDivisio
import SingleBotanyClass
import SingleBotanyOrdo
import SingleBotanyFamily
import SingleBotanyGenus
import SingleBotany



class botanywindow(chooseWindows):

    
    def __init__(self, allTables):

        chooseWindows.__init__(self)

        self.loadGlade('botany.xml')
        self.win1 = self.getWidget('BotanyMainwindow')
        self.oDocumentTools = cuon.DMS.documentTools.documentTools()
        self.ModulNumber = 110500
        self.setStatusBar()
        self.sSearchTable = None

        self.allTables = allTables
        self.singleBotanyDivisio = SingleBotanyDivisio.SingleBotanyDivisio(allTables)
        self.singleBotanyClass = SingleBotanyClass.SingleBotanyClass(allTables)
        self.singleBotanyOrdo = SingleBotanyOrdo.SingleBotanyOrdo(allTables)
        self.singleBotanyFamily = SingleBotanyFamily.SingleBotanyFamily(allTables)
        self.singleBotanyGenus = SingleBotanyGenus.SingleBotanyGenus(allTables)
        self.singleBotany = SingleBotany.SingleBotany(allTables)
        self.singleAddress = cuon.Addresses.SingleAddress.SingleAddress(allTables)

        
        # self.singleBotany.loadTable()
              
        self.EntriesBotanyDivisio = 'botany_divisio.xml'
        self.EntriesBotanyClass = 'botany_class.xml'
        self.EntriesBotanyOrdo = 'botany_ordo.xml'
        self.EntriesBotanyFamily = 'botany_family.xml'
        self.EntriesBotanyGenus = 'botany_genus.xml'
        self.EntriesBotany = 'botany.xml'
                
        
        #singleBotany
 
 
        self.loadEntries(self.EntriesBotanyDivisio)
        self.loadEntries(self.EntriesBotanyClass)
        self.loadEntries(self.EntriesBotanyOrdo)
        self.loadEntries(self.EntriesBotanyFamily)
        self.loadEntries(self.EntriesBotanyGenus)
        self.loadEntries(self.EntriesBotany)
        
        
        self.singleBotanyDivisio.setEntries(self.getDataEntries( self.EntriesBotanyDivisio) )
        self.singleBotanyDivisio.setGladeXml(self.xml)
        self.singleBotanyDivisio.setTree(self.xml.get_widget('tree1') )
        
        self.singleBotanyClass.setEntries(self.getDataEntries( self.EntriesBotanyClass) )
        self.singleBotanyClass.setGladeXml(self.xml)
        self.singleBotanyClass.setTree(self.xml.get_widget('tree1') )

        self.singleBotanyOrdo.setEntries(self.getDataEntries( self.EntriesBotanyOrdo) )
        self.singleBotanyOrdo.setGladeXml(self.xml)
        self.singleBotanyOrdo.setTree(self.xml.get_widget('tree1') )

        self.singleBotanyFamily.setEntries(self.getDataEntries( self.EntriesBotanyFamily) )
        self.singleBotanyFamily.setGladeXml(self.xml)
        self.singleBotanyFamily.setTree(self.xml.get_widget('tree1') )
        
        self.singleBotanyGenus.setEntries(self.getDataEntries( self.EntriesBotanyGenus) )
        self.singleBotanyGenus.setGladeXml(self.xml)
        self.singleBotanyGenus.setTree(self.xml.get_widget('tree1') )
        
        self.singleBotany.setEntries(self.getDataEntries( self.EntriesBotany) )
        self.singleBotany.setGladeXml(self.xml)
        self.singleBotany.setTree(self.xml.get_widget('tree1') )
   
        

        # Menu-items
        self.initMenuItems()

        # Close Menus for Tab

        self.addEnabledMenuItems('tabs','divisio1')
        self.addEnabledMenuItems('tabs','class1')
        self.addEnabledMenuItems('tabs','ordo1')
        self.addEnabledMenuItems('tabs','family1')
        self.addEnabledMenuItems('tabs','genus1')
        self.addEnabledMenuItems('tabs','botany1')


        # seperate Menus
        self.addEnabledMenuItems('botany','botany1')
        self.addEnabledMenuItems('divisio','divisio1')
        self.addEnabledMenuItems('class','class1')
        self.addEnabledMenuItems('ordo','ordo1')
        self.addEnabledMenuItems('family','family1')
        self.addEnabledMenuItems('genus','genus1')

        
        # enabledMenues for Divisio
        self.addEnabledMenuItems('editDivisio','divisio_new1', self.dicUserKeys['articles_new'])
        self.addEnabledMenuItems('editDivisio','divisio_clear1', self.dicUserKeys['articles_delete'])
        #self.addEnabledMenuItems('editDivisio','divisio_print1', self.dicUserKeys['articles_print'])
        self.addEnabledMenuItems('editDivisio','divisio_edit1',self.dicUserKeys['articles_edit'])

        # enabledMenues for Class
        self.addEnabledMenuItems('editClass','class_new1', self.dicUserKeys['articles_new'])
        self.addEnabledMenuItems('editClass','class_clear1', self.dicUserKeys['articles_delete'])
        #self.addEnabledMenuItems('editClass','class_print1', self.dicUserKeys['articles_print'])
        self.addEnabledMenuItems('editClass','class_edit1',self.dicUserKeys['articles_edit'])
        # enabledMenues for Ordo
        self.addEnabledMenuItems('editOrdo','ordo_new1', self.dicUserKeys['articles_new'])
        self.addEnabledMenuItems('editOrdo','ordo_clear1', self.dicUserKeys['articles_delete'])
        #self.addEnabledMenuItems('editOrdo','ordo_print1', self.dicUserKeys['articles_print'])
        self.addEnabledMenuItems('editOrdo','ordo_edit1',self.dicUserKeys['articles_edit'])
        # enabledMenues for Family
        self.addEnabledMenuItems('editFamily','family_new1', self.dicUserKeys['articles_new'])
        self.addEnabledMenuItems('editFamily','family_clear1', self.dicUserKeys['articles_delete'])
        #self.addEnabledMenuItems('editFamily','family_print1', self.dicUserKeys['articles_print'])
        self.addEnabledMenuItems('editFamily','family_edit1',self.dicUserKeys['articles_edit'])
        # enabledMenues for Genus
        self.addEnabledMenuItems('editGenus','genus_new1', self.dicUserKeys['articles_new'])
        self.addEnabledMenuItems('editGenus','genus_clear1', self.dicUserKeys['articles_delete'])
        #self.addEnabledMenuItems('editGenus','genus_print1', self.dicUserKeys['articles_print'])
        self.addEnabledMenuItems('editGenus','genus_edit1',self.dicUserKeys['articles_edit'])
        # enabledMenues for Typus
        self.addEnabledMenuItems('editBotany','new1', self.dicUserKeys['articles_new'])
        self.addEnabledMenuItems('editBotany','clear1', self.dicUserKeys['articles_delete'])
        self.addEnabledMenuItems('editBotany','print1', self.dicUserKeys['articles_print'])
        self.addEnabledMenuItems('editBotany','edit1',self.dicUserKeys['articles_edit'])
      


        # tabs from notebook
        self.tabDivisio = 0
        self.tabClass = 1
        self.tabOrdo = 2
        self.tabFamily = 3
        self.tabGenus = 4
        self.tabBotany = 5
        

        # start
        
        self.tabChanged()

              
       
    
        self.win1.add_accel_group(self.accel_group)
    #Menu File
              
    def on_quit1_activate(self, event):
        print "exit botany v2"
        self.closeWindow()
    # Menu Divisio
    def on_divisio_save1_activate(self, event):
        self.singleBotanyDivisio.save()
        self.setEntriesEditable(self.EntriesBotanyDivisio, False)
        self.tabChanged()
        
    def on_divisio_new1_activate(self, event):
        self.singleBotanyDivisio.newRecord()
        self.setEntriesEditable(self.EntriesBotanyDivisio, True)

    def on_divisio_edit1_activate(self, event):
        self.setEntriesEditable(self.EntriesBotanyDivisio, True)
        
        
    def on_divisio_clear1_activate(self, event):
        self.singleBotanyDivisio.deleteRecord()
                
    # Menu Class
    def on_class_save1_activate(self, event):
        self.singleBotanyClass.divisioId = self.singleBotanyDivisio.ID
        self.singleBotanyClass.save()
        self.setEntriesEditable(self.EntriesBotanyClass, False)
        self.tabChanged()
        
    def on_class_new1_activate(self, event):
        self.singleBotanyClass.newRecord()
        self.setEntriesEditable(self.EntriesBotanyClass, True)

    def on_class_edit1_activate(self, event):
        self.setEntriesEditable(self.EntriesBotanyClass, True)
        
        
    def on_class_clear1_activate(self, event):
        self.singleBotanyClass.deleteRecord()


    # Menu Ordo
    def on_ordo_save1_activate(self, event):
        self.singleBotanyOrdo.botclassId = self.singleBotanyClass.ID
        self.singleBotanyOrdo.save()
        self.setEntriesEditable(self.EntriesBotanyOrdo, False)
        self.tabChanged()
        
    def on_ordo_new1_activate(self, event):
        self.singleBotanyOrdo.newRecord()
        self.setEntriesEditable(self.EntriesBotanyOrdo, True)

    def on_ordo_edit1_activate(self, event):
        self.setEntriesEditable(self.EntriesBotanyOrdo, True)
        
        
    def on_ordo_clear1_activate(self, event):
        self.singleBotanyOrdo.deleteRecord()
        
        
        
    # Menu Family
    def on_family_save1_activate(self, event):
        self.singleBotanyFamily.ordoId = self.singleBotanyOrdo.ID
        self.singleBotanyFamily.save()
        self.setEntriesEditable(self.EntriesBotanyFamily, False)
        self.tabChanged()
        
    def on_family_new1_activate(self, event):
        self.singleBotanyFamily.newRecord()
        self.setEntriesEditable(self.EntriesBotanyFamily, True)

    def on_family_edit1_activate(self, event):
        self.setEntriesEditable(self.EntriesBotanyFamily, True)
        
        
    def on_family_clear1_activate(self, event):
        self.singleBotanyFamily.deleteRecord()        
        

    # Menu Genus
    def on_genus_save1_activate(self, event):
        self.singleBotanyGenus.familyId = self.singleBotanyFamily.ID
        self.singleBotanyGenus.save()
        self.setEntriesEditable(self.EntriesBotanyGenus, False)
        self.tabChanged()
        
    def on_genus_new1_activate(self, event):
        self.singleBotanyGenus.newRecord()
        self.setEntriesEditable(self.EntriesBotanyGenus, True)

    def on_genus_edit1_activate(self, event):
        self.setEntriesEditable(self.EntriesBotanyGenus, True)
        
        
    def on_genus_clear1_activate(self, event):
        self.singleBotanyGenus.deleteRecord()
        
        
    #Menu typus
  
    def on_save1_activate(self, event):
        print "save articles v2"
        self.singleBotany.genusId = self.singleBotanyGenus.ID
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


##    def on_eFindNumber_editing_done(self, event):
##        print 'Find Number'
##        self.searchArticle()

    def on_eFindNumber_key_press_event(self, entry,event):
        if self.checkKey(event,'NONE','Return'):
            self.searchBotany()
            
##    def on_eFindDesignation_editing_done(self, event):
##        print 'Find Designation'
##        self.searchArticle()

    def on_eFindDesignation_key_press_event(self, entry,event):
        if self.checkKey(event,'NONE','Return'):
            self.searchBotany()
            
            
    def on_bBotanyDMS_clicked(self, event):
        print 'dms clicked'
        
        if self.singleBotany.ID > 0:
            print 'ModulNumber', self.ModulNumber
            Dms = cuon.DMS.dms.dmswindow(self.allTables, self.ModulNumber, {'1':self.singleBotany.ID})
   
    def on_chooseBotany_activate(self, event):
        # choose Botany from other Modul
        print '############### Botany choose ID ###################'
        self.setChooseValue(self.singleBotany.ID)
        self.closeWindow()      
        
      
    def on_tree1_row_activated(self, event, data1, data2):
        print 'DoubleClick tree1'
        print event
        print data1
        print data2
        if self.tabOption == self.tabBotany:
            self.activateClick('chooseBotany', event)
    

    def searchBotany(self):
        self.out( 'Searching ....', self.ERROR)
        sName = self.getWidget('eFindName').get_text()
        sLocalName = self.getWidget('eFindLocalName').get_text()
        sDescription = self.getWidget('eFindDescription').get_text()
        #self.out('Name and City = ' + sNumber + ', ' + sDesignation, self.ERROR)
        
        #self.singleBotany.sWhere = 'where number ~* \'.*' + sNumber + '.*\' and designation ~* \'.*' + sDesignation + '.*\''
        if self.tabOption == self.tabBotany:
            sSearchName = 'botany_name'
        else:
            sSearchName = 'name'
            
                
        liSearch = [sSearchName,sName, 'local_name', sLocalName,'description',sDescription]
        
        self.sWhereSearch = self.getWhere(liSearch)
        self.out(self.singleBotany.sWhere, self.ERROR)
        self.refreshTree()

    def refreshTree(self):
        self.singleBotanyDivisio.disconnectTree()
        self.singleBotanyClass.disconnectTree()
        self.singleBotanyOrdo.disconnectTree()
        self.singleBotanyFamily.disconnectTree()
        self.singleBotanyGenus.disconnectTree()
        self.singleBotany.disconnectTree()


        if self.tabOption == self.tabDivisio:
            #self.singleBotanyDivisio.sWhere  ='where task_id = ' + `int(self.singleProjectTasks.ID)`
            if self.sWhereSearch and self.sSearchTable == self.singleBotanyDivisio.sNameOfTable:
               self.singleBotanyDivisio.sWhere  = self.sWhereSearch 
            self.singleBotanyDivisio.connectTree()
            self.singleBotanyDivisio.refreshTree()
        elif self.tabOption == self.tabClass:
            if self.sWhereSearch and self.sSearchTable == self.singleBotanyClass.sNameOfTable:
               self.singleBotanyClass.sWhere  = self.sWhereSearch             
            else:
                self.singleBotanyClass.sWhere  ='where divisio_id = ' + `int(self.singleBotanyDivisio.ID)`
            self.singleBotanyClass.connectTree()
            self.singleBotanyClass.refreshTree()
        elif self.tabOption == self.tabOrdo:
            if self.sWhereSearch and self.sSearchTable == self.singleBotanyOrdo.sNameOfTable:
               self.singleBotanyOrdo.sWhere  = self.sWhereSearch             
            else:
                self.singleBotanyOrdo.sWhere  ='where class_id = ' + `int(self.singleBotanyClass.ID)`
            self.singleBotanyOrdo.connectTree()
            self.singleBotanyOrdo.refreshTree()
        elif self.tabOption == self.tabFamily:
            if self.sWhereSearch and self.sSearchTable == self.singleBotanyFamily.sNameOfTable:
               self.singleBotanyFamily.sWhere  = self.sWhereSearch             
            else:
                self.singleBotanyFamily.sWhere  ='where ordo_id = ' + `int(self.singleBotanyOrdo.ID)`
            self.singleBotanyFamily.connectTree()
            self.singleBotanyFamily.refreshTree()
        elif self.tabOption == self.tabGenus:
            if self.sWhereSearch and self.sSearchTable == self.singleBotanyGenus.sNameOfTable:
               self.singleBotanyGenus.sWhere  = self.sWhereSearch             
            else:
                self.singleBotanyGenus.sWhere  ='where family_id = ' + `int(self.singleBotanyFamily.ID)`
            self.singleBotanyGenus.connectTree()
            self.singleBotanyGenus.refreshTree()
        elif self.tabOption == self.tabBotany:
            if self.sWhereSearch and self.sSearchTable == self.singleBotany.sNameOfTable:
               self.singleBotany.sWhere  = self.sWhereSearch             
            else:
                self.singleBotany.sWhere  ='where genus_id = ' + `int(self.singleBotanyGenus.ID)`
            self.singleBotany.connectTree()
            self.singleBotany.refreshTree()

         
    def tabChanged(self):
        print 'tab changed to :'  + str(self.tabOption)
        self.setTreeVisible(True)
        if self.tabOption == self.tabDivisio :
            self.disableMenuItem('tabs')
            self.enableMenuItem('divisio')
            self.actualEntries = self.singleBotanyDivisio.getEntries()
            self.editAction = 'editDivisio'
            self.setStatusbarText([''])
            self.setTreeVisible(True)
            self.sSearchTable = self.singleBotanyDivisio.sNameOfTable
        elif self.tabOption == self.tabClass :
            self.disableMenuItem('tabs')
            self.enableMenuItem('class')
            self.actualEntries = self.singleBotanyClass.getEntries()
            self.editAction = 'editClass'
            self.setStatusbarText([''])
            self.setTreeVisible(True)
            self.sSearchTable = self.singleBotanyClass.sNameOfTable

        elif self.tabOption == self.tabOrdo :
            self.disableMenuItem('tabs')
            self.enableMenuItem('ordo')
            self.actualEntries = self.singleBotanyOrdo.getEntries()
            self.editAction = 'editOrdo'
            self.setStatusbarText([''])
            self.setTreeVisible(True)
            self.sSearchTable = self.singleBotanyOrdo.sNameOfTable
            
        elif self.tabOption == self.tabFamily :
            self.disableMenuItem('tabs')
            self.enableMenuItem('family')
            self.actualEntries = self.singleBotanyFamily.getEntries()
            self.editAction = 'editFamily'
            self.setStatusbarText([''])
            self.setTreeVisible(True)
            self.sSearchTable = self.singleBotanyFamily.sNameOfTable
            
        elif self.tabOption == self.tabGenus :
            self.disableMenuItem('tabs')
            self.enableMenuItem('genus')
            self.actualEntries = self.singleBotanyGenus.getEntries()
            self.editAction = 'editGenus'
            self.setStatusbarText([''])
            self.setTreeVisible(True)
            self.sSearchTable = self.singleBotanyGenus.sNameOfTable
            
        elif self.tabOption == self.tabBotany:
        
            self.disableMenuItem('tabs')
            self.enableMenuItem('botany')
            self.actualEntries = self.singleBotany.getEntries()
            self.editAction = 'editBotany'
            self.setStatusbarText([''])
            self.setTreeVisible(True)
            self.sSearchTable = self.singleBotany.sNameOfTable
            
            
            
        # refresh the Tree
        self.refreshTree()
        self.enableMenuItem(self.editAction)
        self.editEntries = False
