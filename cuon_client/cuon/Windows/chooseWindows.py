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
        
        self.specialValue = None 
        self.chooseButton = None
    def setChooseButton(self,  button):
        self.chooseButton = button
        
        
    def setChooseEntry(self,sName, entry):
        # sName = name of Menuitem for choose
        # entry = entry to set value
        print '<<<<<<<<<<<<<<< setCooseEntry <<<<<<<<<<<<<<<<<<<<<'
        self.out(sName + ' ' + `entry`)
        self.chooseEntry = entry
        self.chooseMenuitem = self.getWidget(sName)
        self.chooseMenuitem.set_sensitive(True)
        

    def pressChoosebutton(self):
        if self.chooseButton:
            self.activateClick(self.chooseButton, 'clicked')
            
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
    
    
