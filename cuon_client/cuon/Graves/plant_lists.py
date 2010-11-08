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
        
        liService,  liTypeOfGrave, liTypeOfPaid, liPercent,  liPeriodSpring, liPeriodSummer, liPeriodAutumn, liPeriodWinter, liPeriodHolliday, liPeriodUnique, liPeriodYearly= self.rpc.callRP('Grave.getComboBoxEntries',self.dicUser)
        
        cbTypeOfGrave = self.getWidget('cbTypeOfGrave')
        if cbTypeOfGrave:
            liststore = gtk.ListStore(str)
            for TypeOfGrave in liTypeOfGrave:
                liststore.append([TypeOfGrave])
            cbTypeOfGrave.set_model(liststore)
            cbTypeOfGrave.set_text_column(0)
            cbTypeOfGrave.show()
        
        
        cbService = self.getWidget('cbService')
        if cbService:
            liststore = gtk.ListStore(str)
            for service in liService:
                liststore.append([service])
            cbService.set_model(liststore)
            cbService.set_text_column(0)
            cbService.show()
        cbTypeOfPaid = self.getWidget('cbTypeOfPaid')
        if cbTypeOfPaid:
            liststore = gtk.ListStore(str)
            for TypeOfPaid in liTypeOfPaid:
                liststore.append([TypeOfPaid])
            cbTypeOfPaid.set_model(liststore)
            cbTypeOfPaid.set_text_column(0)
            cbTypeOfPaid.show()
        
        
        liGraveYard = self.rpc.callRP('Grave.getComboGraveyards',self.dicUser)
        cbGraveYard = self.getWidget('cbGraveyard')
        if cbGraveYard:
            liststore = gtk.ListStore(str)
            for GraveYard in liGraveYard:
                liststore.append([GraveYard])
            cbGraveYard.set_model(liststore)
            cbGraveYard.set_text_column(0)
            cbGraveYard.show()
        
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
