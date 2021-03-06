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
import SingleArticle
import SingleArticlePurchase
import SingleArticleSale
import SingleArticleWebshop
import SingleArticleStock
import SingleArticleParts


import logging
from cuon.Windows.chooseWindows  import chooseWindows
import cuon.Addresses.addresses
import cuon.Addresses.SingleAddress
import cuon.DMS.documentTools
import cuon.DMS.dms
import cuon.Articles.lists_articles_number1
import cuon.Articles.pickles_articles
import cuon.Articles.materialgroup
import cuon.Articles.SingleMaterialgroups
import cuon.PrefsFinance.SinglePrefsFinanceVat

# Assosiated
try:
    import cuon.Garden.botany
    import cuon.Garden.SingleBotany
except:
    print 'No botany module found'
    
    


class articleswindow(chooseWindows):

    
    def __init__(self, allTables):

        chooseWindows.__init__(self)
        self.loadGlade('articles.xml', 'ArticlesMainwindow')
        #self.win1 = self.getWidget('ArticlesMainwindow')
        #self.win1.maximize()
        self.setStatusBar('vb_main')
        self.oDocumentTools = cuon.DMS.documentTools.documentTools()
        self.ModulNumber = self.MN['Articles']        
        self.allTables = allTables
        self.singleArticleID = -1
        self.singleArticle = SingleArticle.SingleArticle(allTables)
        self.singleArticleForParts = SingleArticle.SingleArticle(allTables)
        self.singleArticlePurchase = SingleArticlePurchase.SingleArticlePurchase(allTables)
        self.singleArticleParts = SingleArticleParts.SingleArticleParts(allTables)
        self.singleArticleSales = SingleArticleSale.SingleArticleSale(allTables)
        self.singleArticleWebshop = SingleArticleWebshop.SingleArticleWebshop(allTables)
        self.singleArticleStock = SingleArticleStock.SingleArticleStock(allTables)
        self.singleAddress = cuon.Addresses.SingleAddress.SingleAddress(allTables)
        try:
            self.singleBotany = cuon.Garden.SingleBotany.SingleBotany(allTables)
        except:
            pass
        self.singlePrefsFinanceVat = cuon.PrefsFinance.SinglePrefsFinanceVat.SinglePrefsFinanceVat(allTables)    
        self.singleMaterialGroup = cuon.Articles.SingleMaterialgroups.SingleMaterialgroups(allTables)
        # self.singleArticle.loadTable()
              
        self.EntriesArticles = 'articles.xml'
        self.EntriesArticlesPurchase = 'articles_purchase.xml'
        self.EntriesArticlesParts = 'articles_parts.xml'
        self.EntriesArticlesSales = 'articles_sales.xml'
        self.EntriesArticlesWebshop = 'articles_webshop.xml'
        self.EntriesArticlesStock = 'articles_stock.xml'
                
        
        #singleArticle
 
 
        self.loadEntries(self.EntriesArticles)
        self.singleArticle.setEntries(self.getDataEntries( self.EntriesArticles) )
        self.singleArticle.setGladeXml(self.xml)
        self.singleArticle.setTreeFields( ['number', 'designation'] )
#        self.singleArticle.setStore( gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING,   gobject.TYPE_UINT) ) 
        self.singleArticle.setTreeOrder('number, designation')
        self.singleArticle.setTree(self.getWidget('tv_article') )
        self.singleArticle.setListHeader(['number', 'designation', ])
        
        
        #singleArticleParts
        
        self.loadEntries(self.EntriesArticlesParts)
        self.singleArticleParts.setEntries(self.getDataEntries( self.EntriesArticlesParts) )
        self.singleArticleParts.setGladeXml(self.xml)
        #self.singleArticleParts.setTreeFields( ['part_id','number','articles.designation', 'quantities'] )
        #self.singleArticleParts.setListHeader(['Article ID', 'Article Number',  'Article Designation', 'Quantities' ])
        #self.singleArticleParts.setStore( gtk.ListStore(gobject.TYPE_UINT, gobject.TYPE_STRING,   gobject.TYPE_STRING, gobject.TYPE_FLOAT,  gobject.TYPE_UINT) ) 
        self.singleArticleParts.setTreeFields( ['part_id','quantities','articles.number as number' ,'articles.designation as ardesignation', 'articles_parts_list.designation as padesignation'] )
        self.singleArticleParts.setListHeader(['Article ID',   'Quantities' , 'Article Number' ,    'Article Designation',  'Part Designation'])
        self.singleArticleParts.setStore( gtk.ListStore(gobject.TYPE_UINT,gobject.TYPE_FLOAT, gobject.TYPE_STRING,  gobject.TYPE_STRING ,  gobject.TYPE_STRING ,  gobject.TYPE_UINT) ) 
        
        self.singleArticleParts.setTreeOrder('part_id')
