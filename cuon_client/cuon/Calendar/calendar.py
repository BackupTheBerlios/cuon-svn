import sys
sys.path.append('/usr/lib/python/')
sys.path.append('/usr/lib/python/site-packages/PIL')

from types import *
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import gobject
import string
import commands
import logging
from cuon.Windows.windows  import windows

import os



class calendarwindow(windows):

    
    def __init__(self, allTables):
        
        windows.__init__(self)
        
        self.loadGlade('calendar.xml', 'CalendarMainwindow')
        #self.win1 = self.getWidget('AddressMainwindow')
        self.win1.maximize()
        
        
        
        
        
