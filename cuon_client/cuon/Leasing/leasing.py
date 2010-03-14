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
from types import *
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import gobject

from cuon.Databases.SingleData import SingleData
import SingleLeasing
#import SingleLeasingPurchase
#import SingleLeasingale
#import SingleLeasingWebshop
#import SingleLeasingtock
#import SingleLeasingParts


import logging
from cuon.Windows.chooseWindows  import chooseWindows
import cuon.Addresses.addresses
import cuon.Addresses.SingleAddress
import cuon.DMS.documentTools
import cuon.DMS.dms




class leasingwindow(chooseWindows):

    
    def __init__(self, allTables):

        chooseWindows.__init__(self)
        self.loadGlade('leasing.xml', 'LeasingMainwindow')
        #self.win1 = self.getWidget('LeasingMainwindow')
        self.win1.maximize()
        self.setStatusBar('vb_main')
        self.oDocumentTools = cuon.DMS.documentTools.documentTools()
        self.ModulNumber = self.MN['Leasing']        
        self.allTables = allTables
        self.singleLeasing = SingleLeasing.SingleLeasing(allTables)
#        self.singleLeasingPurchase = SingleLeasingPurchase.SingleLeasingPurchase(allTables)
#        self.singleLeasingParts = SingleLeasingParts.SingleLeasingParts(allTables)
#        self.singleLeasingales = SingleLeasingale.SingleLeasingale(allTables)
#        self.singleLeasingWebshop = SingleLeasingWebshop.SingleLeasingWebshop(allTables)
#        self.singleLeasingtock = SingleLeasingtock.SingleLeasingtock(allTables)
        self.singleAddress = cuon.Addresses.SingleAddress.SingleAddress(allTables)
        try:
            self.singleBotany = cuon.Garden.SingleBotany.SingleBotany(allTables)
        except:
            pass
            
        self.singleMaterialGroup = cuon.Leasing.SingleMaterialgroups.SingleMaterialgroups(allTables)
        # self.singleLeasing.loadTable()
              
        self.EntriesLeasing = 'Leasing.xml'
#        self.EntriesLeasingPurchase = 'Leasing_purchase.xml'
#        self.EntriesLeasingParts = 'Leasing_parts.xml'
#        self.EntriesLeasingSales = 'Leasing_sales.xml'
#        self.EntriesLeasingWebshop = 'Leasing_webshop.xml'
#        self.EntriesLeasingStock = 'Leasing_stock.xml'
#                
        
        #singleLeasing
 
 
        self.loadEntries(self.EntriesLeasing)
        self.singleLeasing.setEntries(self.getDataEntries( self.EntriesLeasing) )
        self.singleLeasing.setGladeXml(self.xml)
        self.singleLeasing.setTreeFields( ['number', 'designation'] )
#        self.singleLeasing.setStore( gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING,   gobject.TYPE_UINT) ) 
        self.singleLeasing.setTreeOrder('number, designation')
        self.singleLeasing.setTree(self.xml.get_widget('tv_Leasing') )
        self.singleLeasing.setListHeader(['number', 'designation', ])
        
