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
from types import *
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import string
import ConfigParser
import types
from cuon.Misc.fileSelection import fileSelection
import SingleImport

import cuon.XMLRPC.xmlrpc

class export_generic1(fileSelection):
    
    def __init__(self, allTables):
        
        fileSelection.__init__(self)
        
        self.dicFileAttributes = {}
        self.dicFileAttributes['iFile'] = None
        self.dicFileAttributes['splitValue'] = ';'
        self.dicFileAttributes['fromChangedValue'] = None
        self.dicFileAttributes['toChangedValue'] = ''
        self.dicFileAttributes['printHeader'] = 'YES'
        #self.dicFileAttributes['allTables'] = allTables
        self.rpc = cuon.XMLRPC.xmlrpc.myXmlRpc()
        self.iColumns = 0
        self.dicFileAttributes['Decoding'] = None
        self.dicFileAttributes['Encoding'] = None
         
                               

    def readCtrlFile(self, iFileName):
        
        self.dicFileAttributes['exportFile'] = None
        self.dicFileAttributes['exportTablse'] = None
        self.dicFileAttributes['exportHeader'] = None
        self.dicFileAttributes['inputType'] = 'Standard'
        self.dicFileAttributes['liColumns'] = None
        self.dicFileAttributes['Decoding'] = None
        self.dicFileAttributes['Encoding'] = None
        
        self.dicFileAttributes['extraFunction'] = None
        
        try:
            self.cpParser = ConfigParser.ConfigParser()
            
            f = open(iFileName)
            print 'File = ',  iFileName,  f
            self.cpParser.readfp(f)
            f.close()
        except:
            pass
            
        print 'List of sections',  self.getListOfParserSections()
        self.dicFileAttributes['exportFile'] = self.getConfigOption('Export', 'Filename')
        self.dicFileAttributes['exportTables'] = self.getConfigOption('Export', 'Tables')
        self.dicFileAttributes['Columns'] =self.getConfigOption('Export', 'Columns')
        self.dicFileAttributes['Headers'] =self.getConfigOption('Export', 'Headers')
        
        self.dicFileAttributes['Where'] =self.getConfigOption('SQL', 'Where')
        self.dicFileAttributes['Order'] =self.getConfigOption('SQL', 'Order')
        self.dicFileAttributes['Group'] =self.getConfigOption('SQL', 'Group')
        
        
        self.dicFileAttributes['splitValue'] = self.getConfigOption('Values', 'Split')
        self.dicFileAttributes['Encoding'] = self.getConfigOption('Values', 'Encoding')
        self.dicFileAttributes['Decoding'] = self.getConfigOption('Values', 'Decoding')
        self.dicFileAttributes['fromChangedValue'] = None
        self.dicFileAttributes['toChangedValue'] = ''
        self.dicFileAttributes['printHeader'] = self.getConfigOption('Values', 'print_header')
        self.dicFileAttributes['stringDelimit'] = self.getConfigOption('Values', 'string_delimit')
        self.dicFileAttributes['changeFloat'] = self.getConfigOption('Values', 'change_float')
        self.dicFileAttributes['exportHeader'] 
      
        print 'dicFileAttributes'
        print self.dicFileAttributes
        print '#############################'
        
    def standardExport(self):
        #print 'dicfileAttributes', self.dicFileAttributes
        print 'input-file = ', self.dicFileAttributes['exportFile']
        sSql = "select  "
        liColumns = self.dicFileAttributes['Columns'].split(',')
        liHeaders = self.dicFileAttributes['Headers'].split(',')
        
        for i in range(len(liColumns)):
            sSql += liColumns[i] + ' as ' + liHeaders[i] + ' ,  '
        
        sSql = sSql[:len(sSql)-3]
        sSql += 'from ' +  self.dicFileAttributes['exportTables']    
        
        if self.dicFileAttributes['Where'] :
            sSql += ' where ' + self.dicFileAttributes['Where'] 
        if self.dicFileAttributes['Group'] :
            sSql += ' group by ' + self.dicFileAttributes['Group'] 
            
        if self.dicFileAttributes['Order'] :
            sSql += ' order by ' + self.dicFileAttributes['Order'] 
          
        
        print 'sSql = ',  sSql
        liExport  = self.rpc.callRP('Database.executeNormalQuery', sSql, self.dicUser)
        
        try:
            os.remove(self.dicFileAttributes['exportFile'])
        except:
            pass
            
        exportFile = open(self.dicFileAttributes['exportFile'], 'a')   
        if self.dicFileAttributes['printHeader'].upper() == 'YES':
            iHeader = len(liHeaders)
            for aHeader in range(iHeader):
                print 'Header', iHeader,  aHeader
                if iHeader == aHeader+1:
                    exportFile.write(liHeaders[aHeader] )
                else:
                    exportFile.write(liHeaders[aHeader]+ self.dicFileAttributes['splitValue'])
                 
            exportFile.write('\n\n')    
        if liExport:
            
            
            for oneExport in liExport:
                print 'onexport = ',  oneExport
                iOneExport = len(liColumns)
                for aColumn in range(iOneExport):
                    aRow = liHeaders[aColumn].lower().strip()
                    if aRow.find('.') >=0:
                        aRow = aRow[aRow.find('.'):]
                    print 'column',  iOneExport, aColumn
                    if  isinstance(oneExport[aRow], types.StringType) or isinstance(oneExport[aRow], types.UnicodeType):
                        if self.dicFileAttributes['Decoding']:
                            oneExport[aRow] = oneExport[aRow].decode(self.dicFileAttributes['Decoding'])
                            print 'Decoding = ', self.dicFileAttributes['Decoding'],   oneExport[aRow]
                        if self.dicFileAttributes['Encoding']:
                            oneExport[aRow] = oneExport[aRow].encode(self.dicFileAttributes['Encoding'])
                            print 'Encoding = ', self.dicFileAttributes['Encoding'],   oneExport[aRow]
                        if self.dicFileAttributes['stringDelimit']:
                            oneExport[aRow] = self.dicFileAttributes['stringDelimit'] + oneExport[aRow]+ self.dicFileAttributes['stringDelimit']
                    elif  isinstance(oneExport[aRow], types.FloatType):
                        if self.dicFileAttributes['changeFloat']:
                            oneExport[aRow] =  `oneExport[aRow]`
                            oneExport[aRow] = oneExport[aRow].replace('.', self.dicFileAttributes['changeFloat'])
                    else:
                        oneExport[aRow] = `oneExport[aRow]`
                        
                    if iOneExport == aColumn +1:
                        exportFile.write(oneExport[aRow] ) 
                    else:
                        exportFile.write(oneExport[aRow]+self.dicFileAttributes['splitValue']) 
                        
                exportFile.write('\n')
                
            
        exportFile.close()
        
        
    def on_ok_button1_clicked(self, event):
    

        self.on_ok_button_clicked(event)
        self.iFileName = os.path.normpath(self.fileName)
        
        print self.iFileName
        print  self.rpc.getServer()
        print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*'

        self.readCtrlFile(self.iFileName)
        self.standardExport()        
        
