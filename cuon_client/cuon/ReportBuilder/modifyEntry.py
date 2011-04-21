# -*- coding: utf-8 -*-

##Copyright (C) [2005]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

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


import string

import logging

import cPickle
#import cuon.OpenOffice.letter
# localisation
import locale, gettext
locale.setlocale (locale.LC_NUMERIC, '')
import threading
import datetime as DateTime
import drawingReport

from cuon.Windows.chooseWindows  import chooseWindows
class modifyEntryWindow(chooseWindows):

    
    def __init__(self):

        chooseWindows.__init__(self)
        fname = '../usr/share/cuon/glade/reportbuilder.glade2'
        try:
            self.xml = gtk.Builder()
            self.xml.add_from_file(fname)
        except Exception, params:
            print Exception, params
            
           
        try:
            self.xml.connect_signals(self)
        except Exception, params:
            print Exception, params
       
        #me = self.getWidget('daReportHeader')
        self.retEntries = None
 
        self.eName = self.getWidget('eName')
        print 'ename = ',  self.eName
        self.ePosX1 = self.getWidget('ePosX1')
        self.ePosX2 = self.getWidget('ePosX2')
        self.ePosY1 = self.getWidget('ePosY1')
        self.ePosY2 = self.getWidget('ePosY2')
        self.eClass = self.getWidget('eClass')
        
        
        self.win_me = self.getWidget('EntryDialog')
        self.win_me.hide()
       
      
        
    def ModifyEntryShow(self,  dicEntry):
         self.win_me.show()
         
         self.fillEntries(dicEntry)
         
         
    def on_bOK_clicked(self, event):
        self.retEntries = self.readEntries()
        self.win_me.hide()
        
    def fillEntries(self,  dicEntry):
        self.eName.set_text(dicEntry['eName'])
        self.ePosX1.set_text(`dicEntry['x1']`)
        self.ePosX2.set_text(`dicEntry['x2']`)
        self.ePosY1.set_text(`dicEntry['y1']`)
        self.ePosY2.set_text(`dicEntry['y2']`)
     
    def readEntries(self):
        dicEntry = {}
        dicEntry['eName'] = self.eName.get_text()
        dicEntry['x1'] = int(self.ePosX1.get_text())
        dicEntry['x2'] = int(self.ePosX2.get_text())
        dicEntry['y1'] = int(self.ePosY1.get_text())
        dicEntry['y2'] = int(self.ePosY2.get_text())
        
        
        return dicEntry