#        
#        #singleLeasingParts
#        
#        self.loadEntries(self.EntriesLeasingParts)
#        self.singleLeasingParts.setEntries(self.getDataEntries( self.EntriesLeasingParts) )
#        self.singleLeasingParts.setGladeXml(self.xml)
#        self.singleLeasingParts.setTreeFields( ['part_id','designation', 'quantities'] )
#        self.singleLeasingParts.setListHeader(['Leasing', 'Designation','Quantities' ])
#        self.singleLeasingParts.setStore( gtk.ListStore(gobject.TYPE_UINT, gobject.TYPE_STRING, gobject.TYPE_STRING,  gobject.TYPE_UINT) ) 
#        self.singleLeasingParts.setTreeOrder('part_id')
##        self.singleLeasingParts.setListHeader([''])
#
#        self.singleLeasingParts.sWhere  ='where Leasing_id = ' + `self.singleLeasing.ID`
#        self.singleLeasingParts.setTree(self.xml.get_widget('tv_parts') )
#  
#         #singleLeasingPurchase
#        
#        self.loadEntries(self.EntriesLeasingPurchase)
#        self.singleLeasingPurchase.setEntries(self.getDataEntries( self.EntriesLeasingPurchase) )
#        self.singleLeasingPurchase.setGladeXml(self.xml)
#        self.singleLeasingPurchase.setTreeFields( ['Leasing_id','vendorsnumber', 'vendorsdesignation',  'unitprice', 'last_date'] )
#        self.singleLeasingPurchase.setListHeader(['Leasing', 'Vendor ID','Designation','Price', 'Last Date' ])
#        self.singleLeasingPurchase.setStore( gtk.ListStore(gobject.TYPE_UINT, gobject.TYPE_STRING, gobject.TYPE_STRING,  gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_UINT) ) 
#        self.singleLeasingPurchase.setTreeOrder('unitprice asc,vendorsnumber')
##        self.singleLeasingPurchase.setListHeader([''])
#
#        self.singleLeasingPurchase.sWhere  ='where Leasing_id = ' + `self.singleLeasing.ID`
#        self.singleLeasingPurchase.setTree(self.xml.get_widget('tv_purchase') )
#  
#     #singleLeasingales
#        
#        self.loadEntries(self.EntriesLeasingSales)
#        self.singleLeasingales.setEntries(self.getDataEntries( self.EntriesLeasingSales) )
#        self.singleLeasingales.setGladeXml(self.xml)
#        self.singleLeasingales.setTreeFields( ['designation'] )
#        self.singleLeasingales.setStore( gtk.ListStore(gobject.TYPE_STRING,  gobject.TYPE_UINT) ) 
#        self.singleLeasingales.setTreeOrder('designation')
#        self.singleLeasingales.setListHeader([_('Designation')])
#
#        self.singleLeasingales.sWhere  ='where Leasing_number = ' + `self.singleLeasing.ID`
#        self.singleLeasingales.setTree(self.xml.get_widget('tv_sale') )
#
#  
#  #singleLeasingWebshop
#        
#        self.loadEntries(self.EntriesLeasingWebshop)
#        self.singleLeasingWebshop.setEntries(self.getDataEntries( self.EntriesLeasingWebshop) )
#        self.singleLeasingWebshop.setGladeXml(self.xml)
###        self.singleLeasingWebshop.setTreeFields( ['Leasing_number'] )
# ##       self.singleLeasingWebshop.setStore( gtk.ListStore(gobject.TYPE_STRING,  gobject.TYPE_UINT) ) 
#  ##      self.singleLeasingWebshop.setTreeOrder('Leasing_number')
#   ##     self.singleLeasingWebshop.setListHeader([_('Leasing')])
#
#        self.singleLeasingWebshop.sWhere  ='where Leasing_number = ' + `self.singleLeasing.ID`
#        #self.singleLeasingWebshop.setTree(self.xml.get_widget('tree1') )
#
#    #singleLeasingtock
#        
#        self.loadEntries(self.EntriesLeasingStock)
#        self.singleLeasingtock.setEntries(self.getDataEntries( self.EntriesLeasingStock ))
#        self.singleLeasingtock.setGladeXml(self.xml)
###        self.singleLeasingtock.setTreeFields( ['designation'] )
###        self.singleLeasingtock.setStore( gtk.ListStore(gobject.TYPE_STRING,  gobject.TYPE_UINT) ) 
###        self.singleLeasingtock.setTreeOrder('designation')
###        self.singleLeasingtock.setListHeader([_('Designation')])
#
#        self.singleLeasingtock.sWhere  ='where Leasing_id = ' + `self.singleLeasing.ID`
#        #self.singleLeasingtock.setTree(self.xml.get_widget('tree1') )
#  
#        

        # Menu-items
        self.initMenuItems()

        # Close Menus for Tab

        self.addEnabledMenuItems('tabs','mi_Leasing1')
        self.addEnabledMenuItems('tabs','mi_purchase1')
        self.addEnabledMenuItems('tabs','mi_sales1')


        # seperate Menus
        self.addEnabledMenuItems('Leasing','mi_Leasing1')
#        self.addEnabledMenuItems('purchase','mi_purchase1')
#        self.addEnabledMenuItems('sales','mi_sales1')
#        self.addEnabledMenuItems('sales','parts_list1')
#        
        # enabledMenues for Leasing
        self.addEnabledMenuItems('editLeasing','new1', self.dicUserKeys['Leasing_new'])
        self.addEnabledMenuItems('editLeasing','delete1', self.dicUserKeys['Leasing_delete'])
        self.addEnabledMenuItems('editLeasing','print1', self.dicUserKeys['Leasing_print'])
        self.addEnabledMenuItems('editLeasing','edit1',self.dicUserKeys['Leasing_edit'])
        
