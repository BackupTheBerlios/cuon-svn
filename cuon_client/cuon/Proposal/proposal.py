# -*- coding: utf-8 -*-
##Copyright (C) [2003]  [Juergen Hamel, D-32584 Loehne]

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
#from gtk import True, False
import string

from cuon.Databases.SingleData import SingleData
import cuon.Order.SingleOrder
import cuon.Order.SingleOrderSupply
import cuon.Order.SingleOrderGet
import cuon.Order.SingleOrderPosition
import cuon.Order.SingleOrderPayment


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
import cuon.PrefsFinance.prefsFinance
import cuon.PrefsFinance.SinglePrefsFinanceTop
import cuon.Order.SingleOrderInvoice
import cuon.DMS.dms
import cuon.DMS.SingleDMS
import cuon.DMS.documentTools

import cuon.PrefsFinance.prefsFinance
import cuon.PrefsFinance.SinglePrefsFinanceVat


class proposalwindow(chooseWindows):
    """
    @author: Juergen Hamel
    @organization: Cyrus-Computer GmbH, D-32584 Loehne
    @copyright: by Juergen Hamel
    @license: GPL ( GNU GENERAL PUBLIC LICENSE )
    @contact: jh@cyrus.de
    """
    
    
    def __init__(self, allTables, dicOrder=None,  newOrder = False, orderid = 0,Ordertype='Proposal'):

        chooseWindows.__init__(self)
        self.dicOrder = dicOrder
        self.fillArticlesNewID = 0
        self.loadGlade('proposal.xml','ProposalMainwindow')
        #self.win1 = self.getWidget('OrderMainwindow')
        
        self.allTables = allTables
        self.singleOrder = cuon.Order.SingleOrder.SingleOrder(allTables)
        self.singleOrderSupply = cuon.Order.SingleOrderSupply.SingleOrderSupply(allTables)
        self.singleOrderGet = cuon.Order.SingleOrderGet.SingleOrderGet(allTables)
        self.singleOrderPosition = cuon.Order.SingleOrderPosition.SingleOrderPosition(allTables)
        self.singleAddress = cuon.Addresses.SingleAddress.SingleAddress(allTables)
        self.singlePartner = cuon.Addresses.SinglePartner.SinglePartner(allTables)
        self.singleOrderPayment = cuon.Order.SingleOrderPayment.SingleOrderPayment(allTables)
        self.singleAccountInfo =cuon.Finances.SingleAccountInfo.SingleAccountInfo(allTables)
        self.singlePrefsFinanceTop = cuon.PrefsFinance.SinglePrefsFinanceTop.SinglePrefsFinanceTop(allTables)
        self.singleOrderInvoice = cuon.Order.SingleOrderInvoice.SingleOrderInvoice(allTables)
        
        self.singleDMS = cuon.DMS.SingleDMS.SingleDMS(allTables)
        self.documentTools = cuon.DMS.documentTools.documentTools()
        
        self.singleArticle = cuon.Articles.SingleArticle.SingleArticle(allTables)
       
        # self.singleOrder.loadTable()
              
        self.EntriesProposal = 'proposal.xml'
        self.EntriesProposalSupply = 'proposal_supply.xml'
        self.EntriesProposalGet = 'proposal_get.xml'
        self.EntriesProposalPosition = 'proposal_position.xml'
        #self.EntriesproposalMisc = 'proposal_misc.xml'
        self.EntriesProposalInvoice = 'proposal_invoice.xml'
        #self.EntriesproposalPayment = 'proposal_inpayment.xml'
        
        
        
        
        #singleProposal
        
        self.loadEntries(self.EntriesProposal)
        self.singleOrder.setEntries(self.getDataEntries(self.EntriesProposal) )
        self.singleOrder.setGladeXml(self.xml)
        self.singleOrder.setTreeFields( ['number', 'designation'] )
        self.singleOrder.setStore( gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING,   gobject.TYPE_UINT) ) 
        self.singleOrder.setTreeOrder('number')
        self.singleOrder.setTree(self.xml.get_widget('tree1') )
        self.singleOrder.setListHeader([_('number'), _('designation') ])
        self.singleOrder.processStatus = 300
        self.singleOrder.sWhere  ='where process_status between 300 and 399'
        
         #singleOrderSupply
        
        self.loadEntries(self.EntriesProposalSupply)
        self.singleOrderSupply.setEntries(self.getDataEntries(self.EntriesProposalSupply) )
        self.singleOrderSupply.setGladeXml(self.xml)
        self.singleOrderSupply.setTreeFields( ['designation' ] )
        self.singleOrderSupply.setStore( gtk.ListStore(gobject.TYPE_STRING,  gobject.TYPE_UINT) ) 
        self.singleOrderSupply.setTreeOrder('designation')
        self.singleOrderSupply.setListHeader([_('Designation')])

        self.singleOrderSupply.sWhere  ='where ordernumber = ' + `self.singleOrder.ID`
        self.singleOrderSupply.setTree(self.xml.get_widget('tree1') )
  
        #singleOrderGet
        
        self.loadEntries(self.EntriesProposalGet)
        self.singleOrderGet.setEntries(self.getDataEntries(self.EntriesProposalGet) )
        self.singleOrderGet.setGladeXml(self.xml)
        self.singleOrderGet.setTreeFields( ['designation'] )
        self.singleOrderGet.setStore( gtk.ListStore(gobject.TYPE_STRING,  gobject.TYPE_UINT) ) 
        self.singleOrderGet.setTreeOrder('designation')
        self.singleOrderGet.setListHeader([_('Designation')])

        self.singleOrderGet.sWhere  ='where ordernumber = ' + `self.singleOrder.ID`
        self.singleOrderGet.setTree(self.xml.get_widget('tree1') )

        # singlePositions
        
        self.loadEntries(self.EntriesProposalPosition)
        self.singleOrderPosition.setEntries(self.getDataEntries(self.EntriesProposalPosition) )
        self.singleOrderPosition.setGladeXml(self.xml)
        self.singleOrderPosition.setTreeFields( ['position','amount','articleid','articles.number as arnumber','articles.designation as ardsesignation', 'orderposition.designation as designation2'] )
        self.singleOrderPosition.setStore( gtk.ListStore(gobject.TYPE_UINT, gobject.TYPE_FLOAT, gobject.TYPE_UINT ,gobject.TYPE_STRING , gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_UINT) ) 
        self.singleOrderPosition.setTreeOrder('position,articleid')
        self.singleOrderPosition.setListHeader([_('Pos.'),_('Amount'),_('Article-ID'),_('Number'),_('Designation'),_('Designation2')])

        self.singleOrderPosition.sWhere  ='where orderid = ' + `self.singleOrder.ID` + ' and articleid = articles.id '
        self.singleOrderPosition.setTree(self.xml.get_widget('tree1') )
  
        
  #      self.loadEntries(self.EntriesOrderMisc)
        
