# -*- coding: utf-8 -*-

##Copyright (C) [2003]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 

from cuon.Windows.chooseWindows import chooseWindows
import logging
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import gobject
from gtk import TRUE, FALSE
import SingleStock
import SingleStockGoods

import cuon.Articles.articles
import cuon.Addresses.addresses
import cuon.Addresses.SingleAddress
import cuon.Addresses.SinglePartner

import cuon.Articles.SingleArticle


class stockwindow(chooseWindows):
    """
    @author: Jürgen Hamel
    @organization: Cyrus-Computer GmbH, D-32584 Löhne
    @copyright: by Jürgen Hamel
    @license: GPL ( GNU GENERAL PUBLIC LICENSE )
    @contact: jh@cyrus.de
    """


    def __init__(self, allTables):

        chooseWindows.__init__(self)

        self.loadGlade('stock.xml')
        self.win1 = self.getWidget('StockMainwindow')
        
        self.allTables = allTables
        self.singleStock = SingleStock.SingleStock(allTables)
        self.singleStockGoods = SingleStockGoods.SingleStockGoods(allTables)
        self.singleAddress = cuon.Addresses.SingleAddress.SingleAddress(allTables)
        self.singlePartner = cuon.Addresses.SinglePartner.SinglePartner(allTables)
        
        self.singleArticle = cuon.Articles.SingleArticle.SingleArticle(allTables)
       
        # self.singleOrder.loadTable()
              
        self.EntriesStock = 'stock.xml'
        self.EntriesStockGoods = 'stockgoods.xml'
        
        
        
        #singleStock
        
        self.loadEntries(self.EntriesStock)
        self.singleStock.setEntries(self.getDataEntries('stock.xml') )
        self.singleStock.setGladeXml(self.xml)
        self.singleStock.setTreeFields( ['name', 'designation'] )
        self.singleStock.setStore( gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING,   gobject.TYPE_UINT) ) 
        self.singleStock.setTreeOrder('name')
        self.singleStock.setTree(self.xml.get_widget('tree1') )
        self.singleStock.setListHeader([_('name'), _('designation') ])
        
         #singleStockGoods
        
        self.loadEntries(self.EntriesStockGoods)
        self.singleStockGoods.setEntries(self.getDataEntries('stockgoods.xml') )
        self.singleStockGoods.setGladeXml(self.xml)
        self.singleStockGoods.setTreeFields( ['designation' ] )
        self.singleStockGoods.setStore( gtk.ListStore(gobject.TYPE_STRING,  gobject.TYPE_UINT) ) 
        self.singleStockGoods.setTreeOrder('designation')
        self.singleStockGoods.setListHeader([_('Designation')])

        self.singleStockGoods.sWhere  ='where stock_id = ' + `self.singleStock.ID`
        self.singleStockGoods.setTree(self.xml.get_widget('tree1') )

        

        # Menu-items
        self.initMenuItems()

        # Close Menus for Tab

        self.addEnabledMenuItems('tabs','stock1')
        self.addEnabledMenuItems('tabs','goods1')


        # seperate Menus
        self.addEnabledMenuItems('stock','stock1')
        self.addEnabledMenuItems('goods','goods1')

        
        # enabledMenues for Stock
        self.addEnabledMenuItems('editStock','New1')
        self.addEnabledMenuItems('editStock','Edit1')
        self.addEnabledMenuItems('editStock','Delete1')

        # enabledMenues for StockGoods
        self.addEnabledMenuItems('editGoods','goodsnew1')
        self.addEnabledMenuItems('editGoods','goodsedit1')
        self.addEnabledMenuItems('editGoods','goodsclear1')
    

        # tabs from notebook
        self.tabStock = 0
        self.tabGoods = 1

        # start
        
        self.tabChanged()

   
         
         
    #Menu File

    def on_quit1_activate(self, event):
        print "exit stock"
        self.closeWindow()


    #Menu Stock
  
    def on_Save1_activate(self, event):
        print "save stock v2"
        self.singleStock.save()
        self.setEntriesEditable(self.EntriesStock, FALSE)   
        self.tabChanged()
         
        
    def on_New1_activate(self, event):
        print "new stock v2"
        self.singleStock.newRecord()
        self.setEntriesEditable(self.EntriesStock, TRUE)

    def on_Edit1_activate(self, event):
        self.setEntriesEditable(self.EntriesStock, TRUE)

    def on_Delete1_activate(self, event):
        print "delete stock v2"
        self.singleStock.deleteRecord()

 
    #Menu stockGoods
    

    def on_GoodsNew1_activate(self, event):
        self.singleStockGoods.newRecord()
        self.setEntriesEditable(self.EntriesStockGoods, TRUE)

    def on_GoodsEdit1_activate(self, event):
        self.setEntriesEditable(self.EntriesStockGoods, TRUE)

    def on_GoodsSave1_activate(self, event):
        print "save Goods v2"
        self.singleStockGoods.stock_id = self.singleStock.ID
        self.singleStockGoods.save()
        self.setEntriesEditable(self.EntriesStockGoods, FALSE)
        self.tabChanged()
        

    def on_GoodsClear1_activate(self, event):
        print "delete Goods v2"
        self.singleStockGoods.deleteRecord()

  


    # search button
    def on_bSearch_clicked(self, event):
        self.out( 'Searching ....', self.ERROR)
        sNumber = self.getWidget('eFindNumber').get_text()
        sDesignation = self.getWidget('eFindDesignation').get_text()
        self.out('Name and City = ' + sNumber + ', ' + sDesignation, self.ERROR)
        self.singleStock.sWhere = 'where number ~* \'.*' + sNumber + '.*\' and designation ~* \'.*' + sDesignation + '.*\''
        self.out(self.singleStock.sWhere, self.ERROR)
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

    def refreshTree(self):
        self.singleStock.disconnectTree()
        self.singleStockGoods.disconnectTree()
        
        if self.tabOption == self.tabStock:
            self.singleStock.connectTree()
            self.singleStock.refreshTree()

        elif self.tabOption == self.tabGoods:
            self.singleStockGoods.sWhere  ='where ordernumber = ' + `int(self.singleStock.ID)`
            self.singleStockGoods.connectTree()
            self.singleStockGoods.refreshTree()

  
         
    def tabChanged(self):
        print 'tab changed to :'  + str(self.tabOption)
        if self.tabOption == self.tabStock:
            #Address
            self.disableMenuItem('tabs')
            self.enableMenuItem('stock')
            print 'Seite 0'
            self.editAction = 'editStock'
            
        elif self.tabOption == self.tabGoods:
            #Partner
            self.disableMenuItem('tabs')
            self.enableMenuItem('goods')
            self.editAction = 'editGoods'
            print 'Seite 1'
    
        # refresh the Tree
        self.refreshTree()
        self.enableMenuItem(self.editAction)
        self.editEntries = FALSE
