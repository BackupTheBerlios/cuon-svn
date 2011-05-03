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
from cuon.Misc.cuonlists import cuonlists

class plantlists(cuonlists):

    
    def __init__(self, initialWidget = None, initialFilename = None):

        cuonlists.__init__(self, initialWidget,  initialFilename)
       
        self.loadGlade('plantlists.xml')
       
        print 'started the plants list'
        self.getWidget('listdialog1').show()
        
        liService,  liTypeOfGrave, liTypeOfPaid, liPercent,  liPeriodSpring, liPeriodSummer, liPeriodAutumn, liPeriodWinter, liPeriodHolliday, liPeriodUnique, liPeriodYearly, liSorting = self.rpc.callRP('Grave.getComboBoxEntries',self.dicUser)
        
     
        
        
        cbService = self.getWidget('cbService')
        if cbService:
            liststore = gtk.ListStore(str)
            for service in liService:
                liststore.append([service])
            cbService.set_model(liststore)
            cbService.set_text_column(0)
            cbService.show()
      
        cbTypeOfGrave = self.getWidget('cbTypeOfGrave')
        if cbTypeOfGrave:
            liststore = gtk.ListStore(str)
            for TypeOfGrave in liTypeOfGrave:
                liststore.append([TypeOfGrave])
            cbTypeOfGrave.set_model(liststore)
            cbTypeOfGrave.set_text_column(0)
            cbTypeOfGrave.show()      
            
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
        
        liGravePlantList = self.rpc.callRP('Grave.getComboReportLists',self.dicUser, "grave_plant*")
        print 'lists = ',  liGravePlantList
        cbPlantLists = self.getWidget('cbListOfReport')
        if cbPlantLists:
            liststore = gtk.ListStore(str)
            for plantReport  in liGravePlantList:
                liststore.append([plantReport])
            cbPlantLists.set_model(liststore)
            cbPlantLists.set_text_column(0)
            cbPlantLists.show()
        
        
    def on_bOK_clicked(self, event):
        """ Starts to print the list of graves for plants. """
        
        print 'ok clicked'
        dicSearchfields,  nRow,  sName , iOrderSort = self.readSearchDatafields()
        Pdf = self.rpc.callRP('Report.server_graves_plant_standard', dicSearchfields, self.dicUser, nRow, sName,  iOrderSort)
        self.showPdf(Pdf, self.dicUser)
        di1 = self.getWidget('listdialog1')
        di1.hide()
        self.quitFinddialog()

    def readSearchDatafields(self):
        """ read the entries at the search mask and convert them to values for the SQL-Search """
        liReturn = []
        nRow = 0
        iOrderSort = 0
        gyID = -1
        priceID = -1
        
        sGyID = self.getActiveText(self.getWidget('cbGraveyard'))
        try:
            gyID = int(sGyID[sGyID.find('###')+ 3:].strip()) 
        except:
            gyID = -1
            
        sPriceID = self.getActiveText(self.getWidget('cbTypeOfPaid'))
        try:
            priceID = int(sPriceID[sPriceID.find('###')+ 3:].strip()) 
        except:
            priceID = -1    
            
        try:
            iOrderSort = self.getWidget('cbGraveSorting').get_active()
        except:
            iOrderSort = -1
         
        iContract = 1
        
        if self.getWidget('rbContracts_current').get_active():
            iContract = 1
        elif self.getWidget('rbContracts_terminated').get_active():
            iContract = 2
        elif self.getWidget('rbContracts_all').get_active():
            iContract = 3
            
        iService = self.getWidget('cbService').get_active()
       
       
        
        iPlantation = self.getWidget('cbPlants').get_active()
        print 'iservice,  iPlantation = ',  iService,  iPlantation
        
        liReturn.append( gyID)
        liReturn.append( self.getWidget('eGraveFrom').get_text() )
        liReturn.append( self.getWidget('eGraveTo').get_text() )
        liReturn.append( self.getWidget('eSequentialNumberFrom').get_text() )
        liReturn.append( self.getWidget('eSequentialNumberTo').get_text() )
        liReturn.append( self.getWidget('eContractBeginFrom').get_text() )
        liReturn.append( self.getWidget('eContractBeginTo').get_text() )
        liReturn.append( self.getWidget('eContractEndsFrom').get_text() )
        liReturn.append( self.getWidget('eContractEndsTo').get_text() )
        liReturn.append(iContract)
        liReturn.append(iService)
        liReturn.append(iPlantation)
        liReturn.append(priceID)
        
        print 'liReturn = ',  liReturn
        
        sName = self.getActiveText(self.getWidget("cbListOfReport"))
        return liReturn,  nRow,  sName,  iOrderSort
        
