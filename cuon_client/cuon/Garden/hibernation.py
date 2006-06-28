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
import cuon.Staff.SingleStaff

import cuon.DMS.documentTools
import hibernation_outgoing_document
import hibernation_incoming_document

import cuon.DMS.dms
import SingleHibernation

import SingleHibernationPlant
import SingleBotany
import base64
import os

class hibernationwindow(chooseWindows):

    
    def __init__(self, allTables):

        chooseWindows.__init__(self)

        self.loadGlade('hibernation.xml')
        self.win1 = self.getWidget('HibernationMainwindow')
        self.oDocumentTools = cuon.DMS.documentTools.documentTools()
        self.ModulHibernationNumber = 110000        
        self.ModulHibernationPlantNumber = 110100
        
        self.allTables = allTables
        self.dicUserKeys['hibernation_edit'] = 'e'
        self.dicUserKeys['hibernation_delete'] = 'd'
        self.dicUserKeys['hibernation_new'] = 'n'
        self.dicUserKeys['hibernation_print'] = 'p'


        self.singleAddress = cuon.Addresses.SingleAddress.SingleAddress(allTables)
        self.singleStaff = cuon.Staff.SingleStaff.SingleStaff(allTables)
        self.singleBotany = cuon.Garden.SingleBotany.SingleBotany(allTables)

        self.singleHibernation = SingleHibernation.SingleHibernation(allTables)
        self.singleHibernationPlant = SingleHibernationPlant.SingleHibernationPlant(allTables)
        #self.singleHibernationSales = SingleHibernationSale.SingleHibernationSale(allTables)
        #self.singleHibernationWebshop = SingleHibernationWebshop.SingleHibernationWebshop(allTables)
        #self.singleHibernationStock = SingleHibernationStock.SingleHibernationStock(allTables)
        self.singleAddress = cuon.Addresses.SingleAddress.SingleAddress(allTables)
        
        # self.singleHibernation.loadTable()
              
        self.EntriesHibernations = 'hibernation.xml'
        self.EntriesHibernationsPlant = 'hibernation_plant.xml'
        #self.EntriesHibernationsSales = 'Hibernations_sales.xml'
        #self.EntriesHibernationsWebshop = 'Hibernations_webshop.xml'
        #self.EntriesHibernationsStock = 'Hibernations_stock.xml'
                
        
        #singleHibernation
 
 
        self.loadEntries(self.EntriesHibernations)
        self.singleHibernation.setEntries(self.getDataEntries( self.EntriesHibernations) )
        self.singleHibernation.setGladeXml(self.xml)
        self.singleHibernation.setTreeFields( ['hibernation_number', 'addressnumber'] )
#        self.singleHibernation.setStore( gtk.ListStore(gobject.TYPE_UINT, gobject.TYPE_UINT, gobject.TYPE_UINT) ) 
        self.singleHibernation.setTreeOrder('hibernation_number')
        self.singleHibernation.setTree(self.xml.get_widget('tree1') )
        self.singleHibernation.setListHeader(['number', 'designation', ])
        
         #singleHibernationPlant
        
        self.loadEntries(self.EntriesHibernationsPlant)
        self.singleHibernationPlant.setEntries(self.getDataEntries( self.EntriesHibernationsPlant) )
        self.singleHibernationPlant.setGladeXml(self.xml)
        self.singleHibernationPlant.setTreeFields( ['plant_number','botany_number' ] )
        self.singleHibernationPlant.setStore( gtk.ListStore(gobject.TYPE_UINT, gobject.TYPE_UINT, gobject.TYPE_UINT) ) 
        self.singleHibernationPlant.setTreeOrder('plant_number')