#        self.singleArticleParts.setListHeader([''])

        self.singleArticleParts.sWhere  ='where article_id = ' + `self.singleArticle.ID` + ' and part_id = articles.id '
        self.singleArticleParts.setTree(self.getWidget('tv_parts') )
  
         #singleArticlePurchase
        
        self.loadEntries(self.EntriesArticlesPurchase)
        self.singleArticlePurchase.setEntries(self.getDataEntries( self.EntriesArticlesPurchase) )
        self.singleArticlePurchase.setGladeXml(self.xml)
        self.singleArticlePurchase.setTreeFields( ['articles_id','vendorsnumber', 'vendorsdesignation',  'unitprice', 'last_date'] )
        self.singleArticlePurchase.setListHeader(['Article', 'Vendor ID','Designation','Price', 'Last Date' ])
        self.singleArticlePurchase.setStore( gtk.ListStore(gobject.TYPE_UINT, gobject.TYPE_STRING, gobject.TYPE_STRING,  gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_UINT) ) 
        self.singleArticlePurchase.setTreeOrder('unitprice asc,vendorsnumber')
#        self.singleArticlePurchase.setListHeader([''])

        self.singleArticlePurchase.sWhere  ='where articles_id = ' + `self.singleArticle.ID`
        self.singleArticlePurchase.setTree(self.getWidget('tv_purchase') )
  
     #singleArticleSales
        
        self.loadEntries(self.EntriesArticlesSales)
        self.singleArticleSales.setEntries(self.getDataEntries( self.EntriesArticlesSales) )
        self.singleArticleSales.setGladeXml(self.xml)
        self.singleArticleSales.setTreeFields( ['designation'] )
        self.singleArticleSales.setStore( gtk.ListStore(gobject.TYPE_STRING,  gobject.TYPE_UINT) ) 
        self.singleArticleSales.setTreeOrder('designation')
        self.singleArticleSales.setListHeader([_('Designation')])

        self.singleArticleSales.sWhere  ="where articles_number = '" + `self.singleArticle.ID` + "' "
        self.singleArticleSales.setTree(self.getWidget('tv_sale') )

  
  #singleArticleWebshop
        
        self.loadEntries(self.EntriesArticlesWebshop)
        self.singleArticleWebshop.setEntries(self.getDataEntries( self.EntriesArticlesWebshop) )
        self.singleArticleWebshop.setGladeXml(self.xml)
##        self.singleArticleWebshop.setTreeFields( ['articles_number'] )
 ##       self.singleArticleWebshop.setStore( gtk.ListStore(gobject.TYPE_STRING,  gobject.TYPE_UINT) ) 
  ##      self.singleArticleWebshop.setTreeOrder('articles_number')
   ##     self.singleArticleWebshop.setListHeader([_('article')])

        self.singleArticleWebshop.sWhere  ='where articles_number = ' + `self.singleArticle.ID`
        #self.singleArticleWebshop.setTree(self.xml.get_widget('tree1') )

    #singleArticleStock
        
        self.loadEntries(self.EntriesArticlesStock)
        self.singleArticleStock.setEntries(self.getDataEntries( self.EntriesArticlesStock ))
        self.singleArticleStock.setGladeXml(self.xml)
