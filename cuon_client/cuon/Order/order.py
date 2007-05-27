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
import SingleOrderPayment



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
import cuon.PrefsFinance.prefsFinance
import cuon.Finances.SingleAccountInfo



class orderwindow(chooseWindows):
    """
    @author: Juergen Hamel
    @organization: Cyrus-Computer GmbH, D-32584 Loehne
    @copyright: by Juergen Hamel
    @license: GPL ( GNU GENERAL PUBLIC LICENSE )
    @contact: jh@cyrus.de
    """
    
    
    def __init__(self, allTables, dicOrder=None,  newOrder = False):

        chooseWindows.__init__(self)
        self.dicOrder = dicOrder
        self.fillArticlesNewID = 0
        self.loadGlade('order.xml','OrderMainwindow')
        #self.win1 = self.getWidget('OrderMainwindow')
        
        self.allTables = allTables
        self.singleOrder = SingleOrder.SingleOrder(allTables)
        self.singleOrderSupply = SingleOrderSupply.SingleOrderSupply(allTables)
        self.singleOrderGet = SingleOrderGet.SingleOrderGet(allTables)
        self.singleOrderPosition = SingleOrderPosition.SingleOrderPosition(allTables)
        self.singleAddress = cuon.Addresses.SingleAddress.SingleAddress(allTables)
        self.singlePartner = cuon.Addresses.SinglePartner.SinglePartner(allTables)
        self.singleOrderPayment = SingleOrderPayment.SingleOrderPayment(allTables)
        self.singleAccountInfo =cuon.Finances.SingleAccountInfo.SingleAccountInfo(allTables)
        
        self.singleArticle = cuon.Articles.SingleArticle.SingleArticle(allTables)
       
        # self.singleOrder.loadTable()
              
        self.EntriesOrder = 'order.xml'
        self.EntriesOrderSupply = 'order_supply.xml'
        self.EntriesOrderGet = 'order_get.xml'
        self.EntriesOrderPosition = 'order_position.xml'
        self.EntriesOrderMisc = 'order_misc.xml'
        self.EntriesOrderPayment = 'order_inpayment.xml'
        
        
        
        
        #singleOrder
        
        self.loadEntries(self.EntriesOrder)
        self.singleOrder.setEntries(self.getDataEntries(self.EntriesOrder) )
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
        self.singleOrderPosition.setEntries(self.getDataEntries(self.EntriesOrderPosition) )
        self.singleOrderPosition.setGladeXml(self.xml)
        self.singleOrderPosition.setTreeFields( ['position','amount','articleid','designation'] )
        self.singleOrderPosition.setStore( gtk.ListStore(gobject.TYPE_UINT, gobject.TYPE_FLOAT, gobject.TYPE_STRING , gobject.TYPE_STRING,  gobject.TYPE_UINT) ) 
        self.singleOrderPosition.setTreeOrder('position,articleid')
        self.singleOrderPosition.setListHeader([_('Pos.'),_('Amount'),_('Article'),_('Designation')])

        self.singleOrderPosition.sWhere  ='where orderid = ' + `self.singleOrder.ID`
        self.singleOrderPosition.setTree(self.xml.get_widget('tree1') )
  
        
        self.loadEntries(self.EntriesOrderMisc)
        
        
        # singleOrderPayment
        
        self.loadEntries(self.EntriesOrderPayment)
        self.singleOrderPayment.setEntries(self.getDataEntries(self.EntriesOrderPayment) )
        self.singleOrderPayment.setGladeXml(self.xml)
        self.singleOrderPayment.setTreeFields( ['date_of_paid','invoice_number','inpayment','account_id'] )
        self.singleOrderPayment.setStore( gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_FLOAT, gobject.TYPE_STRING, gobject.TYPE_UINT) ) 
        self.singleOrderPayment.setTreeOrder('date_of_paid,invoice_number')
        self.singleOrderPayment.setListHeader([_('Date'),_('Invoice'),_('Inpayment'),_('account')])

        self.singleOrderPayment.sWhere  ='where order_id = ' + `self.singleOrder.ID`
        self.singleOrderPayment.setTree(self.xml.get_widget('tree1') )
  
        # Menu-items
        self.initMenuItems()

        # Close Menus for Tab

        self.addEnabledMenuItems('tabs','order1')
        self.addEnabledMenuItems('tabs','supply1')
        self.addEnabledMenuItems('tabs','gets1')
        self.addEnabledMenuItems('tabs','positions1')
        self.addEnabledMenuItems('tabs','misc1')
        self.addEnabledMenuItems('tabs','payments1')


        # seperate Menus
        self.addEnabledMenuItems('order','order1')
        self.addEnabledMenuItems('supply','supply1')
        self.addEnabledMenuItems('gets','gets1')
        self.addEnabledMenuItems('positions','positions1')
        self.addEnabledMenuItems('payment','payments1')
        self.addEnabledMenuItems('misc','misc1')
        

        
        # enabledMenues for Order
        self.addEnabledMenuItems('editOrder','new1', self.dicUserKeys['new'])
        self.addEnabledMenuItems('editOrder','edit1', self.dicUserKeys['edit'])
        self.addEnabledMenuItems('editOrder','delete1', self.dicUserKeys['delete'])
        self.addEnabledMenuItems('editOrder','print1', self.dicUserKeys['print'])

        # enabledMenues for Supply
        self.addEnabledMenuItems('editSupply','SupplyNew1', self.dicUserKeys['new'])
        self.addEnabledMenuItems('editSupply','SupplyEdit1', self.dicUserKeys['edit'])
        self.addEnabledMenuItems('editSuppy','SupplyDelete1', self.dicUserKeys['delete'])
    
       # enabledMenues for Gets
        self.addEnabledMenuItems('editGets','GetsNew1', self.dicUserKeys['new'])
        self.addEnabledMenuItems('editGets','GetsEdit1', self.dicUserKeys['edit'])
        self.addEnabledMenuItems('editGets','GetsDelete1', self.dicUserKeys['delete'])

        # enabledMenues for Positions
        self.addEnabledMenuItems('editPositions','PositionNew1', self.dicUserKeys['new'])
        self.addEnabledMenuItems('editPositions','PositionEdit1', self.dicUserKeys['edit'])
        self.addEnabledMenuItems('editPositions','PositionDelete1', self.dicUserKeys['delete'])

        # enabledMenues for Payment
        self.addEnabledMenuItems('editPayment','payment_new', self.dicUserKeys['new'])
        self.addEnabledMenuItems('editPayment','payment_edit', self.dicUserKeys['edit'])

        # to misc menu
        
        # enabledMenues for Save 
        self.addEnabledMenuItems('editSave','save1', self.dicUserKeys['save'])
        self.addEnabledMenuItems('editSave','SupplySave1', self.dicUserKeys['save'])
        self.addEnabledMenuItems('editSave','GetsSave1', self.dicUserKeys['save'])
        self.addEnabledMenuItems('editSave','PositionSave1', self.dicUserKeys['save'])
        self.addEnabledMenuItems('editSave','MiscSave', self.dicUserKeys['save'])
        self.addEnabledMenuItems('editSave','payment_save', self.dicUserKeys['save'])


        # tabs from notebook
        self.tabOrder = 0
        self.tabSupply = 1
        self.tabGet = 2
        self.tabPosition = 3
        self.tabInvoice = 4
        self.tabMisc = 5
        self.tabPayment = 6
        

        # start
        if self.dicOrder and not newOrder:
            print self.dicOrder
            existOrder = self.rpc.callRP('Order.checkExistModulOrder', self.dicUser,self.dicOrder)
            print 'existOrder = ', existOrder
            if not existOrder or existOrder == 'NONE':
                print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~ create new'
                self.rpc.callRP('Order.createNewOrder', self.dicUser,self.dicOrder)
            self.singleOrder.sWhere = ' where modul_order_number = ' + `self.dicOrder['ModulOrderNumber']` + ' and modul_number = ' + `self.dicOrder['ModulNumber']`
        elif self.dicOrder and newOrder:
            dicResult = self.rpc.callRP('Order.createNewOrder', self.dicUser,self.dicOrder)
            if dicResult and dicResult != 'NONE':
                orderid = dicResult[0]['last_value']
                if orderid > 0:
                    self.singleOrder.sWhere = ' where id = ' + `orderid` 
                    
                    
        ts = self.getWidget('treeMaterialgroup')
        #treeview.set_model(liststore)
 
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Materialgroups", renderer, text=0)
        ts.append_column(column)
                    
        tt = self.getWidget('treeArticles')
        #treeview.set_model(liststore)
 
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Articles", renderer, text=0)
        tt.append_column(column)
                    
        self.fillMaterialGroup()
        
            
        self.tabChanged()

        self.win1.add_accel_group(self.accel_group)
         
         
    #Menu File

    def on_print_invoice1_activate(self, event):
        dicOrder = {}
        print ' start Invoice printing'
        dicOrder['orderid'] = self.singleOrder.ID
        dicOrder['orderNumber'] = self.singleOrder.getOrderNumber(self.singleOrder.ID)
        dicOrder['invoiceNumber'] = self.rpc.callRP('Order.setInvoiceNumber', dicOrder['orderid'], self.dicUser)
        print ' start Invoice printing 2'

        dicOrder['invoiceNumber'] =  self.singleOrder.getInvoiceNumber()        
        print ' start Invoice printing 3'
        
        print dicOrder
        
        Pdf = self.rpc.callRP('Report.server_order_invoice_document', dicOrder, self.dicUser)
        self.showPdf(Pdf, self.dicUser,'INVOICE')

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

    def on_list_of_invoices1_activate(self, event):
        dicOrder = {}
        print ' start List of Invoices printing'
        dicOrder['Year'] = '2007'
        print 'dicOrder = ', dicOrder
        
        Pdf = self.rpc.callRP('Report.server_order_list_of_invoices', dicOrder, self.dicUser)
        self.showPdf(Pdf, self.dicUser,'INVOICE')

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

    # Menu Misc
    def on_MiscEdit_activate(self, event):
        print 'MiscEdit1'
        self.setEntriesEditable(self.EntriesOrderMisc, TRUE)
    
    def on_MiscSave_activate(self, event):
        print "save misc v2"
        self.singleOrder.setEntries(self.getDataEntries(self.EntriesOrderMisc) )
        self.singleOrder.save()
        self.setEntriesEditable(self.EntriesOrderMisc, FALSE)
        self.singleOrder.setEntries(self.getDataEntries(self.EntriesOrder) )
        self.tabChanged()
  
    #Menu Payment
    def on_payment_save_activate(self, event):
        print "save Positions v2"
       
        self.singleOrderPayment.orderID = self.singleOrder.ID
    
        self.singleOrderPayment.invoiceNumber = self.singleOrder.getInvoiceNumber()
        

        self.singleOrderPayment.save()
        self.setEntriesEditable(self.EntriesOrderPayment, FALSE)

        self.tabChanged()

    def on_payment_edit_activate(self, event):
        print 'PositionEdit1'
        self.setEntriesEditable(self.EntriesOrderPayment, TRUE)
    
    def on_payment_new_activate(self, event):
        print "new Ppayment v2"
        self.singleOrderPayment.newRecord()
        self.getWidget('ePaymentInvoiceNumber').set_text(`self.singleOrder.getInvoiceNumber()`)
        
        self.setEntriesEditable(self.EntriesOrderPayment, TRUE)


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
    
    
    
    
    def disconnectArticlesTree(self):
        try:
            
            self.getWidget('treeArticles').get_selection().disconnect(self.connectArticlesTreeId)
        except:
            pass

    def connectArticlesTree(self):
        try:
            self.connectArticlesTreeId = self.getWidget('treeArticles').get_selection().connect("changed", self.ArticlesTree_select_callback)
        except:
            pass
   
    def ArticlesTree_select_callback(self, treeSelection):
        listStore, iter = treeSelection.get_selected()
        
        print listStore,iter
        
        if listStore and len(listStore) > 0:
           row = listStore[0]
        else:
           row = -1
   
        if iter != None:
            sNewId = listStore.get_value(iter, 0)
            print sNewId
            try:
                self.fillArticlesNewID = int(sNewId[sNewId.find('###')+ 3:])
                #self.setDateValues(newID)
                
            except:
                pass
                   
    def fillArticles(self, mid):
        print 'fill Articles'
        try:
            ts = self.getWidget('treeArticles')
            print 'ts = ', ts
            treestore = gtk.TreeStore(object)
            treestore = gtk.TreeStore(str)
            ts.set_model(treestore)
                
            liArticles = self.rpc.callRP('Article.getArticlesOfMaterialGroup',self.dicUser, mid )
            print 'liArticles ', liArticles
            if liArticles:
                lastGroup = None
                
                #iter = treestore.append(None,[_('Schedul')])
                #print 'iter = ', iter
                iter2 = None
                iter3 = None
                #liDates.reverse()
                for oneArticle in liArticles:
                    articlenumber = oneArticle['number']
                    articledesignation = oneArticle['designation']
                    
                    iter = treestore.append(None,[articlenumber +  ', ' + articledesignation +  '     ###' +`oneArticle['id']` ]) 
                    #print 'add iter', [groupname + '###' +`oneGroup['id']` ]
                    
                    #iter2 = treestore.insert_after(iter,None,['TESTEN'])           
                #print 'End liDates'
            ts.show()
            #self.getWidget('scrolledwindow10').show()
            self.connectArticlesTree()
            print 'ts', ts
            
        except Exception, params:
            print Exception, params    
            


    def disconnectMaterialGroupTree(self):
        try:
            
            self.getWidget('treeMaterialgroup').get_selection().disconnect(self.connectMaterialGroupTreeId)
        except:
            pass

    def connectMaterialGroupTree(self):
        try:
            self.connectMaterialGroupTreeId = self.getWidget('treeMaterialgroup').get_selection().connect("changed", self.MaterialGroupTree_select_callback)
        except:
            pass
   
    def MaterialGroupTree_select_callback(self, treeSelection):
        listStore, iter = treeSelection.get_selected()
        
        print listStore,iter
        
        if listStore and len(listStore) > 0:
           row = listStore[0]
        else:
           row = -1
   
        if iter != None:
            sNewId = listStore.get_value(iter, 0)
            print sNewId
            try:
                newID = int(sNewId[sNewId.find('###')+ 3:])
                self.fillArticles(newID)
                
            except:
                pass
                   
    def fillMaterialGroup(self):
        print 'eSchedulfor changed'
        try:
            ts = self.getWidget('treeMaterialgroup')
            print 'ts = ', ts
            treestore = gtk.TreeStore(object)
            treestore = gtk.TreeStore(str)
            ts.set_model(treestore)
                
            liGroups = self.rpc.callRP('Article.getMaterialGroups',self.dicUser )
            print 'liGroups ', liGroups
            if liGroups:
                lastGroup = None
                
                #iter = treestore.append(None,[_('Schedul')])
                #print 'iter = ', iter
                iter2 = None
                iter3 = None
                #liDates.reverse()
                for oneGroup in liGroups:
                    groupname = oneGroup['name']
                    
                    iter = treestore.append(None,[groupname + '     ###' +`oneGroup['id']` ]) 
                    #print 'add iter', [groupname + '###' +`oneGroup['id']` ]
                    
                    #iter2 = treestore.insert_after(iter,None,['TESTEN'])           
                #print 'End liDates'
            ts.show()
            #self.getWidget('scrolledwindow10').show()
            self.connectMaterialGroupTree()
            print 'ts', ts
            
        except Exception, params:
            print Exception, params    
            
    def on_bPaymentSearchAccount_clicked(self, event):
        acc = cuon.PrefsFinance.prefsFinance.prefsFinancewindow(self.allTables)
        acc.setChooseEntry('choose_acct1', self.getWidget( 'ePaymentAccountID'))

                           

    def on_ePaymentAccountID_changed(self, event):
        print 'eAccountID changed'
        iAcctNumber = self.getChangedValue('ePaymentAccountID')
        eAcctField = self.getWidget('eAccountDesignation')
        cAcct = self.singleAccountInfo.getInfoLine(iAcctNumber)
        eAcctField.set_text(cAcct)
        
