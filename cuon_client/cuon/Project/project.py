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
import os
import os.path
from types import *
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import gobject
import string
import commands

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
import SingleProjectProgramming
import cuon.Staff.staff
import cuon.Staff.SingleStaff
import cuon.Addresses.addresses
import cuon.Addresses.SingleAddress

import cuon.Articles.articles
import cuon.Articles.SingleArticle
import cuon.Editor.programmersEditor




class projectwindow(chooseWindows):

    
    def __init__(self, allTables, dicProject = None, newProject = False, project_id = 0):

        chooseWindows.__init__(self)
        self.oDocumentTools = cuon.DMS.documentTools.documentTools()
        self.ModulNumber = self.MN['Project']
        self.singleProject = SingleProject.SingleProject(allTables)
        self.singleProjectPhases = SingleProjectPhases.SingleProjectPhases(allTables)
        self.singleProjectTasks = SingleProjectTasks.SingleProjectTasks(allTables)
        self.singleProjectTaskStaff = SingleProjectStaffResources.SingleProjectStaffResources(allTables)
        self.singleProjectTaskMaterial = SingleProjectMaterialResources.SingleProjectMaterialResources(allTables)
        self.singleProjectProgramming = SingleProjectProgramming.SingleProjectProgramming(allTables)
        self.singleStaff = cuon.Staff.SingleStaff.SingleStaff(allTables)
        self.singleAddress = cuon.Addresses.SingleAddress.SingleAddress(allTables)
        self.singleArticles = cuon.Articles.SingleArticle.SingleArticle(allTables)
        
        self.allTables = allTables
        self.dicProject = dicProject
        
        # self.singleProject.loadTable()

        # self.xml = gtk.glade.XML()
    
        self.loadGlade('project.xml','ProjectMainwindow' )
        #self.win1 = self.getWidget('ProjectMainwindow')
        self.setStatusBar()


        self.EntriesProject = 'project.xml'
        self.EntriesPhase = 'project_phases.xml'
        self.EntriesTask = 'project_tasks.xml'
        self.EntriesProgramming = 'project_programming.xml'
        self.EntriesTaskStaff = 'project_staff_resources.xml'
        self.EntriesTaskMaterial = 'project_material_resources.xml'
        
        
        self.loadEntries(self.EntriesProject)
        self.loadEntries(self.EntriesPhase)
        self.loadEntries(self.EntriesTask)
        self.loadEntries(self.EntriesProgramming)
        self.loadEntries(self.EntriesTaskStaff)
        self.loadEntries(self.EntriesTaskMaterial)
        
        self.singleProject.setEntries(self.getDataEntries(self.EntriesProject) )
        self.singleProject.setGladeXml(self.xml)
        self.singleProject.setTreeFields( ['name', 'designation'] )
        self.singleProject.setStore( gtk.ListStore(gobject.TYPE_STRING,  gobject.TYPE_STRING,   gobject.TYPE_UINT) ) 
        self.singleProject.setTreeOrder('name')
        self.singleProject.setListHeader([_('Name'), _('Designation')])
        self.singleProject.setTree(self.getWidget('tree1') )

  
        self.singleProjectPhases.setEntries(self.getDataEntries(self.EntriesPhase) )
        self.singleProjectPhases.setGladeXml(self.xml)
        self.singleProjectPhases.setTreeFields( ['name', 'designation'] )
        self.singleProjectPhases.setStore( gtk.ListStore(gobject.TYPE_STRING,  gobject.TYPE_STRING,   gobject.TYPE_UINT) ) 
        self.singleProjectPhases.setTreeOrder('name')
        self.singleProjectPhases.setListHeader([_('Name'), _('Designation')])
        self.singleProjectPhases.setTree(self.getWidget('tree1') )

        self.singleProjectTasks.setEntries(self.getDataEntries(self.EntriesTask) )
        self.singleProjectTasks.setGladeXml(self.xml)
        self.singleProjectTasks.setTreeFields( ['name', 'designation'] )
        self.singleProjectTasks.setStore( gtk.ListStore(gobject.TYPE_STRING,  gobject.TYPE_STRING,   gobject.TYPE_UINT) ) 
        self.singleProjectTasks.setTreeOrder('name')
        self.singleProjectTasks.setListHeader([_('Name'), _('Designation')])
        self.singleProjectTasks.setTree(self.getWidget('tree1') )

        self.singleProjectProgramming.setEntries(self.getDataEntries(self.EntriesProgramming) )
        self.singleProjectProgramming.setGladeXml(self.xml)
        self.singleProjectProgramming.setTreeFields( ['name', 'designation'] )
        self.singleProjectProgramming.setStore( gtk.ListStore(gobject.TYPE_STRING,  gobject.TYPE_STRING,   gobject.TYPE_UINT) ) 
        self.singleProjectProgramming.setTreeOrder('name')
        self.singleProjectProgramming.setListHeader([_('Name'), _('Designation')])
        self.singleProjectProgramming.setTree(self.getWidget('tree1') )

        self.singleProjectTaskStaff.setEntries(self.getDataEntries(self.EntriesTaskStaff) )
        self.singleProjectTaskStaff.setGladeXml(self.xml)
        self.singleProjectTaskStaff.setTree(self.getWidget('tree1') )
        self.singleProjectTaskStaff.sWhere = 'where staff.id = staff_id '
        self.singleProjectTaskMaterial.setEntries(self.getDataEntries(self.EntriesTaskMaterial) )
        self.singleProjectTaskMaterial.setGladeXml(self.xml)
        self.singleProjectTaskMaterial.setTree(self.getWidget('tree1') )
        
        self.ProjectID = project_id
        
        # create a new Project from address or somtething else
        if self.dicProject and not newProject and self.ProjectID == 0:
            print self.dicProject
            existProject = self.rpc.callRP('Project.checkExistModulProject', self.dicUser,self.dicProject)
            print 'existProject = ', existProject
            if not existProject or existProject == 'NONE':
                print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~ create new'
                self.rpc.callRP('Projects.createNewProject', self.dicUser,self.dicProject)
            self.singleProject.sWhere = ' where modul_Project_number = ' + `self.dicProject['ModulProjectNumber']` + ' and modul_number = ' + `self.dicProject['ModulNumber']`
        elif self.dicProject and newProject and self.ProjectID == 0:
            dicResult = self.rpc.callRP('Projects.createNewProject', self.dicUser,self.dicProject)
            if dicResult and dicResult not in ['NONE','ERROR']:
                print 'dicResut = ', dicResult
                self.ProjectID = dicResult
                if self.ProjectID > 0:
                    self.singleProject.sWhere = ' where id = ' + `self.ProjectID` 
        elif self.ProjectID > 0:
            self.singleProject.sWhere = ' where id = ' + `self.ProjectID`
            
        liProjectStatus = self.rpc.callRP('Projects.getComboBoxEntries',self.dicUser)
        
        cbProjectStatus = self.getWidget('cbStatus')
        if cbProjectStatus:
            liststore = gtk.ListStore(str)
            for oneStatus in liProjectStatus:
                liststore.append([oneStatus])
            cbProjectStatus.set_model(liststore)
            cbProjectStatus.set_text_column(0)
            cbProjectStatus.show()
            
        # Trees for Proposal,  Order and Invoice 
        self.treeOrder = cuon.Misc.misc.Treeview()
        
        self.treeOrder.start(self.getWidget('tvProjectOrder'),'Text','Order')
         
         
        # Notes
        self.textbufferSources,  self.viewSources = self.getNotesEditor()
        Scrolledwindow = self.getWidget('scSourceNotes')
        Scrolledwindow.add(self.viewSources)
        self.viewSources.show_all()
        Scrolledwindow.show_all()
        # Menu-items
        self.initMenuItems()

        # All window items
        self.addEnabledMenuItems('window','mi_quit1', 'z')
        
        
        # Close Menus for Tab
        self.addEnabledMenuItems('tabs','mi_project1')
        self.addEnabledMenuItems('tabs','mi_phase1')
        self.addEnabledMenuItems('tabs','mi_task1')
        self.addEnabledMenuItems('tabs','mi_staff_resources1')
        self.addEnabledMenuItems('tabs','mi_material_resources1')
        self.addEnabledMenuItems('tabs','programming1')
               
        # seperate Menus
        self.addEnabledMenuItems('project','mi_project1')
        self.addEnabledMenuItems('phase','mi_phase1')
        self.addEnabledMenuItems('tasks','mi_task1')
        self.addEnabledMenuItems('staff_resources','mi_staff_resources1')
        self.addEnabledMenuItems('material_resources','mi_material_resources1')
        self.addEnabledMenuItems('programming','programming1')
        
        
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


        self.addEnabledMenuItems('editProgramming','programming_main_new' , self.dicUserKeys['project_new'])
        self.addEnabledMenuItems('editProgramming','programming_main_delete', self.dicUserKeys['project_delete'])
        self.addEnabledMenuItems('editProgramming','programming_main_edit', self.dicUserKeys['project_edit'])

        self.addEnabledMenuItems('editStaffRes','staff_resources_new1' , self.dicUserKeys['project_new'])
        self.addEnabledMenuItems('editStaffRes','staff_resources_delete1', self.dicUserKeys['project_delete'])
        self.addEnabledMenuItems('editStaffRes','staff_resources_edit1', self.dicUserKeys['project_edit'])
        
        self.addEnabledMenuItems('editMaterialRes','material_resources_new1' , self.dicUserKeys['project_new'])
        self.addEnabledMenuItems('editMaterialRes','material_resources_delete1', self.dicUserKeys['project_delete'])
        self.addEnabledMenuItems('editMaterialRes','material_resources_edit1', self.dicUserKeys['project_edit'])

        # enabledMenues for Save 
        self.addEnabledMenuItems('editSave','mi_save1', self.dicUserKeys['project_save'])
        self.addEnabledMenuItems('editSave','phasesave1', self.dicUserKeys['project_save'])
        self.addEnabledMenuItems('editSave','task_save1', self.dicUserKeys['project_save'])
        self.addEnabledMenuItems('editSave','staff_resources_save1', self.dicUserKeys['project_save'])
        self.addEnabledMenuItems('editSave','material_resources_save1', self.dicUserKeys['project_save'])
        self.addEnabledMenuItems('editSave','programming_main_save', self.dicUserKeys['project_save'])
        
        # tabs from notebook
        self.tabProject = 0
        self.tabPhases = 1
        self.tabTasks = 2
        self.tabStaffResources = 3
        self.tabMaterialResources = 4
        self.tabOrder = 5
        self.tabProgramming = 6
        
        self.tabProgrammingMain = 100
        
        print 'tab endet'
        self.win1.add_accel_group(self.accel_group)

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
                
      
   
    #Menu  Programming
  
    def on_programming_main_save_activate(self, event):
        self.out( "save projectphases v2")
        self.singleProjectProgramming.projectId = self.singleProject.ID
        self.singleProjectProgramming.save()
        self.setEntriesEditable(self.EntriesProgramming, False)
        self.tabChanged()
        
    def on_programming_main_new_activate(self, event):
        print  "new projectprogramming v2"
        self.singleProjectProgramming.newRecord()
        self.setEntriesEditable(self.EntriesProgramming, True)

    def on_programming_main_edit_activate(self, event):
        print "edit projectprogramming v2"
        self.setEntriesEditable(self.EntriesProgramming, True)
        
        
    def on_programming_main_delete_activate(self, event):
        self.out( "delete projectphases v2")
        self.singleProjectProgramming.deleteRecord()
              
    
    # Buttons
    
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
              

    def on_eFind_key_press_event(self, entry, event):
        print 'eSearch_key_press_event'
        if self.checkKey(event,'NONE','Return'):
            self.findProject()
      
    # search button
    
    
    def on_bSearch_clicked(self, event):
        self.findProject()
    def findProject(self):
        
        self.out( 'Searching ....', self.ERROR)
        sName = self.getWidget('eFindName').get_text()
        sDesignation = self.getWidget('eFindDesignation').get_text()
        self.out('Name and City = ' + sName + ', ' + sDesignation, self.ERROR)
        sID = self.getWidget('eFindID').get_text()
        liSearch = []
        if sName:
            liSearch.append('name')
            liSearch.append(sName)
        if sDesignation:
            liSearch.append('designation')
            liSearch.append(sDesignation)
        if sID:
            liSearch.append('id')
            try:
                liSearch.append(int(sID))
            except:
                liSearch.append(0)
                
        self.singleProject.sWhere = self.getWhere(liSearch) 
        
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
        adr.setChooseEntry('chooseAddress', self.getWidget( 'eAddressNumber'))
        
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
    
    
    # Buttons
    
    # DMS
    def on_bProjectDMS_clicked(self, event):
        print 'dms clicked'
        if self.singleProject.ID > 0:
            print 'ModulNumber', self.ModulNumber
            Dms = cuon.DMS.dms.dmswindow(self.allTables, self.ModulNumber, {'1':self.singleProject.ID})
        
    def on_bPhaseDMS_clicked(self, event):
        print 'dms clicked'
        if self.singleProjectPhases.ID > 0:
            Dms = cuon.DMS.dms.dmswindow(self.allTables, self.MN['Project_phase'], {'1':self.singleProjectPhases.ID})
    
    def on_bTaskDMS_clicked(self, event):
        print 'dms clicked'
        if self.singleProjectTasks.ID > 0:
            Dms = cuon.DMS.dms.dmswindow(self.allTables, self.MN['Project_task'], {'1':self.singleProjectTasks.ID})
        
    def on_bStaffDMS_clicked(self, event):
        print 'dms clicked'
        if self.singleProjectTaskStaff.ID > 0:
            Dms = cuon.DMS.dms.dmswindow(self.allTables, self.MN['Project_staff_resources'], {'1':self.singleProjectTaskStaff.ID})
    
    def on_bMaterialDMS_clicked(self, event):
        print 'dms clicked'
        if self.singleProjectTaskMaterial.ID > 0:
            Dms = cuon.DMS.dms.dmswindow(self.allTables, self.MN['Project_material_resources'], {'1':self.singleProjectTaskMaterial.ID})
    
    def on_bProgrammingDMS_clicked(self, event):
         
        print 'dms clicked'
        if self.singleProjectProgramming.ID > 0:
            Dms = cuon.DMS.dms.dmswindow(self.allTables, self.MN['Project_programming'], {'1':self.singleProjectProgramming.ID})
    
    
    # other buttons
    
    def on_eMRArticleNumber_changed(self, event):
        print 'eMRArticleNumber changed'
        eArticleDes  = self.getWidget('eArticleDesignation')
        sArticleDes  = self.singleArticle.getArticleDesignation(self.getWidget( 'eMRArticleNumber').get_text())
        eArticleDes.set_text(sArticleDes)
        
        
        
        
    def on_bGotoAddress_clicked(self, event):
        print 'Customer-ID ', self.singleProject.firstRecord['customer_id']
        if self.singleProject.firstRecord['customer_id'] > 0:
            print 'start address'
            adr = cuon.Addresses.addresses.addresswindow(self.allTables,addrid=self.singleProject.firstRecord['customer_id'])
    
    # letter buttons
    def on_bLetter_clicked(self, event):
        print 'bLetter clicked'
        if self.singleProject.ID > 0:
            #self.singleAddress.load(self.singleAddress.ID)
            #print 'firstRecord = ', self.singleProject.firstRecord
            print 'ModulNumber', self.ModulNumber
            firstRecord, dicExtInfo = self.getProjectInfos()
            print 'firstRecord = ', firstRecord
            Dms = cuon.DMS.dms.dmswindow(self.allTables, self.MN['Project_info'], {'1':-141}, firstRecord,dicExtInfo)
            
    def on_bLetterPhase_clicked(self, event):
        print 'bLetter clicked'

    def on_bLetterTask_clicked(self, event):
        print 'bLetter clicked'

    def on_bLetterMaterial_clicked(self, event):
        print 'bLetter clicked'

    def on_bLetterStaff_clicked(self, event):
        print 'bLetter clicked'

    def on_bLetterProgramming_clicked(self, event):
        print 'bLetter clicked'



            
    # Toolbar
    
    def on_tbNew_clicked(self, event):
        if self.tabOption == self.tabProject:
            self.on_new1_activate(event)
        elif self.tabOption == self.tabPhases:
            self.on_phasenew1_activate(event)
        elif self.tabOption == self.tabTasks:
            self.on_tasknew1_activate(event)
        elif self.tabOption == self.tabMaterialResources:
            self.on_material_resources_new1_activate(event)    
        elif self.tabOption == self.tabStaffResources:
            self.on_staff_resources_new1_activate(event)     
        elif self.tabOption == self.tabProgrammingMain:
            self.on_programming_main_new1_activate(event)     
            
            
    def on_tbEdit_clicked(self, event):
        if self.tabOption == self.tabProject:
            self.on_edit1_activate(event)
        elif self.tabOption == self.tabPhases:
            self.on_phaseedit1_activate(event)
        elif self.tabOption == self.tabTasks:
            self.on_taskedit1_activate(event)
        elif self.tabOption == self.tabMaterialResources:
            self.on_material_resources_edit1_activate(event)    
        elif self.tabOption == self.tabStaffResources:
            self.on_staff_resources_edit1_activate(event)     
        elif self.tabOption == self.tabProgrammingMain:
            self.on_programming_main_edit1_activate(event)     

    def on_tbSave_clicked(self, event):
        if self.tabOption == self.tabProject:
            self.on_save1_activate(event)
        elif self.tabOption == self.tabPhases:
            self.on_phasesave1_activate(event)
        elif self.tabOption == self.tabTasks:
            self.on_task_save1_activate(event)
        elif self.tabOption == self.tabMaterialResources:
            self.on_material_resources_save1_activate(event)    
        elif self.tabOption == self.tabStaffResources:
            self.on_staff_resources_save1_activate(event)     
        elif self.tabOption == self.tabProgrammingMain:
            self.on_programming_main_save1_activate(event)     

    def on_tbDelete_clicked(self, event):
        if self.tabOption == self.tabProject:
            self.on_delete1_activate(event)
        elif self.tabOption == self.tabPhases:
            self.on_phasedelete1_activate(event)
        elif self.tabOption == self.tabTasks:
            self.on_task_delete1_activate(event)
        elif self.tabOption == self.tabMaterialResources:
            self.on_material_resources_delete1_activate(event)    
        elif self.tabOption == self.tabStaffResources:
            self.on_staff_resources_delete1_activate(event)     
        elif self.tabOption == self.tabProgrammingMain:
            self.on_programming_main_delete1_activate(event)         
            
    def on_tbDMS_clicked(self, event):
        if self.tabOption == self.tabProject:
            self.on_bProjectDMS_clicked(event)
        elif self.tabOption == self.tabPhases:
            self.on_bPhaseDMS_clicked(event)
        elif self.tabOption == self.tabTasks:
            self.on_bTaskDMS_clicked(event)
        elif self.tabOption == self.tabMaterialResources:
            self.on_bMaterialDMS_clicked(event)    
        elif self.tabOption == self.tabStaffResources:
            self.on_bStaffDMS_clicked(event)     
        elif self.tabOption == self.tabProgrammingMain:
            self.on_ProgrammingDMS_clicked(event) 
    
    
    def on_tbLetter_clicked(self, event):
        if self.tabOption == self.tabProject:
            self.on_bLetter_clicked(event)
        elif self.tabOption == self.tabPhases:
            self.on_bLetterPhase_clicked(event)
        elif self.tabOption == self.tabTasks:
            self.on_bLetterTask_clicked(event)
        elif self.tabOption == self.tabMaterialResources:
            self.on_bLetterMaterial_clicked(event)    
        elif self.tabOption == self.tabStaffResources:
            self.on_bLetterStaff_clicked(event)     
        elif self.tabOption == self.tabProgrammingMain:
            self.on_bLetterProgramming_clicked(event) 
    
    
    
    def getProjectInfos(self):
    
        firstRecord = None
        if self.singleProject.ID > 0:
            #self.singleAddress.load(self.singleAddress.ID)
            firstRecord = self.singleProject.firstRecord
            print 'ModulNumber', self.ModulNumber
            #dicNotes = self.rpc.callRP('Address.getNotes',self.singleAddress.ID, self.dicUser)
            #if dicNotes and dicNotes not in ['NONE','ERROR']:
            #    for key in dicNotes:
            #        firstRecord['notes_' + key] = dicNotes[key]
            firstRecord = self.addDateTime(firstRecord)
            if firstRecord.has_key('customer_id') and firstRecord['customer_id'] > 0:
                print 'Customer ID = ', firstRecord['customer_id']
                self.singleAddress.load(firstRecord['customer_id'])
                print self.singleAddress.firstRecord
                for key in self.singleAddress.firstRecord:
                    firstRecord['address_' + key] = self.singleAddress.firstRecord[key]
                    print 'Key, Value = ',key,self.singleAddress.firstRecord[key]
                    
            dicExtInfo ={'sep_info':{'1':self.singleProject.ID},'Modul':self.ModulNumber}
        
        return firstRecord, dicExtInfo
        
    
    
    # Order for this Project
     # view Order 
    def disconnectOrderTree(self):
        try:
            
            self.getWidget('tvProjectOrder').get_selection().disconnect(self.connectOrderTreeId)
        except:
            pass

    def connectOrderTree(self):
        try:
            self.connectOrderTreeId = self.getWidget('tvProjectOrder').get_selection().connect("changed", self.OrderTree_select_callback)
        except:
            pass
   
    def OrderTree_select_callback(self, treeSelection):
        listStore, iter = treeSelection.get_selected()
        self.OrderID = 0
        print listStore,iter
        
        if listStore and len(listStore) > 0:
           row = listStore[0]
        else:
           row = -1
   
        if iter != None:
            sNewId = listStore.get_value(iter, 0)
            print sNewId
            try:
                self.OrderID = int(sNewId[sNewId.find('###')+ 3:])
                #self.setDateValues(newID)
                
            except:
                pass
                
    def on_tvProjectOrder_row_activated(self,event,data1, data2):
        
        self.on_bOrderJumpTo_clicked(event)
        
    def on_bOrderJumpTo_clicked(self,  event):
        
        if self.OrderID:
            orderwindow = cuon.Order.order.orderwindow(self.allTables,None,False,self.OrderID)
        
    def setOrderValues(self):
        liGroup = self.rpc.callRP('Order.getOrderForProject',self.singleProject.ID, self.dicUser)
        print liGroup
        if liGroup and liGroup not in ['NONE','ERROR']:
            self.treeOrder.fillTree(self.getWidget('tvProjectOrder'),liGroup,['number','designation', 'orderedat'],'self.connectOrderTree()')
            self.connectOrderTree()
        else:
            self.treeOrder.fillTree(self.getWidget('tvProjectOrder'),[],['number','designation', 'orderedat'],'self.connectOrderTree()')
            self.connectOrderTree()
    
    # 
    # Programming
    #
    def on_bProgrammingEdit_clicked(self, event):
        print "programming edit clicked"
        exEditor = self.getWidget('eExternalEditor').get_text()
        if exEditor:
            commands.getstatusoutput(edEditor)
        else:
            pe = cuon.Editor.programmersEditor.programmerseditor()


   

    def refreshTree(self):
        self.singleProject.disconnectTree()
        self.singleProjectPhases.disconnectTree()
        self.singleProjectTasks.disconnectTree()
        self.singleProjectTaskStaff.disconnectTree()
        self.singleProjectTaskMaterial.disconnectTree()
        self.singleProjectProgramming.disconnectTree()

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
            
       
            
        elif self.tabOption == self.tabProgramming:
            self.singleProjectProgramming.sWhere  ='where project_id = ' + `int(self.singleProject.ID)`
            self.singleProjectProgramming.connectTree()
            self.singleProjectProgramming.refreshTree()
            

         
    def tabChanged(self):
        self.out( 'tab changed to :'  + str(self.tabOption))
        print self.tabOption
        
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

        elif self.tabOption == self.tabOrder:
            print 'tabchanged Order'
            
            self.setOrderValues()
            
        elif self.tabOption == self.tabProgramming:
            if self.tabOption2 == self.tabProgrammingMain:
                print 'tabchanged Programming'
                
                self.disableMenuItem('tabs')
                self.enableMenuItem('programming')
                
                self.editAction = 'editProgramming'
                self.setTreeVisible(True)
                self.setStatusbarText([self.singleProjectTaskMaterial.sStatus])

        # refresh the Tree
        print "refresh Tree 1"
        self.refreshTree()
        self.enableMenuItem(self.editAction)
        self.editEntries = False
        