#        self.singleHibernationPlant.setListHeader([''])

        self.singleHibernationPlant.sWhere  ='where hibernation_number = ' + `self.singleHibernation.ID`
        self.singleHibernationPlant.setTree(self.xml.get_widget('tree1') )
  
    
        

        # Menu-items
        self.initMenuItems()

        # Close Menus for Tab

        self.addEnabledMenuItems('tabs','mi_Hibernation1')
        self.addEnabledMenuItems('tabs','mi_Plant1')
        self.addEnabledMenuItems('tabs','mi_sales1')


        # seperate Menus
        self.addEnabledMenuItems('Hibernation','mi_Hibernation1')
        self.addEnabledMenuItems('Plant','mi_Plant1')
        self.addEnabledMenuItems('sales','mi_sales1')

        
        # enabledMenues for Hibernation
        self.addEnabledMenuItems('editHibernation','new1', self.dicUserKeys['hibernation_new'])
        self.addEnabledMenuItems('editHibernation','clear1', self.dicUserKeys['hibernation_delete'])
        self.addEnabledMenuItems('editHibernation','print1', self.dicUserKeys['hibernation_print'])
        self.addEnabledMenuItems('editHibernation','edit1',self.dicUserKeys['hibernation_edit'])

       

        # tabs from notebook
        self.tabHibernation = 0
        self.tabPlant = 1
        
        # start
        
        self.tabChanged()

        # enabled menus for Hibernation
        self.addEnabledMenuItems('editHibernation','new1')
        self.addEnabledMenuItems('editHibernation','clear1')
        self.addEnabledMenuItems('editHibernation','print1')

        # enabled menus for Hibernation_Plant
        self.addEnabledMenuItems('editHibernationPlant','PlantNew1')
        self.addEnabledMenuItems('editHibernationPlant','PlantClear1')

        
        
