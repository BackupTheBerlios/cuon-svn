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
from gtk import TRUE, FALSE
import cPickle
import cuon.TypeDefs
from cuon.Databases.dumps import dumps
import os
import os.path



class gladeXml(dumps):

    def __init__(self):

        dumps.__init__(self)
        
        self.liAllMenuItems = []
        self.dictEnabledMenuItems = {}
        self.td = self.loadObject('td')
        self.mainwindowTitle = "C.U.O.N."
        self.xmlAutoconnect = FALSE
        self.rpc = cuon.XMLRPC.xmlrpc.myXmlRpc()


    def setXml(self, xml):
        self.xml = xml
        
    def loadGlade(self, gladeName):
        fname = os.path.normpath(os.environ['CUON_HOME'] + '/' +  'glade_' + gladeName)  
        self.xml = gtk.glade.XML(fname)
        self.setXmlAutoconnect()

    def writeGlade(self, fname):
        xml1  = self.rpc.getServer().src.Databases.py_getInfoOfTable(fname)
        #        print xml1
        # print '------------------------------------------------------------------------------------------------------------------------------'

        # x = self.rpc.getServer().src.XML.py_readDocument('cuon_addresses')  self.enableMenuItems(self.editAction)
        d1 = open(os.path.normpath(os.environ['CUON_HOME'] + '/' + fname),'w')
        d1.write(cPickle.loads(xml1))
        d1.close()

    def loadGladeComplete(self, gladeName):
        fname = 'glade_' + gladeName
        xml1  = self.rpc.getServer().src.Databases.py_getInfoOfTable(fname)
        #        print xml1
        # print '------------------------------------------------------------------------------------------------------------------------------'

        self.rpc = cuon.XMLRPC.xmlrpc.myXmlRpc()
        # x = self.rpc.getServer().src.XML.py_readDocument('cuon_addresses')
        d1 = open(fname,'w')
        d1.write(cPickle.loads(xml1))
        d1.close()
        self.xml = gtk.glade.XML(fname)
        self.setXmlAutoconnect()

       
    def loadGladeFile(self, gladeName):
         self.xml = gtk.glade.XML(gladeName)
         self.setXmlAutoconnect()

    def setXmlAutoconnect(self):
        if self.xmlAutoconnect:
            pass
        else:
            nameFuncMap = {}
            for key in dir(self.__class__):
                nameFuncMap[key] = getattr(self, key)
                
            if  nameFuncMap:
                               
                self.xml.signal_autoconnect(nameFuncMap)

            self.xmlAutoconnect = TRUE

        
    def getWidget(self, sName):
        return self.xml.get_widget(sName )

    def getWidgets(self,sPrefix):
        return self.xml.get_widget_prefix(sPrefix)


    def setTitle(self, sName, sTitle):
        self.getWidget(sName).set_title(sTitle)
    
    
    def initMenuItems(self):
        self.liAllMenuItems = self.getWidgets('mi_')
        

    def enableAllMenuItems(self):
        for i in self.liAllMenuItems:
            if i != None:
                i.set_sensitive(TRUE)

    def disableAllMenuItems(self):
        for i in self.liAllMenuItems:
            if i != None:
                i.set_sensitive(FALSE)

    
    def addEnabledMenuItems(self, sName, sMenuItem):

        if self.dictEnabledMenuItems.has_key(sName):
            liMenuItems = self.dictEnabledMenuItems[sName]
        else:
            liMenuItems = []

        liMenuItems.append(self.getWidget(sMenuItem))

        self.dictEnabledMenuItems[sName] = liMenuItems
        

    def removeEnabledMenuItems(self, sName):
        if self.dictEnabledMenuItems.has_key(sName):
                 del self.dictEnabledMenuItems[sName]
        

    def enableMenuItem(self, sName):
        if  self.dictEnabledMenuItems.has_key(sName):
            liMenuItems =  self.dictEnabledMenuItems[sName]
            for i in liMenuItems:
                if i != None:
                    print sName
                    i.set_sensitive(TRUE)
                else:
                    print 'No Menuitem'

    def disableMenuItem(self, sName):
        try:
            liMenuItems =  self.dictEnabledMenuItems[sName]
            for i in liMenuItems:
                if i != None:
                    i.set_sensitive(FALSE)
                else:
                    print 'No Menuitem'
            
        except:
            print 'No Menuitem'
            
        

    def writeAllGladeFiles(self):

        nameOfGladeFiles  = cPickle.loads(self.rpc.getServer().src.Databases.py_getInfoOfTable('nameOfGladeFiles'))
        print 'nameOfGladefiles' + `nameOfGladeFiles`
        print len(nameOfGladeFiles)
        
        for i in range(0,len(nameOfGladeFiles)):
            self.writeGlade(nameOfGladeFiles[i])
 

    
