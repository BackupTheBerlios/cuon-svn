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
import SingleBotanyGenus


class SingleBotany(SingleData):

    
    def __init__(self, allTables):

        SingleData.__init__(self)
        # tables.dbd and address
        self.sNameOfTable =  "botany"
        self.xmlTableDef = 0
        # self.loadTable()
        # self.saveTable()

        self.loadTable(allTables)
        self.setStore( gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING,  gobject.TYPE_UINT) )
        
        self.listHeader['size'] = [25,10,25,25,10]
        
        self.setTreeFields( ['botany_name', 'local_name'] )
        self.setTreeOrder('botany_name')
        self.setListHeader([_('name'),_('local name')])
        self.oSingleBotanyGenus = SingleBotanyGenus.SingleBotanyGenus(allTables)



        self.genusId = 0
    
    def readNonWidgetEntries(self, dicValues):
        dicValues['genus_id'] = [self.genusId, 'int']
        return dicValues     

    def getBotany(self, id):
        dicRecords = self.load(id)
        liBotany = []
        if dicRecords:
            dicRecord = dicRecords[0]
            liBotany.append(dicRecord['botany_name'])
            liBotany.append(dicRecord['local name'])
            liBotany.append(dicRecord['description'])
            liBotany.append(' ')
            liBotany.append(' ' )
        if not liBotany:
            liBotany.append(' ')
            liBotany.append(' ')
            liBotany.append(' ')
            liBotany.append(' ')
            liBotany.append(' ')
            
        return liBotany

       
    def getBotanyFields(self, id):
        dicRecords = self.load(id)

    def getBotanyNumber(self, id):
        dicRecords = self.load(id)
        return dicRecords[0]['number']
    
    def getBotanyName(self,id):
        dicRecords = self.load(id)
        sName = ''
        if dicRecords and dicRecords[0].has_key('botany_name'):
            sName =  self.oSingleBotanyGenus.getGenusName(dicRecords[0]['genus_id']) + ' ' + dicRecords[0]['botany_name']
        return sName
    def getAssociatedID(self, ArticleID):
        return self.rpc.callRP('Garden.getArticleAssociatedID', ArticleID, self.dicUser)
        
    