#        # singleOrderInvoice
#        self.loadEntries(self.EntriesOrderInvoice)
#        self.singleOrderInvoice.sWhere  ='where orderid = ' + `self.singleOrder.ID`
#        self.singleOrderInvoice.setEntries(self.getDataEntries(self.EntriesOrderInvoice) )
#        self.singleOrderInvoice.setGladeXml(self.xml)
#        self.singleOrderInvoice.setTreeFields([])
#        self.singleOrderInvoice.setTreeOrder('id')
#        self.singleOrderInvoice.setTree(self.xml.get_widget('tree1') )
#        # singleOrderPayment   
#        
#        self.loadEntries(self.EntriesOrderPayment)
#        self.singleOrderPayment.setEntries(self.getDataEntries(self.EntriesOrderPayment) )
#        self.singleOrderPayment.setGladeXml(self.xml)
#        self.singleOrderPayment.setTreeFields( ['date_of_paid','invoice_number','inpayment','account_id'] )
#        self.singleOrderPayment.setStore( gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_FLOAT, gobject.TYPE_STRING, gobject.TYPE_UINT) ) 
#        self.singleOrderPayment.setTreeOrder('date_of_paid desc,id desc')
#        self.singleOrderPayment.setListHeader([_('Date'),_('Invoice'),_('Inpayment'),_('account')])
#
#        self.singleOrderPayment.sWhere  ='where order_id = ' + `self.singleOrder.ID`
#        self.singleOrderPayment.setTree(self.xml.get_widget('tree1') )
#  
        # Menu-items
        self.initMenuItems()

        # Close Menus for Tab

        self.addEnabledMenuItems('tabs','proposal1')
        self.addEnabledMenuItems('tabs','supply1')
        self.addEnabledMenuItems('tabs','gets1')
        self.addEnabledMenuItems('tabs','position1')
        #self.addEnabledMenuItems('tabs','invoice1')
        self.addEnabledMenuItems('tabs','misc1')
        #self.addEnabledMenuItems('tabs','payments1')


        # seperate Menus
        self.addEnabledMenuItems('proposal','proposal1')
        self.addEnabledMenuItems('supply','supply1')
        self.addEnabledMenuItems('gets','gets1')
        self.addEnabledMenuItems('positions','position1')
        #self.addEnabledMenuItems('payment','payments1')
        #self.addEnabledMenuItems('invoice','invoice1')
        self.addEnabledMenuItems('misc','misc1')
        

        
        # enabledMenues for Order
        self.addEnabledMenuItems('editProposal','new1', self.dicUserKeys['new'])
        self.addEnabledMenuItems('editProposal','edit1', self.dicUserKeys['edit'])
        self.addEnabledMenuItems('editProposal','delete1', self.dicUserKeys['delete'])
        self.addEnabledMenuItems('editProposal','print1', self.dicUserKeys['print'])

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
#        # enabledMenues for Invoice
#        self.addEnabledMenuItems('editInvoice','InvoiceEdit1', self.dicUserKeys['edit'])
#
#        # enabledMenues for Payment
#        self.addEnabledMenuItems('editPayment','payment_new', self.dicUserKeys['new'])
#        self.addEnabledMenuItems('editPayment','payment_edit', self.dicUserKeys['edit'])

        # to misc menu
        
        # enabledMenues for Save 
        self.addEnabledMenuItems('editSave','save1', self.dicUserKeys['save'])
        self.addEnabledMenuItems('editSave','SupplySave1', self.dicUserKeys['save'])
        self.addEnabledMenuItems('editSave','GetsSave1', self.dicUserKeys['save'])
        self.addEnabledMenuItems('editSave','PositionSave1', self.dicUserKeys['save'])
        #self.addEnabledMenuItems('editSave','InvoiceSave1', self.dicUserKeys['save'])
        self.addEnabledMenuItems('editSave','MiscSave', self.dicUserKeys['save'])
        #self.addEnabledMenuItems('editSave','payment_save', self.dicUserKeys['save'])


        # tabs from notebook
        self.tabProposal = 0
        self.tabSupply = 1
        self.tabGet = 2
        self.tabPosition = 3
        self.tabInvoice = 4
        self.tabMisc = 5
        self.tabPayment = 6
        self.OrderID = 0

        # start
        self.OrderID = orderid
        if Ordertype == 'Proposal':
            
            if self.dicOrder and not newOrder and self.OrderID == 0:
                print self.dicOrder
                existOrder = self.rpc.callRP('Order.checkExistModulProposal', self.dicUser,self.dicOrder)
                print 'existOrder = ', existOrder
                if not existOrder or existOrder == 'NONE':
                    print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~ create new'
                    self.rpc.callRP('Order.createNewOrder', self.dicUser,self.dicOrder)
                self.singleOrder.sWhere = ' where modul_order_number = ' + `self.dicOrder['ModulOrderNumber']` + ' and modul_number = ' + `self.dicOrder['ModulNumber']`
            elif self.dicOrder and newOrder and self.OrderID == 0:
                try:
                    dicResult = self.rpc.callRP('Order.createNewOrder', self.dicUser,self.dicOrder)
                    print dicResult
                    if dicResult and dicResult not in ['NONE','ERROR'] and int(dicResult) > 0:
                        self.OrderID = dicResult
                        print 'Order-Id = ',  self.OrderID
                        if self.OrderID > 0:
                            self.singleOrder.sWhere = ' where id = ' + `self.OrderID` 
                except:
                    pass
            elif self.OrderID > 0:
                self.singleOrder.sWhere = ' where id = ' + `self.OrderID`
                
                    
        ts = self.getWidget('treeMaterialgroup')
        #treeview.set_model(liststore)
        self.win1.add_accel_group(self.accel_group)
        print "Proposal-Windows = ",  self.win1
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

        
         
         
    #Menu File

    
    def on_quit1_activate(self, event):
        print "exit order v2"
        self.closeWindow()

    #Menu Propsal
  
    def on_save1_activate(self, event):
        print "save order v2"
        self.singleOrder.processStatus = 300
        self.singleOrder.save()
        self.setEntriesEditable(self.EntriesProposal, False)   
        self.tabChanged()
         
        
    def on_new1_activate(self, event):
        print "new proposal v2"
        self.singleOrder.newRecord()
        self.setEntriesEditable(self.EntriesProposal, True)

    def on_edit1_activate(self, event):
        self.setEntriesEditable(self.EntriesProposal, True)


    def on_print_proposal1_activate(self, event):
        dicOrder = {}
        print ' start proposal printing'
        dicOrder['orderid'] = self.singleOrder.ID
        dicOrder['orderNumber'] = self.singleOrder.getOrderNumber(self.singleOrder.ID)
        #dicOrder['proposalNumber'] = self.rpc.callRP('Order.setProposalNumber', dicOrder['orderid'], self.dicUser)
        print ' start proposal printing 2'
        proposalNumber = self.singleOrder.getProposalNumber() 
        dicOrder['proposalNumber'] =  proposalNumber        
        print ' start Proposal printing 3'
        
        print dicOrder
        
        Pdf = self.rpc.callRP('Report.server_proposal_document', dicOrder, self.dicUser)
        fname = self.showPdf(Pdf, self.dicUser,'PROPOSAL')
        #ok = self.rpc.callRP('Finances.createTicketFromInvoice',invoiceNumber,self.dicUser)
        # insert invoice into dms 
        self.documentTools.importDocument(self.singleDMS,self.dicUser,fname)
        self.singleDMS.ModulNumber = self.MN['PROPOSAL']
        self.singleDMS.sep_info_1 = self.singleOrder.ID    
        self.singleDMS.newRecord()
        self.singleDMS.newDate = self.getActualDateTime()['date']
        self.singleDMS.newTitle = _('proposal') + ' ' + `proposalNumber`
        print self.singleDMS.newDate
        self.singleDMS.newCategory = _('proposal')
        self.singleDMS.Rights = 'PROPOSAL'
        
        self.singleDMS.save(['document_image'])
        
        

    def on_all_open_invoice1_activate(self, event):
        
        if self.QuestionMsg('All new invoices are printed ! Do you wish this ? Really ?'):
            oldID = self.singleOrder.ID
            
            
            liOrder = self.rpc.callRP('Order.getAllOrderWithoutInvoice',self.dicUser)
            if liOrder and liOrder not in ['NONE','ERROR']:
                print 'print new Invoices '
                for newID in liOrder:
                    print newID
                    self.singleOrder.load(newID)
                    self.on_print_invoice1_activate(None)
                    
                    
        self.singleOrder.load(oldID)    
        
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

