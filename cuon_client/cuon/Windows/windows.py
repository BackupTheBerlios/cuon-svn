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
import types
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import logging
from cuon.XML.MyXML import MyXML
import dataEntry
import cuon.XMLRPC.xmlrpc

import cuon.Windows.cyr_load_entries
#from  cuon.Windows.gladeXml import gladeXml
# from cuon.XMLRPC.xmlrpc import xmlrpc
from  cuon.Windows.rawWindow import rawWindow

from cuon.Misc.messages import messages
import datetime
import time
import calendar


import os
import os.path
import re
import commands

class windows(rawWindow, MyXML, messages):

    def __init__(self):
        #gladeXml.__init__(self)
        rawWindow.__init__(self)
        MyXML.__init__(self)
        messages.__init__(self)
        self.Search = False
        self.cursor = None
        #xmlrpc.__init__(self)
        self.FirstInit = True
        self.ModulNumber = 1
        self.MN = {}

        self.MN['Mainwindow'] = 10
        self.MN['Client'] = 1000
        
        self.MN['Address'] = 2000
        self.MN['Address_info'] = 2001
        
        self.MN['Partner'] = 2100
        self.MN['Partner_info'] = 2101
        
        self.MN['Partner_Schedul'] = 2200
        self.MN['Partner_Schedul_info'] = 2201

        self.MN['Articles'] = 3000
        self.MN['MaterialGroups'] = 23000

        self.MN['Order'] = 4000
        self.MN['Stock'] = 5000
        self.MN['Staff'] = 6000
        self.MN['StaffFee'] = 6100
        
        self.MN['Project'] = 14000
        self.MN['Project_info'] = 14001

        self.MN['DMS'] = 11000
        self.MN['Forms_Address_Notes_Misc'] = 11010
        self.MN['Forms_Address_Notes_Contacter'] = 11011
        self.MN['Forms_Address_Notes_Rep'] = 11012
        self.MN['Forms_Address_Notes_Salesman'] = 11013
        self.MN['Newsletter'] = 11100
        
        self.MN['Biblio'] = 12000
        self.MN['AI'] = 13000
        self.doEdit = -1
        self.noEdit = -1
        
        self.oldTab = -1
        
        self.sWhereStandard = ''
        self.sWhereSearch = None
        self.sepInfo = {}
        
        self.checkClient()
            
        
        self.testV = "Hallo"
        
        self.rpc = cuon.XMLRPC.xmlrpc.myXmlRpc()
        # x = self.rpc.callRP('src.XML.py_readDocument','cuon_addresses')
        self.DataEntries = { }
        self.tabOption = 0
