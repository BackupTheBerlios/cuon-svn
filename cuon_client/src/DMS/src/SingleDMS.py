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
import os
sys.path.append(os.environ['CUON_PATH'])

from cuon.Databases.SingleData import SingleData
import logging
import threading
import Image
import bz2
import base64


class SingleDMS(SingleData):

    
    def __init__(self, allTables):

        SingleData.__init__(self)
        # tables.dbd and address
        self.sNameOfTable =  "dms"
        self.xmlTableDef = 0
        self.loadTable(allTables)
        # self.saveTable()
        self.size_x = 0
        self.size_y = 0
        self.imageData = 'No Image'
        
        #self.athread = threading.Thread(target = self.loadTable())
        #self.athread.start()
        
        self.listHeader['names'] = ['name',  'ID']
        self.listHeader['size'] = [25,10,25,25,10]
        self.out( "number of Columns ")
        self.out( len(self.table.Columns))
        #
        self.statusfields = ['title']
        self.imageWidget = None

    def readNonWidgetEntries(self, dicValues):
        print 'readNonWidgetEntries(self) by SingleDMS'
        dicValues['size_x'] = [self.size_x,'int']
        dicValues['size_y'] = [self.size_y,'int']
        dicValues['document_image'] = [self.imageData,'text']
                
        return dicValues

    def fillOtherEntries(self, oneRecord):
        self.size_x = oneRecord['size_x']
        self.size_y =  oneRecord['size_y']

        s = oneRecord['document_image']
        print len(s)
        s2 = base64.decodestring(s)
        print 'Size'
        print self.size_x
        print self.size_y
        
        self.imageData =   bz2.decompress(s2)

                
        newIm = Image.fromstring('RGB',[self.size_x, self.size_y], self.imageData)
        newIm.thumbnail([480,400])
        sFile = self.dicUser['prefPath']['tmp'] + 'dms_thumbnail.png'
        newIm.save(sFile)
        self.imageWidget.set_from_file(sFile)
        
