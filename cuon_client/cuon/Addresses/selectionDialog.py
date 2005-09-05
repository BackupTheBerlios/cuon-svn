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
from gtk import TRUE, FALSE

from cuon.Databases.SingleData import SingleData
import logging
from cuon.Windows.windows  import windows

class selectionDialog1(windows):

    
    def __init__(self, selDialog='addresses_search1.xml'):

        windows.__init__(self)
        
        # self.gladeName =  '/usr/share/cuon/glade/addresses_search1.glade2'
        # self.singleAddress.loadTable()
              
        self.loadGlade(selDialog)
        self.getWidget('fileselection1').hide()
        self.filedata = []


    def on_bFiledialogOK_clicked(self, event):
        filedata =  self.getWidget('fileselection1').get_selections()
        if not filedata:
            filedata = self.filedata
        self.getWidget('eFiledata').set_text(filedata[0])
        self.quitFiledialog()

    def on_bFiledialogCancel_clicked(self, event):
        self.quitFiledialog()


    def quitFiledialog(self):
        self.getWidget('fileselection1').hide()
        
        

        
   
                
