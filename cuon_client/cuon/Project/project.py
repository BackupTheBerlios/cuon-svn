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
import SingleProjectStaffResources
import SingleProjectMaterialResources
import cuon.Staff.staff
import cuon.Staff.SingleStaff
import cuon.Addresses.addresses
import cuon.Addresses.SingleAddress

import cuon.Articles.articles
import cuon.Articles.SingleArticle




class projectwindow(chooseWindows):

    
    def __init__(self, allTables):

        chooseWindows.__init__(self)
        self.oDocumentTools = cuon.DMS.documentTools.documentTools()
        
        self.singleProject = SingleProject.SingleProject(allTables)
        self.singleProjectPhases = SingleProjectPhases.SingleProjectPhases(allTables)
        self.singleProjectTasks = SingleProjectTasks.SingleProjectTasks(allTables)
        self.singleProjectTaskStaff = SingleProjectStaffResources.SingleProjectStaffResources(allTables)
        self.singleProjectTaskMaterial = SingleProjectMaterialResources.SingleProjectMaterialResources(allTables)

        self.singleStaff = cuon.Staff.SingleStaff.SingleStaff(allTables)
        self.singleAddress = cuon.Addresses.SingleAddress.SingleAddress(allTables)
        self.singleArticles = cuon.Articles.SingleArticle.SingleArticle(allTables)
        
        self.allTables = allTables
       
        
        # self.singleProject.loadTable()

        # self.xml = gtk.glade.XML()
    
        self.loadGlade('project.xml')
        self.win1 = self.getWidget('ProjectMainwindow')
        self.setStatusBar()


        self.EntriesProject = 'project.xml'
        self.EntriesPhase = 'project_phases.xml'
        self.EntriesTask = 'project_tasks.xml'
        self.EntriesTaskStaff = 'project_staff_resources.xml'
        self.EntriesTaskMaterial = 'project_material_resources.xml'
        
        
        self.loadEntries(self.EntriesProject)
        self.loadEntries(self.EntriesPhase)
        self.loadEntries(self.EntriesTask)
        self.loadEntries(self.EntriesTaskStaff)
        self.loadEntries(self.EntriesTaskMaterial)
        
        self.singleProject.setEntries(self.getDataEntries(self.EntriesProject) )
        self.singleProject.setGladeXml(self.xml)
        self.singleProject.setTreeFields( ['name', 'designation'] )
        self.singleProject.setStore( gtk.ListStore(gobject.TYPE_STRING,  gobject.TYPE_STRING,   gobject.TYPE_UINT) ) 
        self.singleProject.setTreeOrder('name')
        self.singleProject.setListHeader([_('Name'), _('Designation')])
        self.singleProject.setTree(self.xml.get_widget('tree1') )

  
        self.singleProjectPhases.setEntries(self.getDataEntries(self.EntriesPhase) )
        self.singleProjectPhases.setGladeXml(self.xml)
        self.singleProjectPhases.setTreeFields( ['name', 'designation'] )
        self.singleProjectPhases.setStore( gtk.ListStore(gobject.TYPE_STRING,  gobject.TYPE_STRING,   gobject.TYPE_UINT) ) 
        self.singleProjectPhases.setTreeOrder('name')
        self.singleProjectPhases.setListHeader([_('Name'), _('Designation')])
        self.singleProjectPhases.setTree(self.xml.get_widget('tree1') )

        self.singleProjectTasks.setEntries(self.getDataEntries(self.EntriesTask) )
        self.singleProjectTasks.setGladeXml(self.xml)
        self.singleProjectTasks.setTreeFields( ['name', 'designation'] )
        self.singleProjectTasks.setStore( gtk.ListStore(gobject.TYPE_STRING,  gobject.TYPE_STRING,   gobject.TYPE_UINT) ) 
        self.singleProjectTasks.setTreeOrder('name')
        self.singleProjectTasks.setListHeader([_('Name'), _('Designation')])
        self.singleProjectTasks.setTree(self.xml.get_widget('tree1') )

        self.singleProjectTaskStaff.setEntries(self.getDataEntries(self.EntriesTaskStaff) )
        self.singleProjectTaskStaff.setGladeXml(self.xml)
        self.singleProjectTaskStaff.setTree(self.xml.get_widget('tree1') )

        self.singleProjectTaskMaterial.setEntries(self.getDataEntries(self.EntriesTaskMaterial) )
        self.singleProjectTaskMaterial.setGladeXml(self.xml)
        self.singleProjectTaskMaterial.setTree(self.xml.get_widget('tree1') )



        # Menu-items
        self.initMenuItems()

        # Close Menus for Tab
        self.addEnabledMenuItems('tabs','mi_project1')
        self.addEnabledMenuItems('tabs','mi_phase1')
        self.addEnabledMenuItems('tabs','mi_task1')
        self.addEnabledMenuItems('tabs','mi_staff_resources1')
        self.addEnabledMenuItems('tabs','mi_material_resources1')

               
        # seperate Menus
        self.addEnabledMenuItems('project','mi_project1')
        self.addEnabledMenuItems('phase','mi_phase1')
        self.addEnabledMenuItems('tasks','mi_task1')
        self.addEnabledMenuItems('staff_resources','mi_staff_resources1')
        self.addEnabledMenuItems('material_resources','mi_material_resources1')
        
        # enabledMenues for Project
        self.addEnabledMenuItems('editProject','mi_new1' , self.dicUserKeys['project_new'])
        self.addEnabledMenuItems('editProject','mi_clear1', self.dicUserKeys['project_delete'])
