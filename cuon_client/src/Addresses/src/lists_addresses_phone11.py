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
from types import *
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
import copy
import cuon.PDF.report_addresses_phone11
import types


class lists_addresses_phone11(selectionDialog1, standardlist):

    
    def __init__(self):
        selectionDialog1.__init__(self)
        standardlist.__init__(self)
        rep = cuon.PDF.report_addresses_phone11.report_addresses_phone11()
        self.dicReportData =  rep.dicReportData

      
        print "lists_addresses_phone1 start"
        self.getWidget('eFiledata').set_text( self.setFileName(_('partnerphonelist.pdf')))
    
      
       
        self.dicText['yOffSet'] = 20

        
    def on_okbutton1_clicked(self,event):
        print 'ok'
        sFile  = self.getWidget('eFiledata').get_text()
        self.pdfFile = os.path.normpath(sFile)
        dicSearchfields = self.readSearchDatafields()
        self.out(dicSearchfields)
        di1 = self.getWidget('dialog1')
        di1.hide()

        dicResult =  self.rpc.callRP('src.Address.py_getPhonelist11', dicSearchfields, self.dicUser)
        
        for i in dicResult:
            for j in i.keys():
                if type(i[j]) == types.StringType: 
                    i[j] = (i[j].decode('utf-7')).encode('latin-1')
            

        self.dicResults['address'] = dicResult
        self.loadXmlReport('addresses_phonelist11','ReportAddressLists' )

   
    
    def readSearchDatafields(self):
        dicSearchfields = {}
        dicSearchfields['eLastnameFrom'] = self.getWidget('eLastnameFrom').get_text()
        dicSearchfields['eLastnameTo'] = self.getWidget('eLastnameTo').get_text()

        dicSearchfields['eFirstnameFrom'] = self.getWidget('eFirstnameFrom').get_text()
        dicSearchfields['eFirstnameTo'] = self.getWidget('eFirstnameTo').get_text()
        
        dicSearchfields['eCityFrom'] = self.getWidget('eCityFrom').get_text()
        dicSearchfields['eCityTo'] = self.getWidget('eCityTo').get_text()

        dicSearchfields['eCountryFrom'] = self.getWidget('eCountryFrom').get_text()
        dicSearchfields['eCountryTo'] = self.getWidget('eCountryTo').get_text()


        return dicSearchfields
    
        
    def on_cancelbutton_clicked(self,event):
        print 'cancel'
        di1 = self.getWidget('dialog1')
        di1.hide()


    def on_bFileDialog_clicked(self, event):
        print self.filedata
        self.getWidget('fileselection1').set_filename(self.filedata[0])
        self.getWidget('fileselection1').show()
        
  

  
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
