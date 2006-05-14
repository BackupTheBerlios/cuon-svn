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
import cuon.DMS.documentTools
import cuon.DMS.dms
import SingleHibernation


class hibernationwindow(chooseWindows):

    
    def __init__(self, allTables):

        chooseWindows.__init__(self)

        self.loadGlade('hibernation.xml')
        self.win1 = self.getWidget('HibernationMainwindow')
        self.oDocumentTools = cuon.DMS.documentTools.documentTools()
        self.ModulNumber = self.MN['Hibernation']        
        self.allTables = allTables
        self.singleHibernation = SingleArticle.SingleArticle(allTables)
        self.singleHibernationPurchase = SingleArticlePurchase.SingleArticlePurchase(allTables)
        self.singleHibernationSales = SingleArticleSale.SingleArticleSale(allTables)
        self.singleHibernationWebshop = SingleArticleWebshop.SingleArticleWebshop(allTables)
        self.singleHibernationStock = SingleArticleStock.SingleArticleStock(allTables)
        self.singleAddress = cuon.Addresses.SingleAddress.SingleAddress(allTables)
        
        # self.singleHibernation.loadTable()
              
        self.EntriesArticles = 'articles.xml'
        self.EntriesArticlesPurchase = 'articles_purchase.xml'
        self.EntriesArticlesSales = 'articles_sales.xml'
        self.EntriesArticlesWebshop = 'articles_webshop.xml'
        self.EntriesArticlesStock = 'articles_stock.xml'
                
        
        #singleHibernation
 
 
        self.loadEntries(self.EntriesArticles)
        self.singleHibernation.setEntries(self.getDataEntries( self.EntriesArticles) )
        self.singleHibernation.setGladeXml(self.xml)
        self.singleHibernation.setTreeFields( ['number', 'designation'] )
#        self.singleHibernation.setStore( gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING,   gobject.TYPE_UINT) ) 
        self.singleHibernation.setTreeOrder('number')
        self.singleHibernation.setTree(self.xml.get_widget('tree1') )
        self.singleHibernation.setListHeader(['number', 'designation', ])
        
         #singleHibernationPurchase
        
        self.loadEntries(self.EntriesArticlesPurchase)
        self.singleHibernationPurchase.setEntries(self.getDataEntries( self.EntriesArticlesPurchase) )
        self.singleHibernationPurchase.setGladeXml(self.xml)
        self.singleHibernationPurchase.setTreeFields( ['designation' ] )
        self.singleHibernationPurchase.setStore( gtk.ListStore(gobject.TYPE_STRING,  gobject.TYPE_UINT) ) 
        self.singleHibernationPurchase.setTreeOrder('designation')
#        self.singleHibernationPurchase.setListHeader([''])

        self.singleHibernationPurchase.sWhere  ='where articles_number = ' + `self.singleHibernation.ID`
        self.singleHibernationPurchase.setTree(self.xml.get_widget('tree1') )
  
     #singleHibernationSales
        
        self.loadEntries(self.EntriesArticlesSales)
        self.singleHibernationSales.setEntries(self.getDataEntries( self.EntriesArticlesSales) )
        self.singleHibernationSales.setGladeXml(self.xml)
        self.singleHibernationSales.setTreeFields( ['designation'] )
        self.singleHibernationSales.setStore( gtk.ListStore(gobject.TYPE_STRING,  gobject.TYPE_UINT) ) 
        self.singleHibernationSales.setTreeOrder('designation')
        self.singleHibernationSales.setListHeader([_('Designation')])

        self.singleHibernationSales.sWhere  ='where articles_number = ' + `self.singleHibernation.ID`
        self.singleHibernationSales.setTree(self.xml.get_widget('tree1') )

  
  #singleHibernationWebshop
        
        self.loadEntries(self.EntriesArticlesWebshop)
        self.singleHibernationWebshop.setEntries(self.getDataEntries( self.EntriesArticlesWebshop) )
        self.singleHibernationWebshop.setGladeXml(self.xml)
