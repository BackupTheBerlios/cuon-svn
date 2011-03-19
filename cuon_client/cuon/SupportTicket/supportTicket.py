# coding=utf-8
##Copyright (C) [2003]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 

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
from cuon.Windows.chooseWindows  import chooseWindows
import SingleSupportProject
import SingleSupportTicket


import cuon.DMS.documentTools
import cuon.DMS.dms
import os
import cuon.Project.project
import cuon.Project.SingleProject
import cuon.Addresses.addresses
import cuon.Addresses.SingleAddress
import cuon.Addresses.SinglePartner 

class supportticketwindow(chooseWindows):

    
    def __init__(self,   allTables ):
        
        chooseWindows.__init__(self)
        
        
        self.loadGlade('support_ticket.xml','SupportTicketMainwindow' )
        self.win1 = self.getWidget('SupportTicketMainwindow')
        self.ModulNumber = self.MN['SupportTicket']        
        self.allTables = allTables
        
        self.singleSupportProject = SingleSupportProject.SingleSupportProject(allTables)
        self.singleSupportTicket = SingleSupportTicket.SingleSupportTicket(allTables)
        
        self.singleProject = cuon.Project.SingleProject.SingleProject(allTables)
        self.singlePartner = cuon.Addresses.SinglePartner.SinglePartner(allTables)
        self.singleAddress = cuon.Addresses.SingleAddress.SingleAddress(allTables)
        
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
        self.singleSupportTicket.setTreeFields( ['ticket_number', 'short_designation'])
        self.singleSupportTicket.setStore( gtk.ListStore( gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_UINT) ) 
        self.singleSupportTicket.setTreeOrder('reported_day')
        self.singleSupportTicket.setTree(self.getWidget('TicketTree') )
        self.singleSupportTicket.setListHeader([_('Ticket'), _('Short Designation')])
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
        self.addEnabledMenuItems('editProject','new1', self.dicUserKeys['new'])
        self.addEnabledMenuItems('editProject','edit1', self.dicUserKeys['edit'])
        self.addEnabledMenuItems('editProject','delete1', self.dicUserKeys['delete'])

        # enabledMenues for  Ticket
        self.addEnabledMenuItems('editTicket','Ticket_new1', self.dicUserKeys['new'])
        self.addEnabledMenuItems('editTicket','Ticket_edit1', self.dicUserKeys['edit'])
        self.addEnabledMenuItems('editTicket','Ticket_delete1', self.dicUserKeys['delete'])
        # enabledMenues for Save 
        self.addEnabledMenuItems('editSave','save1', self.dicUserKeys['save'])
        self.addEnabledMenuItems('editSave','Ticket_Save1', self.dicUserKeys['save'])
        
        
        # add comboboxes
        liStatus,  liSeverity, liPriority, liReproduced, liPlatform= self.rpc.callRP('Support.getTicketComboBoxEntries',self.dicUser)
        
        print liStatus,  '\n\n',  liSeverity,  '\n\n', liPriority,  '\n\n', liReproduced ,  '\n\n', liPlatform,  '\n\n'
        
        cbTypeOfStatus = self.getWidget('cbTicketStatus')
        if cbTypeOfStatus:
            liststore = gtk.ListStore(str)
            for TypeOfStatus in liStatus:
                liststore.append([TypeOfStatus])
            cbTypeOfStatus.set_model(liststore)
            cbTypeOfStatus.set_text_column(0)
            cbTypeOfStatus.show()

        #same for the find field 
        cbFindTypeOfStatus = self.getWidget('cbFindStatus')
        if cbFindTypeOfStatus:
            liststore = gtk.ListStore(str)
            for TypeOfStatus in liStatus:
                liststore.append([TypeOfStatus])
            cbFindTypeOfStatus.set_model(liststore)
            cbFindTypeOfStatus.set_text_column(0)
            cbFindTypeOfStatus.show()
            
            
        cbTypeOfSeverity = self.getWidget('cbTicketSeverity')
        if cbTypeOfSeverity:
            liststore = gtk.ListStore(str)
            for TypeOfSeverity in liSeverity:
                liststore.append([TypeOfSeverity])
            cbTypeOfSeverity.set_model(liststore)
            cbTypeOfSeverity.set_text_column(0)
            cbTypeOfSeverity.show()

     #same for the find field 
        cbFindTypeOfSeverity = self.getWidget('cbFindSeverity')
        if cbFindTypeOfSeverity:
            liststore = gtk.ListStore(str)
            for TypeOfSeverity in liSeverity:
                liststore.append([TypeOfSeverity])
            cbFindTypeOfSeverity.set_model(liststore)
            cbFindTypeOfSeverity.set_text_column(0)
            cbFindTypeOfSeverity.show()
            
            
            
            
        cbTypeOfPriority = self.getWidget('cbTicketPriority')
        if cbTypeOfPriority:
            liststore = gtk.ListStore(str)
            for TypeOfPriority in liPriority:
                liststore.append([TypeOfPriority])
            cbTypeOfPriority.set_model(liststore)
            cbTypeOfPriority.set_text_column(0)
            cbTypeOfPriority.show()
        
        
        
           
        cbTypeOfReproduced = self.getWidget('cbTicketReproduced')
        if cbTypeOfReproduced:
            liststore = gtk.ListStore(str)
            for TypeOfReproduced in liReproduced:
                liststore.append([TypeOfReproduced])
            cbTypeOfReproduced.set_model(liststore)
            cbTypeOfReproduced.set_text_column(0)
            cbTypeOfReproduced.show()
            
         
           
        cbTypeOfPlatform = self.getWidget('cbTicketPlatform')
        if cbTypeOfPlatform:
            liststore = gtk.ListStore(str)
            for TypeOfPlatform in liPlatform:
                liststore.append([TypeOfPlatform])
            cbTypeOfPlatform.set_model(liststore)
            cbTypeOfPlatform.set_text_column(0)
            cbTypeOfPlatform.show()
            
            
            
        self.tabSupportProject = 0
        self.tabSupportTicket = 1
        # start
        
        self.tabChanged()
     
        self.win1.add_accel_group(self.accel_group)
        
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
        
        
    # modul buttons
    
    # Project
    def on_bSearchProject_clicked(self, event):
        pr = cuon.Project.project.projectwindow(self.allTables, choose='Phase')
        pr.setChooseEntry('chooseProject', self.getWidget( 'eProjectPhaseID'))

                           

    def on_eProjectPhaseID_changed(self, event):
        print 'eProject changed'
        iPhNumber = self.getChangedValue('eProjectPhaseID')
        ePrField = self.getWidget("eProjectPhaseDiscription")
        liPr = self.singlePhase.getInfoForID(iPhNumber)
        sDesc = ' '
        if liPr:
            try:
                sDesc = liPr[0] + ', '  + liPr[1]
            except:
                pass
        ePrField.set_text(sDesc)
     
    #Address
    def on_bSearchAddress_clicked(self, event):
        addr = cuon.Addresses.addresses.addresswindow(self.allTables)
        addr.setChooseEntry('chooseAddress', self.getWidget( 'eAddressNumber'))
        

     # signals from entry eAddressNumber
    
    def on_eAddressNumber_changed(self, event):
        print 'eAdrnbr changed'
        try:
            iAdrNumber = self.getChangedValue('eAddressNumber')
            eAdrField = self.getWidget('eAddressField')
            liAdr = self.singleAddress.getAddress(iAdrNumber)
            print 'Address = ',  liAdr
            eAdrField.set_text(liAdr[0]+',  ' +liAdr[1])
        except Exception,  param:
            print Exception, param
        
       
    def on_bGotoAddress_clicked(self, event):
        iAddrNumber = self.getChangedValue('eAddressNumber')
        adr = cuon.Addresses.addresses.addresswindow(self.allTables, address_id = iAddrNumber)
        
    # Search and show partner
    def on_bSearchPartner_clicked(self, event):
        print 'choose partner'
        adr = cuon.Addresses.addresses.addresswindow(self.allTables)
        adr.setChooseEntry('chooseAddress', self.getWidget( 'ePartnerID'))
        
    def on_ePartnerID_changed(self, event):
        print 'ePartner changed'
        iAdrNumber = self.getChangedValue('ePartnerID')
        eAdrField = self.getWidget('ePartnerField')
        sAdr = self.singlePartner.getAddressFirstlast(iAdrNumber)
        eAdrField.set_text(sAdr)
            
    def on_bGotoPartner_clicked(self, event):
        print 'bshowPartner'
        iPID = int(self.getWidget('ePartnerID').get_text())
        print 'pid = ',  iPID
        if iPID > 0:
        
            self.singlePartner.load(iPID)
            print 'addressid = ',  self.singlePartner.getAddressID()
            
            adr = cuon.Addresses.addresses.addresswindow(self.allTables, self.singlePartner.getAddressID(), iPID)
    
    def on_tbDMS_clicked(self, event):
        self.activateClick('dms1')

    def refreshTree(self):
        self.singleSupportTicket.disconnectTree()
        self.singleSupportProject.disconnectTree()
        #self.singleThink.disconnectTree()
        
        if self.tabOption == self.tabSupportProject:
            print '-->Start SupportTicket refresh Tree'
            self.singleSupportProject.connectTree()
            self.singleSupportProject.refreshTree()
            print '<--End SupportProject  refresh Tree'

        elif self.tabOption == self.tabSupportTicket:
            print 'refresh Tree fpr Ticket'
            self.singleSupportTicket.sWhere  ='where support_project_id = ' + `int(self.singleSupportProject.ID)`
            self.singleSupportTicket.connectTree()
            self.singleSupportTicket.refreshTree()
            #self.singleSupportTicket.getFirstListRecord()
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

