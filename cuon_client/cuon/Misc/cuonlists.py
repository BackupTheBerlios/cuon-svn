from types import *
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import gobject
#from gtk import TRUE, FALSE

import logging
from cuon.Windows.windows  import windows




class cuonlists(windows):

    
    def __init__(self, initialWidget = None, initialFilename = None):
        windows.__init__(self)
        self.fileWidget = None
        self.fileName = None
        self.filedata = []
        
        
        
    
    def on_cancel_button1_clicked(self, event):
        print 'Cancel clicked'
        self.quitFinddialog()

    def showFinddialog(self):
        self.getWidget('listdialog1').show()
 

    def quitFinddialog(self):
        self.getWidget('listdialog1').destroy()
        
    def getFilenames(self):
        return self.fileName


    def on_bNewPredefine_clicked(self, event):
        pass
        
    def on_bEditPredefine_clicked(self, event):
        pass
        
    def on_cbPredefined_changed(self, event):
        pass
        
    def on_bDeletePredefine_clicked(self, event):
        pass
