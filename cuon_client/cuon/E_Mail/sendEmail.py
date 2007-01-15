# -*- coding: utf-8 -*-

##Copyright (C) [2003, 2004, 2005, 2006, 2007]  [Juergen Hamel, D-32584 Loehne]

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

from cuon.Windows.windows  import windows
class sendEmail:

    def __init__(self, Modul = None, dicValues = None):
        windows.__init__(self)
        
        
        self.loadGlade('email.xml')
        self.win1 = self.getWidget('EmailMainwindow')
        self.win1.maximize()
        
        self.setStatusBar()
 
 
 
    def on_quit1_activate(self, event):
        self.closeWindow() 
        
    def on_send1_activate(self, event):
        print 'send mail'
        
       
