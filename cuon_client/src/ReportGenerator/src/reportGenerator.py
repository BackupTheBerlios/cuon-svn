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
import string


import logging
from cuon.Windows.windows  import windows



class reportgeneratorwindow(windows):

    
    def __init__(self, allTables):

        windows.__init__(self)

        self.loadGlade('reportGenerator.xml')
        self.win1 = self.getWidget('reportGeneratorMainwindow')
        self.drawingarea = self.getWidget('daReportHeader')
        self.drawingarea.add_events(gtk.gdk.BUTTON_PRESS_MASK )
        self.drawingarea.add_events(gtk.gdk.BUTTON_RELEASE_MASK )
        

        self.a = 1
        self.dicReportHeader = {}
        

    def on_new1_activate(self, event):
        print 'new 1'
        print event
        
    def  on_daReportHeader_button_press_event(self, widget, event):
        print 'daReportHeader button press'
        print widget
        print '___________________________'
        print event
        print event.button
        print event.x
        print event.y
        
        if event.button == 1:
            # leftMouseButton
            dicValue = {}

            dicValue['type'] = 'rectangle'
            dicValue['x1'] = event.x
            dicValue['y1'] = event.y
            
            self.dicReportHeader[`self.a`] = dicValue
         

    def  on_daReportHeader_button_release_event(self, widget, event):
        print 'daReportHeader button release'
        print widget
        print '___________________________'
        print event
        print event.button
        print event.x
        print event.y
        
        if event.button == 1:
            # leftMouseButton
            dicValue = self.dicReportHeader[`self.a`]
            dicValue['x2'] = event.x - dicValue['x1'] 
            dicValue['y2'] = event.y  - dicValue['y1'] 

            self.a = self.a + 1
        self.draw()
            
    def  on_daReportHeader_expose_event(self, widget, event):
        self.draw()

    def draw(self):
        style = self.drawingarea.get_style()
        gc = style.fg_gc[gtk.STATE_NORMAL]
        if self.dicReportHeader:
            for i in  range(1, self.a  ):
                dicValue = self.dicReportHeader[`i`]
                self.drawingarea.window.draw_rectangle(gc, TRUE, dicValue['x1'], dicValue['y1'], dicValue['x2'], dicValue['y2'])

        
##    def  on_da_reportheader_motion_notify_event(self, event, userdata):
##        print 'daReportHeader motion event'
##        print event
##        print '___________________________'
##        print userdata
        
