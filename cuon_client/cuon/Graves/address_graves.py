
# -*- coding: utf-8 -*-

##Copyright (C) [2009]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 


from cuon.Windows.gladeXml import gladeXml
import gtk
import pygtk
import gobject
import gtk.glade 
import grave

class address_graves(gladeXml):
    
    def __init__(self):
        gladeXml.__init__(self, False)
        self.tree = None
        self.addresses = None


    def setTree(self,  tree1):
        self.tree = tree1
        self.tree.connect("row_activated", self.on_tree_row_activated);
        
    def disconnectTree(self):
        try:
            
            self.tree.get_selection().disconnect(self.connectTreeId)
        except:
            pass

    def connectTree(self):
        try:
            self.connectTreeId = self.tree.get_selection().connect("changed", self.tree_select_callback)
        except:
            pass
   
    def tree_select_callback(self, treeSelection):
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
                #self.setDateValues(newID)
                print 'newID = ',   newID
            except Exception,  params:
                pass
             #   print Exception,  params
                
            #self.fillEntries(newId)
    def on_tree_row_activated(self, event, data1, data2):
        print 'event'
        print "grave_address",   self.addresses.singleAddress.ID,   self.addresses.allTables
        grv = grave.graveswindow( self.addresses.allTables,  addressid = self.addresses.singleAddress.ID)
        
        
    def fillAddressGraves(self,  liDates ,  addresses):
        treeview = self.tree
        self.addresses = addresses
        #treeview.set_model(liststore)
 
        #renderer = gtk.CellRendererText()
        #column = gtk.TreeViewColumn("Scheduls", renderer, text=0)
        #treeview.append_column(column)
        self.disconnectTree()
        
        treestore = gtk.TreeStore(object)
        treestore = gtk.TreeStore(str)
        renderer = gtk.CellRendererText()
 
        column = gtk.TreeViewColumn("Zweite Spalte", renderer, text=0)
        treeview.append_column(column)
        treeview.set_model(treestore)
        
        print 'Schedul by names: ', liDates
        if liDates:
            lastRep = None
            lastSalesman = None
            Schedulname = None
            lastSchedulname = None
            
            iter = treestore.append(None,[_('Graveyard lastname firstname')])
            iter2 = None
            iter3 = None
            for oneDate in liDates:
                Schedulname = oneDate['graves']
                print Schedulname
                iter2 = treestore.insert_after(iter,None,[Schedulname])   
                 
        treeview.show_all()
        
        self.connectTree()
        print 'end filladdressGraves'
        return True
        
        