import sys
from types import *
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import logging
from cuon.XML.MyXML import MyXML
import dataEntry
import cuon.XMLRPC.xmlrpc
import cuon.TypeDefs
import cuon.Windows.cyr_load_entries
from  cuon.Windows.gladeXml import gladeXml
from gtk import TRUE, FALSE
import os
import os.path



class windows(MyXML, gladeXml):

    def __init__(self):
        gladeXml.__init__(self)
        MyXML.__init__(self)
        self.openDB()
        self.oUser = self.loadObject('User')
        
        print `self.oUser`
        self.dicUser = self.oUser.getDicUser()
        
        self.td = self.loadObject('td')
        self.closeDB()
        self.testV = "Hallo"
        
        self.rpc = cuon.XMLRPC.xmlrpc.myXmlRpc()
        # x = self.rpc.getServer().src.XML.py_readDocument('cuon_addresses')
        self.DataEntries = { }
        self.tabOption = 0
#        self.setLogLevel(0)
        self.actualEntries = None
        self.win1 = None
        self.editAction = 'closeMenuItemsForEdit'
        self.editEntries = FALSE

        
    def closeWindow(self):
        self.win1.hide()

        
     
    def setDataEntries(self,sName, dicDE):
        self.DataEntries[sName] = dicDE

    def getDataEntries(self, sName):
        return self.DataEntries[sName]



        

    def loadEntries(self, sName):
        cle = cuon.Windows.cyr_load_entries.cyr_load_entries()
        dicEntries = cle.loadEntries('entry_' + sName )
        dicEntries.setXml(self.xml)
        self.setDataEntries(sName, dicEntries)
        self.setProperties( sName )
        
        

    def setProperties(self, sName):
        self.out('entries for property  = ' + sName)
        entries = self.getDataEntries(sName)
        ##for i in range(0,entries.getCountOfEntries()):
##            entry = entries.getEntryAtIndex(i)
##            # do some stuff with the entry
##            self.out('entry = ' + entry.getName())
##            e1 = self.getWidget(entry.getName())
##            if e1:
##                e1.connect('key_press_event', self.closeMenuEntries)
        self.setEntriesEditable(sName, FALSE)
        
      
                
    def setEntriesEditable(self, sName, ok):
        entries = self.getDataEntries(sName)
        for i in range(0,entries.getCountOfEntries()):
            entry = entries.getEntryAtIndex(i)
            # do some stuff with the entry
            self.out('entry = ' + entry.getName())
            e1 = self.getWidget(entry.getName())
            if e1:
                try:
                    e1.set_editable(ok)
                except:
                    pass
        if ok:
            self.closeMenuEntries()
            
            
    def on_notebook1_switch_page(self, notebook1, page, page_num ):
        self.out( "Notebook switch to page " + `page`)
        self.out( "Notebook switch to page_num" + `page_num`)
        self.out( "Notebook switch to notebook " + `notebook1`)
        self.tabOption = page_num
        
        self.tabChanged()


    def closeMenuEntries(self,sendEntry = None, event = None):
        if self.editEntries == FALSE:
            self.editEntries = TRUE
            self.disableMenuItem(self.editAction)
            

        
        
    def setStatusBar(self):
        print '###----> Statusbar <----###'

        self.statusbar = gtk.Statusbar()
        vbox = self.getWidget('vbox1')
        if vbox:
            print '###----> vbox exist'
            vbox.pack_end(self.statusbar,expand=FALSE)
            self.sb_id = self.statusbar.get_context_id('general_info')
            self.statusbar.show()
       
        else:
            print '###----> vbox do not exist <---###'
            

    def setStatusbarText( self, liText):
        self.statusbar.push(self.sb_id, liText[0])

    def setTreeVisible(self, ok):
        if ok:
            self.getWidget('tree1').set_sensitive(TRUE)
        else:
            self.getWidget('tree1').set_sensitive(FALSE)
            
            
    def startProgressBar(self, Pulse = FALSE):
        fname = os.path.normpath(os.environ['CUON_HOME'] + '/' +  'glade_sqlprogressbar.xml')  
        self.progressbarWindowXML = gtk.glade.XML(fname)
        self.progressbarWindowXML.get_widget('SqlProgressBar').show()
        self.progressbar = self.progressbarWindowXML.get_widget('progressbar1')
        if Pulse:
            self.progressbar.pulse()
        return TRUE
        
    def stopProgressBar(self):
         self.progressbarWindowXML.get_widget('SqlProgressBar').hide()
         
    
    def setProgressBar(self, fPercent, Pulse = FALSE):
        if self.progressbar:
            if Pulse:
                self.progressbar.pulse()
            else:
                self.progressbar.set_fraction(fPercent/100.0)
        else:
            print 'no progressbar'
            
        return TRUE
    

  ##  def setNextFocus(self,oldEntry, event, iOldTabOrder):
##        # cle = cuon.Windows.cyr_load_entries.cyr_load_entries()
##        print iOldTabOrder
##        print event
##        iHighTab = 10000
##        e1 = None
##        print 'len of actualEntries = ' + `self.actualEntries.getCountOfEntries()`
##        for i in range(self.actualEntries.getCountOfEntries()):
##            entry = self.actualEntries.getEntryAtIndex(i)
##            print entry.getName()
##            iTab = entry.getTabOrder()
##            print "iTab vor check = " + `iTab`
##            if iTab < iHighTab and iTab > iOldTabOrder:
##                print "iTab = " + `iTab`
##                iHighTab = iTab
##                e1 = entry
##        if e1:
##            print "Name von Oldentry = " + oldEntry.get_name()
##            print "Name von e1 : " + e1.getName()
##            entryGtk = self.xml.get_widget(e1.getName())
##            if entryGtk:
##                print "Name von GTK-Object = " +  entryGtk.get_name()
##                #entryGtk.set_text('Hallo')
##                entryGtk.grab_focus()

##        return gtk.FALSE
        

    

    
    
