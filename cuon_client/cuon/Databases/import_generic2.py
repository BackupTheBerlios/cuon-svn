# -*- coding: utf-8 -*-

##Copyright (C) [2005]  [JÃ¼rgen Hamel, D-32584 LÃ¶hne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 
import sys
import os
from types import *
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
from cuon.Misc.fileSelection import fileSelection
import cuon.Addresses.SingleCountry


class import_generic2(fileSelection):
    
    def __init__(self, *args):
        
        fileSelection.__init__(self)
        self.iFile = None
        self.fromChangedValue = ' '
        self.toChangedValue = ';'
        
        # set later here args to self.ImportTable
        self.ImportTable = 'countries'
        
    def on_ok_button1_clicked(self, event):
    

        self.on_ok_button_clicked(event)
        self.iFileName = os.path.normpath(self.fileName)
        
        print self.iFileName
        print  self.rpc.getServer()
        print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*'

        
        
        importFile = self.readDocument(self.iFileName)

        oSingleCountry = cuon.Addresses.SingleCountry.SingleCountry()
        oSingleCountry.tree1 = None
        
        if importFile:
            cyRootNode = self.getRootNode(importFile)
            print len(cyRootNode)
            #print cyRootNode[0].toxml()
            #print cyRootNode[1].toxml()
            #print cyRootNode[2].toxml()
            if self.ImportTable == 'countries':
                cyNodes1 = self.getNodes(cyRootNode[2],'countries')
                liImportValues = ['countries_id', 'countries_name', 'countries_iso_code_2','countries_iso_code_3', 'address_format_id']
                liOurValues = ['webshop_id', 'name', 'iso_code_2', 'iso_code_3', 'format_id']
                liOurCheckValues = ['int', 'string', 'string', 'string', 'int']
                
            for i in cyNodes1:
                print `i.toxml()`
                j = 0
                dicValues = {}
                oSingleCountry.ID = (-1)
                for Imp in liImportValues: 
                    xmlDataRecord = self.getNodes(i,Imp)
                    sData = self.getData(xmlDataRecord[0] )
                    print isinstance(`sData`,StringType) , `sData`

                    # now set the values
                    if liOurCheckValues[j] == 'int' or liOurCheckValues[j] == 'float':
                        dicValues[liOurValues[j]] = [sData.encode('ascii'), liOurCheckValues[j]]
                    j = j + 1

                # verify Fields
                dicValues = oSingleCountry.verifyValues(dicValues)
            
                # save to Database
                oSingleCountry.saveExternalData(dicValues)
                    
            
            
