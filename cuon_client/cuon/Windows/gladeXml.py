
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
import cPickle
import cuon.TypeDefs
from cuon.TypeDefs.defaultValues import defaultValues
import os
import os.path



class gladeXml(defaultValues):

    def __init__(self):

        defaultValues.__init__(self)

        self.liAllMenuItems = []
        self.dictEnabledMenuItems = {}
        self.mainwindowTitle = "C.U.O.N."
        self.xmlAutoconnect = False
        self.rpc = cuon.XMLRPC.xmlrpc.myXmlRpc()
        self.accel_group = gtk.AccelGroup()
        self.accel_groups = {}
        self.dicAccelKeys = {}
        self.dicAccelKeys['edit'] = 'e'
        self.dicAccelKeys['save'] = 's'
        self.dicAccelKeys['new'] = 'n'
        self.dicAccelKeys['print'] = 'p'

        
    def setXml(self, xml):
        self.xml = xml
        
    def loadGlade(self, gladeName):
        fname = os.path.normpath(self.td.cuon_path + '/' +  'glade_' + gladeName)  
        self.xml = gtk.glade.XML(fname)
        self.setXmlAutoconnect()

    def writeGlade(self, fname):
        xml1  = eval(self.doDecode(self.rpc.callRP('Database.getInfo', fname)))
        #        print xml1
        # print '------------------------------------------------------------------------------------------------------------------------------'

        # x = self.rpc.callRP('src.XML.py_readDocument', 'cuon_addresses')  self.enableMenuItems(self.editAction)
        d1 = open(os.path.normpath(self.td.cuon_path + '/' + fname),'w')
        d1.write(cPickle.loads(xml1))
        d1.close()

    def loadGladeComplete(self, gladeName):
        fname = 'glade_' + gladeName
        xml1  =eval(self.decode( self.rpc.callRP('Database.getInfo', fname)))
        #        print xml1
        # print '------------------------------------------------------------------------------------------------------------------------------'

        self.rpc = cuon.XMLRPC.xmlrpc.myXmlRpc()
        # x = self.rpc.callRP('src.XML.py_readDocument', 'cuon_addresses')
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

            self.xmlAutoconnect = True

        
    def getWidget(self, sName):
        return self.xml.get_widget(sName )

    def getWidgets(self,sPrefix):
        # bad function in gtk2.8
        #liW = self.xml.get_widget_prefix(sPrefix)
        liW = self.xml.get_widget_prefix('')
        liW2 = []
        for i in liW:
            self.printOut(  i.get_name()[0:3])
            if i.get_name()[0:3] == 'mi_':
                liW2.append(i)
        
        self.printOut( 'Widgets = ', `liW2`)
        return liW2


    def setTitle(self, sName, sTitle):
        self.getWidget(sName).set_title(sTitle)
    
    
    def initMenuItems(self):
        self.liAllMenuItems =  self.getWidgets('mi_')
        self.printOut( 'MenuItems by Init = ', self.liAllMenuItems )

    def enableAllMenuItems(self):
        for i in self.liAllMenuItems:
            if i != None:
                i.set_sensitive(True)

    def disableAllMenuItems(self):
        for i in self.liAllMenuItems:
            if i != None:
                i.set_sensitive(False)

    
    def addEnabledMenuItems(self, sName, sMenuItem, cKey = None):

        if self.dictEnabledMenuItems.has_key(sName):
            liMenuItems = self.dictEnabledMenuItems[sName]
        else:
            liMenuItems = []
        item = self.getWidget(sMenuItem)
        self.printOut( 'item by Enable Menu', `item`)
        if cKey:
            item = self.addKeyToItem(sName, item,cKey)
            
        liMenuItems.append(item)

        self.dictEnabledMenuItems[sName] = liMenuItems

    
    def addKeyToItem(self,sName, item, cKey):
##        if self.accel_groups.has_key(sName):
##            accel = self.accel_groups[sName]
##        else:
##            accel = gtk.AccelGroup()
##            self.accel_groups[sName] = accel
##            
        
            
        item.add_accelerator("activate", self.accel_group, ord(cKey), gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        ##self.accel_groups[sName] = accel
        
        return item
    
##    def setAccel(self, sMenuItem, sName):
##        item = self.getWidget('menuitem1_menu')
##        accel = self.accel_groups[sName]
##        print 'accel by set = ', accel
##        item.set_accel_group(accel)
##        
##        
    def removeEnabledMenuItems(self, sName):
        if self.dictEnabledMenuItems.has_key(sName):
                 del self.dictEnabledMenuItems[sName]
        

    def enableMenuItem(self, sName, sAccel = None, sMenuItem = None):
    
        if  self.dictEnabledMenuItems.has_key(sName):
            liMenuItems =  self.dictEnabledMenuItems[sName]
            for i in liMenuItems:
                if i != None:
                    self.printOut( 'GladeXML-Name = ',sName)
                    i.set_sensitive(True)
                    
                    
                    self.printOut( 'GladeXML-Widget-Name = ', i.get_name())
                    
                else:
                    self.printOut( 'No Menuitem')
##        if sAccel:
##            print 'set Accel'
##            self.setAccel(sMenuItem,sAccel)
##            
    def disableMenuItem(self, sName):
        try:
            liMenuItems =  self.dictEnabledMenuItems[sName]
            for i in liMenuItems:
                if i != None:
                    i.set_sensitive(False)
                else:
                    self.printOut( 'No Menuitem')
            
        except:
            self.printOut( 'No Menuitem')
            
        

    def writeAllGladeFiles(self):

        nameOfGladeFiles  = cPickle.loads(eval(self.doDecode(self.rpc.callRP('Database.getInfo', 'nameOfGladeFiles'))))
        self.printOut( 'nameOfGladefiles' + `nameOfGladeFiles`)
        self.printOut( len(nameOfGladeFiles))
        
        for i in range(0,len(nameOfGladeFiles)):
            self.writeGlade(nameOfGladeFiles[i])
 

    
    def addMenuItem(self, item,sMenue):
        sub1 = item.get_submenu()
        self.printOut( 'sub1 = ', `sub1`)
        newItem = gtk.MenuItem(label = sMenue)
        sub1.append(newItem)
        item.set_submenu(sub1)
        newItem.show()
        return newItem
                 