##        self.singleHibernationWebshop.setTreeFields( ['articles_number'] )
 ##       self.singleHibernationWebshop.setStore( gtk.ListStore(gobject.TYPE_STRING,  gobject.TYPE_UINT) ) 
  ##      self.singleHibernationWebshop.setTreeOrder('articles_number')
   ##     self.singleHibernationWebshop.setListHeader([_('article')])

        self.singleHibernationWebshop.sWhere  ='where articles_number = ' + `self.singleHibernation.ID`
        self.singleHibernationWebshop.setTree(self.xml.get_widget('tree1') )

    #singleHibernationStock
        
        self.loadEntries(self.EntriesArticlesStock)
        self.singleHibernationStock.setEntries(self.getDataEntries( self.EntriesArticlesStock ))
        self.singleHibernationStock.setGladeXml(self.xml)
##        self.singleHibernationStock.setTreeFields( ['designation'] )
##        self.singleHibernationStock.setStore( gtk.ListStore(gobject.TYPE_STRING,  gobject.TYPE_UINT) ) 
##        self.singleHibernationStock.setTreeOrder('designation')
##        self.singleHibernationStock.setListHeader([_('Designation')])

        self.singleHibernationStock.sWhere  ='where articles_number = ' + `self.singleHibernation.ID`
        self.singleHibernationStock.setTree(self.xml.get_widget('tree1') )
  
        

        # Menu-items
        self.initMenuItems()

        # Close Menus for Tab

        self.addEnabledMenuItems('tabs','mi_article1')
        self.addEnabledMenuItems('tabs','mi_purchase1')
        self.addEnabledMenuItems('tabs','mi_sales1')


        # seperate Menus
        self.addEnabledMenuItems('article','mi_article1')
        self.addEnabledMenuItems('purchase','mi_purchase1')
        self.addEnabledMenuItems('sales','mi_sales1')

        
        # enabledMenues for Article
        self.addEnabledMenuItems('editArticle','new1', self.dicUserKeys['articles_new'])
        self.addEnabledMenuItems('editArticle','clear1', self.dicUserKeys['articles_delete'])
        self.addEnabledMenuItems('editArticle','print1', self.dicUserKeys['articles_print'])
        self.addEnabledMenuItems('editArticle','edit1',self.dicUserKeys['articles_edit'])

        # enabledMenues for ArticlePurchase
        self.addEnabledMenuItems('editPurchase','PurchaseNew1', self.dicUserKeys['articles_purchase_new'])
        self.addEnabledMenuItems('editPurchase','PurchaseClear1')
        self.addEnabledMenuItems('editPurchase','PurchaseEdit1', self.dicUserKeys['articles_purchase_edit'])
    
       # enabledMenues for ArticleSales
        self.addEnabledMenuItems('editSales','SalesNew1')
        self.addEnabledMenuItems('editSales','SalesClear1')
        self.addEnabledMenuItems('editSales','SalesEdit1')

       # enabledMenues for ArticleWebshop
        self.addEnabledMenuItems('editWebshop','WebshopClear1')
        self.addEnabledMenuItems('editWebshop','WebshopEdit1')

       # enabledMenues for ArticleStock
        self.addEnabledMenuItems('editStock','StockClear1')
        self.addEnabledMenuItems('editStock','StockEdit1')



        # tabs from notebook
        self.tabArticle = 0
        self.tabPurchase = 1
        self.tabSales = 2
        self.tabWebshop = 3
        self.tabStock = 4
        

        # start
        
        self.tabChanged()

        # enabled menus for article
        self.addEnabledMenuItems('editArticle','new1')
        self.addEnabledMenuItems('editArticle','clear1')
        self.addEnabledMenuItems('editArticle','print1')

        # enabled menus for article_purchase
        self.addEnabledMenuItems('editArticlePurchase','PurchaseNew1')
        self.addEnabledMenuItems('editArticlePurchase','PurchaseClear1')

        # init Comboboxes
        tax_vat =  self.rpc.callRP('src.Misc.py_getListOfTaxVat', self.dicUser)
        cb = self.getWidget('cbVat')
        
        for i in range(len(tax_vat)) :
            li = gtk.ListItem(tax_vat[i])
            cb.list.append_items([li])
            li.show()
    
        self.win1.add_accel_group(self.accel_group)
    #Menu File
              
    def on_quit1_activate(self, event):
        print "exit articles v2"
        self.closeWindow()
  

    #Menu Article
  
    def on_save1_activate(self, event):
        print "save articles v2"
        self.singleHibernation.save()
        self.setEntriesEditable(self.EntriesArticles, False)
        self.tabChanged()
         
        
    def on_new1_activate(self, event):
        print "new articles v2"
        self.singleHibernation.newRecord()
        self.setEntriesEditable(self.EntriesArticles, True)
        

    def on_edit1_activate(self, event):
        self.setEntriesEditable(self.EntriesArticles, True)

    def on_delete1_activate(self, event):
        print "delete articles v2"
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
        

  #Menu Purchase
        
   
    def on_PurchaseSave1_activate(self, event):
        print "save Partner articles v2"
        self.singleHibernationPurchase.articlesNumber = self.singleHibernation.ID
        self.singleHibernationPurchase.save()
        self.setEntriesEditable(self.EntriesArticlesPurchase, False)

        self.tabChanged()
        
    def on_PurchaseNew1_activate(self, event):
        print "new Partner articles v2"
        self.singleHibernationPurchase.newRecord()
        self.setEntriesEditable(self.EntriesArticlesPurchase, True)

    def on_PurchaseEdit1_activate(self, event):
        self.setEntriesEditable(self.EntriesArticlesPurchase, True)

    def on_PurchaseClear1_activate(self, event):
        print "delete Partner articles v2"
        self.singleHibernationPurchase.deleteRecord()

    #Articles Sales
    def on_SalesSave1_activate(self, event):
        print "save Partner articles v2"
        
        self.singleHibernationSales.articlesNumber = self.singleHibernation.ID
        self.singleHibernationSales.save()
        self.setEntriesEditable(self.EntriesArticlesSales, False)

        self.tabChanged()
        
    def on_SalesNew1_activate(self, event):
        print "new Partner articles v2"
        self.singleHibernationSales.newRecord()
        self.setEntriesEditable(self.EntriesArticlesSales, True)

    def on_SalesEdit1_activate(self, event):
        self.setEntriesEditable(self.EntriesArticlesSales, True)

    def on_SalesClear1_activate(self, event):
        print "delete Partner articles v2"
        self.singleHibernationSales.deleteRecord()


 #Articles Webshop
    def on_WebshopSave1_activate(self, event):
        print "save  articles Webshop v2"
        print "article ID = ", self.singleHibernation.ID
        self.singleHibernationWebshop.articlesNumber = self.singleHibernation.ID
        self.singleHibernationWebshop.save()
        self.setEntriesEditable(self.EntriesArticlesWebshop, False)

        self.tabChanged()
        
    def on_WebshopNew1_activate(self, event):
        print "new Partner articles v2"
        self.singleHibernationWebshop.newRecord()
        self.setEntriesEditable(self.EntriesArticlesWebshop, True)

    def on_WebshopEdit1_activate(self, event):
        self.setEntriesEditable(self.EntriesArticlesWebshop, True)

    def on_WebshopClear1_activate(self, event):
        print "delete Partner articles v2"
        self.singleHibernationWebshop.deleteRecord()


 #Articles Stock
    def on_StockSave1_activate(self, event):
        print "save Partner articles v2"
        
        self.singleHibernationStock.articlesNumber = self.singleHibernation.ID
        self.singleHibernationStock.save()
        self.setEntriesEditable(self.EntriesArticlesStock, False)

        self.tabChanged()
        
    def on_StockNew1_activate(self, event):
        print "new Partner articles v2"
        self.singleHibernationStock.newRecord()
        self.setEntriesEditable(self.EntriesArticlesStock, True)

    def on_StockEdit1_activate(self, event):
        self.setEntriesEditable(self.EntriesArticlesStock, True)

    def on_StockClear1_activate(self, event):
        print "delete Partner articles v2"
        self.singleHibernationStock.deleteRecord()



    # Menu Lists

    def on_liArticlesNumber1_activate(self, event):
        self.out( "lists startet")
        Pdf = cuon.Articles.lists_articles_number1.lists_articles_number1()





    def on_chooseArticle_activate(self, event):
        # choose Article from other Modul
        self.setChooseValue(self.singleHibernation.ID)
        print 'Article-ID = ' + `self.singleHibernation.ID`
        self.closeWindow()
  

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
        self.searchArticle()


    def on_eFindNumber_editing_done(self, event):
        print 'Find Number'
        self.searchArticle()

    def on_eFindNumber_key_press_event(self, entry,event):
        if self.checkKey(event,'NONE','Return'):
            self.searchArticle()
            
    def on_eFindDesignation_editing_done(self, event):
        print 'Find Designation'
        self.searchArticle()

    def on_eFindDesignation_key_press_event(self, entry,event):
        if self.checkKey(event,'NONE','Return'):
            self.searchArticle()
        


    def searchArticle(self):
        self.out( 'Searching ....', self.ERROR)
        sNumber = self.getWidget('eFindNumber').get_text()
        sDesignation = self.getWidget('eFindDesignation').get_text()
        self.out('Name and City = ' + sNumber + ', ' + sDesignation, self.ERROR)
        
        #self.singleHibernation.sWhere = 'where number ~* \'.*' + sNumber + '.*\' and designation ~* \'.*' + sDesignation + '.*\''
        liSearch = ['number',sNumber, 'designation', sDesignation]
        self.singleHibernation.sWhere = self.getWhere(liSearch)
        self.out(self.singleHibernation.sWhere, self.ERROR)
        self.refreshTree()

    def refreshTree(self):
        self.singleHibernation.disconnectTree()
        self.singleHibernationPurchase.disconnectTree()
        
        if self.tabOption == self.tabArticle:
            self.singleHibernation.connectTree()
            self.singleHibernation.refreshTree()

        elif self.tabOption == self.tabPurchase:
            self.singleHibernationPurchase.sWhere  ='where articles_number = ' + `int(self.singleHibernation.ID)`
            self.singleHibernationPurchase.connectTree()
            self.singleHibernationPurchase.refreshTree()

        elif self.tabOption == self.tabSales:
            self.singleHibernationSales.sWhere  ='where articles_number = ' + `int(self.singleHibernation.ID)`
            self.singleHibernationSales.connectTree()
            self.singleHibernationSales.refreshTree()

        elif self.tabOption == self.tabWebshop:

            self.singleHibernationWebshop.sWhere  ='where articles_number = ' + `int(self.singleHibernation.ID)`
            self.singleHibernationWebshop.setEmptyEntries()
            self.singleHibernationWebshop.getFirstRecord()
            
            self.singleHibernationWebshop.fillEntries(self.singleHibernationWebshop.ID)

            
            print "-----------> end tab Webshop"
            

        elif self.tabOption == self.tabStock:
            print "-----------> begin tab Stock"
            self.singleHibernationStock.sWhere  ='where articles_number = ' + `int(self.singleHibernation.ID)`
            self.singleHibernationWebshop.setEmptyEntries()
            self.singleHibernationStock.getFirstRecord()
            if self.singleHibernationStock.ID > 0:
                self.singleHibernationStock.fillEntries(self.singleHibernationStock.ID)
            else:
                dicAr = {'articles_number':self.singleHibernation.getArticleNumber(self.singleHibernation.ID)}
                self.singleHibernationStock.fillOtherEntries(dicAr)

            print "-----------> end tab Stock"
     


         
    def tabChanged(self):
        print 'tab changed to :'  + str(self.tabOption)
        self.setTreeVisible(True)
        if self.tabOption == self.tabArticle:
            #Address
            self.disableMenuItem('tabs')
            self.enableMenuItem('article')
            print 'Seite 0'
            self.editAction = 'editArticle'
            
        elif self.tabOption == self.tabPurchase:
            #Partner
            self.disableMenuItem('tabs')
            self.enableMenuItem('purchase')
            self.editAction = 'editArticlePurchase'
            print 'Seite 1'
            
        elif self.tabOption == self.tabSales:
            self.disableMenuItem('tabs')
            self.enableMenuItem('sales')
            self.editAction = 'editArticleSales'
            print 'Seite 2'

        elif self.tabOption == self.tabWebshop:
            self.disableMenuItem('tabs')
            self.enableMenuItem('sales')
            self.editAction = 'editArticleWebshop'
            self.setTreeVisible(False)
            print 'Seite 3'

        elif self.tabOption == self.tabStock:
            self.disableMenuItem('tabs')
            self.enableMenuItem('sales')
            self.editAction = 'editArticleStock'
            self.setTreeVisible(False)
            print 'Seite 4'
            
        # refresh the Tree
        self.refreshTree()
        self.enableMenuItem(self.editAction)
        self.editEntries = False
