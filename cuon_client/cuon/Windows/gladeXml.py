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
import types

try:
    import gtksourceview
    
except:
    try:
        import gtksourceview2 as gtksourceview
    except:
        print 'No gtksourceview import possible. Please install gtksourceview for python!!'
      
class gladeXml(defaultValues):

    def __init__(self, servermod = False):

        defaultValues.__init__(self)
        self.servermod = servermod
        self.xml = None
        self.win1 = None
        self.liAllMenuItems = []
        self.dictEnabledMenuItems = {}
        self.mainwindowTitle = "C.U.O.N."
        self.xmlAutoconnect = False
        self.rpc = cuon.XMLRPC.xmlrpc.myXmlRpc()
        self.accel_group = gtk.AccelGroup()
        self.win_accel_group = gtk.AccelGroup()
        
        self.accel_groups = {}
        self.dicAccelKeys = {}
        self.dicAccelKeys['edit'] = 'e'
        self.dicAccelKeys['save'] = 's'
        self.dicAccelKeys['new'] = 'n'
        self.dicAccelKeys['print'] = 'p'
        


        self.clipboard = gtk.clipboard_get()
        
    def setClipboard(self,  text):
        self.clipboard.set_text(text)
        self.clipboard.store()
        
    def getClipboard(self,  iNumber = 0):
        return self.clipboard.wait_for_text()
        
        
    def getNotesEditor(self,  mime_type =  'text/x-tex',  highlight = True):
        try:
            lm = gtksourceview.SourceLanguagesManager()
            textbufferMisc = gtksourceview.SourceBuffer()
        except:
            textbufferMisc = gtksourceview.Buffer()
            lm = gtksourceview.language_manager_get_default()

        
        
        textbufferMisc.set_data('languages-manager', lm)
        manager = textbufferMisc.get_data('languages-manager')
        
        
        try:
            language = manager.get_language_from_mime_type(mime_type)
            textbufferMisc.set_highlight(highlight)
        except:
            language = manager.guess_language(content_type=mime_type)
            textbufferMisc.set_highlight_syntax(highlight)
        
        
        textbufferMisc.set_language(language)
        try:
            viewMisc = gtksourceview.SourceView(textbufferMisc)
        except:
            viewMisc = gtksourceview.View(textbufferMisc)
            
        viewMisc.set_show_line_numbers(True)
        
        return textbufferMisc,  viewMisc
        
        
    def setTextbuffer(self, widget, liField):
        buffer = gtk.TextBuffer(None)
        text = ''
        print self.oUser.userEncoding
        for i in range(len(liField)):
            print type( liField[i])
            print liField[i]
            
            if isinstance(liField[i], types.StringType):
                text = text + liField[i] + '\n'
            elif isinstance(liField[i], types.UnicodeType):
                text = text + liField[i] + '\n'
                 
            elif isinstance(liField[i], types.ClassType) or isinstance(liField[i], types.InstanceType):
                text = text +  `sValue`
            elif isinstance(liField[i], types.IntType):
                text = text + `liField[i]` + '\n'
            elif isinstance(liField[i], types.FloatType):
                text = text + `liField[i]` + '\n'
                                   
            else:
                text = text + `liField[i]` + '\n'
                
        buffer.set_text(text)
        widget.set_buffer(buffer)
        
    def clearTextBuffer(self, widget):
        bText = ''
        buffer = widget.get_buffer()
        buffer.set_text(bText)
        widget.set_buffer(buffer)
        
    def readTextBuffer(self, widget):
        bText = ''
        buffer = widget.get_buffer()
        bText = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), 1)
        return bText
        
    def getActiveText(self, combobox):
        model = combobox.get_model()
        active = combobox.get_active()
        if active < 0:
            return None
        return model[active][0]

    def add2Textbuffer(self, widget, text, direction = None):
        if text:
            try:
                buffer = widget.get_buffer()
            except:
                buffer = widget
                
            bText = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), 1)
            #print '**********************'
            #print bText
            #print '................'
            #print text
            #print '====================='
            
            if not bText:
                bText = ''
            
            if direction and direction == 'Head':
                bText = text + bText
                buffer.set_text(bText)
    
            elif direction and direction == 'Tail':
                bText += text
                buffer.set_text(bText)
            elif direction and direction == 'Overwrite':
                buffer = gtk.TextBuffer(None)
                buffer.set_text(text)
            else:
                bText += text
                buffer.set_text(bText)
            try:
                widget.set_buffer(buffer)
            except:
                pass
            
            

    def setXml(self, xml):
        self.xml = xml
        
    def loadGlade(self, gladeName,sMainWindow=None, gladePath = None):
        if gladePath:
                fname = os.path.normpath(gladePath )  
        else:
            if self.td.SystemName:
                
                if self.td.SystemName == 'LINUX-Standard':
                    fname = os.path.normpath(self.td.cuon_path + '/' +  'glade_' + gladeName)  
                else:
                    fname = os.path.normpath(self.td.cuon_path + '/' +  'glade_'+ self.td.SystemName + '_' + gladeName)  
                  
                #else:
                #    fname = os.path.normpath(self.td.cuon_path + '/' +  'glade_' + gladeName)  
        
            
            else:
                fname = os.path.normpath(self.td.cuon_path + '/' +  'glade_' + gladeName)  
        fnameAlternate = os.path.normpath(self.td.cuon_path + '/' +  'glade_' + gladeName)  

        print 'fname ',  fname
        print 'fname_Alternate ',  fnameAlternate
        
        try:
            self.xml = gtk.Builder()
            self.xml.add_from_file(fname)
            self.xml.set_translation_domain('cuon')

            print "loaded Builder ",  fname
        except:
            try:
                self.xml = gtk.glade.XML(fname)
                print "loaded Glade ",  fname
                

            except:
                try:
                    self.xml = gtk.Builder()
                    self.xml.add_from_file(fnameAlternate)
                    self.xml.set_translation_domain('cuon')

                    print "loaded Builder ",  fnameAlternate
                   

                except:
                    self.xml = gtk.glade.XML(fnameAlternate)
                    print "loaded Glade ",  fnameAlternate
                    
                        
        print 'glade loaded'
        

        if sMainWindow:
            self.win1 = self.getWidget(sMainWindow)
            if self.win1 and sMainWindow.find('Mainwindow') > 0:
                #self.win1.maximize()
                self.win1.connect("delete-event",self.delete_event)
        print "connect"        
        
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

       
    def loadGladeFile(self, gladeName,sMainWindow=None):
         self.xml = gtk.glade.XML(gladeName)
         if sMainWindow:
            self.win1 = self.getWidget(sMainWindow)
         self.setXmlAutoconnect()
         

    def setXmlAutoconnect(self):
        if self.xmlAutoconnect:
            pass
        else:
            try:
                self.xml.connect_signals(self)
            except Exception, params:
                print Exception, params
                nameFuncMap = {}
                for key in dir(self.__class__):
                    nameFuncMap[key] = getattr(self, key)
                    
                if  nameFuncMap:
                                   
                    self.xml.signal_autoconnect(nameFuncMap)

            self.xmlAutoconnect = True
            self.setWinAccelGroup()
        
    def setWinAccelGroup(self):
        pass
        
    def getWidget(self, sName):
        try:
            return self.xml.get_object(sName)
        except Exception, params:
            print Exception, params
            return self.xml.get_widget(sName )

    def getWidgets(self,sPrefix):
        # bad function in gtk2.8
        #liW = self.xml.get_widget_prefix(sPrefix)
        liW = []
        try:
            liW = self.xml.get_objects()
        except Exception, params:
            print Exception, params
            
            liW = self.xml.get_widget_prefix('')
            
        liW2 = []
        for i in liW:
            try:
                if i.get_name()[0:3] == 'mi_':
                    liW2.append(i)
            except:
                pass
        
        self.printOut( 'Widgets = ', `liW2`)
        return liW2


    def setTitle(self, sName, sTitle):
        self.getWidget(sName).set_title(sTitle)
    
    def initMenuItemsMain(self):
        self.liAllMenuItems =  self.getWidgets('mi_')
        #self.printOut( 'MenuItems by Init = ', self.liAllMenuItems )
        
    def initMenuItems(self):
        self.liAllMenuItems =  self.getWidgets('mi_')
        #self.printOut( 'MenuItems by Init = ', self.liAllMenuItems )
        # All window items
        self.addEnabledMenuItems('window','quit1', 'z')
        self.addEnabledMenuItems('window','mi_quit1', 'z')
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
        # as an example, make ctrl+e focus the widget "entry":
        # entry.add_accelerator("grab_focus", accel_group, 'e', 
        # gtk.GDK.CONTROL_MASK, 0)


        try:
            
            item.add_accelerator("activate", self.accel_group, ord(cKey), gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        except Exception,  params:
            print Exception,  params
            
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
                 
    def setText2Widget(self,sText,sWidget):
        if len(sText) > 0:
            self.getWidget(sWidget).set_text(sText)
        else:
            self.getWidget(sWidget).set_text('')

    def gotoTreeItem(self, iItem,  tree1):
        ''' go to Tree Item
        @param iItem: int to jump to TreeItem, 0 to first, -1 to last Item
        '''
        treeModel = tree1.get_moedel()
        firstIter = treeModel.get_iter_first()
        treeSelection = tree1.get_selection()
        iter =firstIter
        if iItem == 0:
            treeSelection.select_iter(firstIter)
        elif iItem == -1:
            while true:
                iter0 = treeModel.iter_next(iter)
                if  iter0:
                    iter = iter0
            if iter:
                treeSelection.select_iter(iter)
        else:
            pass
            
        
    def setWaitCursor(self):
        pass
##        if self.win1:
##            self.win1.get_parent_window().set_cursor(gtk.gdk.WATCH)
##        
    def setNormalCursor(self):
        pass
##        if self.win1:
##            self.win1.get_parent_window().set_cursor(None)
