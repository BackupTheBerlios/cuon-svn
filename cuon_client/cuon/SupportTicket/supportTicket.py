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
    
    
        #singleSupportTicket
        
        self.loadEntries(self.entriesSupportTicket)
        self.singleSupportTicket.setEntries(self.getDataEntries( self.entriesSupportTicket) )
        self.singleSupportTicket.setGladeXml(self.xml)
        self.singleSupportTicket.setTreeFields( ['header'])
        self.singleSupportTicket.setStore( gtk.ListStore( gobject.TYPE_STRING, gobject.TYPE_UINT) ) 
        self.singleSupportTicket.setTreeOrder('header')
        self.singleSupportTicket.setTree(self.xml.get_widget('tree1') )
        self.singleSupportTicket.setListHeader(['Header'])
        #print 'Widgets - win = ', `self.win1`
        #print 'Widgets - tree1 = ', `self.xml.get_widget('tree1')`
        
        self.tabSupportTicket = 0
        self.tabThinking = 1
        # start
        
        self.tabChanged()
     
    #    self.win1.add_accel_group(self.accel_group)
        
    # File Menu
    def on_quit1_activate(self,  event):
        self.win1.hide()
        
    
    
    # SupportTicket

    def on_new1_activate(self, event):
        if self.tabOption == self.tabSupportTicket:
            self.singleSupportTicket.newRecord()
            self.setEntriesEditable(self.entriesSupportTicket, True)
            
    
    def on_edit1_activate(self, event):        
        if self.tabOption == self.tabSupportTicket:
            self.setEntriesEditable(self.entriesSupportTicket, True)
  
        
    
    def on_save1_activate(self, event):
        
        if self.tabOption == self.tabSupportTicket:
            print "save SupportTicket v2"
            self.singleSupportTicket.save()
            self.setEntriesEditable(self.entriesSupportTicket, False)
            
        self.tabChanged()
         
    
    def on_delete1_activate(self, event):    
        
        if self.tabOption == self.tabSupportTicket:
            self.singleSupportTicket.deleteRecord()

    #Tools
    def on_dms1_activate(self, event):    
        print 'dms clicked'
        if self.singleSupportTicket.ID > 0:
            print 'ModulNumber', self.ModulNumber
            Dms = cuon.DMS.dms.dmswindow(self.allTables, self.ModulNumber, {'1':self.singleSupportTicket.ID})
    
        
   # Toolbar-Buttons 
    
    def on_tbNew_clicked(self, event):
        self.activateClick('new1')
          
    
    def on_tbEdit_clicked(self, event):
        self.activateClick('edit1')
        


    def on_tbSave_clicked(self, event):
        self.activateClick('save1')
       
    def on_tbRemove_clicked(self, event):
        self.activateClick('delete1')
        
    def on_tbDMS_clicked(self, event):
        self.activateClick('dms1')

    def refreshTree(self):
        self.singleSupportTicket.disconnectTree()
        #self.singleThink.disconnectTree()
        
        if self.tabOption == self.tabSupportTicket:
            print '-->Start SupportTicket refresh Tree'
            self.singleSupportTicket.connectTree()
            self.singleSupportTicket.refreshTree()
            print '<--End SupportTicket refresh Tree'

        elif self.tabOption == self.tabThinking:
            print 'refresh Tree fpr Think-Fee'
            self.singleThink.sWhere  ='where SupportTicket_id = ' + `int(self.singleSupportTicket.ID)`
            self.singleThink.getFirstListRecord()
            self.singleThink.fillEntries(self.singleThink.ID)
            


         
    def tabChanged(self):
        print 'tab changed to :'  + str(self.tabOption)
        self.setTreeVisible(True)
        if self.tabOption == self.tabSupportTicket:
            #Staff
            #self.disableMenuItem('tabs')
            #self.enableMenuItem('staff')
            print 'Seite 0'
            #self.editAction = 'editStaff'
            
        elif self.tabOption == self.tabThinking:
            #Fee
            #self.disableMenuItem('tabs')
            #self.enableMenuItem('fee')
            #self.editAction = 'editFee'
            print 'Seite 1'
  
            
        # refresh the Tree
        self.refreshTree()
        self.enableMenuItem(self.editAction)
        self.editEntries = False

