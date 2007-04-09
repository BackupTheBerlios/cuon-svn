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
import SingleArticle
import SingleArticlePurchase
import SingleArticleSale
import SingleArticleWebshop
import SingleArticleStock

import logging
from cuon.Windows.chooseWindows  import chooseWindows
import cuon.Addresses.addresses
import cuon.Addresses.SingleAddress
import cuon.DMS.documentTools
import cuon.DMS.dms
import cuon.Articles.lists_articles_number1
import cuon.Articles.materialgroup
import cuon.Articles.SingleMaterialgroups



class articleswindow(chooseWindows):

    
    def __init__(self, allTables):

        chooseWindows.__init__(self)
        self.loadGlade('articles.xml', 'ArticlesMainwindow')
        #self.win1 = self.getWidget('ArticlesMainwindow')
        self.win1.maximize()
        
        self.oDocumentTools = cuon.DMS.documentTools.documentTools()
        self.ModulNumber = self.MN['Articles']        
        self.allTables = allTables
        self.singleArticle = SingleArticle.SingleArticle(allTables)
        self.singleArticlePurchase = SingleArticlePurchase.SingleArticlePurchase(allTables)
        self.singleArticleSales = SingleArticleSale.SingleArticleSale(allTables)
        self.singleArticleWebshop = SingleArticleWebshop.SingleArticleWebshop(allTables)
        self.singleArticleStock = SingleArticleStock.SingleArticleStock(allTables)
        self.singleAddress = cuon.Addresses.SingleAddress.SingleAddress(allTables)
        
        self.singleMaterialGroup = cuon.Articles.SingleMaterialgroups.SingleMaterialgroups(allTables)
        # self.singleArticle.loadTable()
              
        self.EntriesArticles = 'articles.xml'
        self.EntriesArticlesPurchase = 'articles_purchase.xml'
        self.EntriesArticlesSales = 'articles_sales.xml'
        self.EntriesArticlesWebshop = 'articles_webshop.xml'
        self.EntriesArticlesStock = 'articles_stock.xml'
                
        
        #singleArticle
 
 
        self.loadEntries(self.EntriesArticles)
        self.singleArticle.setEntries(self.getDataEntries( self.EntriesArticles) )
        self.singleArticle.setGladeXml(self.xml)
        self.singleArticle.setTreeFields( ['number', 'designation'] )
#        self.singleArticle.setStore( gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING,   gobject.TYPE_UINT) ) 
        self.singleArticle.setTreeOrder('number')
        self.singleArticle.setTree(self.xml.get_widget('tree1') )
        self.singleArticle.setListHeader(['number', 'designation', ])
        
         #singleArticlePurchase
        
        self.loadEntries(self.EntriesArticlesPurchase)
        self.singleArticlePurchase.setEntries(self.getDataEntries( self.EntriesArticlesPurchase) )
        self.singleArticlePurchase.setGladeXml(self.xml)
        self.singleArticlePurchase.setTreeFields( ['designation' ] )
        self.singleArticlePurchase.setStore( gtk.ListStore(gobject.TYPE_STRING,  gobject.TYPE_UINT) ) 
        self.singleArticlePurchase.setTreeOrder('designation')
#        self.singleArticlePurchase.setListHeader([''])

        self.singleArticlePurchase.sWhere  ='where articles_number = ' + `self.singleArticle.ID`
        self.singleArticlePurchase.setTree(self.xml.get_widget('tree1') )
  
     #singleArticleSales
        
        self.loadEntries(self.EntriesArticlesSales)
        self.singleArticleSales.setEntries(self.getDataEntries( self.EntriesArticlesSales) )
        self.singleArticleSales.setGladeXml(self.xml)
        self.singleArticleSales.setTreeFields( ['designation'] )
        self.singleArticleSales.setStore( gtk.ListStore(gobject.TYPE_STRING,  gobject.TYPE_UINT) ) 
        self.singleArticleSales.setTreeOrder('designation')
        self.singleArticleSales.setListHeader([_('Designation')])

        self.singleArticleSales.sWhere  ='where articles_number = ' + `self.singleArticle.ID`
        self.singleArticleSales.setTree(self.xml.get_widget('tree1') )

  
  #singleArticleWebshop
        
        self.loadEntries(self.EntriesArticlesWebshop)
        self.singleArticleWebshop.setEntries(self.getDataEntries( self.EntriesArticlesWebshop) )
        self.singleArticleWebshop.setGladeXml(self.xml)