#        self.setLogLevel(0)
        self.actualEntries = None
        
        self.editAction = 'closeMenuItemsForEdit'
        self.editEntries = False
        self.dicKeys = {}
        self.dicKeys['CTRL'] = gtk.gdk.CONTROL_MASK 
        self.dicKeys['SHIFT'] = gtk.gdk.SHIFT_MASK 
        self.dicKeys['ALT'] = gtk.gdk.MOD1_MASK
        self.dicKeys['NONE'] = 0 
        
        # as an example, make ctrl+e focus the widget "entry":
        # entry.add_accelerator("grab_focus", accel_group, 'e', 
        # gtk.GDK.CONTROL_MASK, 0)

        
    def closeWindow(self):
        self.saveDataQuestion()
        self.win1.hide()
        
    
    def delete_event(self, widget, event, data=None):
        # If you return FALSE in the "delete_event" signal handler,
        # GTK will emit the "destroy" signal. Returning TRUE means
        # you don't want the window to be destroyed.
        # This is useful for popping up 'are you sure you want to quit?'
        # type dialogs.
        print "delete event occurred"
        
        self.closeWindow()
        # Change FALSE to TRUE and the main window will not be destroyed
        # with a "delete_event".
        return True        
        
    def openWindow(self):
        self.win1.show()
        return False
    def setWinAccelGroup(self):
        if self.win1:
            print 'add accelGroup'
            self.win_accel_group.connect_group(ord('f'),gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE, self.startFind)
            self.win1.add_accel_group(self.win_accel_group)
            #self.win1.add_accelerator(self.startFind(), self.win_accel_group, ord('f'), gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        
    def startFind(self,*args):
        print 'Find something'
        liStatus = commands.getstatusoutput('tracker-search-tool')
        return True
        
    def checkClient(self):
        if not self.dicUser.has_key('client') or not self.dicUser['client'] > 0:
            self.dicUser = {}
            
    def clearSearch(self, event):
        print 'Clear Search activate'
        self.sWhereSearch = None
        self.tabChanged()
        
    def activateClick(self, sItem, event = None, sAction = 'activate'):
        item = self.getWidget(sItem)
        if item:
            item.emit(sAction)
        
     
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
            self.printOut(key)
            text = self.getWidget(dicWidgets[key]).get_text()
            if text:
                dicSearchfields[key] = text
        return dicSearchfields

    
                
    def setEntriesEditable(self, sName, ok):
        self.actualEntries = sName
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
        
    def saveCursor(self):
        self.cursor = self.win1.get_cursor()

    def setEditCursor(self):
        self.saveCursor()
        self.win1.set_cursor(gtk.gdk.PENCIL)
    
    def restoreCursor(self):
        if self.cursor:
            self.win1.set_cursor(self.cursor)
        
    def startEdit(self):
        pass
        #self.setEditCursor()
        
    def endEdit(self):
        pass
        #self.restoreCursor()
        
    def setPageVisible(self, sNotebook, page_num, visible=True):
        nb = self.getWidget(sNotebook)
        
            
    def on_notebook1_switch_page(self, notebook1, page, page_num ):
        #self.out( "Notebook switch to page " + `page`)
        #self.out( "Notebook switch to page_num" + `page_num`)
        #self.out( "Notebook switch to notebook " + `notebook1`)
        if self.doEdit > self.noEdit:
            if self.QuestionMsg('Unsaved Data ! Wish you save them ?'):
                self.saveData()
                self.doEdit = self.noEdit
            else:
                self.doEdit = self.noEdit
                self.endEdit()
            
        self.tabOption = page_num
        
        self.tabChanged()
    def saveData(self):
        pass
        

    def closeMenuEntries(self,sendEntry = None, event = None):
        if self.editEntries == False:
            self.editEntries = True
            self.disableMenuItem(self.editAction)
            

        
        
    def setStatusBar(self):
        self.printOut( '###----> Statusbar <----###')

        self.statusbar = gtk.Statusbar()
        vbox = self.getWidget('vbox1')
        if vbox:
            self.printOut( '###----> vbox exist')
            vbox.pack_end(self.statusbar,expand=False)
            self.sb_id = self.statusbar.get_context_id('general_info')
            self.statusbar.show()
       
        else:
            self.printOut( '###----> vbox do not exist <---###')
            

    def setStatusbarText( self, liText):
        self.statusbar.push(self.sb_id, liText[0])

    def setTreeVisible(self, ok):
        if ok:
            self.getWidget('tree1').set_sensitive(True)
        else:
            self.getWidget('tree1').set_sensitive(False)
            
            
    def startProgressBar(self, Pulse = False, Title=None):
        fname = os.path.normpath(self.td.cuon_path + '/' +  'glade_sqlprogressbar.xml')  
        self.progressbarWindowXML = gtk.glade.XML(fname)
        self.PBW = self.progressbarWindowXML.get_widget('SqlProgressBar')
        if Title:
            self.PBW.set_title(Title)
        self.PBW.show()
        self.progressbar = self.progressbarWindowXML.get_widget('progressbar1')
        if Pulse:
            self.progressbar.pulse()
        
        self.progressbar.show()
        
        #print 'progressbar = ', self.progressbar
        return True
        
    def stopProgressBar(self):
        try:
            
            self.progressbarWindowXML.get_widget('SqlProgressBar').hide()
        except:
            pass
         
    
    def setProgressBar(self, fPercent, Pulse = False):
        try:
            
        
            if self.progressbar:
                if Pulse:
                    self.progressbar.pulse()
                else:
                    if fPercent > 100:
                        fPercent = 0
                    #print 'fPercent/100 = ', fPercent/100.0
                    self.progressbar.set_fraction(fPercent/100.0)
                    while gtk.events_pending():
                        gtk.main_iteration(gtk.FALSE)
                
            else:
                self.printOut( 'no progressbar')
        except:
            pass
            
        return True
    
    def checkKey(self, event,sState, cKey, cKey2=None, cKey3=None):
        ok = False
        cKeyR1 = None
        cKeyR2 = None
        cKeyR3 = None
        
        if cKey == 'Return':
            cKeyR1 = 'KP_Enter'
            cKeyR2 = 'ISO_Enter'
            
        
        #self.printOut( 'keyval', event.keyval)
        #self.printOut( 'keyval-name', gtk.gdk.keyval_name(event.keyval))
        #self.printOut( 'state', event.state)
        if (event.state and self.dicKeys[sState])  or sState == 'NONE':
            self.printOut( 'state is found')
            
            if gtk.gdk.keyval_name(event.keyval) == cKey :
                ok = True
            elif cKey2 and gtk.gdk.keyval_name(event.keyval) == cKey2 :
                ok = True
            elif cKey3 and gtk.gdk.keyval_name(event.keyval) == cKey3 :
                ok = True
            elif cKeyR1 and gtk.gdk.keyval_name(event.keyval) == cKeyR1 :
                ok = True
            elif cKeyR2 and gtk.gdk.keyval_name(event.keyval) == cKeyR2 :
                ok = True
            elif cKeyR3 and gtk.gdk.keyval_name(event.keyval) == cKeyR3 :
                ok = True
            
        self.printOut( 'ok = ', ok)
        return ok
        
        
    def getDate(self, entry):
        #print 'orig', `entry.get_time()`
        #newTime = time.localtime(entry.get_time())
        #                print "Datum und Zeit"
        #                print newTime
        #sValue = time.strftime(self.dicSqlUser['DateTimeformatString'], newTime)
        #print 'entry = ', entry
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
        #print args
        while args:
            s = args.pop()
            v = args.pop()
            self.printOut( 'args s = ', s)
            self.printOut( 'args v = ', v)
            if s:
                if isinstance(v, types.BooleanType) :
                    self.printOut( 'sWhere = ', v )
                    if firstWhere:
                        sWhere = " where " + s +" = " + `v` 
                        firstWhere = False
                    else:
                        sWhere = sWhere +" and " + s + " = " + `v` 
                if isinstance(v, types.IntType) :
                    self.printOut( 'sWhere = ', v )
                    if firstWhere:
                        sWhere = " where " + s +" = " + `v` 
                        firstWhere = False
                    else:
                        sWhere = sWhere +" and " + s + " = " + `v`        
                elif v[0] == '#':
                    
                    v = v[1:]
                    v = v.replace('?','~')
                    v = v.replace('>','^')
                    if firstWhere:
                        sWhere = " where " + s +" " + v 
                        firstWhere = False
                    else:
                        sWhere = sWhere +" and " + s + " " + v 
                        
                else:
                    if firstWhere:
                        sWhere = " where " + s +" ~* \'.*" + v + '.*\''
                        firstWhere = False
                    else:
                        sWhere = sWhere +" and " + s + ' ~* \'.*' + v + '.*\''
        
        #print sWhere 
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
        
    def setProperties(self, sName):
        '''
        sets the property (colors,etc.) of an gtk-widget
        @param sName: The name of the widget
        
        '''
        
        self.out('entries for property  = ' + sName)
        
        entries = self.getDataEntries(sName)
        for i in range(0,entries.getCountOfEntries()):
            entry = entries.getEntryAtIndex(i)
            # do some stuff with the entry
            ##self.out('entry = ' + entry.getName())
            self.printOut( 'entry = ' + entry.getName())
            if entry:
                e1 = self.getWidget(entry.getName())
                if entry.getDuty():
                    try:
                        self.printOut( 'Duty is True by : ' + `entry.getName()`)
                        e1.set_style(self.getStyle('duty','entry', entry.getFgColor(), entry.getBgColor()))
                    except:
                        pass
                else:
                    try:
                        e1.set_style(self.getStyle('standard','entry', entry.getFgColor(), entry.getBgColor()))
                    except:
                        pass
                
