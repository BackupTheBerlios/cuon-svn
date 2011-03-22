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
import os
#sys.path.append(os.environ['CUON_PATH'])
#sys.path.append('/usr/lib/python/')
#sys.path.append('/usr/lib/python/site-packages/PIL')

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
        self.withoutColumns = ['document_image']
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
        
        self.Rights = None
        self.newTitle = None 
        self.newCategory = None
        self.newDate = None
        self.sub1 = None
        self.sub2 = None
        self.sub3 = None
        self.sub4 = None
        self.Extract = None
        
    def createTmpFile(self, sEXT):
        print '#############################################################'
        print 'sExt = ', sEXT
        print '#############################################################'
        
        b = bz2.decompress(self.imageData)
        mi = cuon.Misc.misc.misc()
        #print self.dicUser  
        sFile =self.dicUser['prefPath']['tmp'] +  mi.getRandomFilename('__dms.' + sEXT)
        
        if b:
            f = open(sFile, 'wb')
            if f:
                f.write(b)
                self.tmpFile = sFile
                f.close()
               
        return sFile
            
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
        if self.imageData:
            dicValues['document_image'] = [self.imageData,'text']
        dicValues['file_format'] = [self.fileFormat, 'string']
        dicValues['file_suffix'] = [self.fileSuffix, 'string']
        dicValues['insert_from_module'] = [self.ModulNumber, 'int']
        dicValues['sep_info_1'] = [self.sep_info_1, 'int']
        if self.sub1:
            dicValues['sub1'] = [self.sub1, 'string']
        if self.sub2:
            dicValues['sub2'] = [self.sub2, 'string']
        if self.sub3:
            dicValues['sub3'] = [self.sub3, 'string']
        if self.sub4:
            dicValues['sub4'] = [self.sub4, 'string']
               
            
        #print dicValues
        if self.newTitle:
            
            dicValues['title'] = [self.newTitle, 'string']
        if self.newDate:
            dicValues['document_date'] = [self.newDate, 'date']
        if self.newCategory:
            dicValues['category'] = [self.newCategory, 'string']
        
        if self.Rights:
            rights,groups = self.rpc.callRP('Database.getDMSRights',self.Rights )
            if rights and rights != 'NONE':
                dicValues['document_rights_activated'] = [True,'bool']
                if rights[0] == 'r':
                    dicValues['document_rights_user_read'] = [True,'bool']
                if rights[1] == 'w':
                    dicValues['document_rights_user_write'] = [True,'bool']
                if rights[2] == 'x':
                    dicValues['document_rights_user_execute'] = [True,'bool']
                    
                if rights[3] == 'r':
                    dicValues['document_rights_group_read'] = [True,'bool']
                if rights[4] == 'w':
                    dicValues['document_rights_group_write'] = [True,'bool']
                if rights[5] == 'x':
                    dicValues['document_rights_group_execute'] = [True,'bool']
                if rights[6] == 'r':
                    dicValues['document_rights_all_read'] = [True,'bool']
                if rights[7] == 'w':
                    dicValues['document_rights_all_write'] = [True,'bool']
                if rights[8] == 'x':
                    dicValues['document_rights_all_execute'] = [True,'bool']
                
                if groups and groups != 'NONE':
                    dicValues['document_rights_groups'] = [groups,'string']
                    dicValues['document_rights_user'] = [self.dicUser['Name'],'string']
                    
        # set to empty values
        self.newDate = None
        self.newTitle = None
        self.newCategory = None 
        self.sub1 = None
        self.sub2 = None
        self.sub3 = None
        self.sub4 = None
        try:
            dicValues['dms_extract'] = [self.Extract.get_text(self.Extract.get_start_iter(), self.Extract.get_end_iter(), 1), 'text']   
        except Exception,  param:
            print 'No Extract Widget'
            print Exception,  param
            
            
            
            
        return dicValues
    def loadDocument(self):
        print 'self.ID = ',  self.ID
        sSql = 'select document_image from dms where id = ' + `self.ID`
        liResult = self.rpc.callRP('Database.executeNormalQuery', sSql, self.sqlDicUser )
        
        if liResult:
            print 'keys = ',  liResult[0].keys()
            s = liResult[0]['document_image']
            try:
                self.imageData = base64.decodestring(s)
                 
            except Exception, param:
                print Exception, param
                self.imageData = None
    
    def loadNotes0SaveDocument(self):
        nID = self.rpc.callRP('Misc.getNotes0ID',self.dicUser)
        if nID:
            self.load(nID)
            self.fillOtherEntries(self.firstRecord)
            
    def fillOtherEntries(self, oneRecord):
        try:
            self.Extract.set_text(oneRecord['dms_extract'])
        except:
            pass
        self.fileFormat = oneRecord['file_format']
        self.fileSuffix = oneRecord['file_suffix']
        self.ModulNumber = oneRecord['insert_from_module']
        
        print 'FileFormat by SDMS', self.fileFormat
        self.size_x = oneRecord['size_x']
        self.size_y =  oneRecord['size_y']
        self.checkPermissions()
    
    def getOrigin(self):
        return self.firstRecord['insert_from_module'],  self.firstRecord['sep_info_1']
        
    def setAllWidgetsVisible(self, visible):
        # Buttons and menu-items
        for x in ['bView','edit1']:
            if self.xml:
                self.getWidget(x).set_sensitive(visible)
        
    def setReadWidgetsVisible(self, visible):
        # Buttons and menu-items
        for x in ['bView']:
            if self.xml:
                self.getWidget(x).set_sensitive(visible)
            
    def setWriteWidgetsVisible(self, visible):
        # Buttons and menu-items
        for x in ['bView', 'edit1']:
            if self.xml:
                self.getWidget(x).set_sensitive(visible)
    
    
        
    def checkPermissions(self):
        #print self.getWidget('cbRights').get_active()
        print self.dicUser['Name']
        Permission = self.rpc.callRP('Misc.dmsCheckPermissions',self.ID,self.dicUser)
        print Permission
        # sel all items invisible
        self.setAllWidgetsVisible(False)
        # read 
        if Permission['Read'] and not Permission['Write']:
            self.setReadWidgetsVisible(True)
            print "Read,  not Write visible"    
        else:
            
            self.setAllWidgetsVisible(True)
            print "all to visible "


    def loadMainLogo(self):
        self.imageData = None
        id = self.rpc.callRP('Misc.getIdFromTitle', 'cuon_mainwindow_logo',  self.dicUser)
        print "id for the logo = ",  id
        if id > 0:
            self.load(id)
            
            
            self.loadDocument()
        return self.imageData
        
        
##        s = oneRecord['document_image']
##        print len(s)
##        s2 = base64.decodestring(s)
##        print 'Size'
##        print self.size_x
##        print self.size_y
##        self.imageData = s2
##        if self.fileFormat == 'Image Scanner':
##
##            UC =   bz2.decompress(s2)
##
##
##            newIm = Image.fromstring('RGB',[self.size_x, self.size_y], UC)
##            newIm.thumbnail([480,400])
##            sFile = self.dicUser['prefPath']['tmp'] + 'dms_thumbnail.png'
##            newIm.save(sFile)
##            self.imageWidget.set_from_file(sFile)
##
##        else:
##             
##            logopic = '/usr/lib/cuon/icons/cuon-logo.xpm'
##            pixbuf = gtk.gdk.pixbuf_new_from_file(logopic)
##            scaled_buf = pixbuf.scale_simple(480,400,gtk.gdk.INTERP_BILINEAR)
##            self.imageWidget.set_from_pixbuf(scaled_buf)
##            self.imageWidget.show()
##            #self.imageWidget.set_from_file('/usr/lib/cuon/icons/cuon-logo.jpeg')
