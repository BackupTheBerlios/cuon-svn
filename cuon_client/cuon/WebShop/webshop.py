3.69/2.5
# -*- coding: utf-8 -*-

##Copyright (C) [2003]  [JÃ¼rgen Hamel, D-32584 LÃ¶hne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 

import sys
import os
import os.path
from types import *
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import gobject
from gtk import TRUE, FALSE
import string
from cuon.Databases.SingleData import SingleData

import logging
from cuon.Windows.windows  import windows
import cPickle
# localisation
import locale, gettext
locale.setlocale (locale.LC_NUMERIC, '')
import threading
import datetime as DateTime
import cuon.XMLRPC.xmlrpc 
import SingleWebshop

class webshopwindow(windows):

    
    def __init__(self, allTables):

        windows.__init__(self)
        #myXmlRpc.__init__(self)
        #self.singleWebshop = SingleWebshop.SingleWebshop(allTables)
        self.rpc = cuon.XMLRPC.xmlrpc.myXmlRpc()
  
        self.WebTable = self.rpc.callRP('src.Databases.py_getXmlData','countries')

        print `self.WebTable`
        self.loadGlade('webshop.xml')
        self.win1 = self.getWidget('WebshopMainwindow')
        self.setStatusBar()
  
    def on_choosePrinter1_activate(self, event):
        pass
        
    def on_UpdateAddresses1_activate(self, event):    
        self.updateAddress()
        
    def updateAddress(self):
                
        self.rpc.callRP('src.WebShop.py_updateAddress', self.dicUser)
        #print `liRecords`
    
        