#        # enabledMenues for LeasingParts
#        self.addEnabledMenuItems('editLeasingParts','PartsListNew', self.dicUserKeys['Leasing_new'])
#        self.addEnabledMenuItems('editPLeasingarts','PartsListDelete')
#        self.addEnabledMenuItems('editLeasingParts','PartsListEdit', self.dicUserKeys['Leasing_edit'])
#    
#
#        # enabledMenues for LeasingPurchase
#        self.addEnabledMenuItems('editLeasingPurchase','PurchaseNew1', self.dicUserKeys['Leasing_purchase_new'])
#        self.addEnabledMenuItems('editLeasingPurchase','PurchaseDelete1')
#        self.addEnabledMenuItems('editLeasingPurchase','PurchaseEdit1', self.dicUserKeys['Leasing_purchase_edit'])
#    
#       # enabledMenues for Leasingales
#        self.addEnabledMenuItems('editLeasingales','SalesNew1')
#        self.addEnabledMenuItems('editLeasingales','SalesDelete1')
#        self.addEnabledMenuItems('editLeasingales','SalesEdit1')
#
#       # enabledMenues for LeasingWebshop
#        self.addEnabledMenuItems('editLeasingWebshop','WebshopClear1')
#        self.addEnabledMenuItems('editLeasingWebshop','WebshopEdit1')
#
#       # enabledMenues for Leasingtock
#        self.addEnabledMenuItems('editLeasingtock','StockClear1')
#        self.addEnabledMenuItems('editLeasingtock','StockEdit1')

        # enabledMenues for Save 
        self.addEnabledMenuItems('editSave','save1', self.dicUserKeys['Leasing_save'])
#        self.addEnabledMenuItems('editSave','PartsListSave', self.dicUserKeys['Leasing_save'])
#        self.addEnabledMenuItems('editSave','PurchaseSave1', self.dicUserKeys['Leasing_save'])
#        self.addEnabledMenuItems('editSave','SalesSave1', self.dicUserKeys['Leasing_save'])
#        self.addEnabledMenuItems('editSave','WebshopSave1', self.dicUserKeys['Leasing_save'])
#        self.addEnabledMenuItems('editSave','StockSave1', self.dicUserKeys['Leasing_save'])

        # tabs from notebook
        self.tabLeasing = 0
        self.tabParts = 1
        self.tabPurchase = 2
        self.tabSales = 3
        self.tabWebshop = 4
        self.tabStock = 5
        

        # start
        
        self.tabChanged()

        # enabled menus for Leasing
        self.addEnabledMenuItems('editLeasing','new1')
        self.addEnabledMenuItems('editLeasing','clear1')
        self.addEnabledMenuItems('editLeasing','print1')

