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
from gtk import TRUE, FALSE

from cuon.Databases.SingleData import SingleData
import SingleArticle
import SingleArticlePurchase
import SingleArticleSale
import logging
from cuon.Windows.chooseWindows  import chooseWindows
import cuon.Addresses.addresses
import cuon.Addresses.SingleAddress


class articleswindow(chooseWindows):

    
    def __init__(self, allTables):

        chooseWindows.__init__(self)

        self.loadGlade('articles.xml')
        self.win1 = self.getWidget('ArticlesMainwindow')
        
        self.allTables = allTables
        self.singleArticle = SingleArticle.SingleArticle(allTables)
        self.singleArticlePurchase = SingleArticlePurchase.SingleArticlePurchase(allTables)
        self.singleArticleSales = SingleArticleSale.SingleArticleSale(allTables)
        self.singleAddress = cuon.Addresses.SingleAddress.SingleAddress(allTables)
        
        # self.singleArticle.loadTable()
              
        self.EntriesArticles = 'articles.xml'
        self.EntriesArticlesPurchase = 'articles_purchase.xml'
        self.EntriesArticlesSales = 'articles_sales.xml'
                
        
        #singleArticle
 
 
        self.loadEntries(self.EntriesArticles)
        self.singleArticle.setEntries(self.getDataEntries('articles.xml') )
        self.singleArticle.setGladeXml(self.xml)
        self.singleArticle.setTreeFields( ['number', 'designation'] )
#        self.singleArticle.setStore( gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING,   gobject.TYPE_UINT) ) 
        self.singleArticle.setTreeOrder('number')
        self.singleArticle.setTree(self.xml.get_widget('tree1') )
        self.singleArticle.setListHeader(['number', 'designation', ])
        
         #singleArticlePurchase
        
        self.loadEntries(self.EntriesArticlesPurchase)
        self.singleArticlePurchase.setEntries(self.getDataEntries('articles_purchase.xml') )
        self.singleArticlePurchase.setGladeXml(self.xml)
        self.singleArticlePurchase.setTreeFields( ['designation' ] )
        self.singleArticlePurchase.setStore( gtk.ListStore(gobject.TYPE_STRING,  gobject.TYPE_UINT) ) 
        self.singleArticlePurchase.setTreeOrder('designation')
