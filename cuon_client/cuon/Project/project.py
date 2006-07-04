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
import os
import os.path
from types import *
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import gobject
from gtk import TRUE, FALSE
import string


import logging
from cuon.Windows.chooseWindows  import chooseWindows
import cPickle
#import cuon.OpenOffice.letter
# localisation
import locale, gettext
locale.setlocale (locale.LC_NUMERIC, '')
import threading

import cuon.DMS.documentTools
import cuon.DMS.dms
import SingleProject
import SingleProjectPhases
import SingleProjectTasks
import SingleProjectResourses





class projectwindow(chooseWindows):

    
    def __init__(self, allTables):

        chooseWindows.__init__(self)
        self.oDocumentTools = cuon.DMS.documentTools.documentTools()
        
        self.singleProject = SingleProject.SingleProject(allTables)
        
        self.allTables = allTables
       
        
        # self.singleProject.loadTable()

        # self.xml = gtk.glade.XML()
    
        self.loadGlade('project.xml')
        self.win1 = self.getWidget('ProjectMainwindow')
        self.setStatusBar()


        self.EntriesProject = 'project.xml'
        
        self.loadEntries(self.EntriesProject)
        
        self.singleProject.setEntries(self.getDataEntries(self.EntriesProject) )
        self.singleProject.setGladeXml(self.xml)
        self.singleProject.setTreeFields( ['name', 'designation'] )
        self.singleProject.setStore( gtk.ListStore(gobject.TYPE_STRING,  gobject.TYPE_STRING,   gobject.TYPE_UINT) ) 
        self.singleProject.setTreeOrder('name')
        self.singleProject.setListHeader([_('Name'), _('Designation')])
        self.singleProject.setTree(self.xml.get_widget('tree1') )

  
      


        # Menu-items
        self.initMenuItems()

        # Close Menus for Tab
        self.addEnabledMenuItems('tabs','mi_address1')
        self.addEnabledMenuItems('tabs','mi_bank1')
        self.addEnabledMenuItems('tabs','mi_misc1')
        self.addEnabledMenuItems('tabs','mi_partner1')
        self.addEnabledMenuItems('tabs','mi_schedul1')

               
        # seperate Menus
        self.addEnabledMenuItems('address','mi_address1')
        self.addEnabledMenuItems('partner','mi_partner1')
        self.addEnabledMenuItems('schedul','mi_schedul1')
        self.addEnabledMenuItems('bank','mi_bank1')
        self.addEnabledMenuItems('misc','mi_misc1')

      
         
        

        # tabs from notebook
        self.tabProject = 0
        self.tabPhases = 1
        self.tabTasks = 2
        self.tabStaffResources = 3
        self.tabMaterialResources = 4
        
        

        self.tabChanged()
        

    #Menu File
              
    def on_quit1_activate(self, event):
        self.out( "exit Project v2")
        self.closeWindow() 
    
        


    #Menu Address
  
    def on_save1_activate(self, event):
        self.out( "save addresses v2")
        self.singleProject.save()
        self.setEntriesEditable(self.EntriesProject, FALSE)
        self.tabChanged()
        
    def on_new1_activate(self, event):
        self.out( "new addresses v2")
        self.singleProject.newRecord()
        self.setEntriesEditable(self.EntriesProject, TRUE)

    def on_edit1_activate(self, event):
        self.out( "edit addresses v2")
        self.setEntriesEditable(self.EntriesProject, TRUE)
    def on_print1_activate(self, event):
        self.out( "print addresses v2")
        p = printAddress.printAddress(self.singleProject.getFirstRecord() )
        
    def on_delete1_activate(self, event):
        self.out( "delete addresses v2")
        self.singleProject.deleteRecord()



    def on_bShowDMS_clicked(self, event):
        print 'dms clicked'
        if self.singleProject.ID > 0:
            print 'ModulNumber', self.ModulNumber
            Dms = cuon.DMS.dms.dmswindow(self.allTables, self.ModulNumber, {'1':self.singleProject.ID})
        
    

        
    def on_chooseAddress_activate(self, event):
        # choose Address from other Modul
        if self.tabOption == self.tabProject:
            print '############### Address choose ID ###################'
            self.setChooseValue(self.singleProject.ID)
            self.closeWindow()
        elif self.tabOption == self.tabStaffResources:
            print '############### Address choose ID ###################'
            self.setChooseValue(self.singlePartner.ID)
            self.closeWindow()

        else:
            print '############### No ID found,  choose ID -1 ###################'
            self.setChooseValue('-1')
            self.closeWindow()
 
              

        
    # search button
    def on_bSearch_clicked(self, event):
        self.out( 'Searching ....', self.ERROR)
        sName = self.getWidget('eFindName').get_text()
        sCity = self.getWidget('eFindCity').get_text()
        self.out('Name and City = ' + sName + ', ' + sCity, self.ERROR)
        self.singleProject.sWhere = 'where lastname ~* \'.*' + sName + '.*\' and city ~* \'.*' + sCity + '.*\''
        self.out(self.singleProject.sWhere, self.ERROR)
        self.refreshTree()

    def refreshTree(self):
        self.singleProject.disconnectTree()
        self.singlePartner.disconnectTree()
        
        if self.tabOption == self.tabProject:
            self.singleProject.connectTree()
            self.singleProject.refreshTree()
        elif self.tabOption == self.tabTasks:
            self.singleMisc.sWhere  ='where address_id = ' + `int(self.singleProject.ID)`
            self.singleMisc.fillEntries(self.singleMisc.findSingleId())

        elif self.tabOption == self.tabStaffResources:
            self.singlePartner.sWhere  ='where addressid = ' + `int(self.singleProject.ID)`
            self.singlePartner.connectTree()
            self.singlePartner.refreshTree()
        elif self.tabOption == self.tabMaterialResources:
            self.singleSchedul.sWhere  ='where partnerid = ' + `int(self.singlePartner.ID)`
            self.singleSchedul.connectTree()
            self.singleSchedul.refreshTree()
            
     


         
    def tabChanged(self):
        self.out( 'tab changed to :'  + str(self.tabOption))
        
        if self.tabOption == self.tabProject:
            #Address
            self.disableMenuItem('tabs')
            self.enableMenuItem('address')

            self.actualEntries = self.singleProject.getEntries()
            self.editAction = 'editAddress'
            self.setStatusbarText([''])
          
            self.setTreeVisible(TRUE)
            

            self.out( 'Seite 0')


        elif self.tabOption == self.tabPhases:
            self.out( 'Seite 2')
            self.disableMenuItem('tabs')
            self.enableMenuItem('bank')
           
            self.editAction = 'editBank'
            self.setTreeVisible(FALSE)
            self.setStatusbarText([self.singleProject.sStatus])


        elif self.tabOption == self.tabTasks:
            self.out( 'Seite 3')

            self.disableMenuItem('tabs')
            self.enableMenuItem('misc')
            self.editAction = 'editMisc'
            self.setTreeVisible(FALSE)
            self.setStatusbarText([self.singleProject.sStatus])




        elif self.tabOption == self.tabStaffResources:
            #Partner
            self.disableMenuItem('tabs')
            self.enableMenuItem('partner')
            
            self.out( 'Seite 1')
            self.editAction = 'editPartner'
            self.setTreeVisible(TRUE)
            self.setStatusbarText([self.singleProject.sStatus])

            
        elif self.tabOption == self.tabMaterialResources:
            #Scheduling
            self.disableMenuItem('tabs')
            self.enableMenuItem('schedul')
            
            self.out( 'Seite 4')
            self.editAction = 'editSchedul'
            self.setTreeVisible(TRUE)
            self.setStatusbarText([self.singlePartner.sStatus])

        # refresh the Tree
        self.refreshTree()
        self.enableMenuItem(self.editAction)
        self.editEntries = FALSE
        