#        # enabled menus for Leasing_purchase
#        self.addEnabledMenuItems('editLeasingPurchase','PurchaseNew1')
#        self.addEnabledMenuItems('editLeasingPurchase','PurchaseClear1')

       
        self.win1.add_accel_group(self.accel_group)
    #Menu File
              
    def on_quit1_activate(self, event):
        print "exit Leasing v2"
        self.closeWindow()
  

    #Menu Leasing
  
    def on_save1_activate(self, event):
        print "save Leasing v2"
        self.singleLeasing.save()
        self.setEntriesEditable(self.EntriesLeasing, False)
        self.tabChanged()
         
        
    def on_new1_activate(self, event):
        print "new Leasing v2"
        self.singleLeasing.newRecord()
        self.setEntriesEditable(self.EntriesLeasing, True)
        

    def on_edit1_activate(self, event):
        self.setEntriesEditable(self.EntriesLeasing, True)

    def on_delete1_activate(self, event):
        print "delete Leasing v2"
        self.singleLeasing.deleteRecord()


  #Menu Parts
        
   
    def on_parts_list_save_activate(self, event):
        print "save Parts Leasing v2"
        self.singleLeasingParts.LeasingID = self.singleLeasing.ID
        self.singleLeasingParts.save()
        self.setEntriesEditable(self.EntriesLeasingParts, False)

        self.tabChanged()
        
    def on_parts_list_new_activate(self, event):
        print "new Parts Leasing v2"
        self.singleLeasingParts.newRecord()
        self.setEntriesEditable(self.EntriesLeasingParts, True)

    def on_parts_list_edit_activate(self, event):
        self.setEntriesEditable(self.EntriesLeasingParts, True)

    def on_parts_list_delete_activate(self, event):
        print "delete Parts Leasing v2"
        self.singleLeasingParts.deleteRecord()


  #Menu Purchase
        
   
    def on_PurchaseSave1_activate(self, event):
        print "save Partner Leasing v2"
        self.singleLeasingPurchase.LeasingID = self.singleLeasing.ID
        self.singleLeasingPurchase.save()
        self.setEntriesEditable(self.EntriesLeasingPurchase, False)

        self.tabChanged()
        
    def on_PurchaseNew1_activate(self, event):
        print "new Purchase Leasing v2"
        self.singleLeasingPurchase.newRecord()
        self.setEntriesEditable(self.EntriesLeasingPurchase, True)

    def on_PurchaseEdit1_activate(self, event):
        self.setEntriesEditable(self.EntriesLeasingPurchase, True)

    def on_PurchaseDelete1_activate(self, event):
        print "delete Purchase Leasing v2"
        self.singleLeasingPurchase.deleteRecord()

    #Leasing Sales
    def on_SalesSave1_activate(self, event):
        print "save Sales Leasing v2"
        
        self.singleLeasingales.LeasingNumber = self.singleLeasing.ID
        self.singleLeasingales.save()
        self.setEntriesEditable(self.EntriesLeasingSales, False)

        self.tabChanged()
        
    def on_SalesNew1_activate(self, event):
        print "new Partner Leasing v2"
        self.singleLeasingales.newRecord()
        self.setEntriesEditable(self.EntriesLeasingSales, True)

    def on_SalesEdit1_activate(self, event):
        self.setEntriesEditable(self.EntriesLeasingSales, True)

    def on_SalesDelete1_activate(self, event):
        print "delete Sales Leasing v2"
        self.singleLeasingales.deleteRecord()


 #Leasing Webshop
    def on_WebshopSave1_activate(self, event):
        print "save  Leasing Webshop v2"
        print "Leasing ID = ", self.singleLeasing.ID
        self.singleLeasingWebshop.LeasingNumber = self.singleLeasing.ID
        self.singleLeasingWebshop.save()
        self.setEntriesEditable(self.EntriesLeasingWebshop, False)

        self.tabChanged()
        
    def on_WebshopNew1_activate(self, event):
        print "new Partner Leasing v2"
        self.singleLeasingWebshop.newRecord()
        self.setEntriesEditable(self.EntriesLeasingWebshop, True)

    def on_WebshopEdit1_activate(self, event):
        self.setEntriesEditable(self.EntriesLeasingWebshop, True)

    def on_WebshopClear1_activate(self, event):
        print "delete Partner Leasing v2"
        self.singleLeasingWebshop.deleteRecord()

    def on_bChooseCategory_clicked(self, event):
        pass
        
 #Leasing Stock
    def on_StockSave1_activate(self, event):
        print "save Partner Leasing v2"
        
        self.singleLeasingtock.LeasingID = self.singleLeasing.ID
        self.singleLeasingtock.save()
        self.setEntriesEditable(self.EntriesLeasingStock, False)

        self.tabChanged()
        
    def on_StockNew1_activate(self, event):
        print "new Partner Leasing v2"
        self.singleLeasingtock.newRecord()
        self.setEntriesEditable(self.EntriesLeasingStock, True)

    def on_StockEdit1_activate(self, event):
        self.setEntriesEditable(self.EntriesLeasingStock, True)

    def on_StockClear1_activate(self, event):
        print "delete Partner Leasing v2"
        self.singleLeasingtock.deleteRecord()



    # Menu Lists

    def on_liLeasingNumber1_activate(self, event):
        self.out( "lists startet")
        Pdf = cuon.Leasing.lists_Leasing_number1.lists_Leasing_number1()

    #Menu pickles_Leasing
    
    def on_one_standard1_activate(self, event):
        pdf = cuon.Leasing.pickles_Leasing.pickles_Leasing(1)
    def on_sp101_activate(self, event):
        pdf = cuon.Leasing.pickles_Leasing.pickles_Leasing(1, 'sp101')
    def on_sp102_activate(self, event):
        pdf = cuon.Leasing.pickles_Leasing.pickles_Leasing(1, 'sp102')
        
    def on_two_standard1_activate(self, event):
        pdf = cuon.Leasing.pickles_Leasing.pickles_Leasing(2)
    def on_sp201_activate(self, event):
        pdf = cuon.Leasing.pickles_Leasing.pickles_Leasing(2, 'sp201')
    def on_sp202_activate(self, event):
        pdf = cuon.Leasing.pickles_Leasing.pickles_Leasing(2, 'sp202')
        
    def on_three_standard1_activate(self, event):
        pdf = cuon.Leasing.pickles_Leasing.pickles_Leasing(3)
    def on_sp301_activate(self, event):
        pdf = cuon.Leasing.pickles_Leasing.pickles_Leasing(3, 'sp301')
    def on_sp302_activate(self, event):
        pdf = cuon.Leasing.pickles_Leasing.pickles_Leasing(3, 'sp302')
        
    def on_four_standard1_activate(self, event):
        pdf = cuon.Leasing.pickles_Leasing.pickles_Leasing(4)
    def on_sp401_activate(self, event):
        pdf = cuon.Leasing.pickles_Leasing.pickles_Leasing(4, 'sp401')
    def on_sp402_activate(self, event):
        pdf = cuon.Leasing.pickles_Leasing.pickles_Leasing(4, 'sp402')
        

    def on_tbNew_clicked(self, event):
        if self.tabOption == self.tabLeasing:
            self.on_new1_activate(event)
        elif self.tabOption == self.tabPurchase:
            self.on_PurchaseNew1_activate(event)
        elif self.tabOption == self.tabSales:
            self.on_SalesNew1_activate(event)
        elif self.tabOption == self.tabWebshop:
            self.on_WebshopNew1_activate(event)
        elif self.tabOption == self.tabStock:
            self.on_StockNew1_activate(event)   
            
    def on_tbEdit_clicked(self, event):
        if self.tabOption == self.tabLeasing:
            self.on_edit1_activate(event)
        elif self.tabOption == self.tabPurchase:
            self.on_PurchaseEdit1_activate(event)
        elif self.tabOption == self.tabSales:
            self.on_SalesEdit1_activate(event)
        elif self.tabOption == self.tabWebshop:
            self.on_WebshopEdit1_activate(event)
        elif self.tabOption == self.tabStock:
            self.on_StockEdit1_activate(event)   
            
    def on_tbSave_clicked(self, event):
        if self.tabOption == self.tabLeasing:
            self.on_save1_activate(event)
        elif self.tabOption == self.tabPurchase:
            self.on_PurchaseSave1_activate(event)
        elif self.tabOption == self.tabSales:
            self.on_SalesSave1_activate(event)
        elif self.tabOption == self.tabWebshop:
            self.on_WebshopSave1_activate(event)
        elif self.tabOption == self.tabStock:
            self.on_StockSave1_activate(event)   
            
    def on_chooseLeasing_activate(self, event):
        # choose Leasing from other Modul
        self.setChooseValue(self.singleLeasing.ID)
        print 'Leasing-ID = ' + `self.singleLeasing.ID`
        self.closeWindow()
  
    def on_tree1_row_activated(self, event, data1, data2):
        print 'DoubleClick tree1'
        self.activateClick('chooseLeasing', event)
    #choose Vendor button
    def on_bChooseVendor_clicked(self, event):
        adr = cuon.Addresses.addresses.addresswindow(self.allTables)
        adr.setChooseEntry('chooseAddress', self.getWidget( 'eAddressNumber'))
        
    # signals from entry eAddressNumber
    
    def on_eAddressNumber_changed(self, event):
        print 'eAdrnbr changed'
        eAdrField = self.getWidget('eAddressField1')
        liAdr = self.singleAddress.getAddress(long(self.getWidget( 'eAddressNumber').get_text()))
        eAdrField.set_text(liAdr[0] + ', ' + liAdr[4])


    # search button
    def on_bSearch_clicked(self, event):
        self.searchLeasing()


    def on_eFindNumber_editing_done(self, event):
        print 'Find Number'
        self.searchLeasing()

    def on_eFindNumber_key_press_event(self, entry,event):
        if self.checkKey(event,'NONE','Return'):
            self.searchLeasing()
            
    def on_eFindDesignation_editing_done(self, event):
        print 'Find Designation'
        self.searchLeasing()

    def on_eFindDesignation_key_press_event(self, entry,event):
        if self.checkKey(event,'NONE','Return'):
            self.searchLeasing()
            
            
    def on_eFindMaterialGroupID_key_press_event(self, entry,event):
        if self.checkKey(event,'NONE','Return'):
            self.searchLeasing()
            
        
    

    def searchLeasing(self):
        self.out( 'Searching ....', self.ERROR)
        sNumber = self.getWidget('eFindNumber').get_text()
        sDesignation = self.getWidget('eFindDesignation').get_text()
        sID = self.getWidget('eFindMaterialGroupID').get_text()
        print "sID  = ",  sID
        
        #self.out('Name and City = ' + sNumber + ', ' + sDesignation, self.ERROR)
        liSearch = []
        if sNumber:
            liSearch.append('number')
            liSearch.append(sNumber)
            
        if sDesignation:
            liSearch.append('designation')
            liSearch.append(sDesignation)
        
        if sID:
            print "material group search"
            liSearch.append('material_group')
            liSearch.append(int(sID))
            
        self.singleLeasing.sWhere = self.getWhere(liSearch)
        #self.out(self.singleLeasing.sWhere, self.ERROR)
        self.refreshTree()


    
    def on_bChooseMaterialGroup_clicked(self, event):
        print 'materialgroup'
        mag = cuon.Leasing.materialgroup.materialgroupwindow(self.allTables)
        mag.setChooseEntry('chooseMaterialgroup', self.getWidget( 'eCategoryNr'))
                             
    def on_eCategoryNr_changed(self, event):
        print 'eCategory changed'
        iMaterialGroup = self.getChangedValue('eCategoryNr')
        sGroupName = self.singleMaterialGroup.getNameAndDesignation(iMaterialGroup)
        if len(sGroupName) > 0:
            self.getWidget('eCategory').set_text(sGroupName)
        else:
            self.getWidget('eCategory').set_text('')
            
            
            
            
    def on_bSearchAssociated_clicked(self, event):
        print 'search associated'
        LeasingAssociated = self.getWidget('cbAssociatedWith').get_active()
        if LeasingAssociated == 1:
            #botany
            bot = cuon.Garden.botany.botanywindow(self.allTables)
            bot.setChooseEntry('chooseBotany',  self.getWidget('eAssociatedNr'))
        
                             
    def on_eAssociatedNr_changed(self, event):
        print 'eAssocsiatedNr changed'
