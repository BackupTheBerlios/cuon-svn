# -*- coding: utf-8 -*-

##Copyright (C) [2009]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 

import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
from  cuon.Windows.gladeXml import gladeXml


class ArticlesFastSelection(gladeXml):
    def __init__(self ):
        gladeXml.__init__(self, False)
        
    def FastSelectionStart(self):
        print "start Fast Selection"
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

    def on_treeArticles_row_activated(self, event, data1, data2):
        print "treeArticles row activated"
        self.on_bQuickAppend_clicked(event)

    def on_bQuickAppend_clicked(self, event):
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
                   