import sys
import types
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import string
import logging
import dataEntry
import cuon.XMLRPC.xmlrpc
import cuon.TypeDefs
import cuon.Windows.cyr_load_entries
import os
import os.path
from  cuon.Windows.windows  import windows


class chooseWindows(windows):

    def __init__(self):
        windows.__init__(self)

        self.chooseEntry = None
        self.chooseMenuItem = None
        
    def setChooseEntry(self,sName, entry):
        # sName = name of Menuitem for choose
        # entry = entry to set value
        print '<<<<<<<<<<<<<<< setCooseEntry <<<<<<<<<<<<<<<<<<<<<'
        self.chooseEntry = entry
        self.chooseMenuitem = self.getWidget(sName)
        self.chooseMenuitem.set_sensitive()
        

    def setChooseValue(self, chooseValue):
        print '<<<<<<<<<<<<<<< setCooseValue <<<<<<<<<<<<<<<<<<<<<'
        
        self.chooseEntry.set_text(`chooseValue`)
        if self.chooseMenuitem:
            self.chooseMenuitem.set_sensitive(False)
            self.closeWindow()

    def getChangedValue(self, sName):
        iNumber = 0
        s = self.getWidget( sName).get_text()
        if s:
            if len(string.strip(s)) > 0:
                if s.isdigit():
                    iNumber = long(s)
                else:
                    s = string.strip(s)
                    if s[len(s) - 1] == 'L':
                        iNumber = long(s[0:len(s) -1])
                    
        return iNumber
    
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
    
