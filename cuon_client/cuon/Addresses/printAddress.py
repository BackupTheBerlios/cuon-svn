# -*- coding: utf-8 -*-
##Copyright (C) [2003]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

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
#from gtk import TRUE, FALSE

from cuon.Databases.SingleData import SingleData
import logging
from cuon.Windows.windows  import windows
from  cuon.Addresses.selectionDialog import selectionDialog1

import os.path
import cuon.XMLRPC.xmlrpc

import copy

class printAddress:

    
    def __init__(self, resultSet):


        self.dicReportData =  rep.dicReportData

        
        print "print Address start"
        

        sFile = _('Address')
 
      
    
        dicResult =  resultSet
        #print `dicResult`
        
        
        for j in dicResult.keys():
            if isinstance(dicResult[j],types.UnicodeType):
                dicResult[j] = (dicResult[j].decode('utf-7')).encode('latin-1')
            

    
        self.out( dicResult )
        print dicResult
        print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*'
        liTemp = []
        liTemp.append(dicResult)
        self.dicResults['address'] =liTemp
        self.loadXmlReport('printAddress', 'ReportAddressLists')



  