#        
#        iMaterialGroup = self.getChangedValue('eCategoryNr')
#        sGroupName = self.singleMaterialGroup.getNameAndDesignation(iMaterialGroup)
#        if len(sGroupName) > 0:
#            self.getWidget('eAssocsiatedText').set_text(sGroupName)
#        else:
#            self.getWidget('eAssocsiatedText').set_text('')        
#            
        self.on_cbAssociatedWith_changed(event)
            
            
    def on_bGotoAssociated_clicked(self, event):
        if self.getWidget('cbAssociatedWith').get_active() == 1:
            # Botany
            bot = cuon.Garden.botany.botanywindow(self.allTables)
            
    def on_cbAssociatedWith_changed(self, event):
        
        print 'goto associated'
        
        LeasingAssociated = self.getWidget('cbAssociatedWith').get_active()
        if LeasingAssociated == 1:
            print 'cbAssociatedID read'
            #iBotID = self.singleBotany.getAssociatedID(self.singleLeasing.ID)
            #print 'Botany ID = ', iBotID
            #sBotany = self.singleBotany.getBotanyName(iBotID)
            iBotID = self.singleLeasing.firstRecord['associated_id']
            print 'Botany ID = ', iBotID
            sBotany = self.singleBotany.getBotanyName(iBotID)
            if sBotany:
                sBotany = self.singleBotany.getBotanyName(iBotID)
                self.setText2Widget(sBotany,'eAssocsiatedText')
            else:
                self.setText2Widget('','eAssocsiatedText')
                
                
        else:
            self.setText2Widget('','eAssocsiatedText')
            
            
            
    def on_bQuickAppend_clicked(self, event):
        pass
        
        
    
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
        if self.singleLeasing.ID > 0:
            print 'ModulNumber', self.ModulNumber
            Dms = cuon.DMS.dms.dmswindow(self.allTables, self.ModulNumber, {'1':self.singleLeasing.ID})
        
        
    def refreshTree(self):
        self.singleLeasing.disconnectTree()
        self.singleLeasingPurchase.disconnectTree()
        
        if self.tabOption == self.tabLeasing:
            self.singleLeasing.setTreeSensitive(True)
            self.singleLeasing.connectTree()
            self.singleLeasing.refreshTree()
            self.on_cbAssociatedWith_changed(None)
            self.singleLeasing.connectTree()
            self.singleLeasing.refreshTree()
        elif self.tabOption == self.tabParts:
            self.singleLeasingParts.sWhere  ='where Leasing_id = ' + `int(self.singleLeasing.ID)`
            self.singleLeasingParts.connectTree()
            self.singleLeasingParts.refreshTree()
            self.singleLeasingParts.setTreeSensitive(True)   
        elif self.tabOption == self.tabPurchase:
            self.singleLeasingPurchase.sWhere  ='where Leasing_id = ' + `int(self.singleLeasing.ID)`
            self.singleLeasingPurchase.connectTree()
            self.singleLeasingPurchase.refreshTree()
            self.singleLeasingPurchase.setTreeSensitive(True)
        elif self.tabOption == self.tabSales:
            self.singleLeasingales.sWhere  ='where Leasing_number = ' + `int(self.singleLeasing.ID)`
            self.singleLeasingales.connectTree()
            self.singleLeasingales.refreshTree()

        elif self.tabOption == self.tabWebshop:

            self.singleLeasingWebshop.sWhere  ='where Leasing_number = ' + `int(self.singleLeasing.ID)`
            self.singleLeasingWebshop.setEmptyEntries()
            self.singleLeasingWebshop.getFirstRecord()
            
            self.singleLeasingWebshop.fillEntries(self.singleLeasingWebshop.ID)

            
            print "-----------> end tab Webshop"
            

        elif self.tabOption == self.tabStock:
            print "-----------> begin tab Stock"
            
            self.singleLeasingtock.sWhere  ='where Leasing_id = ' + `int(self.singleLeasing.ID)`
            self.singleLeasingWebshop.setEmptyEntries()
            self.singleLeasingtock.getFirstRecord()
            self.singleLeasingtock.LeasingID = self.singleLeasing.ID
            if self.singleLeasingtock.ID > 0:
                self.singleLeasingtock.fillEntries(self.singleLeasingtock.ID)
            else:
                #dicAr = {'Leasing_number':self.singleLeasing.getLeasingNumber(self.singleLeasing.ID)}
                dicAr = {'Leasing_id':self.singleLeasing.ID}
                
                self.singleLeasingtock.fillOtherEntries(dicAr)

            print "-----------> end tab Stock"
 
         
    def tabChanged(self):
        print 'tab changed to :'  + str(self.tabOption)
        
        if self.tabOption == self.tabLeasing:
            #Leasing
            self.disableMenuItem('tabs')
            self.enableMenuItem('Leasing')
            print 'Seite 0'
            self.editAction = 'editLeasing'
            self.setStatusbarText([''])
            
       
        elif self.tabOption == self.tabParts:
            #Parts
            self.disableMenuItem('tabs')
            self.enableMenuItem('Parts')
            self.editAction = 'editLeasingParts'
            print 'Seite 1'
            self.setStatusbarText([self.singleLeasing.sStatus])
            
        elif self.tabOption == self.tabPurchase:
            #Purchase
            self.disableMenuItem('tabs')
            self.enableMenuItem('purchase')
            self.editAction = 'editLeasingPurchase'
            print 'Seite 1'
            self.setStatusbarText([self.singleLeasing.sStatus])
        elif self.tabOption == self.tabSales:
            self.disableMenuItem('tabs')
            self.enableMenuItem('sales')
            self.editAction = 'editLeasingales'
            print 'Seite 2'
            self.setStatusbarText([self.singleLeasing.sStatus])
        elif self.tabOption == self.tabWebshop:
            self.disableMenuItem('tabs')
            self.enableMenuItem('sales')
            self.editAction = 'editLeasingWebshop'
            self.singleLeasingWebshop.setTreeSensitive(False)
            print 'Seite 3'
            self.setStatusbarText([self.singleLeasing.sStatus])
        elif self.tabOption == self.tabStock:
            self.disableMenuItem('tabs')
            self.enableMenuItem('sales')
            self.editAction = 'editLeasingtock'
            self.setStatusbarText([self.singleLeasing.sStatus])
            print 'Seite 4'
            
        # refresh the Tree
        self.refreshTree()
        self.enableMenuItem(self.editAction)
        self.editEntries = False
