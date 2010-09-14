# -*- coding: utf-8 -*-

##Copyright (C) [2003-2004]  [Jürgen Hamel, D-32584 Löhne]

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
#from gtk import TRUE, FALSE

import logging
from cuon.Windows.windows  import windows


class plantlists(windows):

    
    def __init__(self, initialWidget = None, initialFilename = None):

        windows.__init__(self)
       
        self.loadGlade('plantlists.xml')
        self.fileWidget = None
        self.fileName = None
        self.filedata = []
        print 'started the plants list'
        self.getWidget('dialog1').show()
        
        
    def on_bOK_clicked(self, event):
        print 'ok clicked'
       
        self.quitFinddialog()

    def on_cancel_button1_clicked(self, event):
        print 'Cancel clicked'
        self.quitFinddialog()

    def showFinddialog(self):
        self.getWidget('dialog1').show()
 

    def quitFinddialog(self):
        self.getWidget('dialog1').destroy()
        
    def getFilenames(self):
        return self.fileName