##                e1.connect('key_press_event', self.closeMenuEntries)
        self.setEntriesEditable(sName, False)
        
      
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
        @param cSType: a switch for the applied item ( ex. duty )
        
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
        #print pColor
        colorFG =  map.alloc_color(0,0,0)
        colorBG =  map.alloc_color(255*255,255*255, 255*255)
        colorBase =  map.alloc_color(130*255,180*255,220*255)
        colorText = map.alloc_color(180*255, 180*255,70*255)
        colorLight = map.alloc_color("#FF9999")
        colorMid = map.alloc_color("#FF9999")
        colorDark = map.alloc_color("#FF9999")
        newStyle = defaultStyle.copy()
        try:
            sTypeBG = 'BG'
            sTypeFG = 'FG'
            
            if cType == 'duty':
                
                #print 'BG/FG',numberBG, numberFG
                sTypeBG = 'DUTY_BG'
                sTypeFG = 'DUTY_FG'
                
                    
        
                
            #print 'Standard BG/FG',numberBG, numberFG
            if numberBG[0] == '#':
                colorBase =  map.alloc_color(numberBG)
            else:
                colorBase =  map.alloc_color(pColor[sTypeBG])
                
            if numberFG[0] == '#':
                colorText = map.alloc_color(numberFG)
            else:
                colorText = map.alloc_color(pColor[sTypeFG])
    
            
                            
                            
                
            
            '''
            entry : s (base) for background, t ( text) for foreground
            button: b (BG) for background, f (FG) for foreground
            '''
            
            cSwitch = []
            
            if cType == 'duty':
       
                if cWidget == 'entry':
                    cSwitch.append( 's')
                    cSwitch.append('t')
            else:
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
    
        except:
            newStyle = defaultStyle.copy()       
        return newStyle




    def loadProfile(self, sProfile = None):
        
        if  not sProfile :
            self.printOut( self.oUser.getDicUser()['Name'])
            sProfile = self.rpc.callRP('User.getNameOfStandardProfile', self.oUser.getDicUser() )

            self.printOut( 'Profile = ')
            self.printOut( sProfile)

        self.printOut( '-----------------------------------------------------------------------------------')
        self.printOut( 'Profile = ', sProfile)
        
        if sProfile:
            result = self.rpc.callRP('User.getStandardProfile',  sProfile,  self.oUser.getDicUser() )
            self.printOut( 'Result Profile')
            #print  'result: ', result
            
            if result != 'NONE':
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
                
                self.loadUserFromPreferences(result)

                
        else:
            self.printOut( 'no standard-Profile defined')
        self.printOut( '__________________________________________________________')
        self.printOut( 'Profile loaded')
        #self.oUser.refreshDicUser()
        self.printOut( self.oUser.getDicUser())
        self.printOut( '__________________________________________________________')
        

    def setDateToEntry(self, event, entryName):
        ok = False
        try:
            print event
            t0 = event.get_date()
            print t0
            t1 = `t0[0]`+' '+ `t0[1] +1` + ' ' + `t0[2]` 
            print t1
            t2 = time.localtime(time.mktime(time.strptime(t1,'%Y %m %d')))
            sTime = time.strftime(self.dicUser['DateformatString'], t2)
            print sTime
           
            eDate = self.getWidget(entryName)
            eDate.set_text(sTime)
            ok = True
        except:
          pass  
        
        return ok
        

    def setDateToCalendar(self, sDate, entryName):
        ok = False
        try:
            
            Cal  = self.getWidget(entryName)
            dt = time.strptime(sDate, self.dicUser['DateformatString'])
            print 'Date', dt
            print dt[0]
            print dt[1]
            Cal.select_month(dt[1] - 1, dt[0])
            Cal.select_day(dt[3])

        except:
            pass
        
        return ok
        
        
        
    def on_key_press_event(self, oEntry, data):
        print 'Key-event',oEntry
        if gtk.gdk.keyval_name(data.keyval) == 'Return' :
            print 'return found'
            
            print oEntry.get_name()
            sEntryName = oEntry.get_name()
            entries = self.getDataEntries(self.actualEntries)
            for i in range(0,entries.getCountOfEntries()):
                entry = entries.getEntryAtIndex(i)
                if entry.getName() == sEntryName:
                # do some stuff with the entry
                #self.out('entry = ' + entry.getName())
                    try:
                        #e1.set_editable(ok)
                        print 'My-Entry = ', entry.getName()
                        sNextWidget = entry.getNextWidget()
                        if sNextWidget == 'LAST':
                            self.saveDataQuestion()
                            
                        else:
                            self.getWidget(sNextWidget).grab_focus()
                            
                            
                    except:
                        pass
        
        print 'key-data', data
        
   
    def saveDataQuestion(self):
        self.saveData()
        self.doEdit = self.noEdit
        
    def loadUserFromPreferences(self, result):
        self.oUser = self.oUser.getUser(result)
        print 'user by windows = ', self.oUser
        print 'dicUser = ', self.oUser.getDicUser()
        self.openDB()
        self.saveObject('User', self.oUser)
        self.closeDB()
            
    def RGBToHTMLColor(self, rgb_tuple):
        """ convert an (R, G, B) tuple to #RRGGBB """
        hexcolor = '#%04x%04x%04x' % rgb_tuple
        # that's it! '%02x' means zero-padded, 2-digit hex values
        return hexcolor
    
    def HTMLColorToRGB(self, colorstring):
        """ convert #RRGGBB to an (R, G, B) tuple """
        colorstring = colorstring.strip()
        if colorstring[0] == '#': colorstring = colorstring[1:]
        if len(colorstring) != 6:
            raise ValueError, "input #%s is not in #RRGGBB format" % colorstring
        r, g, b = colorstring[:2], colorstring[2:4], colorstring[4:]
        r, g, b = [int(n, 16) for n in (r, g, b)]
        return (r, g, b)
    
    def setColor2Text(self, event, sEntry):
        #print event
        Color = event.get_color()
        eColor = self.getWidget(sEntry)
        eColor.set_text(self.RGBToHTMLColor((Color.red, Color.green, Color.blue)))
        
