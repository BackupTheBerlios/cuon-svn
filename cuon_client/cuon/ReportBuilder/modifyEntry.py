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
import types
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
        self.eValue = self.getWidget('eValue')
        self.eType = self.getWidget('eType')
        self.eResultSet = self.getWidget('eResultSet')
        self.eFormat = self.getWidget('eFormat')
        self.eVariable = self.getWidget('eVariable')
        self.eMemory = self.getWidget('eMemory')
        self.eFormula = self.getWidget('eFormula')
        self.eProperty = self.getWidget('eProperty')
        
        self.eFont = self.getWidget('eFont')
        self.eFontSize = self.getWidget('eFontSize')
        self.eJustification = self.getWidget('eJustification')
        self.eFG = self.getWidget('eFG')
        self.eBG = self.getWidget('eBG')
        self.eGrayScale = self.getWidget('eGrayScale')
        
        
        
        self.win_me = self.getWidget('EntryDialog')
        self.win_me.hide()
       
        self.modifiedEntry = None
      
        
    def ModifyEntryShow(self,  dicEntry):
         self.win_me.show()
         
         self.fillEntries(dicEntry)
         
         
    def on_bOK_clicked(self, event):
        self.retEntries = self.readEntries()
        self.win_me.hide()
    
    def on_bApply_clicked(self, event):
        self.retEntries = self.readEntries()
        
    def on_bCancel_clicked(self, event):
        self.win_me.hide()    
        
    def checkXmlValue(self, sValue):
        
        if isinstance(sValue, types.IntType):
            sValue = `sValue`
        elif isinstance(sValue, types.FloatType):
            sValue = `sValue`
        elif isinstance(sValue, types.DictType):
            if sValue.has_key('rColor'):
                sValue = `sValue['rColor']` + ', ' + `sValue['gColor']` + ', ' + `sValue['bColor']` 
        else:
            if not sValue:
                sValue = ""
            sValue = sValue.strip()

        return sValue
    def fillEntries(self,  dicEntry):
        self.eName.set_text(self.checkXmlValue(dicEntry['name']))
        
        self.ePosX1.set_text(self.checkXmlValue(dicEntry['posX1']))
        self.ePosX2.set_text(self.checkXmlValue(dicEntry['posX2']))
        self.ePosY1.set_text(self.checkXmlValue(dicEntry['posY1']))
        self.ePosY2.set_text(self.checkXmlValue(dicEntry['posY2']))
        self.eClass.set_text(self.checkXmlValue(dicEntry['class']))
        self.eValue.set_text(self.checkXmlValue(dicEntry['value']))
        self.eType.set_text(self.checkXmlValue(dicEntry['type']))
        self.eResultSet.set_text(self.checkXmlValue(dicEntry['resultSet']))
        self.eFormat.set_text(self.checkXmlValue(dicEntry['format']))
        self.eVariable.set_text(self.checkXmlValue(dicEntry['variable']))
        self.eMemory.set_text(self.checkXmlValue(dicEntry['memory']))
        self.eFormula.set_text(self.checkXmlValue(dicEntry['formula']))
        self.eProperty.set_text(self.checkXmlValue(dicEntry['property']))
        self.eFont.set_text(self.checkXmlValue(dicEntry['font']))
        self.eFontSize.set_text(self.checkXmlValue(dicEntry['fontsize']))
        self.eJustification.set_text(self.checkXmlValue(dicEntry['fontjustification']))
        self.eFG.set_text(self.checkXmlValue(dicEntry['foregroundColor']))
        self.eBG.set_text(self.checkXmlValue(dicEntry['backgroundColor']))
        if dicEntry['grayScale']:
            self.eGrayScale.set_text(self.checkXmlValue(dicEntry['grayScale']))
        else:
            self.eGrayScale.set_text("0.0")
            
        
    def readEntries(self):
        dicEntry = {}
        dicEntry['name'] = self.eName.get_text()
        dicEntry['posX1'] = int(self.ePosX1.get_text())
        dicEntry['posX2'] = int(self.ePosX2.get_text())
        dicEntry['posY1'] = int(self.ePosY1.get_text())
        dicEntry['posY2'] = int(self.ePosY2.get_text())
        dicEntry['class'] = self.eClass.get_text()
        dicEntry['value'] = self.eValue.get_text()
        dicEntry['type'] = self.eType.get_text()
        dicEntry['resultSet'] = self.eResultSet.get_text()
        dicEntry['format'] = self.eFormat.get_text()
        dicEntry['variable'] = self.eVariable.get_text()
        dicEntry['memory'] = self.eMemory.get_text()
        dicEntry['formula'] = self.eFormula.get_text()
        dicEntry['property'] = self.eProperty.get_text()
        dicEntry['font'] = self.eFont.get_text()
        dicEntry['fontsize'] = self.eFontSize.get_text()
        dicEntry['fontjustification'] = self.eJustification.get_text()
        dicEntry['foregroundColor'] = self.eFG.get_text()
        dicEntry['backgroundColor'] = self.eBG.get_text()
        try:
            dicEntry['grayScale'] = float(self.eGrayScale.get_text())
        except:
            dicEntry['grayScale'] = 0.0
        
        print 'dicEntry at modifyEntry1',  dicEntry
        self.replaceEntry( dicEntry)
        
        self.activateClick('bRefresh',sAction = "clicked")
        
        return dicEntry

    def replaceEntry(self,  dicEntry):
        pass
        
