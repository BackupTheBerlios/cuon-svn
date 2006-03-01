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
import logging
from cuon.XML.MyXML import MyXML
import dataEntry
import cuon.XMLRPC.xmlrpc
import cuon.TypeDefs.typedefs
import cuon.Windows.cyr_load_entries
from  cuon.Windows.gladeXml import gladeXml
# from cuon.XMLRPC.xmlrpc import xmlrpc
from cuon.Misc.messages import messages
import datetime
import time
import calendar


import os
import os.path
import re


class windows(MyXML, gladeXml, messages):

    def __init__(self):
        gladeXml.__init__(self)
        MyXML.__init__(self)
        messages.__init__(self)
        self.Search = False
        
        #xmlrpc.__init__(self)
        
        self.openDB()
        self.oUser = None
        self.dicUser = None
        self.dicSqlUser = None
        self.dicUserKeys = None
        self.loadUserInfo()

        self.td = cuon.TypeDefs.typedefs.typedefs()
        
        self.ModulNumber = 1
        self.MN = {}

        self.MN['Mainwindow'] = 10
        self.MN['Client'] = 1000
        self.MN['Address'] = 2000
        self.MN['Partner'] = 2100

        self.MN['Articles'] = 3000
        self.MN['Order'] = 4000
        self.MN['Stock'] = 5000
        self.MN['DMS'] = 11000
        self.MN['Biblio'] = 12000
        self.MN['AI'] = 13000

        self.sWhereStandard = ''
        self.sepInfo = {}
        
        self.checkClient()
            
        self.td = self.loadObject('td')
        self.closeDB()
        self.testV = "Hallo"
        
        self.rpc = cuon.XMLRPC.xmlrpc.myXmlRpc()
        # x = self.rpc.callRP('src.XML.py_readDocument','cuon_addresses')
        self.DataEntries = { }
        self.tabOption = 0
#        self.setLogLevel(0)
        self.actualEntries = None
        self.win1 = None
        self.editAction = 'closeMenuItemsForEdit'
        self.editEntries = False
        self.dicKeys = {}
        self.dicKeys['CTRL'] = gtk.gdk.CONTROL_MASK 
        self.dicKeys['SHIFT'] = gtk.gdk.SHIFT_MASK 
        self.dicKeys['ALT'] = gtk.gdk.MOD1_MASK
        self.dicKeys['NONE'] = 0 
        
        
        
    def closeWindow(self):
        self.win1.hide()

    def checkClient(self):
        if not self.dicUser['client'] > 0:
            self.dicUser = {}
            
    def loadUserInfo(self):
        self.oUser = self.loadObject('User')
        if self.oUser:
            print `self.oUser`
            self.dicUser = self.oUser.getDicUser()
            self.dicSqlUser = self.oUser.getSqlDicUser()
            print `self.dicUser`
        else:
            self.dicUser = {}
        self.dicUserKeys = self.oUser.getDicUserKeys()
           
    
        
     
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
        
        

    def readSearchDatafields(self, dicWidgets):
        dicSearchfields = {}
   
        for key in dicWidgets.keys():
            print key
            text = self.getWidget(dicWidgets[key]).get_text()
            if text:
                dicSearchfields[key] = text
        return dicSearchfields

    def setProperties(self, sName):
        self.out('entries for property  = ' + sName)
        
        entries = self.getDataEntries(sName)
        for i in range(0,entries.getCountOfEntries()):
            entry = entries.getEntryAtIndex(i)
            # do some stuff with the entry
            ##self.out('entry = ' + entry.getName())
            print 'entry = ' + entry.getName()
            if entry.getDuty():
                e1 = self.getWidget(entry.getName())
                if e1:
                    print 'Duty is True by : ' + `entry.getName()`
                    e1.set_style(self.getStyle('duty','entry', entry.getFgColor(), entry.getBgColor()))
