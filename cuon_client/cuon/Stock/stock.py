# -*- coding: utf-8 -*-

##Copyright (C) [2003]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

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
import cuon.Stock.lists_stockgoods_number1

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
       
              
        self.EntriesStock = 'stock.xml'
        self.EntriesStockGoods = 'stockgoods.xml'
        
        
        
        #singleStock
        
        self.loadEntries(self.EntriesStock)
        self.singleStock.setEntries(self.getDataEntries('stock.xml') )
        self.singleStock.setGladeXml(self.xml)
        self.singleStock.setTreeFields( ['name', 'designation'] )
        self.singleStock.setStore( gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING,   gobject.TYPE_UINT) ) 
        self.singleStock.setTreeOrder('name')
        self.singleStock.setTree(self.xml.get_widget('tv_stock') )
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
        self.singleStockGoods.setTree(self.xml.get_widget('tv_goods') )

        

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
        self.singleStockGoods.article_id = self.singleArticle.ID        
        self.singleStockGoods.save()
        self.setEntriesEditable(self.EntriesStockGoods, FALSE)
        self.tabChanged()
        

    def on_GoodsClear1_activate(self, event):
        print "delete Goods v2"
        self.singleStockGoods.deleteRecord()

    # Menu Lists

    def on_articleList1_activate(self, event):
        self.out( "lists startet")
        Pdf = cuon.Stock.lists_stockgoods_number1.lists_stockgoods_number1()


  


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

 
    # Tab Supply choose address 
    def on_bSearchSupply_clicked(self, event):
        adr = cuon.Addresses.addresses.addresswindow(self.allTables)
        adr.setChooseEntry('chooseAddress', self.getWidget( 'eSupplyNumber'))

        
        # Tab Positions choose article 
    def on_bArticleSearch_clicked(self, event):
        ar = cuon.Articles.articles.articleswindow(self.allTables)
        ar.setChooseEntry('chooseArticle', self.getWidget( 'eArticleID'))

                           

    def on_eArticleID_changed(self, event):
        print 'eArticle changed'
        try:
            iArtNumber = self.getChangedValue('eArticleID')
            print 'eArticleID', iArtNumber
            self.singleArticle.load(iArtNumber)
            firstRecord  = self.singleArticle.getFirstRecord()
            print 'firstRecord by article = ', `firstRecord`
            if firstRecord.has_key('number'):
                self.getWidget('eGoodsArticleNumber').set_text(firstRecord['number'])
                if firstRecord['designation'] :
                    self.getWidget('eGoodsArticleDesignation1').set_text(firstRecord['designation'])
        except Exception,param:
            print Exception, param
        
    def refreshTree(self):
        self.singleStock.disconnectTree()
        self.singleStockGoods.disconnectTree()
        
        if self.tabOption == self.tabStock:
            self.singleStock.connectTree()
            self.singleStock.refreshTree()

        elif self.tabOption == self.tabGoods:
            self.singleStockGoods.sWhere  ='where stock_id = ' + `int(self.singleStock.ID)`
            self.singleStockGoods.connectTree()
            self.singleStockGoods.refreshTree()

    def on_tbNew_clicked(selfself,  event):
        if self.tabOption == self.tabStock:
             self.activateClick('new1')
        elif self.tabOption == self.tabGoods:
             self.activateClick('goodsnew1')
    def on_tbEdit_clicked(selfself,  event):
        if self.tabOption == self.tabStock:
             self.activateClick('edit1')
        elif self.tabOption == self.tabGoods:
             self.activateClick('goodsedit1')
           
    def on_tbSave_clicked(selfself,  event):
        if self.tabOption == self.tabStock:
             self.activateClick('save1')
        elif self.tabOption == self.tabGoods:
             self.activateClick('goodssave1')
            
         
    def tabChanged(self):
        print 'tab changed to :'  + str(self.tabOption)
        if self.tabOption == self.tabStock:
            #Stock
            self.disableMenuItem('tabs')
            self.enableMenuItem('stock')
            print 'Seite 0'
            self.editAction = 'editStock'
            
        elif self.tabOption == self.tabGoods:
            #Goods
            self.disableMenuItem('tabs')
            self.enableMenuItem('goods')
            self.editAction = 'editGoods'
            print 'Seite 1'
    
        # refresh the Tree
        self.refreshTree()
        self.enableMenuItem(self.editAction)
        self.editEntries = FALSE