#        self.addEnabledMenuItems('editProject','mi_print1', self.dicUserKeys['project_print'])
        self.addEnabledMenuItems('editProject','mi_edit1', self.dicUserKeys['project_edit'])
        
        
        self.addEnabledMenuItems('editPhase','phasenew1' , self.dicUserKeys['project_new'])
        self.addEnabledMenuItems('editPhase','phasedelete1', self.dicUserKeys['project_delete'])
        self.addEnabledMenuItems('editPhase','phaseedit1', self.dicUserKeys['project_edit'])

        self.addEnabledMenuItems('editTasks','task_new' , self.dicUserKeys['project_new'])
        self.addEnabledMenuItems('editTasks','task_delete1', self.dicUserKeys['project_delete'])
        self.addEnabledMenuItems('editTasks','task_edit', self.dicUserKeys['project_edit'])

        self.addEnabledMenuItems('editStaffRes','task_new' , self.dicUserKeys['project_new'])
        self.addEnabledMenuItems('editStaffRes','task_delete1', self.dicUserKeys['project_delete'])
        self.addEnabledMenuItems('editStaffRes','task_edit', self.dicUserKeys['project_edit'])
        
        self.addEnabledMenuItems('editMaterialRes','task_new' , self.dicUserKeys['project_new'])
        self.addEnabledMenuItems('editMaterialRes','task_delete1', self.dicUserKeys['project_delete'])
        self.addEnabledMenuItems('editMaterialRes','task_edit', self.dicUserKeys['project_edit'])

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
    
        


    #Menu Project
  
    def on_save1_activate(self, event):
        self.out( "save project v2")
        self.singleProject.save()
        self.setEntriesEditable(self.EntriesProject, False)
        self.tabChanged()
        
    def on_new1_activate(self, event):
        self.out( "new project v2")
        self.singleProject.newRecord()
        self.setEntriesEditable(self.EntriesProject, True)

    def on_edit1_activate(self, event):
        self.out( "edit project v2")
        self.setEntriesEditable(self.EntriesProject, True)
        
    def on_delete1_activate(self, event):
        self.out( "delete project v2")
        self.singleProject.deleteRecord()


    #Menu Phases
  
    def on_phasesave1_activate(self, event):
        self.out( "save projectphases v2")
        self.singleProjectPhases.projectId = self.singleProject.ID
        self.singleProjectPhases.save()
        self.setEntriesEditable(self.EntriesPhase, False)
        self.tabChanged()
        
    def on_phasenew1_activate(self, event):
        self.out( "new projectphases v2")
        self.singleProjectPhases.newRecord()
        self.setEntriesEditable(self.EntriesPhase, True)

    def on_phaseedit1_activate(self, event):
        self.out( "edit projectphases v2")
        self.setEntriesEditable(self.EntriesPhase, True)
        
        
    def on_phasedelete1_activate(self, event):
        self.out( "delete projectphases v2")
        self.singleProjectPhases.deleteRecord()
        