##    def on_list_of_invoices1_activate(self, event):
##        dicOrder = {}
##        print ' start List of Invoices printing'
##        dicOrder['Year'] = '2007'
##        print 'dicOrder = ', dicOrder
##        
##        Pdf = self.rpc.callRP('Report.server_order_list_of_invoices', dicOrder, self.dicUser)
##        self.showPdf(Pdf, self.dicUser,'INVOICE')

    def on_delete1_activate(self, event):
        print "delete order v2"
        self.singleOrder.deleteRecord()

 
    #Menu Gets
  
    def on_GetsSave1_activate(self, event):
        print "save order v2"
        self.singleOrderGet.ordernumber = self.singleOrder.ID
        self.singleOrderGet.save()
        self.setEntriesEditable(self.EntriesOrderGet, False)   
        self.tabChanged()
         
        
    def on_GetsNew1_activate(self, event):
        print "new order v2"
        self.singleOrderGet.newRecord()
        self.setEntriesEditable(self.EntriesOrderGet, True)

    def on_GetsEdit1_activate(self, event):
        self.setEntriesEditable(self.EntriesOrderGet, True)

    def on_GetsDelete1_activate(self, event):
        print "delete order v2"
        self.singleOrderGet.deleteRecord()


 
    # Menu Supply

    def on_SupplyNew1_activate(self, event):
        self.singleOrderSupply.newRecord()
        self.setEntriesEditable(self.EntriesOrderSupply, True)

    def on_SupplyEdit1_activate(self, event):
        self.setEntriesEditable(self.EntriesOrderSupply, True)

    def on_SupplySave1_activate(self, event):
        print "save Supply v2"
        self.singleOrderSupply.ordernumber = self.singleOrder.ID
        self.singleOrderSupply.save()
        self.setEntriesEditable(self.EntriesOrderSupply, False)
        self.tabChanged()
        

    def on_SupplyDelete1_activate(self, event):
        print "delete Supply v2"
        self.singleOrderSupply.deleteRecord()

    #Menu Positions
    def on_PositionSave1_activate(self, event):
        print "save Positions v2"
        EndPosition = False
        self.singleOrderPosition.orderID = self.singleOrder.ID
        print "Proposal ID by position",  self.singleOrderPosition.orderID
        if self.singleOrderPosition.ID == -1:
            self.singleOrderPosition.TreePos = self.singleOrderPosition.TREELAST
        self.singleOrderPosition.save()
        self.setEntriesEditable(self.EntriesProposalPosition, False)
        
        self.tabChanged()
           

    def on_PositionEdit1_activate(self, event):
        print 'PositionEdit1'
        self.setEntriesEditable(self.EntriesProposalPosition, True)
    
    def on_PositionNew1_activate(self, event):
        print "new Partner articles v2"
        self.singleOrderPosition.newRecord()
        self.setEntriesEditable(self.EntriesProposalPosition, True)

    def on_PositionDelete1_activate(self, event):
        print "delete Partner articles v2"
        self.singleOrderPosition.deleteRecord()
    # Menu Invoice 
    def on_InvoiceSave1_activate(self, event):
        print "save Invoice v2"
        
        self.singleOrderInvoice.orderId = self.singleOrder.ID
        self.singleOrderInvoice.save()
        self.setEntriesEditable(self.EntriesOrderInvoice, False)
        
        #self.tabChanged()
            

    def on_InvoiceEdit1_activate(self, event):
        print 'invoiceEdit1'
        self.setEntriesEditable(self.EntriesOrderInvoice, True)
    # Menu Misc
    def on_MiscEdit_activate(self, event):
        print 'MiscEdit1'
        self.setEntriesEditable(self.EntriesOrderMisc, True)
    
    def on_MiscSave_activate(self, event):
        print "save misc v2"
        self.singleOrder.setEntries(self.getDataEntries(self.EntriesOrderMisc) )
        self.singleOrder.save()
        self.setEntriesEditable(self.EntriesOrderMisc, False)
        self.singleOrder.setEntries(self.getDataEntries(self.EntriesOrder) )
        self.tabChanged()
  
    #Menu Payment
    def on_payment_save_activate(self, event):
        print "save Positions v2"
       
        self.singleOrderPayment.orderID = self.singleOrder.ID
    
        self.singleOrderPayment.invoiceNumber = self.singleOrder.getInvoiceNumber()
        

        newid = self.singleOrderPayment.save()
        print 'newid = ', newid
        ok = self.rpc.callRP('Finances.createTicketFromInpayment',newid,self.dicUser)

        self.setEntriesEditable(self.EntriesOrderPayment, False)
        
        self.tabChanged()

    def on_payment_edit_activate(self, event):
        print 'PositionEdit1'
        self.setEntriesEditable(self.EntriesOrderPayment, True)
    
    def on_payment_new_activate(self, event):
        print "new Ppayment v2"
        self.singleOrderPayment.newRecord()
        self.getWidget('ePaymentInvoiceNumber').set_text(`self.singleOrder.getInvoiceNumber()`)
        
        self.setEntriesEditable(self.EntriesOrderPayment, True)

    # create a order of this proposal
    def  on_create_order1_activate(self, event):
        print "start to change to Order"
        ok = self.rpc.callRP('Order.changeProposal2Order',self.singleOrder.ID,  self.dicUser)
        self.on_quit1_activate(event)
        
    # search button
    def on_bSearch_clicked(self, event, data=None):
        self.findOrder()
        
        
    def findOrder(self):
        print 'findAddress'
        self.out( 'Searching ....', self.ERROR)
        sNumber = self.getWidget('eFindOrderNumber').get_text()
        sDesignation = self.getWidget('eFindOrderDesignation').get_text()
        sID = self.getWidget('eFindOrderID').get_text()
        sInvoiceNumber = self.getWidget('eFindOrderInvoiceNumber').get_text()
        sYear = self.getWidget('eFindOrderYear').get_text()
        
        liSearch = []
        if sNumber:
            liSearch.append('number')
            liSearch.append(sNumber)
