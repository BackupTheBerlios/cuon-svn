# -*- coding: utf-8 -*-
##Copyright (C) [2003]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 

from cuon.Databases.SingleData import SingleData
import logging
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import gobject



class SingleArticle(SingleData):

    
    def __init__(self, allTables):

        SingleData.__init__(self)
        # tables.dbd and address
        self.sNameOfTable =  "articles"
        self.xmlTableDef = 0
        # self.loadTable()
        # self.saveTable()

        self.loadTable(allTables)
        self.setStore( gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING,  gobject.TYPE_UINT) )
        self.listHeader['names'] = ['number', 'designation', 'ID']
        self.listHeader['size'] = [25,10,25,25,10]
        print "number of Columns "
        print len(self.table.Columns)
        #
        self.statusfields = ['number', 'designation']
        
    def getArticle(self, id):
        dicRecords = self.load(id)
        liArticle = []
        print dicRecords
        if dicRecords:
            try:
                dicRecord = dicRecords[0]
                liArticle.append(dicRecord['number'])
                liArticle.append(dicRecord['designation'])
                liArticle.append (' ')
                liArticle.append(' ')
                liArticle.append(' ' )
            except:
                pass
                
        if not liArticle:
            liArticle.append(' ')
            liArticle.append(' ')
            liArticle.append(' ')
            liArticle.append(' ')
            liArticle.append(' ')
            
        return liArticle

       
    def getArticleFields(self, id):
        dicRecords = self.load(id)

    def getArticleNumber(self, id):
        dicRecords = self.load(id)
        return dicRecords[0]['number']
    
    def getArticleDesignation(self, id):
        print "id = ",  id
        sDesignation = ' '
        try:
            dicRecords = self.load(id)
            print dicRecords
            sDesignation = dicRecords[0]['designation']
        except:
            pass
        return sDesignation
            
    def getArticleShort(self, id):
        dicRecords = self.load(id)
        sReturn = ' '
        try:
            sReturn = dicRecords[0]['number'] + ',' + dicRecords[0]['designation']
        except:
            sReturn = ' '
            
        return sReturn
        
    def getPrice(self, Modul, iModulID, ArticleID):
        return self.rpc.callRP('Article.getPrice', Modul,iModulID, ArticleID,  self.dicUser)
        
        
    def getArticleAssociatedWith(self):
        return self.firstRecord['associated_with']
        
