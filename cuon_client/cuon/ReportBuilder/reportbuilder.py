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
from cuon.Windows.chooseWindows  import chooseWindows
import cPickle
#import cuon.OpenOffice.letter
# localisation
import locale, gettext
locale.setlocale (locale.LC_NUMERIC, '')
import threading
import datetime as DateTime

class reportbuilderwindow(chooseWindows):

    
    def __init__(self, dicFilename = 'test'):

        chooseWindows.__init__(self)
        fname = '../usr/share/cuon/glade/reportbuilder.glade2'
        
        # self.setLogLevel(self.INFO)
       
        
        try:
            self.xml = gtk.Builder()
            self.xml.add_from_file(fname)
        except Exception, params:
            print Exception, params
            
        
            
        try:
            self.xml.connect_signals(self)
        except Exception, params:
            print Exception, params
        #self.loadGlade('reportbuilder.xml')
        self.win1 = self.getWidget('reportbuildermainwindow')
        self.win1.show()
        #self.setStatusBar()
       
        
        if dicFilename:
            self.dicCurrentFilename = dicFilename
            self.readDocument(dicFilename)
        else:
            self.dicCurrentFilename = {'TYPE':'FILE','NAME':'./new.txt'}
       
        
        
        
        
        
        
    def readDocument(self, dicFilename):
        "Opens the file given in filename and reads it in"
        print 'dicFilename = ',  dicFilename 
        if dicFilename['TYPE'] == 'SSH':
            dicFilename['TMPNAME'] = 'tmp_editor_ssh_tab_GUI_0' 
            s1 = 'scp -P ' + dicFilename['PORT'] +  ' ' + dicFilename['USER'] + '@' + dicFilename['HOST'] + '://' 
            s1 +=  dicFilename['NAME'] + ' ' + dicFilename['TMPNAME']
            os.system(s1)
            filename = dicFilename['TMPNAME']
            
        else:
           
           filename = dicFilename['NAME']
           
           
        doc = self.readDocument(filename)
    
        #print  `doc`
        cyRootNode = self.getRootNode(doc)