##        self.singleArticleStock.setTreeFields( ['designation'] )
##        self.singleArticleStock.setStore( gtk.ListStore(gobject.TYPE_STRING,  gobject.TYPE_UINT) ) 
##        self.singleArticleStock.setTreeOrder('designation')
##        self.singleArticleStock.setListHeader([_('Designation')])

        self.singleArticleStock.sWhere  ='where articles_id = ' + `self.singleArticle.ID`
        #self.singleArticleStock.setTree(self.xml.get_widget('tree1') )
  
        

        # Menu-items
        self.initMenuItems()

        # All window items
        self.addEnabledMenuItems('window','quit1', 'z')
        # Close Menus for Tab

        self.addEnabledMenuItems('tabs','mi_article1')
        self.addEnabledMenuItems('tabs','mi_purchase1')
        self.addEnabledMenuItems('tabs','mi_sales1')


        # seperate Menus
        self.addEnabledMenuItems('article','mi_article1')
        self.addEnabledMenuItems('purchase','mi_purchase1')
        self.addEnabledMenuItems('sales','mi_sales1')
        self.addEnabledMenuItems('sales','parts_list1')
        
        # enabledMenues for Article
        self.addEnabledMenuItems('editArticle','new1', self.dicUserKeys['articles_new'])
        self.addEnabledMenuItems('editArticle','delete1', self.dicUserKeys['articles_delete'])
        self.addEnabledMenuItems('editArticle','print1', self.dicUserKeys['articles_print'])
        self.addEnabledMenuItems('editArticle','edit1',self.dicUserKeys['articles_edit'])
        
        # enabledMenues for ArticleParts
        self.addEnabledMenuItems('editArticleParts','PartsListNew', self.dicUserKeys['articles_new'])
        self.addEnabledMenuItems('editPArticlearts','PartsListDelete')
        self.addEnabledMenuItems('editArticleParts','PartsListEdit', self.dicUserKeys['articles_edit'])
    

        # enabledMenues for ArticlePurchase
        self.addEnabledMenuItems('editArticlePurchase','PurchaseNew1', self.dicUserKeys['articles_purchase_new'])
        self.addEnabledMenuItems('editArticlePurchase','PurchaseDelete1')
        self.addEnabledMenuItems('editArticlePurchase','PurchaseEdit1', self.dicUserKeys['articles_purchase_edit'])
    
       # enabledMenues for ArticleSales
        self.addEnabledMenuItems('editArticleSales','SalesNew1')
        self.addEnabledMenuItems('editArticleSales','SalesDelete1')
        self.addEnabledMenuItems('editArticleSales','SalesEdit1')

       # enabledMenues for ArticleWebshop
        self.addEnabledMenuItems('editArticleWebshop','WebshopClear1')
        self.addEnabledMenuItems('editArticleWebshop','WebshopEdit1')

       # enabledMenues for ArticleStock
        self.addEnabledMenuItems('editArticleStock','StockClear1')
        self.addEnabledMenuItems('editArticleStock','StockEdit1')

        # enabledMenues for Save 
        self.addEnabledMenuItems('editSave','save1', self.dicUserKeys['articles_save'])
        self.addEnabledMenuItems('editSave','PartsListSave', self.dicUserKeys['articles_save'])
        self.addEnabledMenuItems('editSave','PurchaseSave1', self.dicUserKeys['articles_save'])
        self.addEnabledMenuItems('editSave','SalesSave1', self.dicUserKeys['articles_save'])
        self.addEnabledMenuItems('editSave','WebshopSave1', self.dicUserKeys['articles_save'])
        self.addEnabledMenuItems('editSave','StockSave1', self.dicUserKeys['articles_save'])

        # tabs from notebook
        self.tabArticle = 0
        self.tabParts = 1
        self.tabPurchase = 2
        self.tabSales = 3
        self.tabWebshop = 4
        self.tabStock = 5
        
        self.textbufferNotes,  self.viewNotes = self.getNotesEditor()
        
        
        
        Scrolledwindow = self.getWidget('scArticleNotes')
        Scrolledwindow.add(self.viewNotes)
        self.viewNotes.show_all()
        Scrolledwindow.show_all()

        # set the widget
        self.singleArticle.NotesArticles = self.textbufferNotes
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


  #Menu Parts
        
   
    def on_parts_list_save_activate(self, event):
        print "save Parts articles v2"
        self.singleArticleParts.articlesID = self.singleArticle.ID
        self.singleArticleParts.save()
        self.setEntriesEditable(self.EntriesArticlesParts, False)

        self.tabChanged()
        
    def on_parts_list_new_activate(self, event):
        print "new Parts articles v2"
        self.singleArticleParts.newRecord()
        self.setEntriesEditable(self.EntriesArticlesParts, True)

    def on_parts_list_edit_activate(self, event):
        self.setEntriesEditable(self.EntriesArticlesParts, True)

    def on_parts_list_delete_activate(self, event):
        print "delete Parts articles v2"
        self.singleArticleParts.deleteRecord()


  #Menu Purchase
        
   
    def on_PurchaseSave1_activate(self, event):
        print "save Partner articles v2"
        self.singleArticlePurchase.articlesID = self.singleArticle.ID
        self.singleArticlePurchase.save()
        self.setEntriesEditable(self.EntriesArticlesPurchase, False)

        self.tabChanged()
        
    def on_PurchaseNew1_activate(self, event):
        print "new Purchase articles v2"
        self.singleArticlePurchase.newRecord()
        self.setEntriesEditable(self.EntriesArticlesPurchase, True)

    def on_PurchaseEdit1_activate(self, event):
        self.setEntriesEditable(self.EntriesArticlesPurchase, True)

    def on_PurchaseDelete1_activate(self, event):
        print "delete Purchase articles v2"
        self.singleArticlePurchase.deleteRecord()

    #Articles Sales
    def on_SalesSave1_activate(self, event):
        print "save Sales articles v2"
        
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

    def on_SalesDelete1_activate(self, event):
        print "delete Sales articles v2"
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
        
        self.singleArticleStock.articlesID = self.singleArticle.ID
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

    #Menu pickles_articles
    
    def on_one_standard1_activate(self, event):
        pdf = cuon.Articles.pickles_articles.pickles_articles(1)
    def on_sp101_activate(self, event):
        pdf = cuon.Articles.pickles_articles.pickles_articles(1, 'sp101')
    def on_sp102_activate(self, event):
        pdf = cuon.Articles.pickles_articles.pickles_articles(1, 'sp102')
        
    def on_two_standard1_activate(self, event):
        pdf = cuon.Articles.pickles_articles.pickles_articles(2)
    def on_sp201_activate(self, event):
        pdf = cuon.Articles.pickles_articles.pickles_articles(2, 'sp201')
    def on_sp202_activate(self, event):
        pdf = cuon.Articles.pickles_articles.pickles_articles(2, 'sp202')
        
    def on_three_standard1_activate(self, event):
        pdf = cuon.Articles.pickles_articles.pickles_articles(3)
    def on_sp301_activate(self, event):
        pdf = cuon.Articles.pickles_articles.pickles_articles(3, 'sp301')
    def on_sp302_activate(self, event):
        pdf = cuon.Articles.pickles_articles.pickles_articles(3, 'sp302')
        
    def on_four_standard1_activate(self, event):
        pdf = cuon.Articles.pickles_articles.pickles_articles(4)
    def on_sp401_activate(self, event):
        pdf = cuon.Articles.pickles_articles.pickles_articles(4, 'sp401')
    def on_sp402_activate(self, event):
        pdf = cuon.Articles.pickles_articles.pickles_articles(4, 'sp402')
        

    def on_tbNew_clicked(self, event):
        if self.tabOption == self.tabArticle:
            self.on_new1_activate(event)
        if self.tabOption == self.tabParts:
            self.on_parts_list_new_activate(event)
        elif self.tabOption == self.tabPurchase:
            self.on_PurchaseNew1_activate(event)
        elif self.tabOption == self.tabSales:
            self.on_SalesNew1_activate(event)
        elif self.tabOption == self.tabWebshop:
            self.on_WebshopNew1_activate(event)
        elif self.tabOption == self.tabStock:
            self.on_StockNew1_activate(event)   
            
    def on_tbEdit_clicked(self, event):
        if self.tabOption == self.tabArticle:
            self.on_edit1_activate(event)
        if self.tabOption == self.tabParts:
            self.on_parts_list_edit_activate(event)
        elif self.tabOption == self.tabPurchase:
            self.on_PurchaseEdit1_activate(event)
        elif self.tabOption == self.tabSales:
            self.on_SalesEdit1_activate(event)
        elif self.tabOption == self.tabWebshop:
            self.on_WebshopEdit1_activate(event)
        elif self.tabOption == self.tabStock:
            self.on_StockEdit1_activate(event)   
            
    def on_tbSave_clicked(self, event):
        if self.tabOption == self.tabArticle:
            self.on_save1_activate(event)
        if self.tabOption == self.tabParts:
            self.on_parts_list_save_activate(event)
        elif self.tabOption == self.tabPurchase:
            self.on_PurchaseSave1_activate(event)
        elif self.tabOption == self.tabSales:
            self.on_SalesSave1_activate(event)
        elif self.tabOption == self.tabWebshop:
            self.on_WebshopSave1_activate(event)
        elif self.tabOption == self.tabStock:
            self.on_StockSave1_activate(event)   
            
            
            
    def on_tbDuplicate_clicked(self, event):       
        print 'Duplicate this article'
        newID = self.rpc.callRP("Article.duplicateArticle",self.singleArticle.ID ,  self.dicUser)


            
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


    # search button Article
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
            
            
    def on_eFindMaterialGroupID_key_press_event(self, entry,event):
        if self.checkKey(event,'NONE','Return'):
            self.searchArticle()
            
        
    

    def searchArticle(self):
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
            
        self.singleArticle.sWhere = self.getWhere(liSearch)
        #self.out(self.singleArticle.sWhere, self.ERROR)
        self.refreshTree()

    # button search article at partslist
    
    def on_bPartsFindArticle_clicked(self, event):
        
        ar = cuon.Articles.articles.articleswindow(self.allTables)
        ar.setChooseEntry('chooseArticle', self.getWidget( 'ePartsArticleID'))
        
                           

    def on_ePartsArticleID_changed(self, event):
        print 'eArticle changed'
       
        iArtNumber = self.getChangedValue('ePartsArticleID')
        iPartNumber = self.singleArticle.ID 
        
        eArtField = self.getWidget('ePartsArticleDesignation')
        eArtNumber = self.getWidget('ePartsArticleNumber')
        #liArt = self.singleArticleForParts.getArticle(iArtNumber)
        #self.setTextbuffer(eArtField,liArt)
        dicPrices = self.singleArticleForParts.getSellingPrices(iArtNumber, iPartNumber)
        print 'Prices for ',  iArtNumber,  iPartNumber,  dicPrices 
        if iArtNumber and iArtNumber > 0:
            eArtField.set_text(self.singleArticleForParts.getArticleDesignation(iArtNumber))
            eArtNumber.set_text(self.singleArticleForParts.getArticleNumber(iArtNumber))
        else:
            eArtField.set_text('')
            eArtNumber.set_text('')
        if len(dicPrices) == 9:
            self.getWidget('eArticlePriceI').set_text(self.getCheckedValue(`dicPrices['s1']`,  'toStringFloat'))
            self.getWidget('eArticlePriceII').set_text(self.getCheckedValue(`dicPrices['s2']`,  'toStringFloat'))
            self.getWidget('eArticlePriceIII').set_text(self.getCheckedValue(`dicPrices['s3']`,  'toStringFloat'))
            self.getWidget('eArticlePriceIV').set_text(self.getCheckedValue(`dicPrices['s4']`,  'toStringFloat'))
            
            self.getWidget('eArticleTotalPriceI').set_text(self.getCheckedValue(`dicPrices['ts1']`,  'toStringFloat'))
            self.getWidget('eArticleTotalPriceII').set_text(self.getCheckedValue(`dicPrices['ts2']`,  'toStringFloat'))
            self.getWidget('eArticleTotalPriceIII').set_text(self.getCheckedValue(`dicPrices['ts3']`,  'toStringFloat'))
            self.getWidget('eArticleTotalPriceIV').set_text(self.getCheckedValue(`dicPrices['ts4']`,  'toStringFloat'))

        
    # search button Parts List
    def on_bPLSearch_clicked(self, event):
        self.searchParts()


    def on_ePLFind_key_press_event(self, entry,  event):
        print 'Find Parts'
        if self.checkKey(event,'NONE','Return'):
            print 'find parts return event'
            self.searchParts()
    
    
    def searchParts(self):
        sNumber = self.getWidget('ePLFindNumber').get_text()
        sDesignation = self.getWidget('ePLFindDesignation').get_text()
        sID = self.getWidget('ePLFindID').get_text()
        sDescription =  self.getWidget('ePLFindDescription').get_text()
        sMaterialGroup =  self.getWidget('ePLFindMaterialGroup').get_text()
        print "sID  = ",  sID
        
        #self.out('Name and City = ' + sNumber + ', ' + sDesignation, self.ERROR)
        liSearch = []
        if sNumber:
            liSearch.append('articles.number')
            liSearch.append(sNumber)
            
        if sDescription:
            liSearch.append('articles_parts_list.designation')
            liSearch.append(sDescription)

        if sDesignation:
            liSearch.append('articles.designation')
            liSearch.append(sDesignation)

        if sMaterialGroup:
            liSearch.append('material_group')
            liSearch.append(sMaterialGroup)
            
        if sID:
            liSearch.append('part_id')
            liSearch.append(sID)
        
        print 'liSearch = ',  liSearch
        self.singleArticleParts.sWhere = self.getWhere(liSearch) + ' and articles_parts_list.article_id = ' + `self.singleArticleID` + ' and articles_parts_list.part_id = articles.id '
        print self.singleArticleParts.sWhere
        #self.out(self.singleArticle.sWhere, self.ERROR)
        self.Find = True 
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
            
            
            
            
    def on_bSearchAssociated_clicked(self, event):
        print 'search associated'
        articleAssociated = self.getWidget('cbAssociatedWith').get_active()
        if articleAssociated == 1:
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
        
        articleAssociated = self.getWidget('cbAssociatedWith').get_active()
        if articleAssociated == 1:
            print 'cbAssociatedID read'
            #iBotID = self.singleBotany.getAssociatedID(self.singleArticle.ID)
            #print 'Botany ID = ', iBotID
            #sBotany = self.singleBotany.getBotanyName(iBotID)
            iBotID = self.singleArticle.firstRecord['associated_id']
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
        
        

    def on_eTaxVat_changed(self, event):
        TaxVat = self.getChangedValue('eTaxVta')
        sTaxVat = self.singlePrefsFinanceVat.getNameAndDesignation(iTaxVat)
        if sTaxVat:
            self.getWidget('eTaxVatTex').set_text(sTaxVat)
        else:
            self.getWidget('eTaxVatText').set_text('')
 
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

    def on_tbDMS_clicked(self, event):
        print 'dms clicked'
        if self.singleArticle.ID > 0:
            print 'ModulNumber', self.ModulNumber
            Dms = cuon.DMS.dms.dmswindow(self.allTables, self.ModulNumber, {'1':self.singleArticle.ID})
        

    def on_bShowDMS_clicked(self, event):
        print 'dms clicked'
        if self.singleArticle.ID > 0:
            print 'ModulNumber', self.ModulNumber
            Dms = cuon.DMS.dms.dmswindow(self.allTables, self.ModulNumber, {'1':self.singleArticle.ID})
        
        
    def refreshTree(self):
        self.singleArticle.disconnectTree()
        self.singleArticlePurchase.disconnectTree()
        
        if self.tabOption == self.tabArticle:
            self.singleArticle.setTreeSensitive(True)
            self.singleArticle.connectTree()
            self.singleArticle.refreshTree()
            self.on_cbAssociatedWith_changed(None)
            self.singleArticle.connectTree()
            self.singleArticle.refreshTree()
        elif self.tabOption == self.tabParts:
            print 'refresh tree at parts'
            if self.Find:
                self.Find = False
            else:
                self.singleArticleParts.sWhere  ='where article_id = ' + `int(self.singleArticle.ID)`  + ' and part_id = articles.id '
            self.singleArticleParts.connectTree()
            self.singleArticleParts.refreshTree()
            self.singleArticleParts.setTreeSensitive(True)   
        elif self.tabOption == self.tabPurchase:
            self.singleArticlePurchase.sWhere  ='where articles_id = ' + `int(self.singleArticle.ID)`
            self.singleArticlePurchase.connectTree()
            self.singleArticlePurchase.refreshTree()
            self.singleArticlePurchase.setTreeSensitive(True)
        elif self.tabOption == self.tabSales:
            self.singleArticleSales.sWhere  ="where articles_number = '" + `int(self.singleArticle.ID)` + "' "
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
            
            self.singleArticleStock.sWhere  ='where articles_id = ' + `int(self.singleArticle.ID)`
            self.singleArticleWebshop.setEmptyEntries()
            self.singleArticleStock.getFirstRecord()
            self.singleArticleStock.articlesID = self.singleArticle.ID
            if self.singleArticleStock.ID > 0:
                self.singleArticleStock.fillEntries(self.singleArticleStock.ID)
            else:
                #dicAr = {'articles_number':self.singleArticle.getArticleNumber(self.singleArticle.ID)}
                dicAr = {'articles_id':self.singleArticle.ID}
                
                self.singleArticleStock.fillOtherEntries(dicAr)

            print "-----------> end tab Stock"
 
         
    def tabChanged(self):
        print 'tab changed to :'  + str(self.tabOption)
        
        if self.tabOption == self.tabArticle:
            #Article
            self.disableMenuItem('tabs')
            self.enableMenuItem('article')
            print 'Seite 0'
            self.editAction = 'editArticle'
            self.setStatusbarText([''])
            self.lastTab = self.tabArticle
       
        elif self.tabOption == self.tabParts:
            #Parts
            if self.lastTab == self.tabArticle:
                self.singleArticleID = self.singleArticle.ID
            self.disableMenuItem('tabs')
            self.enableMenuItem('Parts')
            self.editAction = 'editArticleParts'
            print 'Seite 1'
            self.setStatusbarText([self.singleArticle.sStatus])
            
        elif self.tabOption == self.tabPurchase:
            #Purchase
            self.lastTab = self.tabPurchase
            self.disableMenuItem('tabs')
            self.enableMenuItem('purchase')
            self.editAction = 'editArticlePurchase'
            print 'Seite 1'
            self.setStatusbarText([self.singleArticle.sStatus])
        elif self.tabOption == self.tabSales:
            self.lastTab = self.tabSales
            self.disableMenuItem('tabs')
            self.enableMenuItem('sales')
            self.editAction = 'editArticleSales'
            print 'Seite 2'
            self.setStatusbarText([self.singleArticle.sStatus])
        elif self.tabOption == self.tabWebshop:
            self.lastTab = self.tabWebshop
            self.disableMenuItem('tabs')
            self.enableMenuItem('sales')
            self.editAction = 'editArticleWebshop'
            self.singleArticleWebshop.setTreeSensitive(False)
            print 'Seite 3'
            self.setStatusbarText([self.singleArticle.sStatus])
        elif self.tabOption == self.tabStock:
            self.lastTab = self.tabStock
            self.disableMenuItem('tabs')
            self.enableMenuItem('sales')
            self.editAction = 'editArticleStock'
            self.setStatusbarText([self.singleArticle.sStatus])
            print 'Seite 4'
            
        # refresh the Tree
        self.refreshTree()
        self.enableMenuItem(self.editAction)
        self.editEntries = False
