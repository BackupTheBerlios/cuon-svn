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
import cuon.Order.order
import cuon.DMS.documentTools

import cuon.DMS.dms
import SingleHibernation

import SingleHibernationPlant
import SingleBotany
import base64
import os
import time

class hibernationwindow(chooseWindows):

    
    def __init__(self, allTables):

        chooseWindows.__init__(self)

        self.loadGlade('hibernation.xml', 'HibernationMainwindow')
        #self.win1 = self.getWidget('HibernationMainwindow')
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
        
        self.singleHibernation.setTree(self.xml.get_widget('tree1') )
        self.singleHibernation.sWhere  = ' where address.id = addressnumber'
        
         #singleHibernationPlant
        
        self.loadEntries(self.EntriesHibernationsPlant)
        self.singleHibernationPlant.setEntries(self.getDataEntries( self.EntriesHibernationsPlant) )
        self.singleHibernationPlant.setGladeXml(self.xml)
##        self.singleHibernationPlant.setTreeFields( ['plant_number','botany_number' ] )
##        self.singleHibernationPlant.setStore( gtk.ListStore(gobject.TYPE_UINT, gobject.TYPE_UINT, gobject.TYPE_UINT) ) 
##        self.singleHibernationPlant.setTreeOrder('plant_number')
#        self.singleHibernationPlant.setListHeader([''])

        self.singleHibernationPlant.sWhere  ='where hibernation_number = ' + `int(self.singleHibernation.ID)` + ' and botany.id = botany_number'
            
        self.singleHibernationPlant.setTree(self.xml.get_widget('tree1') )
  
    
        

        # Menu-items
        self.initMenuItems()

        # Close Menus for Tab

        self.addEnabledMenuItems('tabs','hibernation1')
        self.addEnabledMenuItems('tabs','plant1')
        #self.addEnabledMenuItems('tabs','mi_sales1')


        # seperate Menus
        self.addEnabledMenuItems('Hibernation','hibernation1')
        self.addEnabledMenuItems('Plant','plant1')
        #self.addEnabledMenuItems('sales','mi_sales1')

        
        # enabledMenues for Hibernation
        self.addEnabledMenuItems('editHibernation','new1', self.dicUserKeys['new'])
        self.addEnabledMenuItems('editHibernation','clear1', self.dicUserKeys['delete'])
        self.addEnabledMenuItems('editHibernation','print1', self.dicUserKeys['print'])
        self.addEnabledMenuItems('editHibernation','edit1',self.dicUserKeys['edit'])

        # enabledMenues for Hibernation_plant
        self.addEnabledMenuItems('editHibernationPlant','PlantNew1', self.dicUserKeys['new'])
        self.addEnabledMenuItems('editHibernationPlant','PlantClear1', self.dicUserKeys['delete'])
        #self.addEnabledMenuItems('editHibernationPlant','PlantPrint1', self.dicUserKeys['hibernation_plant_print'])
        self.addEnabledMenuItems('editHibernationPlant','PlantEdit1',self.dicUserKeys['edit'])

        # enabledMenues for Save 
        self.addEnabledMenuItems('editSave','PlantSave1', self.dicUserKeys['save'])
        self.addEnabledMenuItems('editSave','save1', self.dicUserKeys['save'])


        # tabs from notebook
        self.tabHibernation = 0
        self.tabPlant = 1
        
        # start
        
        self.tabChanged()