##                e1.connect('key_press_event', self.closeMenuEntries)
        self.setEntriesEditable(sName, False)
        
      
                
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
        if self.editEntries == False:
            self.editEntries = True
            self.disableMenuItem(self.editAction)
            

        
        
    def setStatusBar(self):
        print '###----> Statusbar <----###'

        self.statusbar = gtk.Statusbar()
        vbox = self.getWidget('vbox1')
        if vbox:
            print '###----> vbox exist'
            vbox.pack_end(self.statusbar,expand=False)
            self.sb_id = self.statusbar.get_context_id('general_info')
            self.statusbar.show()
       
        else:
            print '###----> vbox do not exist <---###'
            

    def setStatusbarText( self, liText):
        self.statusbar.push(self.sb_id, liText[0])

    def setTreeVisible(self, ok):
        if ok:
            self.getWidget('tree1').set_sensitive(True)
        else:
            self.getWidget('tree1').set_sensitive(False)
            
            
    def startProgressBar(self, Pulse = False):
        fname = os.path.normpath(os.environ['CUON_HOME'] + '/' +  'glade_sqlprogressbar.xml')  
        self.progressbarWindowXML = gtk.glade.XML(fname)
        self.progressbarWindowXML.get_widget('SqlProgressBar').show()
        self.progressbar = self.progressbarWindowXML.get_widget('progressbar1')
        if Pulse:
            self.progressbar.pulse()
        return True
        
    def stopProgressBar(self):
         self.progressbarWindowXML.get_widget('SqlProgressBar').hide()
         
    
    def setProgressBar(self, fPercent, Pulse = False):
        if self.progressbar:
            if Pulse:
                self.progressbar.pulse()
            else:
                self.progressbar.set_fraction(fPercent/100.0)
        else:
            print 'no progressbar'
            
        return True
    
    def checkKey(self, event,sState, cKey):
        ok = False
        print 'keyval', event.keyval
        print 'keyval-name', gtk.gdk.keyval_name(event.keyval)
        print 'state', event.state
        if (event.state and self.dicKeys[sState])  or sState == 'NONE':
            print 'state is found'
            
            if gtk.gdk.keyval_name(event.keyval) == cKey :
                ok = True
        print 'ok = ', ok
        return ok
        
        
    def getDate(self, entry):
        #print 'orig', `entry.get_time()`
        #newTime = time.localtime(entry.get_time())
        #                print "Datum und Zeit"
        #                print newTime
        #sValue = time.strftime(self.dicSqlUser['DateTimeformatString'], newTime)
        print 'entry = ', entry
        newTime = time.strptime(entry.get_text(), self.dicSqlUser['DateformatString'])
        
        return newTime
        
    def setDate(self, entry, newTime):
        entry.set_text(time.strftime(self.dicSqlUser['DateformatString'],newTime))
        
        
    def addOneDay(self, entry, event):
        oldTime = self.getDate(entry)
        aDay = datetime.timedelta(days=1)
        newTime = datetime.datetime(oldTime[0],oldTime[1], oldTime[2]) + aDay
        self.setDate(entry, newTime.timetuple())
        
    def removeOneDay(self, entry, event):
        oldTime = self.getDate(entry)
        aDay = datetime.timedelta(days=-1)
        newTime = datetime.datetime(oldTime[0],oldTime[1], oldTime[2]) + aDay
        self.setDate(entry, newTime.timetuple())
  
    def getWhere(self, args):
        sWhere = None
        args.reverse()
        firstWhere = True
        while args:
            s = args.pop()
            v = args.pop()
            #print 'args s = ', s
            #print 'args v = ', v
            if v:
                if firstWhere:
                    sWhere = " where " + s +" ~* \'.*" + v + '.*\''
                    firstWhere = False
                else:
                    sWhere = sWhere +" and " + s + ' ~* \'.*' + v + '.*\''
                    
        return sWhere
    
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

