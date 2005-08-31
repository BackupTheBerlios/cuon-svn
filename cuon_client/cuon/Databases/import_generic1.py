# -*- coding: utf-8 -*-

##Copyright (C) [2005]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

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
import string

from cuon.Misc.fileSelection import fileSelection
import SingleImport



class import_generic1(fileSelection):
    
    def __init__(self, allTables):
        
        fileSelection.__init__(self)
        self.iFile = None
        self.splitValue = ';'
        self.fromChangedValue = None
        self.toChangedValue = ''
        self.allTables = allTables
        
        
    def on_ok_button1_clicked(self, event):
    

        self.on_ok_button_clicked(event)
        self.iFileName = os.path.normpath(self.fileName)
        
        print self.iFileName
        print  self.rpc.getServer()
        print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*'

        ctrlFile = open(self.iFileName)
        inputFile = None
        importTable = None
        importHeader = None
        
        liColumns = []

        
        if ctrlFile:
            s = ctrlFile.readline()
            while s:
                liS = s.split('=')
                if liS:
                    for i in range(len(liS)):
                        liS[i] = liS[i].strip()
                        liS[0] = liS[0][0:len(liS[0])]
                        print '1:', `liS`
                    if liS[0] == 'filename':
                        inputFile = liS[1]
                    if liS[0] == 'table':
                        importTable = liS[1]
                    if liS[0] == 'splitvalue':
                        self.splitValue = liS[1]
                    if liS[0] == 'from_changed_value':
                        self.fromChangedValue = liS[1]
                    if liS[0] == 'to_changed_value':
                        self.toChangedValue = liS[1]
    
                    if liS[0] == 'header':
                        importHeader = liS[1]        
                    if liS[0] == 'column':
                        s2 = liS[1]
                        if s2:
                            liS2 = s2.split(',')
                            print 'liS2', `liS2`
                            dicColumn = {}
                            dicColumn['name'] = liS2[0].strip()
                            dicColumn['field'] = liS2[1].strip()
                            liColumns.append(dicColumn)
                            print 'licolumns-0', `liColumns`
                s = ctrlFile.readline()
            
            print 'licolumns', `liColumns`
                        
            ctrlFile.close()
        
        importFile = open(inputFile)

        s1 = importFile.readline()
        lS2 = s1.split(self.fromChangedValue)
##        # Headlines
##        # for exmple 
##        #['ADRNR;ANREDE;LAND;NAME1;NAME2;ORT;PLZ;STRASSE;ANSPRANREDE;ANSPRTITEL;ANSPRNACHNAME;ANSPRVORNAME;BRIEFANREDE;ABTEILUNGKLAR;ABTEILUNG;FUNKTION;KRITERIUM;EINORDNUNG\r\n']
##        #
        
        oSingleImport = SingleImport.SingleImport(self.allTables)
        oSingleImport.setImportTable(importTable)
            
        
        
        s1 = importFile.readline()
        if importHeader.upper() == 'YES':
                    s1 = importFile.readline()
                    
        while s1:
            print s1
            print '----'
            if self.fromChangedValue:
                s1 = s1.replace(self.fromChangedValue,self.toChangedValue)
            lS1 = s1.split(self.splitValue)
            
            #exportFile.write(s1)
            #print lS1
            # now set the values
            dicValues = {}
            for i in range(len(liColumns)):
                dicValues[liColumns[i]['name']] = [lS1[i].strip(),liColumns[i]['field']]

            print `dicValues`
            # verify Fields
            dicValues = oSingleImport.verifyValues(dicValues)
          
            # save to Database
            oSingleImport.newRecord()
            
            oSingleImport.saveExternalData(dicValues)
            
            s1 = importFile.readline()
            #s1 = None
        importFile.close()

            

        
