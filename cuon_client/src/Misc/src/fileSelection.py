##Copyright (C) [2003-2004]  [Jürgen Hamel, D-32584 Löhne]

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

import logging
from cuon.Windows.windows  import windows

class fileSelection(windows):

    
    def __init__(self, initialWidget = None, initialFilename = None):

        windows.__init__(self)
        
        self.loadGlade('fileselection.xml')
        self.fileWidget = None
        self.filename = None
        self.filedata = []
        
        if initialWidget:
            self.fileWidget = initalWidget

        if initialFilename:
            self.fileName = initialFilename
            self.getWidget('fileselection1').set_filename(self.fileName)
            

        
    def ok_button1_clicked(self, event):
        filedata =  self.getWidget('fileselection1').get_selections()
        if not filedata:
            filedata = self.filedata
        self.fileName = filedata[0]
        if self.fileWidget:
            
            self.getWidget(self.fileWidget).set_text(self.FileName)
        self.quitFiledialog()

    def on_cancel_button1_clicked(self, event):
        self.quitFiledialog()


    def quitFiledialog(self):
        self.getWidget('fileselection1').hide()
        