##        return False
        

    def getStyle(self, cType, cWidget,  numberFG, numberBG):
        '''
        define an new Style for gtk-widgets
        thanks to
        /-----------------------------------------------------------------------\
        | Tony Denault                     | Email: denault@irtf.ifa.hawaii.edu |
        | Institute for Astronomy          |              Phone: (808) 932-2378 |
        | 640 North Aohoku Place           |                Fax: (808) 933-0737 |
        | Hilo, Hawaii 96720               |                                    |
        \-----------------------------------------------------------------------/
        @param cSwitch: a switch for the applied item
        f = foreground
        b = background
        l = light
        d = dark
        m = mid
        t = text
        s = base

        
        @return: the new style
        '''        
        defaultStyle = self.win1.get_style()
        map = self.win1.get_colormap()
        pColor = self.dicUser['prefColor']
        colorFG =  map.alloc_color(0,0,0)
        colorBG =  map.alloc_color(255*255,255*255, 255*255)
        colorBase =  map.alloc_color(130*255,180*255,220*255)
        colorText = map.alloc_color(180*255, 180*255,70*255)
        colorLight = map.alloc_color("#FF9999")
        colorMid = map.alloc_color("#FF9999")
        colorDark = map.alloc_color("#FF9999")
        
        if pColor['FG'] == 0:
            if pColor['BG'] == 0:
                if cType == 'duty':
                    colorBase =  map.alloc_color("#5feeec")
                    colorText = map.alloc_color("#af0000")
                
        newStyle = defaultStyle.copy()
        '''
        entry : s (base) for background, t ( text) for foreground
        button: b (BG) for background, f (FG) for foreground
        '''
        
        cSwitch = []
        
        if cType == 'duty':
   
            if cWidget == 'entry':
                cSwitch.append( 's')
                cSwitch.append('t')
                
        for cs in cSwitch:
            if cs == 'f':
                for  i in range(5 ):
                    newStyle.fg[i] = colorFG;


            elif cs == 'b':
                for  i in range(5 ):
                    newStyle.bg[i] = colorBG;

            elif cs == 's':
                for  i in range(5 ):
                    newStyle.base[i] = colorBase;
                  
            elif cs == 'l':
                for  i in range(5 ):
                    newStyle.light[i] = colorLight;

            elif cs == 'd':
                for  i in range(5 ):
                    newStyle.dark[i] = colorDark;

            elif cs == 'm':
                for  i in range(5 ):
                    newStyle.mid[i] = colorMid;

            elif cs == 't':
                for  i in range(5 ):
                    newStyle.text[i] = colorText;

    
        return newStyle




    def loadProfile(self, sProfile = None):
        
        if  not sProfile :
            print self.oUser.getDicUser()['Name']
            sProfile = self.rpc.callRP('src.User.py_getNameOfStandardProfile', self.oUser.getDicUser() )

            print 'Profile = '
            print sProfile

        print '-----------------------------------------------------------------------------------'
        print 'Profile = ', sProfile
        
        if sProfile:
            result = self.rpc.callRP('src.User.py_getStandardProfile',  sProfile,  self.oUser.getDicUser() )
            print 'Result Profile'
            print result
            if result:
                self.oUser.userLocales ='de'
                if result.has_key('encoding'):
                    self.oUser.userEncoding = result['encoding']
                self.oUser.userPdfEncoding = 'latin-1'

                #self.oUser.userDateTimeFormatString = "%x %X"
                #self.oUser.userTimeFormatString = "%H:%M"

                self.oUser.serverAddress = None
                self.oUser.userSQLDateFormat = 'DD.MM.YYYY'
                self.oUser.userSQLTimeFormat = 'HH24:MI'
                #self.oUser.prefPath = {}

                self.oUser.prefPath['StandardInvoice1'] =  result['path_to_docs_invoices']
                self.oUser.prefPath['StandardSupply1'] =  result['path_to_docs_supply']
                self.oUser.prefPath['StandardPickup1'] =  result['path_to_docs_pickup']
                self.oUser.prefPath['AddressLists'] =   result['path_to_docs_address_lists']

                self.oUser.prefPath['ReportStandardInvoice1'] =   result['path_to_report_invoices']
                self.oUser.prefPath['ReportStandardSupply1'] =  result['path_to_report_supply']
                self.oUser.prefPath['ReportStandardPickup1'] =  result['path_to_report_pickup']

                self.oUser.prefPath['ReportAddressLists'] =  result['path_to_report_address_lists']

                self.oUser.prefDMS['scan_device'] = result['scanner_device']
                self.oUser.prefDMS['scan_r'] = {'x':result['scanner_brx'], 'y':result['scanner_bry']}
                self.oUser.prefDMS['scan_mode'] = result['scanner_mode']
                self.oUser.prefDMS['scan_contrast'] = result['scanner_contrast']
                self.oUser.prefDMS['scan_brightness'] = result['scanner_brightness']
                self.oUser.prefDMS['scan_white_level'] = result['scanner_white_level']
                self.oUser.prefDMS['scan_depth'] = result['scanner_depth']
                self.oUser.prefDMS['scan_resolution'] = result['scanner_resolution']

                
        else:
            print 'no standard-Profile defined'
        print '__________________________________________________________'
        print 'Profile loaded'
        self.oUser.refreshDicUser()
        print self.oUser.getDicUser()
        print '__________________________________________________________'
        