##        # enabled menus for Hibernation
##        self.addEnabledMenuItems('editHibernation','new1')
##        self.addEnabledMenuItems('editHibernation','clear1')
##        self.addEnabledMenuItems('editHibernation','print1')
##
##        # enabled menus for Hibernation_Plant
##        self.addEnabledMenuItems('editHibernationPlant','PlantNew1')
##        self.addEnabledMenuItems('editHibernationPlant','PlantClear1')

        
        
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
        self.doEdit = self.noEdit

         
        
    def on_new1_activate(self, event):
        print "new Hibernations v2"
        self.doEdit = self.tabHibernation
        self.singleHibernation.newRecord()
        self.setEntriesEditable(self.EntriesHibernations, True)
        NewNumber = self.rpc.callRP('Garden.getNewHibernationNumber', self.dicUser)
        self.getWidget('eHibernationNumber').set_text(`NewNumber`)
        
        self.getWidget('eHibernationNumber').grab_focus()
        

    def on_edit1_activate(self, event):
        self.doEdit = self.tabHibernation
        self.setEntriesEditable(self.EntriesHibernations, True)
        self.getWidget('eHibernationNumber').grab_focus()
        
    def on_clear1_activate(self, event):
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
        self.doEdit = self.noEdit
        

        self.singleHibernationPlant.hibernationID = self.singleHibernation.ID
        self.singleHibernationPlant.save()
        self.setEntriesEditable(self.EntriesHibernationsPlant, False)

        self.tabChanged()
        
    def on_PlantNew1_activate(self, event):
        print "new Partner Hibernations v2"
        self.doEdit = self.tabPlant

        self.singleHibernationPlant.newRecord()
        ePN1 = self.getNewPlantNumber()
        
            
        
        self.getWidget('ePlantNumber').set_text(`ePN1`)
        self.setEntriesEditable(self.EntriesHibernationsPlant, True)

    def on_PlantEdit1_activate(self, event):
        self.doEdit = self.tabPlant
     
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
        self.showPdf(Pdf, self.dicUser)
        
        #Pdf = hibernation_incoming_document.hibernation_incoming_document(dicOrder)
        
    def on_print_pickup_document1_activate(self, event):
        dicOrder = {}
        print "Start print pickup document 1"
        
        dicOrder['pickupNumber'] = self.rpc.callRP('Garden.getPickupNumber',self.singleHibernation.ID, self.dicUser)
        print "Start print pickup document 2"

        dicOrder['orderNumber'] = self.singleHibernation.ID
        print "Start print incoming document 3"

        Pdf = self.rpc.callRP('Report.server_hibernation_pickup_document', dicOrder, self.dicUser)
        self.showPdf(Pdf, self.dicUser)    
        
    def on_print_invoice1_activate(self, event):
        dicOrder = {}
        print "Start print invoice 1"
        
        dicOrder['pickupNumber'] = self.rpc.callRP('Garden.getPickupNumber',self.singleHibernation.ID, self.dicUser)
        
        dicOrder['orderNumber'] = self.singleHibernation.ID
        dicOrder['orderModulNumber'] = self.self.ModulHibernationNumber
        
                 
        ord = cuon.Order.order.orderwindow(self.allTables, dicOrder)
        
    def on_print_outgoing_document1_activate(self, event):
        dicOrder = {}
        #Pdf = hibernation_outgoing_document.hibernation_outgoing_document(dicOrder)



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
        bot = cuon.Garden.botany.botanywindow(self.allTables)
        bot.setChooseEntry('chooseBotany', self.getWidget( 'ePlantBotanyNumber'))
        
    # signals from entry eEndsStaffNumber
    def on_ePlantBotanyNumber_changed(self, event):
        print 'eBotanyNumber changed'
        eAdrField = self.getWidget('eBotanyName')
        cAdr = self.singleBotany.getBotanyName(self.getChangedValue('ePlantBotanyNumber'))
        if cAdr:
            eAdrField.set_text(cAdr)
        else:
            eAdrField.set_text(' ') 


    def on_bSetSequence_clicked(self, event):
        print 'Set Sequence clicked'
        sSeq = self.getWidget('eSequence').get_text()
        nSeq = self.getCheckedValue(sSeq,'int')
        if not nSeq > 0:
            print nSeq
            year = time.localtime(time.time())[0]
            print year
            newSeq = self.rpc.callRP('Garden.getNewSequenceNumber', year, self.dicUser) + 1
            
            print 'nSeq2 = ', newSeq
            if newSeq > 0:
                self.getWidget('eSequence').set_text(`newSeq`)
                if self.getWidget('eBeginDate').get_text() == '':
                    
                    sDate = self.getCheckedValue(time.localtime(time.time()),'date')
                    print 'sDate = ', sDate
                    
                    self.getWidget('eBeginDate').set_text(self.getCheckedValue(sDate,'toStringDate' ))
                    
      
    # goto Address 
    def on_bGotoAddress_clicked(self, event):
        adr = cuon.Addresses.addresses.addresswindow(self.allTables, self.singleAddress.ID)
        
    # search button
    def on_bSearch_clicked(self, event):
        self.searchHibernation()


    def on_eFindNumber_editing_done(self, event):
        print 'Find Number'
        self.searchHibernation()

    def on_eFindButton_key_press_event(self, entry,event):
        if self.checkKey(event,'NONE','Return'):
            self.searchHibernation()
            
    
    # goto Botany
    def on_bGotoBotany_clicked(self, event):
        if self.singleBotany.ID > 0:
            bot = cuon.Garden.botany.botanywindow(self.allTables, self.singleBotany.ID)

    def searchHibernation(self):
        self.out( 'Searching ....', self.ERROR)
        sNumber = self.getWidget('eFindNumber').get_text()
        sAddressLastname = self.getWidget('eFindDesignation').get_text()
        #self.out('Name and City = ' + sNumber + ', ' + sAddressLastname, self.ERROR)
        
        #self.singleHibernation.sWhere = 'where number ~* \'.*' + sNumber + '.*\' and designation ~* \'.*' + sDesignation + '.*\''
        sSeq = self.getWidget('eFindSequence').get_text()
        liSearch = []
        if sNumber:
            liSearch.append('hibernation_number')
            liSearch.append(sNumber)
        if sSeq:
            liSearch.append('sequence_of_stock')
            try:
                liSearch.append(int(sSeq))
            except:
                liSearch.append(0)
            
        if sAddressLastname:
            liSearch.append('address.lastname')
            liSearch.append(sAddressLastname)
        bHR = self.getWidget('cbSearchHibReady').get_active()
        bIW = self.getWidget('cbSearchInvoiceWrote').get_active()
        
            
        print 'bHR = ', bHR
        print 'bIW = ', bIW
        liSearch.append('status_ready')
        liSearch.append(bHR)
        liSearch.append('status_invoice_printed')
        liSearch.append(bIW)
        
        self.singleHibernation.sWhere = self.getWhere(liSearch) + ' and address.id = addressnumber'
        self.out('Hibernation sWhere = ' + `self.singleHibernation.sWhere`)
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
     
  
    def on_bDupOrder_clicked(self, event):
        self.printOut('bDupOrder pressed')
        # first load new OrderNumber
        NewNumber = self.rpc.callRP('Garden.getNewHibernationNumber', self.dicUser)
        # then dup EntriesHibernations
        oldHibID = self.singleHibernation.ID
        dicEntries = self.singleHibernation.readEntries()
        self.out(dicEntries)
        oldHibernationNumber = 0
        if dicEntries:
            
            # replace Values
            for sField in dicEntries:
                print sField
                print dicEntries[sField]
                print '--------------------------'
                if sField == 'hibernation_number':
                    oldHibernationNumber = dicEntries[sField][0] 
                    print 'set new Number'
                    dicEntries[sField][0] = NewNumber
                elif sField == 'addressnumber':
                    pass
                elif sField == 'client':
                    pass
                elif dicEntries[sField][1] == u'int':
                    print 'Field ist int'
                    dicEntries[sField][0] = 0
                    
                elif dicEntries[sField][1] == u'float':
                    print 'Field ist float'
                    dicEntries[sField][0] = 0.0
                
                elif dicEntries[sField][1] == u'bool':
                    print 'Field ist bool'
                    dicEntries[sField][0] = False

                elif dicEntries[sField][1] == u'text':
                    print 'Field ist text'
                    
                elif dicEntries[sField][1] == u'string':
                    print 'Field ist string'
                    dicEntries[sField][0] = ''
                elif dicEntries[sField][1] == u'date':
                    print 'Field ist date'
                    dicEntries[sField][0] = ''   
                else:
                    dicEntries[sField][0] = ''
                
        self.out(dicEntries)
        # Now save the values:
        self.singleHibernation.ID = -1
        newID = self.singleHibernation.saveExternalData(dicEntries)
        print 'newID = ', newID
        #now add the plants
        sSql = 'select id from hibernation_plant where hibernation_number = ' + `oldHibID`
        sSql += ' and client = ' + `self.dicUser['client']` + " and status != 'delete' "
        liIds = self.rpc.callRP('Database.executeNormalQuery',sSql, self.dicUser)
        self.out(liIds)
        if liIds:
            for plantid in range(len(liIds)):
                liRecord = self.singleHibernationPlant.load(liIds[plantid]['id'])
                self.out('liRecord = ')
                self.out(liRecord)
                self.out('-----------------------------------------------')
                dicEntries = {}
                dicEntries['price_last_year'] = [liRecord[0]['price'],u'float']
                dicEntries['price'] = [0.0,u'float']
                dicEntries['hibernation_number'] = [newID,u'int']
                dicEntries['plant_notice'] = [liRecord[0]['plant_notice'],u'string']
                dicEntries['botany_number'] = [liRecord[0]['botany_number'],u'int']
                dicEntries['diameter'] = [liRecord[0]['diameter'],u'float']
                #ePN1 = self.getNewPlantNumber()
                dicEntries['plant_number'] = [0,u'int']

                self.singleHibernationPlant.ID = -1
                newPlantID = self.singleHibernationPlant.saveExternalData(dicEntries)
                print 'newPlantID = ', newPlantID
                
                #self.singleHibernationPlant.ID = newPlantID
                #self.singleHibernationPlant.load(newPlantID)
                
                


                
                    
                    

            
                    
                
                
        
            
        #restore the values
        self.singleHibernation.ID = oldHibID
        self.singleHibernation.load(oldHibID)
        self.refreshTree()
        
    def on_bReorgPlantnumber_clicked(self, event):
        print 'bReorgPlantNumber pressed'
        self.rpc.callRP('Garden.reorgPlantNumber',self.singleHibernation.ID, self.dicUser)
        
        
    def saveData(self):
        print 'save Hibernation'
        if self.doEdit == self.tabHibernation:
            print 'save 1'
            self.on_save1_activate(None)
        elif self.doEdit == self.tabPlant:
            print 'save 2'
            self.on_PlantSave1_activate(None)
            
    def getNewPlantNumber(self):
        # set ePlantNumber + 1
        ePN1 = 0
        ePN = self.singleHibernationPlant.getLastNumber(self.singleHibernation.ID)
        print 'ePN = ', ePN
        try:
            if ePN and int(ePN) > 0:
                
                ePN1 = ePN + 1
            else:
                ePN1 = 1
        except:
            ePN1 = 1
        return ePN1
        
        
    def refreshTree(self):
        self.singleHibernation.disconnectTree()
        self.singleHibernationPlant.disconnectTree()
        
        if self.tabOption == self.tabHibernation:
            self.singleHibernation.connectTree()
            self.singleHibernation.refreshTree()

        elif self.tabOption == self.tabPlant:
            self.singleHibernationPlant.sWhere  ='where hibernation_number = ' + `int(self.singleHibernation.ID)`+ ' and botany.id = botany_number'
            self.singleHibernationPlant.connectTree()
            self.singleHibernationPlant.refreshTree()

   


         
    def tabChanged(self):
        print 'tab changed to :'  + str(self.tabOption)
        self.setTreeVisible(True)
        if self.tabOption == self.tabHibernation:
            #Address
            self.disableMenuItem('tabs')
            self.enableMenuItem('Hibernation','editHibernation','hibernation1' )
            
            print 'Seite 0'
            self.editAction = 'editHibernation'
            
            
        elif self.tabOption == self.tabPlant:
            #Partner
            self.disableMenuItem('tabs')
            self.enableMenuItem('Plant','editHibernationPlant','plant1')
            self.editAction = 'editHibernationPlant'
            print 'Seite 1'
            
     
        # refresh the Tree
        self.refreshTree()
        self.enableMenuItem(self.editAction)
        self.editEntries = False
