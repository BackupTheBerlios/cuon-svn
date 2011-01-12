# -*- coding: utf-8 -*-
##Copyright (C) [2003-2005]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 

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
#import cuon.Login.User
import SingleDMS
import dms 

import cuon.Misc.misc
import cuon.Misc.cuon_dialog

import os

try:
    import Image
except:
    print "no package Image found"
    print ""
    
import bz2
import re
import binascii
import cuon.DMS.documentTools
import base64

GtkSV = True 
try:
    import gtksourceview
    
except:
    try:
        import gtksourceview2 as gtksourceview
    except:
        print 'No gtksourceview import possible. Please install gtksourceview for python!!'
        GtkSV = False


class dmswindow(windows):

    
    def __init__(self, allTables, module = 0, sep_info = None, dicVars={}, dicExtInfo={}):
        
        windows.__init__(self)

        self.ModulNumber = self.MN['DMS']
        self.dicVars = dicVars
        self.dicExtInfo = dicExtInfo
        
            
        self.allTables = allTables
        
        self.openDB()
        self.oUser = self.loadObject('User')
        self.closeDB()
        #print self.oUser
        #print '-.............................'
        self.oDocumentTools = cuon.DMS.documentTools.documentTools()
        
        #print '1 --'
        self.singleDMS = SingleDMS.SingleDMS(allTables)
        #print '2 --'
        self.singleDMS.username = self.oUser.getUserName()
        self.loadGlade('dms.xml', 'DMSMainwindow')
        #self.win1 = self.getWidget('DMSMainwindow')
        #self.win1 = self.getWidget('DMSMainwindow')
        self.diaLink = self.getWidget('diaLink')
        self.diaLink.hide()
        
        self.scanfile = None
        self.liPrintNewsletter = None
        #print '3 --'
        self.EntriesPreferences = 'dms.xml'
        
        if sep_info:
            try:
                if sep_info.has_key('1'):
                    self.sepInfo['1'] = sep_info['1']
                if sep_info.has_key('2'):
                    self.sepInfo['2'] = sep_info['2']
                if sep_info.has_key('3'):
                    self.sepInfo['3'] = sep_info['3']
            except:
                print 'Error by sep-info'
        else:
            self.sepInfo['1'] = self.MN['DMS']

        ##print "Sep-Info 1 ",  self.sepInfo['1']
        #print '4 --'   
        if module > 0:
            self.ModulNumber = module
        if  self.ModulNumber != self.MN['DMS'] :
            self.sWhereStandard = ' where insert_from_module = ' + `self.ModulNumber`
            self.sWhereStandard = self.sWhereStandard + ' and  sep_info_1 = ' +  `self.sepInfo['1']`            
        else:
            scd = cuon.Misc.cuon_dialog.cuon_dialog()
        ##print '5 --'        
        if self.ModulNumber == self.MN['Newsletter']:
            cd = cuon.Misc.cuon_dialog.cuon_dialog()
            ok, res = cd.inputLine( _('Print Newsletter'), _('insert label(s) for newsletter'))
            print 'ok = ',  ok, 'Res = ',  res
            if ok and res:
                self.liPrintNewsletter = self.rpc.callRP('Address.getNewsletterAddresses', res, self.dicUser)
                print 'self.liPrintNewsletter = ',  self.liPrintNewsletter
                if self.liPrintNewsletter and self.liPrintNewsletter not in ['NONE','ERROR']:
                    self.getWidget('bFaxNewsletter').set_sensitive(True)
                    self.getWidget('bPrintNewsletter').set_sensitive(True)
    
        
        #print '6 --'
        self.loadEntries(self.EntriesPreferences)
        
        
        self.singleDMS.sWhere = self.sWhereStandard
        self.singleDMS.setEntries(self.getDataEntries('dms.xml') )
        self.singleDMS.setGladeXml(self.xml)
        self.singleDMS.ModulNumber = self.ModulNumber
        print 'self.singleDMS.ModulNumber', self.singleDMS.ModulNumber
        self.singleDMS.setTreeFields( ['title', 'category','document_date'] )
        self.singleDMS.setStore( gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING,  gobject.TYPE_UINT) ) 
        self.singleDMS.setTreeOrder('title, document_date')
        self.singleDMS.setListHeader([_('Title'), _('Category'), _('Doc.-Date')])
        self.singleDMS.setTree(self.getWidget('tree1') )
        #print '7 --'
        self.singleDMS.imageWidget = self.getWidget('iThumbnail')
        #print '7 -0'
        # Menu-items
        self.initMenuItems()

        #print '7 05'
        
        # Close Menus for Tab
        self.addEnabledMenuItems('tabs','')
        print '7 -1'
        # enabledMenues for Preferences
        #self.addEnabledMenuItems('editProfile','profile1')
        self.addEnabledMenuItems('editDMS','clear1',self.dicUserKeys['delete'])
        #print '7 -2'
        #self.addEnabledMenuItems('editProfile','save1')
        self.addEnabledMenuItems('editDMS','new1',self.dicUserKeys['new'])
        #print '7 -3'
        self.addEnabledMenuItems('editDMS','edit1',self.dicUserKeys['edit'])
        #print '7 -4'
        # enabledMenues for Save 
        self.addEnabledMenuItems('editSave','save1', self.dicUserKeys['save'])
        # tabs from notebook
        self.tabDocument = 0
        self.tabAcc = 1
        self.tabExtract = 2
        
          # add keys
        print "accelgroup = ",  self.accel_group
        try:
            self.win1.add_accel_group(self.accel_group)
        except:
            pass
            
            
        #Now check for automatic-Actions
        self.LastDoc = None
        #print '9 --'
        if self.dicExtInfo and self.dicExtInfo.has_key('LastDoc'):
            print 'lastdoc found'
            self.activateClick('new1')
            self.LastDoc =self.dicExtInfo['LastDoc']
            self.activateClick('bImport',None,'clicked')
        
        
        # notes
        print 'GTKSV = ',  GtkSV
        if GtkSV:
            
            self.textbufferMisc,  self.viewMisc = self.getNotesEditor()
            Vbox = self.getWidget('vbExtract')
            oldScrolledwindow = self.getWidget('scExtract')
            #oldScrolledwindow.remove(self.getWidget('tvNotesMisc'))
            oldScrolledwindow.add(self.viewMisc)
            self.viewMisc.show_all()
            oldScrolledwindow.show_all()
            
            
            
            #Vbox.remove(oldScrolledwindow)
            #Vbox.add(self.viewMisc)
            #Vbox.show_all()
            self.singleDMS.Extract = self.textbufferMisc
   


        #print '8 --'
        self.tabOption = self.tabDocument
        self.tabChanged()
        
      
    # Menu items
        

    def on_save1_activate(self, event):
        print 'save1'
        oldID = self.singleDMS.ID
        self.singleDMS.sep_info_1 = self.sepInfo['1']
        self.singleDMS.ModulNumber = self.ModulNumber
        newID = self.singleDMS.save(['document_image'])
        
        self.setEntriesEditable(self.EntriesPreferences, False)
        print 'oldID + and new = ',  oldID, newID
        if oldID == -1 and newID > 0:
            # is a new entry
            print 'file suffix = ',  self.singleDMS.fileSuffix
            s = self.rpc.callRP('Misc.getTextExtract', newID , self.singleDMS.fileSuffix, self.dicUser)
        self.tabChanged()
        
    def on_new1_activate(self, event):
        self.singleDMS.newRecord()
        dicDate = self.getActualDateTime()
        self.getWidget('eDocumentDate').set_text(dicDate['date'])
        
        self.setEntriesEditable(self.EntriesPreferences, True)
        

    def on_edit1_activate(self, event):
        if self.tabOption == self.tabDocument:
            self.setEntriesEditable(self.EntriesPreferences, True)