##        self.singleArticleWebshop.setTreeFields( ['articles_number'] )
 ##       self.singleArticleWebshop.setStore( gtk.ListStore(gobject.TYPE_STRING,  gobject.TYPE_UINT) ) 
  ##      self.singleArticleWebshop.setTreeOrder('articles_number')
   ##     self.singleArticleWebshop.setListHeader([_('article')])

        self.singleArticleWebshop.sWhere  ='where articles_number = ' + `self.singleArticle.ID`
        self.singleArticleWebshop.setTree(self.xml.get_widget('tree1') )

    #singleArticleStock
        
        self.loadEntries(self.EntriesArticlesStock)
        self.singleArticleStock.setEntries(self.getDataEntries( self.EntriesArticlesStock ))
        self.singleArticleStock.setGladeXml(self.xml)
##        self.singleArticleStock.setTreeFields( ['designation'] )
##        self.singleArticleStock.setStore( gtk.ListStore(gobject.TYPE_STRING,  gobject.TYPE_UINT) ) 
##        self.singleArticleStock.setTreeOrder('designation')
##        self.singleArticleStock.setListHeader([_('Designation')])

        self.singleArticleStock.sWhere  ='where articles_number = ' + `self.singleArticle.ID`
        self.singleArticleStock.setTree(self.xml.get_widget('tree1') )
  
        

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

       
        self.win1.add_accel_group(self.accel_group)
    #Menu File
              
    def on_quit1_activate(self, event):
        print "exit articles v2"
        self.closeWindow()
  

    #Menu Article
  
    def on_save1_activate(self, event):
        print "save articles v2"
        self.singleArticle.save()
        self.setEntriesEditable(self.EntriesArticles, False)
        self.tabChanged()
         
        
    def on_new1_activate(self, event):
        print "new articles v2"
        self.singleArticle.newRecord()
        self.setEntriesEditable(self.EntriesArticles, True)
        

    def on_edit1_activate(self, event):
        self.setEntriesEditable(self.EntriesArticles, True)

    def on_delete1_activate(self, event):
        print "delete articles v2"
        self.singleArticle.deleteRecord()


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
        if self.singleArticle.ID > 0:
            print 'ModulNumber', self.ModulNumber
            Dms = cuon.DMS.dms.dmswindow(self.allTables, self.ModulNumber, {'1':self.singleArticle.ID})
        

  #Menu Purchase
        
   
    def on_PurchaseSave1_activate(self, event):
        print "save Partner articles v2"
        self.singleArticlePurchase.articlesNumber = self.singleArticle.ID
        self.singleArticlePurchase.save()
        self.setEntriesEditable(self.EntriesArticlesPurchase, False)

        self.tabChanged()
        
    def on_PurchaseNew1_activate(self, event):
        print "new Partner articles v2"
        self.singleArticlePurchase.newRecord()
        self.setEntriesEditable(self.EntriesArticlesPurchase, True)

    def on_PurchaseEdit1_activate(self, event):
        self.setEntriesEditable(self.EntriesArticlesPurchase, True)

    def on_PurchaseClear1_activate(self, event):
        print "delete Partner articles v2"
        self.singleArticlePurchase.deleteRecord()

    #Articles Sales
    def on_SalesSave1_activate(self, event):
        print "save Partner articles v2"
        
        self.singleArticleSales.articlesNumber = self.singleArticle.ID
        self.singleArticleSales.save()
        self.setEntriesEditable(self.EntriesArticlesSales, False)

        self.tabChanged()
        
    def on_SalesNew1_activate(self, event):
        print "new Partner articles v2"
        self.singleArticleSales.newRecord()
        self.setEntriesEditable(self.EntriesArticlesSales, True)

    def on_SalesEdit1_activate(self, event):
        self.setEntriesEditable(self.EntriesArticlesSales, True)

    def on_SalesClear1_activate(self, event):
        print "delete Partner articles v2"
        self.singleArticleSales.deleteRecord()


 #Articles Webshop
    def on_WebshopSave1_activate(self, event):
        print "save  articles Webshop v2"
        print "article ID = ", self.singleArticle.ID
        self.singleArticleWebshop.articlesNumber = self.singleArticle.ID
        self.singleArticleWebshop.save()
        self.setEntriesEditable(self.EntriesArticlesWebshop, False)

        self.tabChanged()
        
    def on_WebshopNew1_activate(self, event):
        print "new Partner articles v2"
        self.singleArticleWebshop.newRecord()
        self.setEntriesEditable(self.EntriesArticlesWebshop, True)

    def on_WebshopEdit1_activate(self, event):
        self.setEntriesEditable(self.EntriesArticlesWebshop, True)

    def on_WebshopClear1_activate(self, event):
        print "delete Partner articles v2"
        self.singleArticleWebshop.deleteRecord()

    def on_bChooseCategory_clicked(self, event):
        pass
        
 #Articles Stock
    def on_StockSave1_activate(self, event):
        print "save Partner articles v2"
        
        self.singleArticleStock.articlesNumber = self.singleArticle.ID
        self.singleArticleStock.save()
        self.setEntriesEditable(self.EntriesArticlesStock, False)

        self.tabChanged()
        
    def on_StockNew1_activate(self, event):
        print "new Partner articles v2"
        self.singleArticleStock.newRecord()
        self.setEntriesEditable(self.EntriesArticlesStock, True)

    def on_StockEdit1_activate(self, event):
        self.setEntriesEditable(self.EntriesArticlesStock, True)

    def on_StockClear1_activate(self, event):
        print "delete Partner articles v2"
        self.singleArticleStock.deleteRecord()



    # Menu Lists

    def on_liArticlesNumber1_activate(self, event):
        self.out( "lists startet")
        Pdf = cuon.Articles.lists_articles_number1.lists_articles_number1()





    def on_chooseArticle_activate(self, event):
        # choose Article from other Modul
        self.setChooseValue(self.singleArticle.ID)
        print 'Article-ID = ' + `self.singleArticle.ID`
        self.closeWindow()
  
    def on_tree1_row_activated(self, event, data1, data2):
        print 'DoubleClick tree1'
        self.activateClick('chooseArticle', event)
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
        liSearch = []
        if sNumber:
            liSearch.append('number')
            liSearch.append(sNumber)
            
        if sDesignation:
            liSearch.append('designation')
            liSearch.append(sDesignation)
                
        self.singleArticle.sWhere = self.getWhere(liSearch)
        self.out(self.singleArticle.sWhere, self.ERROR)
        self.refreshTree()


    
    def on_bChooseMaterialGroup_clicked(self, event):
        print 'materialgroup'
        mag = cuon.Articles.materialgroup.materialgroupwindow(self.allTables)
        mag.setChooseEntry('chooseMaterialgroup', self.getWidget( 'eCategoryNr'))
        
    def on_eCategoryNr_changed(self, event):
        print 'eCategory changed'
        iMaterialGroup = self.getChangedValue('eCategoryNr')
        sGroupName = self.singleMaterialGroup.getNameAndDesignation(iMaterialGroup)
        if len(sGroupName) > 0:
            self.getWidget('eCategory').set_text(sGroupName)
        else:
            self.getWidget('eCategory').set_text('')

    def on_bGotoAssociated_clicked(self, event):
        print 'goto associated'
        
    def refreshTree(self):
        self.singleArticle.disconnectTree()
        self.singleArticlePurchase.disconnectTree()
        
        if self.tabOption == self.tabArticle:
            self.singleArticle.connectTree()
            self.singleArticle.refreshTree()

        elif self.tabOption == self.tabPurchase:
            self.singleArticlePurchase.sWhere  ='where articles_number = ' + `int(self.singleArticle.ID)`
            self.singleArticlePurchase.connectTree()
            self.singleArticlePurchase.refreshTree()

        elif self.tabOption == self.tabSales:
            self.singleArticleSales.sWhere  ='where articles_number = ' + `int(self.singleArticle.ID)`
            self.singleArticleSales.connectTree()
            self.singleArticleSales.refreshTree()

        elif self.tabOption == self.tabWebshop:

            self.singleArticleWebshop.sWhere  ='where articles_number = ' + `int(self.singleArticle.ID)`
            self.singleArticleWebshop.setEmptyEntries()
            self.singleArticleWebshop.getFirstRecord()
            
            self.singleArticleWebshop.fillEntries(self.singleArticleWebshop.ID)

            
            print "-----------> end tab Webshop"
            

        elif self.tabOption == self.tabStock:
            print "-----------> begin tab Stock"
            self.singleArticleStock.sWhere  ='where articles_number = ' + `int(self.singleArticle.ID)`
            self.singleArticleWebshop.setEmptyEntries()
            self.singleArticleStock.getFirstRecord()
            if self.singleArticleStock.ID > 0:
                self.singleArticleStock.fillEntries(self.singleArticleStock.ID)
            else:
                dicAr = {'articles_number':self.singleArticle.getArticleNumber(self.singleArticle.ID)}
                self.singleArticleStock.fillOtherEntries(dicAr)

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