#        self.singleArticlePurchase.setListHeader([''])

        self.singleArticlePurchase.sWhere  ='where articles_number = ' + `self.singleArticle.ID`
        self.singleArticlePurchase.setTree(self.xml.get_widget('tree1') )
  
     #singleArticleSales
        
        self.loadEntries(self.EntriesArticlesSales)
        self.singleArticleSales.setEntries(self.getDataEntries('articles_sales.xml') )
        self.singleArticleSales.setGladeXml(self.xml)
        self.singleArticleSales.setTreeFields( ['designation'] )
        self.singleArticleSales.setStore( gtk.ListStore(gobject.TYPE_STRING,  gobject.TYPE_UINT) ) 
        self.singleArticleSales.setTreeOrder('designation')
        self.singleArticleSales.setListHeader([_('Designation')])

        self.singleArticleSales.sWhere  ='where articles_number = ' + `self.singleArticle.ID`
        self.singleArticleSales.setTree(self.xml.get_widget('tree1') )
  

        

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
        self.addEnabledMenuItems('editArticle','new1')
        self.addEnabledMenuItems('editArticle','clear1')
        self.addEnabledMenuItems('editArticle','print1')
        self.addEnabledMenuItems('editArticle','edit1')

        # enabledMenues for ArticlePurchase
        self.addEnabledMenuItems('editPurchase','PurchaseNew1')
        self.addEnabledMenuItems('editPurchase','PurchaseClear1')
        self.addEnabledMenuItems('editPurchase','PurchaseEdit1')
    
       # enabledMenues for ArticlePurchase
        self.addEnabledMenuItems('editSales','SalesNew1')
        self.addEnabledMenuItems('editSales','SalesClear1')
        self.addEnabledMenuItems('editSales','SalesEdit1')



        # tabs from notebook
        self.tabArticle = 0
        self.tabPurchase = 1
        self.tabSales = 2
        

        # start
        
        self.tabChanged()

        # enabled menus for article
        self.addEnabledMenuItems('editArticle','new1')
        self.addEnabledMenuItems('editArticle','clear1')
        self.addEnabledMenuItems('editArticle','print1')

        # enabled menus for article_purchase
        self.addEnabledMenuItems('editArticlePurchase','PurchaseNew1')
        self.addEnabledMenuItems('editArticlePurchase','PurchaseClear1')

         
         
    #Menu File
              
    def on_quit1_activate(self, event):
        print "exit articles v2"
        self.closeWindow()


    #Menu Article
  
    def on_save1_activate(self, event):
        print "save articles v2"
        self.singleArticle.save()
        self.setEntriesEditable(self.EntriesArticles, FALSE)
        self.tabChanged()
         
        
    def on_new1_activate(self, event):
        print "new articles v2"
        self.singleArticle.newRecord()
        self.setEntriesEditable(self.EntriesArticles, TRUE)
        

    def on_edit1_activate(self, event):
        self.setEntriesEditable(self.EntriesArticles, TRUE)

    def on_delete1_activate(self, event):
        print "delete articles v2"
        self.singleArticle.deleteRecord()

    def on_quit1_activate(self, event):
        self.closeWindow() 
 

  #Menu Purchase
        
   
    def on_PurchaseSave1_activate(self, event):
        print "save Partner articles v2"
        self.singleArticlePurchase.articlesNumber = self.singleArticle.ID
        self.singleArticlePurchase.save()
        self.setEntriesEditable(self.EntriesArticlesPurchase, FALSE)

        self.tabChanged()
        
    def on_PurchaseNew1_activate(self, event):
        print "new Partner articles v2"
        self.singleArticlePurchase.newRecord()
        self.setEntriesEditable(self.EntriesArticlesPurchase, TRUE)

    def on_PurchaseEdit1_activate(self, event):
        self.setEntriesEditable(self.EntriesArticlesPurchase, TRUE)

    def on_PurchaseClear1_activate(self, event):
        print "delete Partner articles v2"
        self.singleArticlePurchase.deleteRecord()

    #Articles Sales
    def on_SalesSave1_activate(self, event):
        print "save Partner articles v2"
        
        self.singleArticleSales.articlesNumber = self.singleArticle.ID
        self.singleArticleSales.save()
        self.setEntriesEditable(self.EntriesArticlesSales, FALSE)

        self.tabChanged()
        
    def on_SalesNew1_activate(self, event):
        print "new Partner articles v2"
        self.singleArticleSales.newRecord()
        self.setEntriesEditable(self.EntriesArticlesSales, TRUE)

    def on_SalesEdit1_activate(self, event):
        self.setEntriesEditable(self.EntriesArticlesSales, TRUE)

    def on_SalesClear1_activate(self, event):
        print "delete Partner articles v2"
        self.singleArticleSales.deleteRecord()



    def on_chooseArticle_activate(self, event):
        # choose Article from other Modul
        self.setChooseValue(self.singleArticle.ID)
        print 'Article-ID = ' + `self.singleArticle.ID`
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
        self.out( 'Searching ....', self.ERROR)
        sNumber = self.getWidget('eFindNumber').get_text()
        sDesignation = self.getWidget('eFindDesignation').get_text()
        self.out('Name and City = ' + sNumber + ', ' + sDesignation, self.ERROR)
        self.singleArticle.sWhere = 'where number ~* \'.*' + sNumber + '.*\' and designation ~* \'.*' + sDesignation + '.*\''
        self.out(self.singleArticle.sWhere, self.ERROR)
        self.refreshTree()

                     

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
 
     


         
    def tabChanged(self):
        print 'tab changed to :'  + str(self.tabOption)
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
            
        # refresh the Tree
        self.refreshTree()
        self.enableMenuItem(self.editAction)
        self.editEntries = FALSE