##        record = self.singleArticle.getFirstRecord()
##        if record:
##            print record
##            self.getWidget('eOrderPositionsUnit').set_text(record['unit'])
##            
##        if self.singleOrderPosition.ID == -1 and record:
##            self.getWidget('eOrderPositionsTaxVat').set_text(record['tax_vat'])
##          
    def on_bQuickAppend_clicked(self, event):
        # Qick append a positions
        if self.singleOrderPosition.ID != -1:
            self.on_PositionNew1_activate(event)
        if self.getWidget('eAmount').get_text() == '':
            print 'get_text none'
            self.getWidget('eAmount').set_text('1')
        self.getWidget('eArticleID').set_text(`self.fillArticlesNewID`)
        self.on_PositionSave1_activate(event)


    def on_Mainwindow_key_press_event(self, oEntry, data):
        ''' Overwrite def '''
        sKey = gtk.gdk.keyval_name(data.keyval)
        print 'sKey : ',sKey
        if self.tabOption == self.tabPosition:
            if sKey == 'KP_Add' or sKey == 'plus' :
                self.on_PositionEdit1_activate(None)
                if self.getWidget('eAmount').get_text() == '':
                    self.getWidget('eAmount').set_text('1')
                else:
                    try:
                        wAmount = self.getWidget('eAmount')
                        f1 = float(wAmount.get_text())
                        f2 = f1 + 1.000
                        print f1, f2
                        wAmount.set_text( self.getCheckedValue(f2, 'toLocaleString'))
                        print 'gesetzte zahl = ', wAmount.get_text()
                    except Exception, params:
                        print Exception, params
                self.on_PositionSave1_activate(None)        

            elif sKey == 'KP_Subtract' or sKey == 'minus' :
                self.on_PositionEdit1_activate(None)
                if self.getWidget('eAmount').get_text() == '':
                    self.getWidget('eAmount').set_text('0')
                else:
                    try:
                        wAmount = self.getWidget('eAmount')
                        f1 = float(wAmount.get_text())
                        f2 = f1 - 1.000
                        print f1, f2
                        wAmount.set_text( `self.getCheckedValue(f2, 'toStringFloat')`)
                        print 'gesetzte zahl = ', wAmount.get_text()
                    except Exception, params:
                        print Exception, params            
                self.on_PositionSave1_activate(None)        
            
        
        else:
            self.MainwindowEventHandling(oEntry, data)
      
    def on_treeArticles_row_activated(self, event, data1, data2):
        self.on_bQuickAppend_clicked(event)

    def refreshTree(self):
        self.singleOrder.disconnectTree()
        self.singleOrderSupply.disconnectTree()
        self.singleOrderGet.disconnectTree()
        self.singleOrderPosition.disconnectTree()
        
        if self.tabOption == self.tabOrder:
            self.singleOrder.setEntries(self.getDataEntries(self.EntriesOrder) )
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

        elif self.tabOption == self.tabMisc:
            self.singleOrder.setEntries(self.getDataEntries(self.EntriesOrderMisc) )
            self.singleOrder.connectTree()
            self.singleOrder.refreshTree()

        elif self.tabOption == self.tabPayment:
            self.singleOrderPayment.sWhere  ='where order_id = ' + `int(self.singleOrder.ID)`
            self.singleOrderPayment.connectTree()
            self.singleOrderPayment.refreshTree()
         
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
            
        elif self.tabOption == self.tabMisc:
            self.disableMenuItem('tabs')
            self.enableMenuItem('misc')
            self.editAction = 'editMisc'
            print 'Seite 5'
            
        elif self.tabOption == self.tabPayment:
            self.disableMenuItem('tabs')
            self.enableMenuItem('payment')
            self.editAction = 'editPayment'
            print 'Seite 6'  
         
        # refresh the Tree
        self.refreshTree()
        self.enableMenuItem(self.editAction)
        self.editEntries = FALSE