#            liSearch.append('lastname2')
#            liSearch.append(sName)
        if sID:
            liSearch.append('id')
            try:
                liSearch.append(int(sID))
            except:
                liSearch.append(0)
            
        if sDesignation:
            liSearch.append('designation')
            liSearch.append(sDesignation)
        if sYear:
            liSearch.append('date_part(orderedat,year)')
            liSearch.append(sYear)    
             
        if sInvoiceNumber:
            liSearch.append('###id = (select order_number from list_of_invoices where invoice_number = ' + sInvoiceNumber +')')
            liSearch.append(sInvoiceNumber)    
       
             
        self.singleOrder.sWhere = self.getWhere(liSearch) 
        
        
        self.oldTab = -1
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
                    sA = self.getCheckedValue(oneArticle['a'],  'toLocaleString')
                    sB = self.getCheckedValue(oneArticle['b'],  'toLocaleString')
                    sC = articleprice = self.getCheckedValue( oneArticle['c'],  'toLocaleString')
                    
                    iter = treestore.append(None,[sA +  ' - ' + sB + '  ' + sC +  '     ###' +`oneArticle['id']` ]) 
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
        cAcct = self.singleAccountInfo.getInfoLineForID(iAcctNumber)
        if cAcct and cAcct not in ['NONE','ERROR']:
            eAcctField.set_text(cAcct)
        
