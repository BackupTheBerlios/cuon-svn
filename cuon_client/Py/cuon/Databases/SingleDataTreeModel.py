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
import gobject
from gtk import TRUE, FALSE


COLUMN_NAME       = 0
COLUMN_ZIPCODE      = 1
COLUMN_CITY    = 2
COLUMN_STREET= 3
COLUMN_ID = 4


class SingleDataTreeModel:
    def __init__(self):
        print 'new TreeModel'
        

    def createModel(self, data):
        self.store.clear()     
        for item in data:
            iter = self.store.append()
            #            store.set(iter, COLUMN_NAME, item[0], COLUMN_ZIPCODE, item[1], COLUMN_CITY, item[2], COLUMN_STREET, item[3], COLUMN_ID, item[4] )
            iLen = len(item)
            for i in range(iLen):
                self.store.set(iter,i, item[i] )
                            
        
        return self.store

    def setColumns(self, tree1, listHeader):
        t1 = 0
        columns = tree1.get_columns()
        for i in columns:
            tree1.remove_column(i)
            
        for i in listHeader['names']:
            column = gtk.TreeViewColumn(i, gtk.CellRendererText(), text=t1)
#            column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
#            column.set_fixed_width(30)
            column.set_clickable(TRUE)
        
            tree1.append_column(column)
            t1 = t1 +1
            

    def setStore(self, store):
        self.store = store
                
