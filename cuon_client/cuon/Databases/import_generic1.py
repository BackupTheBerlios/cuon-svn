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
from cuon.Misc.fileSelection import fileSelection
import cuon.Addresses.SingleAddress


class import_generic1(fileSelection):
    
    def __init__(self):
        
        fileSelection.__init__(self)
        self.iFile = None
        self.fromChangedValue = ' '
        self.toChangedValue = ';'
        
        
        
    def on_ok_button1_clicked(self, event):
    

        self.on_ok_button_clicked(event)
        self.iFileName = os.path.normpath(self.fileName)
        
        print self.iFileName
        print  self.rpc.getServer()
        print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*'
        
        importFile = open(self.iFileName)
        #exportFile = open('/home/jh/exp2.asc','wa')
        s1 = importFile.readline()
        lS2 = s1.split(self.fromChangedValue)
        # Headlines
        # for exmple 
        #['ADRNR;ANREDE;LAND;NAME1;NAME2;ORT;PLZ;STRASSE;ANSPRANREDE;ANSPRTITEL;ANSPRNACHNAME;ANSPRVORNAME;BRIEFANREDE;ABTEILUNGKLAR;ABTEILUNG;FUNKTION;KRITERIUM;EINORDNUNG\r\n']
        #
        oSingleAddress = cuon.Addresses.SingleAddress.SingleAddress()
        
        s1 = importFile.readline()
        while s1:
            print s1
            print '----'
            lS1 = s1.split(self.fromChangedValue)
            s1 = s1.replace(self.fromChangedValue,self.toChangedValue)
            #exportFile.write(s1)
            print lS1
            # now set the values
            dicValues = {}
            
            # verify Fields
            dicValues = oSingleAddress.verifyValues(dicValues)
            
            # save to Database
            oSingleAddress.saveExternalData(dicValues)
            
            s1 = importFile.readline()
            
        importFile.close()
        print lS2
        #exportFile.close()
            

        
