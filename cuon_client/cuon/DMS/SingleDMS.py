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
#sys.path.append(os.environ['CUON_PATH'])
sys.path.append('/usr/lib/python/')
sys.path.append('/usr/lib/python/site-packages/PIL')

from cuon.Databases.SingleData import SingleData
import logging
import threading
import Image
import bz2
import base64
import cuon.Misc.misc
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import time

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
        self.ModulNumber = 0
        
        
        #self.athread = threading.Thread(target = self.loadTable())
        #self.athread.start()
        
        self.listHeader['names'] = ['name',  'ID']
        self.listHeader['size'] = [25,10,25,25,10]
        self.out( "number of Columns ")
        self.out( len(self.table.Columns))
        #
        self.statusfields = ['title']
        self.imageWidget = None
        self.fileFormat = None
        self.fileSuffix = None
        
        self.tmpfile = None
        self.ModulNumber = 0
    def createTmpFile(self, sEXT):
        print '#############################################################'
        print 'sExt = ', sEXT
        print '#############################################################'
        
        b = bz2.decompress(self.imageData)
        mi = cuon.Misc.misc.misc()
        print self.dicUser  
        sFile =self.dicUser['prefPath']['tmp'] +  mi.getRandomFilename('__dms.' + sEXT)
        if b:
            f = open(sFile, 'wb')
            if f:
                f.write(b)
                self.tmpFile = sFile
                
            
    def readNonWidgetEntries(self, dicValues):
        newTime = time.localtime()
        tValue =  time.strftime(self.dicUser['DateTimeformatString'], newTime)
        if not self.fileFormat:
            self.fileFormat = 'NONE'
        if not self.fileSuffix:
            self.fileSuffix = 'NONE'
        
        print 'readNonWidgetEntries(self) by SingleDMS'
        dicValues['size_x'] = [self.size_x,'int']
        dicValues['size_y'] = [self.size_y,'int']
        dicValues['document_image'] = [self.imageData,'text']
        dicValues['file_format'] = [self.fileFormat, 'string']
        dicValues['file_suffix'] = [self.fileSuffix, 'string']
        dicValues['insert_from_module'] = [self.ModulNumber, 'int']
        dicValues['sep_info_1'] = [self.sep_info_1, 'int']
        
        return dicValues

    def fillOtherEntries(self, oneRecord):
        
        self.fileFormat = oneRecord['file_format']
        self.fileSuffix = oneRecord['file_suffix']
        self.ModulNumber = oneRecord['insert_from_module']
        
        print 'FileFormat by SDMS', self.fileFormat
        self.size_x = oneRecord['size_x']
        self.size_y =  oneRecord['size_y']

        s = oneRecord['document_image']
        print len(s)
        s2 = base64.decodestring(s)
        print 'Size'
        print self.size_x
        print self.size_y
        self.imageData = s2
        if self.fileFormat == 'Image Scanner':

            UC =   bz2.decompress(s2)


            newIm = Image.fromstring('RGB',[self.size_x, self.size_y], UC)
            newIm.thumbnail([480,400])
            sFile = self.dicUser['prefPath']['tmp'] + 'dms_thumbnail.png'
            newIm.save(sFile)
            self.imageWidget.set_from_file(sFile)

        else:
             
            logopic = '/usr/lib/cuon/icons/cuon-logo.xpm'
            pixbuf = gtk.gdk.pixbuf_new_from_file(logopic)
            scaled_buf = pixbuf.scale_simple(480,400,gtk.gdk.INTERP_BILINEAR)
            self.imageWidget.set_from_pixbuf(scaled_buf)
            self.imageWidget.show()
            #self.imageWidget.set_from_file('/usr/lib/cuon/icons/cuon-logo.jpeg')