##        record = self.singleArticle.getFirstRecord()
##        if record:
##            print record
##            self.getWidget('eOrderPositionsUnit').set_text(record['unit'])
##            
##        if self.singleOrderPosition.ID == -1 and record:
##            self.getWidget('eOrderPositionsTaxVat').set_text(record['tax_vat'])
##          
    def on_eAccountNumber_changed(self, event):
        sAcct = event.get_text()
        
        id = self.rpc.callRP('Finances.getAcctID',sAcct, self.dicUser)
        if id > 0:
            self.getWidget('ePaymentAccountID').set_text(`id`)
            
    def createSimplePayment(self, sType):
        
        self.setMainwindowNotebook('F7')
        self.on_payment_new_activate(None)
        invoice_sum = self.rpc.callRP('Finances.getTotalAmount', self.singleOrder.ID, self.dicUser)
        invoice_sum =  self.getCheckedValue(invoice_sum,'toLocaleString')
        self.getWidget('ePaymentCashDiscount').set_text('0.00')
        self.getWidget('ePaymentInpayment').set_text(invoice_sum)
        dicDate = self.getActualDateTime()
        print dicDate
        print invoice_sum
        self.getWidget('ePaymentDate').set_text(dicDate['date'])
        print 'sType = ', self.dicUser['prefFinances'][sType]
        self.getWidget('eAccountNumber').set_text(self.dicUser['prefFinances'][sType])
        if 'cash' in sType:
            print 'cash found'
            self.getWidget('rPaymentCash').set_active(True)
        elif 'bank' in sType:
            print 'bank found'
            self.getWidget('rPaymentTransfer').set_active(True)
        elif 'Debit' in sType:
            print 'debit found'
            self.getWidget('rPaymentDirectDebit').set_active(True)
        elif 'creditCard' in sType:
            print 'creditCard found'
            self.getWidget('rPaymentCreditCard').set_active(True)
        
        self.on_payment_save_activate(None)
        
    def on_bInvoiceTOP_clicked(self, event):
        print 'choose TOP'
        top = cuon.PrefsFinance.prefsFinance.prefsFinancewindow(self.allTables)
        top.setChooseEntry('chooseTOP', self.getWidget( 'eInvoiceTOPID'))
        
    def on_eInvoiceTOPID_changed(self, event):
        print 'eTOPID changed'
        eTopField = self.getWidget('tvInvoiceTOP')
        try:
            liTop = self.singlePrefsFinanceTop.getTOP(long(self.getWidget( 'eInvoiceTOPID').get_text()))
            self.setTextbuffer(eTopField, liTop)
            
        except Exception,param:
            self.setTextbuffer(eTopField, ' ')
            print Exception,param

    def on_bSimpleCash1_clicked(self, event):
        self.createSimplePayment('cash1')
    def on_bSimpleCash2_clicked(self, event):
        self.createSimplePayment('cash2')
       
    def on_bSimpleBank1_clicked(self, event):
        self.createSimplePayment('bank1')
    def on_bSimpleBank2_clicked(self, event):
        self.createSimplePayment('bank2')
    def on_bSimpleBank3_clicked(self, event):
        self.createSimplePayment('bank3')
    def on_bDirectDebit1_clicked(self, event):
        self.createSimplePayment('directDebit1')
    def on_bDirectDebit2_clicked(self, event):
        self.createSimplePayment('directDebit2')
      
    def on_bDirectDebit3_clicked(self, event):
        self.createSimplePayment('directDebit3')
    
    def on_bCreditCard1_clicked(self, event):
        self.createSimplePayment('creditCard1')
      
    def on_bShowExtInfo_clicked(self, event ):
        print 'show ext. Infos '
        dms = cuon.DMS.dms.dmswindow(self.allTables,self.MN['Order'], {'1':self.singleOrder.ID})
        
    def on_bQuickAppend_clicked(self, event):
        # Qick append a positions
        if self.singleOrderPosition.ID != -1:
            self.on_PositionNew1_activate(event)
        if self.getWidget('eAmount').get_text() == '':
            print 'get_text none'
            self.getWidget('eAmount').set_text('1')
        self.getWidget('eArticleID').set_text(`self.fillArticlesNewID`)
        self.getWidget('ePrice').set_text(self.getCheckedValue(self.rpc.callRP('Article.getArticlePrice', self.fillArticlesNewID,self.dicUser),'toStringFloat'))
        self.getWidget('ePosition').set_text(`self.rpc.callRP('Order.getNextPosition', self.singleOrder.ID,self.dicUser)`)
        
        self.on_PositionSave1_activate(event)


    def on_Mainwindow_key_press_event(self, oEntry, data):
        ''' Overwrite def '''
        sKey = gtk.gdk.keyval_name(data.keyval)
        print 'sKey : ',sKey
        if self.tabOption == self.tabPosition:
            if sKey == 'KP_Add' :
                wAmount = self.getWidget('eAmount')

                self.on_PositionEdit1_activate(None)
                if wAmount.get_text() == '':
                    wAmount.set_text('1')
                else:
                    try:
                        f1 = float(wAmount.get_text())
                        f2 = f1 + 1.000
                        print f1, f2
                        wAmount.set_text( self.getCheckedValue(f2, 'toLocaleString'))
                        print 'gesetzte zahl = ', wAmount.get_text()
                    except Exception, params:
                        print Exception, params
                self.on_PositionSave1_activate(None)        

            elif sKey == 'KP_Subtract' :
                wAmount = self.getWidget('eAmount')

                self.on_PositionEdit1_activate(None)
                if wAmount.get_text() == '':
                    wAmount.set_text('0')
                else:
                    try:
                        
                        f1 = float(wAmount.get_text())
                        f2 = f1 - 1.000
                        print f1, f2
                        wAmount.set_text( self.getCheckedValue(f2, 'toLocaleString'))
                        print 'gesetzte zahl = ', wAmount.get_text()
                    except Exception, params:
                        print Exception, params            
                self.on_PositionSave1_activate(None)        
            else:
                self.MainwindowEventHandling(oEntry, data)
        
        else:
            self.MainwindowEventHandling(oEntry, data)
      
    def on_treeArticles_row_activated(self, event, data1, data2):
        self.on_bQuickAppend_clicked(event)

    def  on_tbCreateOrder_clicked (self, event):
        self.on_create_order1_activate(event)
        
    def on_tbNew_clicked(self,  event):
        if self.tabOption == self.tabProposal:
            self.on_new1_activate(event)
        elif self.tabOption == self.tabPosition:
            self.on_PositionNew1_activate(event)
            
            
    def on_tbEdit_clicked(self,  event):
        if self.tabOption == self.tabProposal:
            self.on_edit1_activate(event)
        elif self.tabOption == self.tabPosition:
            self.on_PositionEdit1_activate(event)
            
    def on_tbSave_clicked(self,  event):
        if self.tabOption == self.tabProposal: 
            self.on_save1_activate(event)    
        elif self.tabOption == self.tabPosition:
            self.on_PositionSave1_activate(event)
            
    
    # Tax Vat choose
    def  on_bTaxVatForAllPositions_clicked(self, event):
        print 'cbVat search'
        print event
        
        pf = cuon.PrefsFinance.prefsFinance.prefsFinancewindow(self.allTables)
        pf.setChooseEntry('chooseTaxVat', self.getWidget( 'eTaxVatForAllPositionsID'))
        
    def on_eTaxVatForAllPositionsID_changed(self, event):
        print 'eCategory changed'
        iTaxVat = self.getChangedValue('eTaxVatForAllPositionsID')
        sTaxVat = self.singlePrefsFinanceVat.getNameAndDesignation(iTaxVat)
        if sTaxVat:
            self.getWidget('eTaxVatForAllPositionsID').set_text(sTaxVat)
        else:
            self.getWidget('eTaxVatForAllPositionsID').set_text('')
 
 
    def refreshTree(self):
        self.singleOrder.disconnectTree()
        self.singleOrderSupply.disconnectTree()
        self.singleOrderGet.disconnectTree()
        self.singleOrderPosition.disconnectTree()
        #self.singleOrderInvoice.disconnectTree()
        
        if self.tabOption == self.tabProposal:
            self.singleOrder.setEntries(self.getDataEntries(self.EntriesProposal) )
            if self.OrderID > 0:
                self.singleOrder.sWhere = ' where id = ' + `self.OrderID`
            
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
            self.singleOrderPosition.sWhere  ='where orderid = ' + `int(self.singleOrder.ID)` + ' and articleid = articles.id '
            self.singleOrderPosition.connectTree()
            self.singleOrderPosition.refreshTree()
            
        elif self.tabOption == self.tabInvoice:
            #self.singleOrder.connectTree()
            #self.singleOrder.refreshTree()
            self.singleOrderInvoice.sWhere  ='where orderid = ' + `self.singleOrder.ID`
            print 'Singleid =',  self.singleOrderInvoice.findSingleId()
            self.singleOrderInvoice.fillEntries(self.singleOrderInvoice.findSingleId())
            
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
        if self.tabOption == self.tabProposal:
            #Proposal
            self.disableMenuItem('tabs')
            self.enableMenuItem('proposal')
            print 'Seite 0'
            self.editAction = 'editProposal'
            self.setTreeVisible(True)
        elif self.tabOption == self.tabSupply:
            #Partner
            self.disableMenuItem('tabs')
            self.enableMenuItem('supply')
            self.editAction = 'editSupply'
            self.setTreeVisible(True)

            print 'Seite 1'
            
        elif self.tabOption == self.tabGet:
            self.disableMenuItem('tabs')
            self.enableMenuItem('gets')
            self.editAction = 'editGets'
            self.setTreeVisible(True)
            print 'Seite 2'
        elif self.tabOption == self.tabPosition:
            self.disableMenuItem('tabs')
            self.enableMenuItem('positions')
            self.editAction = 'editPositions'
            self.setTreeVisible(True)
            print 'Seite 3'  
         
         
        elif self.tabOption == self.tabInvoice:
            self.disableMenuItem('tabs')
            self.enableMenuItem('invoice')
            self.editAction = 'editInvoice'
            self.setTreeVisible(False)
            print 'Seite 4'
            
        elif self.tabOption == self.tabMisc:
            self.disableMenuItem('tabs')
            self.enableMenuItem('misc')
            self.setTreeVisible(False)
            self.editAction = 'editMisc'
            print 'Seite 5'
            
        elif self.tabOption == self.tabPayment:
            self.disableMenuItem('tabs')
            self.enableMenuItem('payment')
            self.editAction = 'editPayment'
            self.setTreeVisible(True)
            print 'Seite 6'  
         
        # refresh the Tree
        self.refreshTree()
        self.enableMenuItem(self.editAction)
        self.editEntries = False
