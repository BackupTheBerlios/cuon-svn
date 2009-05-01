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
        
        # Set Values for SchedulTree
        tCal = self.getWidget('tCalendars')
        #treeview.set_model(liststore)
 
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn(_("Calendar"), renderer, text=0)
        tCal.append_column(column)
        
        # Set Values for AllSchedulTree
        tAll = self.getWidget('tAllScheduls')
        #treeview.set_model(liststore)
 
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn(_("Calendar"), renderer, text=0)
        tAll.append_column(column)
        
        
        # Set Values for SchedulTree
        tCustom = self.getWidget('tCustom')
        #treeview.set_model(liststore)
 
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn(_("Calendar"), renderer, text=0)
        tCustom.append_column(column)

        self.CalendarChanged()
        


    def on_calendar1_day_selected(self, event):
            
        self.CalendarChanged()
        
        
    def CalendarChanged(self):
        oCal = self.getWidget('calendar1')
        oDate = oCal.get_date()
        print oDate
        
        
