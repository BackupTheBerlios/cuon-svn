# -*- coding: utf-8 -*-

##Copyright (C) [2003-2004]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 

from gtk import TRUE, FALSE

from cuon.XML.MyXML import MyXML
import copy
import cPickle
import cuon.TypeDefs

import os
import os.path
import string

import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import gobject
from gtk import TRUE, FALSE


class reportField( MyXML):
    def __init__(self, da):
        MyXML.__init__(self)
        self.da = da
        
        self.Values = {}
        self.Values['x1_offSet'] = 0
        self.Values['y1_offSet'] = 0
        self.Values['x2_offSet'] = 0
        self.Values['y2_offSet'] = 0

        self.Values['x1'] = 0
        self.Values['y1'] = 0
        self.Values['x2'] = 0
        self.Values['y2'] = 0
        

        
    def draw(self):
        style = self.da.get_style()
        gc = style.fg_gc[gtk.STATE_NORMAL]
        
        self.da.window.draw_rectangle(gc, TRUE, self.Values['x1'], self.Values['y1'], self.Values['x2'], self.Values['y2'])

    
        
