# -*- coding: utf-8 -*-
##Copyright (C) [2003]  [Juergen Hamel, D-32584 Loehne]

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
from gtk import TRUE, FALSE
import string

from cuon.Databases.SingleData import SingleData
import SingleOrder
import SingleOrderSupply
import SingleOrderGet
import SingleOrderPosition



import logging
from cuon.Windows.chooseWindows  import chooseWindows
import cuon.Articles.articles
import cuon.Addresses.addresses
import cuon.Addresses.SingleAddress
import cuon.Addresses.SinglePartner

import cuon.Articles.SingleArticle
import cuon.Order.standard_invoice
import cuon.Order.standard_delivery_note
import cuon.Order.standard_pickup_note
import cuon.XMLRPC.xmlrpc




class orderwindow(chooseWindows):
    """
    @author: Juergen Hamel
    @organization: Cyrus-Computer GmbH, D-32584 Loehne
    @copyright: by Juergen Hamel
    @license: GPL ( GNU GENERAL PUBLIC LICENSE )
    @contact: jh@cyrus.de
    """
    
    
    def __init__(self, allTables):

        chooseWindows.__init__(self)

        self.loadGlade('order.xml')
        self.win1 = self.getWidget('OrderMainwindow')
        
        self.allTables = allTables
        self.singleOrder = SingleOrder.SingleOrder(allTables)
        self.singleOrderSupply = SingleOrderSupply.SingleOrderSupply(allTables)
        self.singleOrderGet = SingleOrderGet.SingleOrderGet(allTables)
        self.singleOrderPosition = SingleOrderPosition.SingleOrderPosition(allTables)
        self.singleAddress = cuon.Addresses.SingleAddress.SingleAddress(allTables)
        self.singlePartner = cuon.Addresses.SinglePartner.SinglePartner(allTables)
        
        self.singleArticle = cuon.Articles.SingleArticle.SingleArticle(allTables)
       
        # self.singleOrder.loadTable()
              
        self.EntriesOrder = 'order.xml'
        self.EntriesOrderSupply = 'order_supply.xml'
        self.EntriesOrderGet = 'order_get.xml'
        self.EntriesOrderPosition = 'order_position.xml'
        
        
        
        #singleOrder
        
        self.loadEntries(self.EntriesOrder)
        self.singleOrder.setEntries(self.getDataEntries('order.xml') )
        self.singleOrder.setGladeXml(self.xml)
        self.singleOrder.setTreeFields( ['number', 'designation'] )
        self.singleOrder.setStore( gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING,   gobject.TYPE_UINT) ) 
        self.singleOrder.setTreeOrder('number')
        self.singleOrder.setTree(self.xml.get_widget('tree1') )
        self.singleOrder.setListHeader([_('number'), _('designation') ])
        
         #singleOrderSupply
        
        self.loadEntries(self.EntriesOrderSupply)
        self.singleOrderSupply.setEntries(self.getDataEntries('order_supply.xml') )
        self.singleOrderSupply.setGladeXml(self.xml)
        self.singleOrderSupply.setTreeFields( ['designation' ] )
        self.singleOrderSupply.setStore( gtk.ListStore(gobject.TYPE_STRING,  gobject.TYPE_UINT) ) 
        self.singleOrderSupply.setTreeOrder('designation')
        self.singleOrderSupply.setListHeader([_('Designation')])

        self.singleOrderSupply.sWhere  ='where ordernumber = ' + `self.singleOrder.ID`
        self.singleOrderSupply.setTree(self.xml.get_widget('tree1') )
  
        #singleOrderGet
        
        self.loadEntries(self.EntriesOrderGet)
        self.singleOrderGet.setEntries(self.getDataEntries('order_get.xml') )
        self.singleOrderGet.setGladeXml(self.xml)
        self.singleOrderGet.setTreeFields( ['designation'] )
        self.singleOrderGet.setStore( gtk.ListStore(gobject.TYPE_STRING,  gobject.TYPE_UINT) ) 
        self.singleOrderGet.setTreeOrder('designation')
        self.singleOrderGet.setListHeader([_('Designation')])

        self.singleOrderGet.sWhere  ='where ordernumber = ' + `self.singleOrder.ID`
        self.singleOrderGet.setTree(self.xml.get_widget('tree1') )

        # singlePositions
        
        self.loadEntries(self.EntriesOrderPosition)
        self.singleOrderPosition.setEntries(self.getDataEntries('order_position.xml') )
        self.singleOrderPosition.setGladeXml(self.xml)
        self.singleOrderPosition.setTreeFields( ['designation'] )
        self.singleOrderPosition.setStore( gtk.ListStore(gobject.TYPE_STRING,  gobject.TYPE_UINT) ) 
        self.singleOrderPosition.setTreeOrder('designation')
        self.singleOrderPosition.setListHeader([_('Designation')])

        self.singleOrderPosition.sWhere  ='where orderid = ' + `self.singleOrder.ID`
        self.singleOrderPosition.setTree(self.xml.get_widget('tree1') )
  
        

        # Menu-items
        self.initMenuItems()

        # Close Menus for Tab

        self.addEnabledMenuItems('tabs','order1')
        self.addEnabledMenuItems('tabs','supply1')
        self.addEnabledMenuItems('tabs','gets1')
        self.addEnabledMenuItems('tabs','positions1')


        # seperate Menus
        self.addEnabledMenuItems('order','order1')
        self.addEnabledMenuItems('supply','supply1')
        self.addEnabledMenuItems('gets','gets1')
        self.addEnabledMenuItems('positions','positions1')

        
        # enabledMenues for Order
        self.addEnabledMenuItems('editOrder','new1')
        self.addEnabledMenuItems('editOrder','clear1')
        self.addEnabledMenuItems('editOrder','print1')

        # enabledMenues for Supply
        self.addEnabledMenuItems('editSupply','SupplyNew1')
        self.addEnabledMenuItems('editSuppy','SupplyClear1')
    
       # enabledMenues for Gets
        self.addEnabledMenuItems('editGets','GetsNew1')
        self.addEnabledMenuItems('editGets','GetsClear1')

        # enabledMenues for Positions
        self.addEnabledMenuItems('editPositions','PositionNew1')
        self.addEnabledMenuItems('editPositions','PositionClear1')




        # tabs from notebook
        self.tabOrder = 0
        self.tabSupply = 1
        self.tabGet = 2
        self.tabPosition = 3
        self.tabInvoice = 4

        # start
        
        self.tabChanged()

   
         
         
    #Menu File

    def on_print_invoice1_activate(self, event):
        dicOrder = {}
        dicOrder['orderNumber'] = self.singleOrder.getOrderNumber(self.singleOrder.ID)
        dicOrder['invoiceNumber'] =  self.singleOrder.getInvoiceNumber()        
        invoice = cuon.Order.standard_invoice.standard_invoice(dicOrder)

    def on_print_delivery_note1_activate(self, event):
        print 'delivery note'
        dicOrder = {}
        dicOrder['orderNumber'] = self.singleOrder.getOrderNumber(self.singleOrder.ID)
        dicOrder['deliveryNumber'] =  self.singleOrderSupply.getDeliveryNumber(self.singleOrder.ID)        
        invoice = cuon.Order.standard_delivery_note.standard_delivery_note(dicOrder)
               
    def on_print_pickup_note1_activate(self, event):
        print 'pickup note'
        
        dicOrder = {}
        dicOrder['orderNumber'] = self.singleOrder.getOrderNumber(self.singleOrder.ID)
        dicOrder['pickupNumber'] =  self.singleOrderGet.getPickupNumber(self.singleOrder.ID)
        dicOrder['addressNumber'] = self.singleOrderGet.getAddressNumber(self.singleOrderGet.ID)
        print 'Addressnumber by Orderget = ' + `dicOrder['addressNumber']`
        dicOrder['partnerNumber'] = self.singleOrderGet.getPartnerNumber(self.singleOrderGet.ID)
        print 'partnernumber by Orderget = ' + `dicOrder['partnerNumber']`
        dicOrder['forwardingAgencyNumber'] = self.singleOrderGet.getForwardingAgencyNumber(self.singleOrderGet.ID)
        print 'ForwardAgencynumber by Orderget = ' + `dicOrder['forwardingAgencyNumber']`
        dicOrder['contactPersonNumber'] = self.singleOrderGet.getContactPersonNumber(self.singleOrderGet.ID)
        print 'ContactPersonnumber by Orderget = ' + `dicOrder['contactPersonNumber']`
              
                
        
        pdf = cuon.Order.standard_pickup_note.standard_pickup_note(dicOrder)
               
    def on_quit1_activate(self, event):
        print "exit order v2"
        self.closeWindow()


    #Menu Order
  
    def on_save1_activate(self, event):
        print "save order v2"
        self.singleOrder.save()
        self.setEntriesEditable(self.EntriesOrder, FALSE)   
        self.tabChanged()
         
        
    def on_new1_activate(self, event):
        print "new order v2"
        self.singleOrder.newRecord()
        self.setEntriesEditable(self.EntriesOrder, TRUE)

    def on_edit1_activate(self, event):
        self.setEntriesEditable(self.EntriesOrder, TRUE)

    def on_delete1_activate(self, event):
        print "delete order v2"
        self.singleOrder.deleteRecord()

 
    #Menu Gets
  
    def on_GetsSave1_activate(self, event):
        print "save order v2"
        self.singleOrderGet.ordernumber = self.singleOrder.ID
        self.singleOrderGet.save()
        self.setEntriesEditable(self.EntriesOrderGet, FALSE)   
        self.tabChanged()
         
        
    def on_GetsNew1_activate(self, event):
        print "new order v2"
        self.singleOrderGet.newRecord()
        self.setEntriesEditable(self.EntriesOrderGet, TRUE)

    def on_GetsEdit1_activate(self, event):
        self.setEntriesEditable(self.EntriesOrderGet, TRUE)

    def on_GetsDelete1_activate(self, event):
        print "delete order v2"
        self.singleOrderGet.deleteRecord()


 
    # Menu Supply

    def on_SupplyNew1_activate(self, event):
        self.singleOrderSupply.newRecord()
        self.setEntriesEditable(self.EntriesOrderSupply, TRUE)

    def on_SupplyEdit1_activate(self, event):
        self.setEntriesEditable(self.EntriesOrderSupply, TRUE)

    def on_SupplySave1_activate(self, event):
        print "save Supply v2"
        self.singleOrderSupply.ordernumber = self.singleOrder.ID
        self.singleOrderSupply.save()
        self.setEntriesEditable(self.EntriesOrderSupply, FALSE)
        self.tabChanged()
        

    def on_SupplyDelete1_activate(self, event):
        print "delete Supply v2"
        self.singleOrderSupply.deleteRecord()

    #Menu Positions
    def on_PositionSave1_activate(self, event):
        print "save Positions v2"
       
        self.singleOrderPosition.orderID = self.singleOrder.ID

        self.singleOrderPosition.save()
        self.setEntriesEditable(self.EntriesOrderSupply, FALSE)

        self.tabChanged()

    def on_PositionEdit1_activate(self, event):
        print 'PositionEdit1'
        self.setEntriesEditable(self.EntriesOrderPosition, TRUE)
    
    def on_PositionNew1_activate(self, event):
        print "new Partner articles v2"
        self.singleOrderPosition.newRecord()
        self.setEntriesEditable(self.EntriesOrderPosition, TRUE)

    def on_PositionDelete1_activate(self, event):
        print "delete Partner articles v2"
        self.singleOrderPosition.deleteRecord()


 


    # search button
    def on_bSearch_clicked(self, event):
        self.out( 'Searching ....', self.ERROR)
        sNumber = self.getWidget('eFindNumber').get_text()
        sDesignation = self.getWidget('eFindDesignation').get_text()
        self.out('Name and City = ' + sNumber + ', ' + sDesignation, self.ERROR)
        self.singleOrder.sWhere = 'where number ~* \'.*' + sNumber + '.*\' and designation ~* \'.*' + sDesignation + '.*\''
        self.out(self.singleOrder.sWhere, self.ERROR)
        self.refreshTree()


    # Tab Custom choose address 
    def on_bSearchCustom_clicked(self, event):
        adr = cuon.Addresses.addresses.addresswindow(self.allTables)
        adr.setChooseEntry('chooseAddress', self.getWidget( 'eAddressNumber'))

    # signals from entry eAddressNumber
    
    def on_eAddressNumber_changed(self, event):
        print 'eAdrnbr changed'
        iAdrNumber = self.getChangedValue('eAddressNumber')
        eAdrField = self.getWidget('tvAddress')
        liAdr = self.singleAddress.getAddress(iAdrNumber)
        self.setTextbuffer(eAdrField,liAdr)

    # Tab Supply choose address 
    def on_bSearchSupply_clicked(self, event):
        adr = cuon.Addresses.addresses.addresswindow(self.allTables)
        adr.setChooseEntry('chooseAddress', self.getWidget( 'eSupplyNumber'))

    def on_eSupplyNumber_changed(self, event):
        print 'eSupply changed'
        iAdrNumber = self.getChangedValue('eSupplyNumber')
        eAdrField = self.getWidget('tvSupply')
        liAdr = self.singleAddress.getAddress(iAdrNumber)
        self.setTextbuffer(eAdrField,liAdr)

        # Tab Gets  choose address 
    def on_bSearchGet_clicked(self, event):
        adr = cuon.Addresses.addresses.addresswindow(self.allTables)
        adr.setChooseEntry('chooseAddress', self.getWidget( 'eGetsNumber'))

    def on_eGetsNumber_changed(self, event):
        print 'eGets changed'
        iAdrNumber = self.getChangedValue('eGetsNumber')
        eAdrField = self.getWidget('tvGets')
        liAdr = self.singleAddress.getAddress(iAdrNumber)
        self.setTextbuffer(eAdrField,liAdr)

    def on_bSearchGetsPartner_clicked(self, event):
        adr = cuon.Addresses.addresses.addresswindow(self.allTables)
        adr.setChooseEntry('chooseAddress', self.getWidget( 'eGetsPartner'))

    def on_eGetsPartner_changed(self, event):
        print 'eGetsPartner changed'
        iAdrNumber = self.getChangedValue('eGetsPartner')
        eAdrField = self.getWidget('tvGetsPartner')
        liAdr = self.singlePartner.getAddress(iAdrNumber)
        self.setTextbuffer(eAdrField,liAdr)



    def on_bSearchForwardingAgency_clicked(self, event):
        adr = cuon.Addresses.addresses.addresswindow(self.allTables)
        adr.setChooseEntry('chooseAddress', self.getWidget( 'eForwardingAgency'))

    def on_eForwardingAgency_changed(self, event):
        print 'eForwardingAgency changed'
        iAdrNumber = self.getChangedValue('eForwardingAgency')
        eAdrField = self.getWidget('tvForwardingAgency')
        liAdr = self.singleAddress.getAddress(iAdrNumber)
        self.setTextbuffer(eAdrField,liAdr)


    def on_bContactPerson_clicked(self, event):
        adr = cuon.Addresses.addresses.addresswindow(self.allTables)
        adr.setChooseEntry('chooseAddress', self.getWidget( 'eContactPerson'))

    def on_eContactPerson_changed(self, event):
        print 'eContactPerson changed'
        iAdrNumber = self.getChangedValue('eContactPerson')
        eAdrField = self.getWidget('tvContactPerson')
        liAdr = self.singlePartner.getAddress(iAdrNumber)
        self.setTextbuffer(eAdrField,liAdr)

        
        # Tab Positions choose article 
    def on_bArticleSearch_clicked(self, event):
        ar = cuon.Articles.articles.articleswindow(self.allTables)
        ar.setChooseEntry('chooseArticle', self.getWidget( 'eArticleID'))

                           

    def on_eArticleID_changed(self, event):
        print 'eArticle changed'
        iArtNumber = self.getChangedValue('eArticleID')
        eArtField = self.getWidget('tvArticle')
        liArt = self.singleArticle.getArticle(iArtNumber)
        self.setTextbuffer(eArtField,liArt)
        record = self.singleArticle.getFirstRecord()
        if record:
            print record
            self.getWidget('eOrderPositionsUnit').set_text(record['unit'])
            
        if self.singleOrderPosition.ID == -1 and record:
            self.getWidget('eOrderPositionsTaxVat').set_text(record['tax_vat'])
          
    def fillcbeTOP(self):
        cbeTop = self.getWidget('cbeTOP')
        liCbe = XMLRPC.xmlrpc().callRP('py_getListOfTOPs')
        print `liCbe`

    def refreshTree(self):
        self.singleOrder.disconnectTree()
        self.singleOrderSupply.disconnectTree()
        self.singleOrderGet.disconnectTree()
        self.singleOrderPosition.disconnectTree()
        
        if self.tabOption == self.tabOrder:
            self.singleOrder.connectTree()
            self.singleOrder.refreshTree()

        elif self.tabOption == self.tabSupply:
            self.singleOrderSupply.sWhere  ='where ordernumber = ' + `int(self.singleOrder.ID)`
            self.singleOrderSupply.connectTree()
            self.singleOrderSupply.refreshTree()

        elif self.tabOption == self.tabGet:
            self.singleOrderGet.sWhere  ='where ordernumber = ' + `int(self.singleOrder.ID)`
            self.singleOrderGet.connectTree()
            self.singleOrderGet.refreshTree()
 
        elif self.tabOption == self.tabPosition:
            self.singleOrderPosition.sWhere  ='where orderid = ' + `int(self.singleOrder.ID)`
            self.singleOrderPosition.connectTree()
            self.singleOrderPosition.refreshTree()
            
        elif self.tabOption == self.tabInvoice:
            self.singleOrder.connectTree()
            self.singleOrder.refreshTree()
            self.fillcbeTOP()



         
    def tabChanged(self):
        print 'tab changed to :'  + str(self.tabOption)
        if self.tabOption == self.tabOrder:
            #Address
            self.disableMenuItem('tabs')
            self.enableMenuItem('order')
            print 'Seite 0'
            self.editAction = 'editOrder'
            
        elif self.tabOption == self.tabSupply:
            #Partner
            self.disableMenuItem('tabs')
            self.enableMenuItem('supply')
            self.editAction = 'editSupply'
            print 'Seite 1'
            
        elif self.tabOption == self.tabGet:
            self.disableMenuItem('tabs')
            self.enableMenuItem('gets')
            self.editAction = 'editGets'
            print 'Seite 2'
        elif self.tabOption == self.tabPosition:
            self.disableMenuItem('tabs')
            self.enableMenuItem('positions')
            self.editAction = 'editPositions'
            print 'Seite 3'  
         
         
        elif self.tabOption == self.tabInvoice:
            self.disableMenuItem('tabs')
            self.enableMenuItem('invoice')
            self.editAction = 'editInvoice'
            print 'Seite 4'  
         
        # refresh the Tree
        self.refreshTree()
        self.enableMenuItem(self.editAction)
        self.editEntries = FALSE