##        elif self.tabOption == self.tabPrinting:
##            self.setEntriesEditable(self.EntriesPreferencesPrinting, True)
##        elif self.tabOption == self.tabPathToReports:
##            self.setEntriesEditable(self.EntriesPreferencesPathToReports, True)
##        elif self.tabOption == self.tabPathToDocs:
##            self.setEntriesEditable(self.EntriesPreferencesPathToDocs, True)


    def on_clear1_activate(self, event):
        self.singleDMS.deleteRecord()

    def on_quit1_activate(self, event):
        self.closeWindow() 

    def on_eDMSSearch_key_press_event(self, entry, event):
        print 'eSearch_key_press_event'
        if self.checkKey(event,'NONE','Return'):
            self.findDMS()
        
    def on_bSearch_clicked(self, event):
        self.findDMS()
        
    def findDMS(self):
        print 'Search'
        dicSearchfields = self.readSearchDatafields(  {'title':'eSearchTitle', 'category':'eSearchCategory',  'sub1':'eSearchSub1',  'sub2':'eSearchSub2',  'sub3': 'eSearchSub3',  'sub4':'eSearchSub4',  'sub5':'eSearchSub5',  'search1':'eSearchSearch1',  'search2': 'eSearchSearch2',   'search3':'eSearchSearch3',  'search4': 'eSearchSearch4', 'FullText':'eFindFullText'})

        print dicSearchfields
        
        sWhere = ''
        if dicSearchfields:
            for key in dicSearchfields.keys():
                if key == 'FullText':
                    if dicSearchfields[key]:
                        liFullText = dicSearchfields[key].split(' ')
                        if liFullText:
                            if sWhere:
                                sWhere +=  "and  ( "
                            else:
                                sWhere = " where   ("
                        
                            for sSearch in liFullText:
                                sWhere +=  " dms_extract  ~* \'"  + sSearch + "\'  and "
                            
                            sWhere = sWhere[:len(sWhere)-4] + " ) " 
                        
                else:
                    if dicSearchfields[key]:
                        if sWhere:
                            sWhere = sWhere + ' and ' +  key+ " ~* \'"  + dicSearchfields[key] + "\' "
                        else:
                            sWhere = 'where  ' +  key + " ~* \'"  + dicSearchfields[key] + "\' "
                            
            if self.ModulNumber != self.MN['DMS']:
                sWhere += ' and insert_from_module = ' + `self.ModulNumber` 
            
        else:
            sWhere = self.sWhereStandard
            
        print sWhere
        
        self.singleDMS.sWhere = sWhere
        self.refreshTree()
        
        
    def on_bScan_clicked(self, event):
        self.scanDocument()
        self.singleDMS.fileFormat = self.dicUser['prefDMS']['fileformat']['scanImage']['format']

    def on_bScanMulti_clicked(self,event):
        print 'Multi-Scan'
        try:
            status,data = commands.getstatusoutput('scan.sh')
            if status == 0:
                if data.find('FILENAME:') > -1:
                    filename = data[data.find('FILENAME:')+9:data.find('###')]
                    print 'Filename = ', filename
                    self.LastDoc = filename
                    self.on_bImport_clicked(None)
                
        except Exception, params:
            print Exception, params
            
        
    
    def on_bImport_clicked(self, event):
        print 'bImport'
        if self.LastDoc:
            filename = self.LastDoc
            self.LastDoc = None
        else:
            filename = self.getWidget("gfcb_ImportFile").get_filename()
            
        self.oDocumentTools.importDocument( self.singleDMS, self.dicUser, filename )
        

    def on_bLink_clicked(self, event):
        print 'bLink'
        self.diaLink.show()
    def on_okbutton1_clicked(self, event):
        print 'ok clicked'
        sLink = self.getWidget('eLink').get_text()
        print sLink
        self.diaLink.hide()
        self.singleDMS.imageData = sLink
        self.singleDMS.fileFormat = self.dicUser['prefDMS']['fileformat']['LINK']['format']

    def on_cancelbutton1_clicked(self, event):
        print 'cancel clicked'
        self.diaLink.hide()
        
    def on_bFaxNewsletter_clicked(self, event):
        pass
    def on_bPrintNewsletter_clicked(self, event):
        print 'print Newsletter'
        print self.liPrintNewsletter
        for onePrint in self.liPrintNewsletter:
          self.oDocumentTools.viewDocument(self.singleDMS, self.dicUser, onePrint, Action='PrintNewsletter')  
        
    def on_bFaxLastDocument_clicked(self, event):
        if self.singleDMS.tmpFile:
            cDiag = cuon.Misc.cuon_dialog.cuon_dialog()
            ok, phone_number = cDiag.inputLine('Fax','Input Phone-Number')
            print ok 
            if ok:
                print self.singleDMS.tmpFile
                filename = self.singleDMS.tmpFile[:len(self.singleDMS.tmpFile)-3] + 'pdf'
                print filename
                singleDMS2 = SingleDMS.SingleDMS(self.allTables)
                
                self.oDocumentTools.importDocument( singleDMS2, self.dicUser, filename)
                #phone_number = '05744 511750'
                self.rpc.callRP('Misc.faxData',self.dicUser, base64.encodestring(singleDMS2.imageData),phone_number)
    def on_bWriteLastDocument_clicked(self, event):
        print 'write last document back'
        if self.dicExtInfo:
            self.dicExtInfo['LastDoc'] = self.singleDMS.tmpFile
            self.dicExtInfo['Save'] = 'OVERWRITE'
        self.LastDoc = self.singleDMS.tmpFile

        self.on_edit1_activate(None)
        
        self.on_bImport_clicked(None)
        self.on_save1_activate(None)
        
            
    def on_bWriteLastDocumentAs_clicked(self, event):
        if self.dicExtInfo:
            self.dicExtInfo['LastDoc'] = self.singleDMS.tmpFile
            self.dicExtInfo['Save'] = 'NEW'

            dm2 = cuon.DMS.dms.dmswindow(self.allTables, self.dicExtInfo['Modul'], self.dicExtInfo['sep_info'],None,self.dicExtInfo)
    
    def on_bView_clicked(self, event):
        print  self.dicUser['prefDMS']['fileformat']['scanImage']['format']
        print  self.singleDMS.fileFormat

        self.oDocumentTools.viewDocument(self.singleDMS, self.dicUser, self.dicVars)
        
            
    def on_tree1_row_activated(self, event, data1, data2):
        self.on_bView_clicked(event)
        
    def on_tree1_columns_changed(self, event=None, data=None):
        print event, data
        
    # toolbar buttons
    
    def on_tbNew_clicked(self, event):
        print "tbnew"
        if self.tabOption >= self.tabDocument:
            self.on_new1_activate(event)
        
    def on_tbEdit_clicked(self, event):
        if self.tabOption >= self.tabDocument:
            self.on_edit1_activate(event)
            
    def on_tbSave_clicked(self, event):
        if self.tabOption >= self.tabDocument:
            self.on_save1_activate(event)
            
            
    def on_tbDelete_clicked(self, event):
        if self.tabOption >= self.tabDocument:
            self.on_clear1_activate(event)
            
    def on_tbExit_clicked(self, event):
        print 'close'
        if self.tabOption >= self.tabDocument:
            self.on_quit1_activate(event)
            
    def refreshTree(self):
        self.singleDMS.disconnectTree()
    
        
        if self.tabOption == self.tabDocument:
            
            #self.singleDMS.sWhere = " where username = \'" + self.oUser.getUserName() + "\'"
            self.singleDMS.connectTree()
            self.singleDMS.refreshTree()
            #self.ModulNumber = self.MN['DMS']
            
    def tabChanged(self):
        self.out( 'tab changed to :'  + str(self.tabOption))
        
        if self.tabOption == self.tabDocument:
            #Preferences
            self.disableMenuItem('tabs')
            self.enableMenuItem('editDMS')

            self.actualEntries = self.singleDMS.getEntries()
            self.editAction = 'editDMS'
            self.setTreeVisible(True)
            self.out( 'Seite 0')
            self.singleDMS.setEntries(self.getDataEntries(self.EntriesPreferences) )
            # set the Entries manually, because there is no tree event
            self.singleDMS.fillEntries(self.singleDMS.ID)


        else:
            
            self.setTreeVisible(False)

        # refresh the Tree
        self.refreshTree()
        self.enableMenuItem(self.editAction)
        self.editEntries = False
        
    
    def scanDocument(self):
    
        self.oDocumentTools.scanDocument(self.singleDMS, self.dicUser)
        
   
                        
