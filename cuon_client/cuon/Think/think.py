import sys
sys.path.append('/usr/lib/python/')
sys.path.append('/usr/lib/python/site-packages/PIL')

from types import *
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import gobject
import string
import commands
import logging
from cuon.Windows.windows  import windows
import SingleMindmap
import cuon.DMS.documentTools
import cuon.DMS.dms
import os



class thinkwindow(windows):

    
    def __init__(self,   allTables ):
        
        windows.__init__(self)
        
        
        self.loadGlade('think.xml','ThinkMainwindow' )
        self.win1 = self.getWidget('ThinkMainwindow')
        self.ModulNumber = self.MN['Think']        
        self.allTables = allTables
        self.singleMindmap = SingleMindmap.SingleMindmap(allTables)
        
        self.entriesMindmap = 'mindmap.xml'
    
    
        #singleMindmap
        
        self.loadEntries(self.entriesMindmap)
        self.singleMindmap.setEntries(self.getDataEntries( self.entriesMindmap) )
        self.singleMindmap.setGladeXml(self.xml)
        self.singleMindmap.setTreeFields( ['header'])
        self.singleMindmap.setStore( gtk.ListStore( gobject.TYPE_STRING, gobject.TYPE_UINT) ) 
        self.singleMindmap.setTreeOrder('header')
        self.singleMindmap.setTree(self.xml.get_widget('tree1') )
        self.singleMindmap.setListHeader(['Header'])
        #print 'Widgets - win = ', `self.win1`
        #print 'Widgets - tree1 = ', `self.xml.get_widget('tree1')`
        
        self.tabMindmap = 0
        self.tabThinking = 1
        # start
        
        self.tabChanged()
     
    #    self.win1.add_accel_group(self.accel_group)
        
    # File Menu
    def on_quit1_activate(self,  event):
        self.win1.hide()
        
    
    
    # Mindmap

    def on_new1_activate(self, event):
        if self.tabOption == self.tabMindmap:
            self.singleMindmap.newRecord()
            self.setEntriesEditable(self.entriesMindmap, True)
            
    
    def on_edit1_activate(self, event):        
        if self.tabOption == self.tabMindmap:
            self.setEntriesEditable(self.entriesMindmap, True)
  
        
    
    def on_save1_activate(self, event):
        
        if self.tabOption == self.tabMindmap:
            print "save mindmap v2"
            self.singleMindmap.save()
            self.setEntriesEditable(self.entriesMindmap, False)
            
        self.tabChanged()
         
    
    def on_delete1_activate(self, event):    
        
        if self.tabOption == self.tabMindmap:
            self.singleMindmap.deleteRecord()

    #Tools
    def on_dms1_activate(self, event):    
        print 'dms clicked'
        if self.singleMindmap.ID > 0:
            print 'ModulNumber', self.ModulNumber
            Dms = cuon.DMS.dms.dmswindow(self.allTables, self.ModulNumber, {'1':self.singleMindmap.ID})
    
        
   # Toolbar-Buttons 
    
    def on_tbNew_clicked(self, event):
        self.activateClick('new1')
          
    
    def on_tbEdit_clicked(self, event):
        self.activateClick('edit1')
        


    def on_tbSave_clicked(self, event):
        self.activateClick('save1')
       
    def on_tbRemove_clicked(self, event):
        self.activateClick('delete1')
        
    def on_tbDMS_clicked(self, event):
        self.activateClick('dms1')

    def refreshTree(self):
        self.singleMindmap.disconnectTree()
        #self.singleThink.disconnectTree()
        
        if self.tabOption == self.tabMindmap:
            print '-->Start Mindmap refresh Tree'
            self.singleMindmap.connectTree()
            self.singleMindmap.refreshTree()
            print '<--End Mindmap refresh Tree'

        elif self.tabOption == self.tabThinking:
            print 'refresh Tree fpr Think-Fee'
            self.singleThink.sWhere  ='where mindmap_id = ' + `int(self.singleMindmap.ID)`
            self.singleThink.getFirstListRecord()
            self.singleThink.fillEntries(self.singleThink.ID)
            


         
    def tabChanged(self):
        print 'tab changed to :'  + str(self.tabOption)
        self.setTreeVisible(True)
        if self.tabOption == self.tabMindmap:
            #Staff
            #self.disableMenuItem('tabs')
            #self.enableMenuItem('staff')
            print 'Seite 0'
            #self.editAction = 'editStaff'
            
        elif self.tabOption == self.tabThinking:
            #Fee
            #self.disableMenuItem('tabs')
            #self.enableMenuItem('fee')
            #self.editAction = 'editFee'
            print 'Seite 1'
  
            
        # refresh the Tree
        self.refreshTree()
        self.enableMenuItem(self.editAction)
        self.editEntries = False

