# -*- coding: utf-8 -*-
##Copyright (C) [2003]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 

import sys
import types
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import gobject
from gtk import TRUE, FALSE

from cuon.Databases.SingleData import SingleData
import logging
from cuon.Windows.windows  import windows
from  cuon.Addresses.selectionDialog import selectionDialog1

import os.path
import cuon.XMLRPC.xmlrpc

from cuon.PDF.standardlist import standardlist
import cuon.PDF.XML.report_articles_number1
import copy

class lists_stockgoods_number1(selectionDialog1, standardlist):

    
    def __init__(self):
        selectionDialog1.__init__(self,'stockgoods_search1.xml')
        standardlist.__init__(self)

        rep = cuon.PDF.XML.report_articles_number1.report_articles_number1()
        self.dicReportData =  rep.dicReportData

        
        print "lists_articles_number1 start"
        
        sFile = self.getWidget('eFiledata').set_text(self.setFileName (_('stockgoods_number1.pdf') ))
        sFile = self.setFileName ( _('Test' ))
 
      
    

        
    def on_okbutton1_clicked(self,event):
        print 'ok'
        sFile  = self.getWidget('eFiledata').get_text()
        self.pdfFile = os.path.normpath(sFile)
        dicSearchfields = self.readSearchDatafields()
        self.out(dicSearchfields)
        di1 = self.getWidget('dialog1')
        di1.hide()

        dicResult =  self.rpc.callRP('src.Stock.py_getstockgoodslist1', dicSearchfields, self.dicUser)
        for i in dicResult:
            for j in i.keys():
                if isinstance(i[j],types.UnicodeType):
                    i[j] = (i[j].decode('utf-7')).encode('latin-1')
            

    
        self.out( dicResult )
        print dicResult
        print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*'
        
        self.dicResults['articles'] = dicResult
        self.loadXmlReport('stockgoods_number1', 'ReportStockgoodsLists')


   
    def readSearchDatafields(self):
        dicSearchfields = {}
        dicSearchfields['eNumberFrom'] = self.getWidget('eNumberFrom').get_text()
        dicSearchfields['eNumberTo'] = self.getWidget('eNumberTo').get_text()

        dicSearchfields['eDesignationFrom'] = self.getWidget('eDesignationFrom').get_text()
        dicSearchfields['eDesignationTo'] = self.getWidget('eDesignationTo').get_text()
        
        dicSearchfields['eStockFrom'] = self.getWidget('eStockFrom').get_text()
        dicSearchfields['eStockTo'] = self.getWidget('eStockTo').get_text()

        dicSearchfields['eActualStockFrom'] = self.getWidget('eActualStockFrom').get_text()
        dicSearchfields['eActualStockTo'] = self.getWidget('eActualStockTo').get_text()


        return dicSearchfields
    
        
    def on_cancelbutton1_clicked(self,event):
        print 'cancel'
        di1 = self.getWidget('dialog1')
        di1.hide()


    def on_bFileDialog_clicked(self, event):
        print self.filedata
        self.getWidget('fileselection1').set_filename(self.filedata[0])
        self.getWidget('fileselection1').show()
        
  

  