##        for i in range(len(tax_vat)) :
##            li = gtk.ListItem(tax_vat[i])
##            cb.list.append_items([li])
##            li.show()
##    
        self.win1.add_accel_group(self.accel_group)
    #Menu File
              
    def on_quit1_activate(self, event):
        print "exit Hibernations v2"
        self.closeWindow()
  

    #Menu Hibernation
  
    def on_save1_activate(self, event):
        print "save Hibernations v2"
        self.singleHibernation.save()
        self.setEntriesEditable(self.EntriesHibernations, False)
        self.tabChanged()
         
        
    def on_new1_activate(self, event):
        print "new Hibernations v2"
        self.singleHibernation.newRecord()
        self.setEntriesEditable(self.EntriesHibernations, True)
        

    def on_edit1_activate(self, event):
        self.setEntriesEditable(self.EntriesHibernations, True)

    def on_delete1_activate(self, event):
        print "delete Hibernations v2"
        self.singleHibernation.deleteRecord()


    #choose Manufactor button
    def on_bChooseManufactor_clicked(self, event):
        adr = cuon.Addresses.addresses.addresswindow(self.allTables)
        adr.setChooseEntry(_('chooseAddress'), self.getWidget( 'eManufactorNumber'))
        
    # signals from entry eManufactorNumber
    
    def on_eManufactorNumber_changed(self, event):
        print 'eManufactor changed'
        eAdrField = self.getWidget('eManufactorField1')
        liAdr = self.singleAddress.getAddress(self.getWidget( 'eManufactorNumber').get_text())
        eAdrField.set_text(liAdr[0] + ', ' + liAdr[4])


    def on_bShowDMS_clicked(self, event):
        print 'dms clicked'
        if self.singleHibernation.ID > 0:
            print 'ModulNumber', self.ModulNumber
            Dms = cuon.DMS.dms.dmswindow(self.allTables, self.ModulNumber, {'1':self.singleHibernation.ID})
        

  #Menu Plant
        
   
    def on_PlantSave1_activate(self, event):
        print "save Partner Hibernations v2"
        self.singleHibernationPlant.hibernationID = self.singleHibernation.ID
        self.singleHibernationPlant.save()
        self.setEntriesEditable(self.EntriesHibernationsPlant, False)

        self.tabChanged()
        
    def on_PlantNew1_activate(self, event):
        print "new Partner Hibernations v2"
        self.singleHibernationPlant.newRecord()
        self.setEntriesEditable(self.EntriesHibernationsPlant, True)

    def on_PlantEdit1_activate(self, event):
        self.setEntriesEditable(self.EntriesHibernationsPlant, True)

    def on_PlantClear1_activate(self, event):
        print "delete Partner Hibernations v2"
        self.singleHibernationPlant.deleteRecord()

   

    # Print Menus


    def on_print_icoming_document1_activate(self, event):
        dicOrder = {}
        print "Start print incoming document 1"
        
        dicOrder['incomingNumber'] = self.rpc.callRP('Garden.getIncomingNumber',self.singleHibernation.ID, self.dicUser)
        print "Start print incoming document 2"

        dicOrder['orderNumber'] = self.singleHibernation.ID
        print "Start print incoming document 3"

        Pdf = self.rpc.callRP('Report.server_hibernation_incoming_document', dicOrder, self.dicUser)
        print "PDF", Pdf
        
        s = self.doDecode(Pdf)
        fname = self.saveTmpData(s)
        os.system('gpdf  ' + fname + ' &')
        
        
        #Pdf = hibernation_incoming_document.hibernation_incoming_document(dicOrder)
    def on_print_outgoing_document1_activate(self, event):
        dicOrder = {}
        Pdf = hibernation_outgoing_document.hibernation_outgoing_document(dicOrder)



    def on_chooseHibernation_activate(self, event):
        # choose Hibernation from other Modul
        self.setChooseValue(self.singleHibernation.ID)
        print 'Hibernation-ID = ' + `self.singleHibernation.ID`
        self.closeWindow()
  

    #choose Address button
    def on_bChooseAddress_clicked(self, event):
        adr = cuon.Addresses.addresses.addresswindow(self.allTables)
        adr.setChooseEntry('chooseAddress', self.getWidget( 'eAddressNumber'))
        
    # signals from entry eAddressNumber
    
    def on_eAddressNumber_changed(self, event):
        print 'eAdrnbr changed'
        iAdrNumber = self.getChangedValue('eAddressNumber')
        eAdrField = self.getWidget('tvAddress')
        liAdr = self.singleAddress.getAddress(iAdrNumber)
        if liAdr:
            self.setTextbuffer(eAdrField,liAdr)
        else:
            self.setTextbuffer(eAdrField,' ')

    #   choose begin Staff button
    def on_bChooseBeginStaff_clicked(self, event):
        adr = cuon.Staff.staff.staffwindow(self.allTables)
        adr.setChooseEntry('chooseStaff', self.getWidget( 'eBeginStaffNumber'))
        
        
    # signals from entry eBeginStaffNumber
    def on_eBeginStaffNumber_changed(self, event):
        print 'eBeginStaffNumber changed'
        eAdrField = self.getWidget('eBeginStaffName')
        cAdr = self.singleStaff.getFullName( self.getChangedValue('eBeginStaffNumber'))
        if cAdr:
            eAdrField.set_text(cAdr)
        else:
            eAdrField.set_text(' ') 
    #   choose ends Staff button
    def on_bChooseEndsStaff_clicked(self, event):
        adr = cuon.Staff.staff.staffwindow(self.allTables)
        adr.setChooseEntry('chooseStaff', self.getWidget( 'eEndsStaffNumber'))
        
    # signals from entry eEndsStaffNumber
    def on_eEndsStaffNumber_changed(self, event):
        print 'eEndsStaffNumber changed'
        eAdrField = self.getWidget('eEndsStaffName')
        cAdr = self.singleStaff.getFullName(self.getChangedValue('eEndsStaffNumber'))
        if cAdr:
            eAdrField.set_text(cAdr)
        else:
            eAdrField.set_text(' ') 


    def on_bChooseBotany_clicked(self, event):
        adr = cuon.Garden.botany.botanywindow(self.allTables)
        adr.setChooseEntry('chooseBotany', self.getWidget( 'ePlantBotanyNumber'))
        
    # signals from entry eEndsStaffNumber
    def on_ePlantBotanyNumber_changed(self, event):
        print 'eBotanyNumber changed'
        eAdrField = self.getWidget('eBotanyName')
        cAdr = self.singleBotany.getBotanyName(self.getChangedValue('ePlantBotanyNumber'))
        if cAdr:
            eAdrField.set_text(cAdr)
        else:
            eAdrField.set_text(' ') 



    # search button
    def on_bSearch_clicked(self, event):
        self.searchHibernation()


    def on_eFindNumber_editing_done(self, event):
        print 'Find Number'
        self.searchHibernation()

    def on_eFindNumber_key_press_event(self, entry,event):
        if self.checkKey(event,'NONE','Return'):
            self.searchHibernation()
            
    def on_eFindDesignation_editing_done(self, event):
        print 'Find Designation'
        self.searchHibernation()

    def on_eFindDesignation_key_press_event(self, entry,event):
        if self.checkKey(event,'NONE','Return'):
            self.searchHibernation()
        


    def searchHibernation(self):
        self.out( 'Searching ....', self.ERROR)
        sNumber = self.getWidget('eFindNumber').get_text()
        sDesignation = self.getWidget('eFindDesignation').get_text()
        self.out('Name and City = ' + sNumber + ', ' + sDesignation, self.ERROR)
        
        #self.singleHibernation.sWhere = 'where number ~* \'.*' + sNumber + '.*\' and designation ~* \'.*' + sDesignation + '.*\''
        liSearch = ['number',sNumber, 'designation', sDesignation]
        self.singleHibernation.sWhere = self.getWhere(liSearch)
        self.out(self.singleHibernation.sWhere, self.ERROR)
        self.refreshTree()


    def on_bDMS_clicked(self, event):
        self.out('bDMS clicked')
        if self.singleHibernation.ID > 0:
            print 'ModulNumber', self.ModulHibernationNumber
            Dms = cuon.DMS.dms.dmswindow(self.allTables, self.ModulHibernationNumber, {'1':self.singleHibernation.ID})
        
    def on_bPlantDMS_clicked(self, event):
        self.out('bPlantDMS clicked')
        if self.singleHibernationPlant.ID > 0:
            print 'ModulNumber', self.ModulHibernationPlantNumber
            Dms = cuon.DMS.dms.dmswindow(self.allTables, self.ModulHibernationPlantNumber, {'1':self.singleHibernation.ID})
        
    def refreshTree(self):
        self.singleHibernation.disconnectTree()
        self.singleHibernationPlant.disconnectTree()
        
        if self.tabOption == self.tabHibernation:
            self.singleHibernation.connectTree()
            self.singleHibernation.refreshTree()

        elif self.tabOption == self.tabPlant:
            self.singleHibernationPlant.sWhere  ='where hibernation_number = ' + `int(self.singleHibernation.ID)`
            self.singleHibernationPlant.connectTree()
            self.singleHibernationPlant.refreshTree()

   


         
    def tabChanged(self):
        print 'tab changed to :'  + str(self.tabOption)
        self.setTreeVisible(True)
        if self.tabOption == self.tabHibernation:
            #Address
            self.disableMenuItem('tabs')
            self.enableMenuItem('Hibernation')
            print 'Seite 0'
            self.editAction = 'editHibernation'
            
        elif self.tabOption == self.tabPlant:
            #Partner
            self.disableMenuItem('tabs')
            self.enableMenuItem('Plant')
            self.editAction = 'editHibernationPlant'
            print 'Seite 1'
            
     
        # refresh the Tree
        self.refreshTree()
        self.enableMenuItem(self.editAction)
        self.editEntries = False
