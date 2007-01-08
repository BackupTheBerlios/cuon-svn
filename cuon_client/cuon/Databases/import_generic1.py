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
        self.dicFileAttributes = {}
        self.dicFileAttributes['iFile'] = None
        self.dicFileAttributes['splitValue'] = ';'
        self.dicFileAttributes['fromChangedValue'] = None
        self.dicFileAttributes['toChangedValue'] = ''
        self.dicFileAttributes['allTables'] = allTables
        
        self.iColumns = 0
        
          
         
                               

    def readCtrlFile(self, iFilename):
        ctrlFile = open(self.iFileName)
        self.dicFileAttributes['inputFile'] = None
        self.dicFileAttributes['importTable'] = None
        self.dicFileAttributes['importHeader'] = None
        self.dicFileAttributes['inputType'] = 'Standard'
        self.dicFileAttributes['liColumns'] = []
        self.dicFileAttributes['decodeData'] = None
        
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
                        self.dicFileAttributes['inputFile'] = liS[1]
                    if liS[0] == 'type':
                        self.dicFileAttributes['inputType'] = liS[1]
                    if liS[0] == 'table':
                        self.dicFileAttributes['importTable'] = liS[1]
                    if liS[0] == 'splitvalue':
                        self.dicFileAttributes['splitValue'] = liS[1]
                    if liS[0] == 'from_changed_value':
                        self.dicFileAttributes['fromChangedValue'] = liS[1]
                    if liS[0] == 'to_changed_value':
                        self.dicFileAttributes['toChangedValue'] = liS[1]
                    if liS[0] == 'decode_data':
                        self.dicFileAttributes['decodeData'] = liS[1]
    
                    if liS[0] == 'header':
                        self.dicFileAttributes['importHeader'] = liS[1]        
                    if liS[0] == 'column':
                        self.iColumns += 1
                        s2 = liS[1]
                        if s2:
                            liS2 = s2.split(',')
                            #print 'liS2', `liS2`
                            dicColumn = {}
                            dicColumn['name'] = liS2[0].strip()
                            dicColumn['field'] = liS2[1].strip()
                            self.dicFileAttributes['liColumns'].append(dicColumn)
                            #print 'licolumns-0', `self.dicFileAttributes['liColumns']`
                s = ctrlFile.readline()
            
            #print 'licolumns', `self.dicFileAttributes['liColumns']`
                        
            ctrlFile.close()

                               
    def standardImport(self):
        #print 'dicfileAttributes', self.dicFileAttributes
        importFile = open(self.dicFileAttributes['inputFile'])

        s1 = importFile.readline()
        lS2 = s1.split(self.dicFileAttributes['splitValue'])
        print 'icolumns = ', self.iColumns
        while (len(lS2) < self.iColumns):
            s1 += importFile.readline()
            lS2 = s1.split(self.dicFileAttributes['splitValue'])
##            
            
##        # Headlines
##        # for exmple 
##        #['ADRNR;ANREDE;LAND;NAME1;NAME2;ORT;PLZ;STRASSE;ANSPRANREDE;ANSPRTITEL;ANSPRNACHNAME;ANSPRVORNAME;BRIEFANREDE;ABTEILUNGKLAR;ABTEILUNG;FUNKTION;KRITERIUM;EINORDNUNG\r\n']
##        #
        print 'len lS2 = ', len(lS2)
        
        oSingleImport = SingleImport.SingleImport(self.dicFileAttributes['allTables'])
        print 'Type : ', self.dicFileAttributes['inputType'][0:8]
        if len(self.dicFileAttributes['inputType']) > 8 and  self.dicFileAttributes['inputType'][0:8] == 'webshop_':
            print 'Webshop settings'
        else:
            oSingleImport.setImportTable(self.dicFileAttributes['importTable'])
        
        s1 = importFile.readline()
        if self.dicFileAttributes['importHeader'].upper() == 'YES':
                    s1 = importFile.readline()

        se = 1
        while True:
            #print s1
            print '----'
            if self.dicFileAttributes['decodeData']:
                s1 = s1.decode(self.dicFileAttributes['decodeData']).encode('utf-8')
            if self.dicFileAttributes['fromChangedValue']:
                s1 = s1.replace(self.dicFileAttributes['fromChangedValue'],self.dicFileAttributes['toChangedValue'])
            lS1 = s1.split(self.dicFileAttributes['splitValue'])
            
                
            while (len(lS1) < self.iColumns):
                s1 += importFile.readline().strip()
                if self.dicFileAttributes['decodeData']:
                    s1 = s1.decode(self.dicFileAttributes['decodeData']).encode('utf-8')
                if self.dicFileAttributes['fromChangedValue']:
                    s1 = s1.replace(self.dicFileAttributes['fromChangedValue'],self.dicFileAttributes['toChangedValue'])
                    
                lS1 = s1.split(self.dicFileAttributes['splitValue'])
                
            #exportFile.write(s1)
            print lS1
            # now set the values
            dicValues = {}
            #print 'self.dicFileAttributes = ', self.dicFileAttributes
            
            for i in range(len(self.dicFileAttributes['liColumns'])):
                if self.dicFileAttributes['liColumns'][i]['field'] != 'none':
                    #print '###--> ', self.dicFileAttributes['liColumns'][i]['field']
                    dicValues[self.dicFileAttributes['liColumns'][i]['name']] = [lS1[i].strip(),self.dicFileAttributes['liColumns'][i]['field']]


            #print `self.dicUser`    


            if self.dicFileAttributes['inputType'] == 'Standard':
                
                # verify Fields
                dicValues = oSingleImport.verifyValues(dicValues)
                # save to Database
                oSingleImport.newRecord()
                oSingleImport.saveExternalData(dicValues)

            elif self.dicFileAttributes['inputType'] == 'stock_goods':
                    self.rpc.callRP('src.Articles.py_insertGoods', 1,dicValues['article'][0],float(dicValues['st'][0]), self.dicUser)
            elif self.dicFileAttributes['inputType'] == 'webshop_article':
                    dicValues['products_model'][0] = dicValues['products_model'][0].decode('latin-1').encode('utf-8')
                    dicValues['remark_w'][0] = dicValues['remark_w'][0].decode('latin-1').encode('utf-8')
                    dicValues['s9'][0] = dicValues['s9'][0].decode('latin-1').encode('utf-8')
                    if dicValues['s8'][0]:
                        dicValues['s8'][0] = dicValues['s8'][0].decode('latin-1').encode('utf-8')
                    
                    s9 = dicValues['products_model'][0][0:3]
                    if  s9 == '913' or s9 == '311' or  s9 == '301' or s9 =='302' or s9 =='303'  :
                        #print `dicValues`
                        result = self.rpc.callRP('src.Articles.py_insertWebshopArticle', dicValues, self.dicUser)
                    #print ' webshop-data for article', `result`
                    
                    
                    
            s1 = importFile.readline().strip()
            se += 1
            #print se
            #s1 = None
        importFile.close()

            

        



    def on_ok_button1_clicked(self, event):
    

        self.on_ok_button_clicked(event)
        self.iFileName = os.path.normpath(self.fileName)
        
        print self.iFileName
        print  self.rpc.getServer()
        print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*'

        self.readCtrlFile(self.iFileName)
        self.standardImport()        
        
                     