#Menu Tasks
  
    def on_task_save1_activate(self, event):
        self.out( "save projectphases v2")
        self.singleProjectTasks.phaseId = self.singleProjectPhases.ID
        self.singleProjectTasks.save()
        self.setEntriesEditable(self.EntriesTask, False)
        self.tabChanged()
        
    def on_tasknew1_activate(self, event):
        self.out( "new projectphases v2")
        self.singleProjectTasks.newRecord()
        self.setEntriesEditable(self.EntriesTask, True)

    def on_taskedit1_activate(self, event):
        self.out( "edit projectphases v2")
        self.setEntriesEditable(self.EntriesTask, True)
        
        
    def on_task_delete1_activate(self, event):
        self.out( "delete projectphases v2")
        self.singleProjectTasks.deleteRecord()
                
        
#Menu Staff resources
  
    def on_staff_resources_save1_activate(self, event):
        self.out( "save projectphases v2")
        print 'staff2'
        self.singleProjectTaskStaff.taskId = self.singleProjectTasks.ID
        print 'task4 = ', self.singleProjectTasks.ID

        self.singleProjectTaskStaff.save()
        print 'task5 = ', self.singleProjectTasks.ID
        
        self.setEntriesEditable(self.EntriesTaskStaff, False)
        print 'task6 = ', self.singleProjectTasks.ID
        
        self.tabChanged()
        print 'task7 = ', self.singleProjectTasks.ID
        
    def on_staff_resources_new1_activate(self, event):
        self.out( "new projectphases v2")
        print 'staff1'
        print 'task1 = ', self.singleProjectTasks.ID
        self.singleProjectTaskStaff.newRecord()
        print 'task2 = ', self.singleProjectTasks.ID
        self.setEntriesEditable(self.EntriesTaskStaff, True)
        print 'task3 = ', self.singleProjectTasks.ID

    def on_staff_resources_edit1_activate(self, event):
        self.out( "edit projectphases v2")
        self.setEntriesEditable(self.EntriesTaskStaff, True)
        
        
    def on_staff_resources_delete1_activate(self, event):
        self.out( "delete projectphases v2")
        self.singleProjectTaskStaff.deleteRecord()
                
        
 #Menu Material resources
  
    def on_material_resources_save1_activate(self, event):
        self.out( "save projectphases v2")
        self.singleProjectTaskMaterial.taskId = self.singleProjectTasks.ID
        self.singleProjectTaskMaterial.save()
        self.setEntriesEditable(self.EntriesTaskMaterial, False)
        self.tabChanged()
        
    def on_material_resources_new1_activate(self, event):
        self.out( "new projectphases v2")
        self.singleProjectTaskMaterial.newRecord()
        self.setEntriesEditable(self.EntriesTaskMaterial, True)

    def on_material_resources_edit1_activate(self, event):
        self.out( "edit projectphases v2")
        self.setEntriesEditable(self.EntriesTaskMaterial, True)
        
        
    def on_material_resources_delete1_activate(self, event):
        self.out( "delete projectphases v2")
        self.singleProjectTaskMaterial.deleteRecord()
                
               
    def on_bShowDMS_clicked(self, event):
        print 'dms clicked'
        if self.singleProject.ID > 0:
            print 'ModulNumber', self.ModulNumber
            Dms = cuon.DMS.dms.dmswindow(self.allTables, self.ModulNumber, {'1':self.singleProject.ID})
        
    

        
