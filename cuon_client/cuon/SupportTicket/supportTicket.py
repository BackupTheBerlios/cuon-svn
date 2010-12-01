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
import commands
import logging
from cuon.Windows.windows  import windows
import SingleSupportProject
import SingleSupportTicket

import cuon.DMS.documentTools
import cuon.DMS.dms
import os



class supportticketwindow(windows):

    
    def __init__(self,   allTables ):
        
        windows.__init__(self)
        
        
        self.loadGlade('support_ticket.xml','SupportTicketMainwindow' )
        self.win1 = self.getWidget('SupportTicketMainwindow')
        self.ModulNumber = self.MN['SupportTicket']        
        self.allTables = allTables
        
        self.singleSupportProject = SingleSupportProject.SingleSupportProject(allTables)
        self.singleSupportTicket = SingleSupportTicket.SingleSupportTicket(allTables)
        
        
        self.entriesSupportProject = 'support_project.xml'
        self.entriesSupportTicket = 'support_ticket.xml'
    
        print "single Project settings"
      #singleSupportProject
        print "tree1 = " ,  self.getWidget('ProjectTree')
        self.loadEntries(self.entriesSupportProject)
        self.singleSupportProject.setEntries(self.getDataEntries( self.entriesSupportProject) )
        self.singleSupportProject.setGladeXml(self.xml)
        self.singleSupportProject.setTreeFields( ['support_project_number', 'designation'])
        self.singleSupportProject.setStore( gtk.ListStore( gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_UINT) ) 
        self.singleSupportProject.setTreeOrder('support_project_number')
        self.singleSupportProject.setTree(self.getWidget('ProjectTree') )
        self.singleSupportProject.setListHeader([_('Number'),  _('Designation')])
        #print 'Widgets - win = ', `self.win1`
    
        #singleSupportTicket
        
        self.loadEntries(self.entriesSupportTicket)
        self.singleSupportTicket.setEntries(self.getDataEntries( self.entriesSupportTicket) )
        self.singleSupportTicket.setGladeXml(self.xml)
        self.singleSupportTicket.setTreeFields( ['ticket_number', 'designation'])
        self.singleSupportTicket.setStore( gtk.ListStore( gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_UINT) ) 
        self.singleSupportTicket.setTreeOrder('reported_day')
        self.singleSupportTicket.setTree(self.getWidget('TicketTree') )
        self.singleSupportTicket.setListHeader([_('Ticket'), _('Designation')])
        #print 'Widgets - win = ', `self.win1`
        #print 'Widgets - tree1 = ', `self.xml.get_widget('tree1')`
        
        # Menu-items
        self.initMenuItems()

        # Close Menus for Tab

        self.addEnabledMenuItems('Support','Projects')
        self.addEnabledMenuItems('Support','Ticket')


        # seperate Menus
        self.addEnabledMenuItems('Projects','Projects')
        self.addEnabledMenuItems('Ticket','Ticket')
        
        # enabledMenues for  Project
        self.addEnabledMenuItems('editProject','new1')
        self.addEnabledMenuItems('editProject','edit1')
        self.addEnabledMenuItems('editProject','delete1')

        # enabledMenues for  Ticket
        self.addEnabledMenuItems('editTicket','Ticket_new1')
        self.addEnabledMenuItems('editTicket','Ticket_edit1')
        self.addEnabledMenuItems('editTicket','Ticket_delete1')
        # enabledMenues for Save 
        self.addEnabledMenuItems('editSave','save1', self.dicUserKeys['articles_save'])
        self.addEnabledMenuItems('editSave','Ticket_Save1', self.dicUserKeys['articles_save'])
        
        self.tabSupportProject = 0
        self.tabSupportTicket = 1
        # start
        
        self.tabChanged()
     
    #    self.win1.add_accel_group(self.accel_group)
        
    # File Menu
    def on_quit1_activate(self,  event):
        self.win1.hide()
        
    
    
    # Support Project

    def on_new1_activate(self, event):
        print "new support project"
        self.singleSupportProject.newRecord()
        
        self.setEntriesEditable(self.entriesSupportProject, True)
        
    
    def on_edit1_activate(self, event):        
        
        self.setEntriesEditable(self.entriesSupportProject, True)
  
        
    
    def on_save1_activate(self, event):
        
        print "save SupportTicket v2"
        self.singleSupportProject.save()
        self.setEntriesEditable(self.entriesSupportProject, False)
        
        self.tabChanged()
         
    
    def on_delete1_activate(self, event):    
        
       
        self.singleSupportProject.deleteRecord()

  # Support Ticket

    def on_ticket_new1_activate(self, event):
        print "new support ticket"
        self.singleSupportTicket.newRecord()
        
        self.setEntriesEditable(self.entriesSupportTicket, True)
        
    
    def on_ticket_edit1_activate(self, event):        
        
        self.setEntriesEditable(self.entriesSupportTicket, True)
  
        
    
    def on_ticket_save1_activate(self, event):
        
        print "save SupportTicket v2"
        self.singleSupportTicket.save()
        self.setEntriesEditable(self.entriesSupportTicket, False)
        
        self.tabChanged()
         
    
    def on_ticket_delete1_activate(self, event):    
        
       
        self.singleSupportTicket.deleteRecord()




    #Tools
    def on_dms1_activate(self, event):    
        print 'dms clicked'
        if self.singleSupportTicket.ID > 0:
            print 'ModulNumber', self.ModulNumber
            Dms = cuon.DMS.dms.dmswindow(self.allTables, self.ModulNumber, {'1':self.singleSupportTicket.ID})
    
        
   # Toolbar-Buttons 
    
    def on_tbNew_clicked(self, event):
        print "tabOption ",  self.tabOption
        if self.tabOption == self.tabSupportProject:
            self.activateClick('new1')
        elif self.tabOption == self.tabSupportTicket:
            self.activateClick('Ticket_new1')
          
    
    def on_tbEdit_clicked(self, event):
        if self.tabOption == self.tabSupportProject:
            self.activateClick('edit1')
        elif self.tabOption == self.tabSupportTicket:
            self.activateClick('Ticket_edit1')


    def on_tbSave_clicked(self, event):
        if self.tabOption == self.tabSupportProject:
            self.activateClick('save1')
        elif self.tabOption == self.tabSupportTicket:
            self.activateClick('Ticket_save1')
            
            
    def on_tbRemove_clicked(self, event):
        if self.tabOption == self.tabSupportProject:
            self.activateClick('delete1')
        elif self.tabOption == self.tabSupportTicket:
            self.activateClick('Ticket_delete1')
        
        
        
    def on_tbDMS_clicked(self, event):
        self.activateClick('dms1')

    def refreshTree(self):
        self.singleSupportTicket.disconnectTree()
        #self.singleThink.disconnectTree()
        
        if self.tabOption == self.tabSupportProject:
            print '-->Start SupportTicket refresh Tree'
            self.singleSupportProject.connectTree()
            self.singleSupportProject.refreshTree()
            print '<--End SupportProject  refresh Tree'

        elif self.tabOption == self.tabSupportTicket:
            print 'refresh Tree fpr Ticket'
            self.singleSupportTicket.sWhere  ='where SupportTicket_id = ' + `int(self.singleSupportProject.ID)`
            self.singleSupportTicket.getFirstListRecord()
            #self.singleSupportTicket.fillEntries(self.singleSupportTicket.ID)
            


         
    def tabChanged(self):
        print 'tab changed to :'  + str(self.tabOption)
        self.setTreeVisible(True)
        if self.tabOption == self.tabSupportProject:
            #Project
            self.disableMenuItem('tabs')
            self.enableMenuItem('Project')
            print 'Seite 0'
            #self.editAction = 'editStaff'
            
        elif self.tabOption == self.tabSupportTicket:
            #Fee
            self.disableMenuItem('tabs')
            self.enableMenuItem('Ticket')
            self.singleSupportTicket.SupportProjectId = self.singleSupportProject.ID
            #self.editAction = 'editFee'
            print 'Seite 1'
  
            
        # refresh the Tree
        self.refreshTree()
        self.enableMenuItem(self.editAction)
        self.editEntries = False