##    def on_chooseAddress_activate(self, event):
##        # choose Address from other Modul
##        if self.tabOption == self.tabProject:
##            print '############### Address choose ID ###################'
##            self.setChooseValue(self.singleProject.ID)
##            self.closeWindow()
##        elif self.tabOption == self.tabStaffResources:
##            print '############### Address choose ID ###################'
##            self.setChooseValue(self.singlePartner.ID)
##            self.closeWindow()
##
##        else:
##            print '############### No ID found,  choose ID -1 ###################'
##            self.setChooseValue('-1')
##            self.closeWindow()
## 
              

        
    # search button
    def on_bSearch_clicked(self, event):
        self.out( 'Searching ....', self.ERROR)
        sName = self.getWidget('eFindName').get_text()
        sCity = self.getWidget('eFindCity').get_text()
        self.out('Name and City = ' + sName + ', ' + sCity, self.ERROR)
        self.singleProject.sWhere = 'where lastname ~* \'.*' + sName + '.*\' and city ~* \'.*' + sCity + '.*\''
        self.out(self.singleProject.sWhere, self.ERROR)
        self.refreshTree()
    # events and buttons
    
    # Project
    def on_calendar1_day_selected_double_click(self, event):
        print event
        print event.get_date()
        self.setDateToEntry(event,'eProjectStartAt')
        
    def on_calendar2_day_selected_double_click(self, event):
        print event
        print event.get_date()
        self.setDateToEntry(event,'eProjectEndsAt')
        
    def on_eProjectStartAt_changed(self, event):
        print event 
        self.setDateToCalendar(event.get_text(),'calendar1')
            
    def on_eProjectEndsAt_changed(self, event):
        print event 
        self.setDateToCalendar(event.get_text(),'calendar2')
        
    #choose button
    def on_bChoose_clicked(self, event):
        adr = cuon.Addresses.addresses.addresswindow(self.allTables)
        adr.setChooseEntry(_('chooseAddress'), self.getWidget( 'eAddressNumber'))
        
    # signals from entry eAddressNumber
    
    def on_eAddressNumber_changed(self, event):
        print 'eAdressNumber changed'
        eAdrField = self.getWidget('tvOrderer')
        liAdr = self.singleAddress.getAddress(self.getWidget( 'eAddressNumber').get_text())
        self.setTextbuffer(eAdrField,liAdr)
    # Phase

    def on_PhaseCalendar1_day_selected_double_click(self, event):
        print event
        print event.get_date()
        self.setDateToEntry(event,'ePhaseStartAt')
        
    def on_PhaseCalendar2_day_selected_double_click(self, event):
        print event
        print event.get_date()
        self.setDateToEntry(event,'ePhaseEndsAt')
        
    def on_ePhaseStartAt_changed(self, event):
        print event 
        self.setDateToCalendar(event.get_text(),'PhaseCalendar1')
            
    def on_ePhaseEndsAt_changed(self, event):
        print event 
        self.setDateToCalendar(event.get_text(),'PhaseCalendar2')
        
        
    
    # Tasks 
    
    def on_TaskCalendar1_day_selected_double_click(self, event):
        print event
        print event.get_date()
        self.setDateToEntry(event,'eTaskStartAt')
        
    def on_TaskCalendar2_day_selected_double_click(self, event):
        print event
        print event.get_date()
        self.setDateToEntry(event,'eTaskEndsAt')
        
    def on_eTaskStartAt_changed(self, event):
        print event 
        self.setDateToCalendar(event.get_text(),'TaskCalendar1')
            
    def on_eTaskEndsAt_changed(self, event):
        print event 
        self.setDateToCalendar(event.get_text(),'TaskCalendar2')
                
        
    # Staff-Resources 
    
    def on_staffCalendar1_day_selected_double_click(self, event):
        print event
        print event.get_date()
        self.setDateToEntry(event,'eSRPlanedDate')
        
    def on_staffCalendar2_day_selected_double_click(self, event):
        print event
        print event.get_date()
        self.setDateToEntry(event,'eSRRealDate')
        
    def on_eSRPlanedDate_changed(self, event):
        print event 
        self.setDateToCalendar(event.get_text(),'staffCalendar1')
            
    def on_eSRRealDate_changed(self, event):
        print event 
        self.setDateToCalendar(event.get_text(),'staffCalendar2')
                
                
    #choose Staff button
    def on_bChooseStaff_clicked(self, event):
        adr = cuon.Staff.staff.staffwindow(self.allTables)
        adr.setChooseEntry(_('chooseStaff'), self.getWidget( 'eSRStaffNumber'))
        
    # signals from entry eSRStaffNumber
    
    def on_eSRStaffNumber_changed(self, event):
        print 'eStaf changed'
        eAdrField = self.getWidget('tvStaff')
        liAdr = self.singleStaff.getAddress(self.getWidget( 'eSRStaffNumber').get_text())
        self.setTextbuffer(eAdrField,liAdr)
    
    
    # material resources
    #choose button
    def on_bChooseArticle_clicked(self, event):
        art = cuon.Articles.articles.articleswindow(self.allTables)
        art.setChooseEntry(_('chooseArticle'), self.getWidget( 'eMRArticleNumber'))
        
    # signals from entry eAddressNumber
    
    def on_eMRArticleNumber_changed(self, event):
        print 'eMRArticleNumber changed'
        eArticleDes  = self.getWidget('eArticleDesignation')
        sArticleDes  = self.singleArticle.getArticleDesignation(self.getWidget( 'eMRArticleNumber').get_text())
        eArticleDes.set_text(sArticleDes)
    def refreshTree(self):
        self.singleProject.disconnectTree()
        self.singleProjectPhases.disconnectTree()
        self.singleProjectTasks.disconnectTree()
        self.singleProjectTaskStaff.disconnectTree()
        self.singleProjectTaskMaterial.disconnectTree()


        if self.tabOption == self.tabProject:
            self.singleProject.connectTree()
            self.singleProject.refreshTree()
            
        elif self.tabOption == self.tabPhases:
            self.singleProjectPhases.sWhere  ='where project_id = ' + `int(self.singleProject.ID)`
            self.singleProjectPhases.connectTree()
            self.singleProjectPhases.refreshTree()
                
        elif self.tabOption == self.tabTasks:
            self.singleProjectTasks.sWhere  ='where phase_id = ' + `int(self.singleProjectPhases.ID)`
            self.singleProjectTasks.connectTree()
            self.singleProjectTasks.refreshTree()
            
        elif self.tabOption == self.tabStaffResources:
            self.singleProjectTaskStaff.sWhere  ='where task_id = ' + `int(self.singleProjectTasks.ID)`
            self.singleProjectTaskStaff.connectTree()
            self.singleProjectTaskStaff.refreshTree()
            
        elif self.tabOption == self.tabMaterialResources:
            self.singleProjectTaskMaterial.sWhere  ='where task_id = ' + `int(self.singleProjectTasks.ID)`
            self.singleProjectTaskMaterial.connectTree()
            self.singleProjectTaskMaterial.refreshTree()
            
     


         
    def tabChanged(self):
        self.out( 'tab changed to :'  + str(self.tabOption))
        print self.tabProject
        
        if self.tabOption == self.tabProject :
            #Project
            self.disableMenuItem('tabs')
            self.enableMenuItem('project')

            self.actualEntries = self.singleProject.getEntries()
            self.editAction = 'editProject'
            self.setStatusbarText([''])
          
            self.setTreeVisible(True)

        elif self.tabOption == self.tabPhases:
            self.disableMenuItem('tabs')
            self.enableMenuItem('phase')
           
            self.editAction = 'editPhase'
            self.setTreeVisible(True)
            self.setStatusbarText([self.singleProject.sStatus])


        elif self.tabOption == self.tabTasks:

            self.disableMenuItem('tabs')
            self.enableMenuItem('tasks')
            self.editAction = 'editTask'
            self.setTreeVisible(True)
            self.setStatusbarText([self.singleProject.sStatus])




        elif self.tabOption == self.tabStaffResources:
            #Partner
            self.disableMenuItem('tabs')
            self.enableMenuItem('staff_resources')
            
            self.editAction = 'editStaffRes'
            self.setTreeVisible(True)
            self.setStatusbarText([self.singleProject.sStatus])

            
        elif self.tabOption == self.tabMaterialResources:
            print 'tabchanged material Resources'
            
            self.disableMenuItem('tabs')
            self.enableMenuItem('material_resources')
            
            self.editAction = 'editMaterialRes'
            self.setTreeVisible(True)
            self.setStatusbarText([self.singleProjectTaskMaterial.sStatus])

        # refresh the Tree
        print "refresh Tree 1"
        self.refreshTree()
        self.enableMenuItem(self.editAction)
        self.editEntries = False
        
