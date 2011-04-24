# -*- coding: utf-8 -*-

##Copyright (C) [2005]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 

import sys
import os
import os.path
import types
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import gobject


import string

import logging

import cPickle
#import cuon.OpenOffice.letter
# localisation
import locale, gettext
locale.setlocale (locale.LC_NUMERIC, '')
import threading
import datetime as DateTime
import drawingReport
import cuon.Misc.cuon_dialog

from modifyEntry import modifyEntryWindow

class reportbuilderwindow(modifyEntryWindow):

    
    def __init__(self, dicFilename = None):

        
        modifyEntryWindow.__init__(self)
        self.dicPage = {}
        self.dicText = {}
        # self.setLogLevel(self.INFO)
       
        self.dicText['class'] = 'Label'
        self.dicText['text'] = 'NoTitle'
        self.dicText['x1'] = 0
        self.dicText['x1'] = 0
        self.dicText['y1'] = 0
        self.dicText['x2'] = 0
        self.dicText['y2'] = 0
        self.dicText['font'] = 'courier'
        self.dicText['fontsize'] = 12
        self.dicText['kursiv'] = 'no'
        self.dicText['bold'] = 'no'
        self.dicText['underline'] = 'no'
        self.dicText['subscript'] = 'no'
        self.dicText['fontjustification'] = 'left'
        self.dicText['yOffSet'] = 20
        self.dicText['Papersize'] = self.pagesizes['A4']
        self.dicText['Papersize_Width'], self.dicText['Papersize_Height'] = self.dicText['Papersize']
        
        self.dicText['Orientation'] = 'Portrait' #  'Landscape' # 'Portrait'
        
        self.dicPage['ReportFootAppendToGroup']  = 0 
        self.dicPage['PageFootAppendToGroup']  = 0 
        
        self.dicText['TopMargin'] = 30
        self.activeRegion = 1
        self.activeGroup = 0
        
        self.drawReportHeader = {}
        self.drawPageHeader = {}
        self.drawGroup = {}
        self.drawPageFooter = {}
        self.drawReportFooter = {}
        self.reportHeaderDA = None
        self.PageHeaderDA = None
        self.reportGroupsDA = []
        self.PageFooterDA = None
        self.reportFooterDA = None
        
        
        daR = self.getWidget('daReportHeader')
        daR.set_events(gtk.gdk.EXPOSURE_MASK | gtk.gdk.LEAVE_NOTIFY_MASK | gtk.gdk.BUTTON_PRESS_MASK | gtk.gdk.POINTER_MOTION_MASK  | gtk.gdk.POINTER_MOTION_HINT_MASK)
      
        daR = self.getWidget('daPageHeader')
        daR.set_events(gtk.gdk.EXPOSURE_MASK | gtk.gdk.LEAVE_NOTIFY_MASK | gtk.gdk.BUTTON_PRESS_MASK | gtk.gdk.POINTER_MOTION_MASK  | gtk.gdk.POINTER_MOTION_HINT_MASK)
        
        daR = self.getWidget('daGroups')
        daR.set_events(gtk.gdk.EXPOSURE_MASK | gtk.gdk.LEAVE_NOTIFY_MASK | gtk.gdk.BUTTON_PRESS_MASK | gtk.gdk.POINTER_MOTION_MASK  | gtk.gdk.POINTER_MOTION_HINT_MASK)
        
        daR = self.getWidget('daPageFooter')
        daR.set_events(gtk.gdk.EXPOSURE_MASK | gtk.gdk.LEAVE_NOTIFY_MASK | gtk.gdk.BUTTON_PRESS_MASK | gtk.gdk.POINTER_MOTION_MASK  | gtk.gdk.POINTER_MOTION_HINT_MASK)
        
        daR = self.getWidget('daReportFooter')
        daR.set_events(gtk.gdk.EXPOSURE_MASK | gtk.gdk.LEAVE_NOTIFY_MASK | gtk.gdk.BUTTON_PRESS_MASK | gtk.gdk.POINTER_MOTION_MASK  | gtk.gdk.POINTER_MOTION_HINT_MASK)
      
        
 
        #self.loadGlade('reportbuilder.xml')
        
        self.win1 = self.getWidget('reportbuildermainwindow')
        self.win1.show()
        
        #self.setStatusBar()
       
        print 'dicFilename at reportbuilder',  dicFilename
        if dicFilename:
            self.dicCurrentFilename = dicFilename
            self.readReportDocument(dicFilename)
        else:
            self.dicCurrentFilename = {'TYPE':'FILE','NAME':'./new.txt'}
       
        
    # menu File
    def on_save_activate(self, event):
        print 'save clicked'
        self.saveFile()
    
    
    #Events
    
    # Report Header
    
    
    
    def on_daReportHeader_button_press_event(self,  oWidget,  data):
      
        print 'mouse button = ',  oWidget , data,  data.x,  data.y
        self.activateClick("rRHactive", "clicked")
        if data.button == 3:
            liEntries = self.reportHeaderDA.getEntryAtPosition(data.x,  data.y)
            for dicEntry in liEntries:
                print 'Entry at mousepointer: ',  dicEntry['eName']
            if liEntries:
                self.modifyEntry(liEntries[0])
     
    
        
    def on_daReportHeader_key_press_event(self, oWidget,  data ):
        print 'key = ',  oWidget,  data
     
        
        
    # Page Header
    
    
    
    def on_daPageHeader_button_press_event(self,  oWidget,  data):
      
        print 'mouse button = ',  oWidget , data,  data.x,  data.y
        self.activateClick("rPHactive", "clicked")
        if data.button == 3:
            liEntries = self.PageHeaderDA.getEntryAtPosition(data.x,  data.y)
            for dicEntry in liEntries:
                print 'Entry at mousepointer: ',  dicEntry['eName']
            if liEntries:
                self.modifyEntry(liEntries[0])
     
    
        
    def on_daPageHeader_key_press_event(self, oWidget,  data ):
        print 'key = ',  oWidget,  data
     
     # Report Groups
    
    
    
    def on_daGroups_button_press_event(self,  oWidget,  data):
      
        print 'mouse button = ',  oWidget , data,  data.x,  data.y
        self.activateClick("rGactive", "clicked")
        if data.button == 3:
            liEntries = self.reportGroupsDA[0].getEntryAtPosition(data.x,  data.y)
            for dicEntry in liEntries:
                print 'Entry at mousepointer: ',  dicEntry['eName']
            if liEntries:
                self.modifyEntry(liEntries[0])
     
    
        
    def on_daGroups_key_press_event(self, oWidget,  data ):
        print 'key = ',  oWidget,  data
     
     # Page Footer
    
    
    
    def on_daPageFooter_button_press_event(self,  oWidget,  data):
      
        print 'mouse button = ',  oWidget , data,  data.x,  data.y
        self.activateClick("rPFactive", "clicked")
        if data.button == 3:
            liEntries = self.PageFooterDA.getEntryAtPosition(data.x,  data.y)
            for dicEntry in liEntries:
                print 'Entry at mousepointer: ',  dicEntry['eName']
            if liEntries:
                #print liEntries,  len(liEntries)
                if len(liEntries)> 1:
                    sText = 'Choose: \n'
                    for l in range(0, len(liEntries)):
                        sText += `l` + "  "  + liEntries[l]['eName'] + "\n"
                        
                    cd = cuon.Misc.cuon_dialog.cuon_dialog()
                    ok, res = cd.inputLine(  'choose',  sText)
                    print 'ok = ',  ok, 'Res = ',  res
                    if ok and res:   
                        try:
                            self.modifyEntry(liEntries[int(res)])
                        except:
                            pass
                            
                        
                        
                else:
                    self.modifyEntry(liEntries[0])
     
    
        
    def on_daPageFooter_key_press_event(self, oWidget,  data ):
        print 'key = ',  oWidget,  data
     
     # Report Footer
    
    
    
    def on_daReportFooter_button_press_event(self,  oWidget,  data):
      
        print 'mouse button = ',  oWidget , data,  data.x,  data.y
        self.activateClick("rRFactive", "clicked")
        if data.button == 3:
            liEntries = self.reportFooterDA.getEntryAtPosition(data.x,  data.y)
            for dicEntry in liEntries:
                print 'Entry at mousepointer: ',  dicEntry['eName']
            if liEntries:
                self.modifyEntry(liEntries[0])
     
    
        
    def on_daReportFooter_key_press_event(self, oWidget,  data ):
        print 'key = ',  oWidget,  data
     
     
     
     
    # toggle report part
    
    def on_rAll_toggled(self, event):
        print 'radiobutton toggled'
        liButtons = ['rRHactive', 'rPHactive','rGactive','rPFactive','rRFactive']
        for l in range (len(liButtons)):
            rAll = self.getWidget(liButtons[l])
            if rAll.get_active():
                self.activeRegion = l+1
                print 'active = ',  self.activeRegion
            
    # functions
    
    def modifyEntry(self, dicEntry):
        self.ModifyEntryShow(dicEntry)
      
    def on_bRefresh_clicked(self, event):
        print 'bRefresh clicked'
        
        
    def on_tbSave_clicked(self, event):
        self.activateClick('save')
        self.saveFile()
     
    def replaceEntry(self,  dicEntry):
        
        print 'active Region = ',  self.activeRegion
        da = None
        if self.activeRegion == 1:
            da = self.reportHeaderDA
        elif self.activeRegion == 2:
            da = self.PageHeaderDA
        elif self.activeRegion == 3:
            da = self.reportGroupsDA[self.activeGroup]
        elif self.activeRegion == 4:
            da = self.PageFooterDA
        elif self.activeRegion == 5:
            da = self.reportFooterDA              
            
        da.replaceEntryByName(dicEntry)
        
        
    def saveFile(self):    
        liEntry,  liReport = self.reportValues.getEntries()
        
        # report header
        sDoc = "<report>\n"
        if liReport:
            
            sDoc = self.addList(sDoc,  liReport)
                    
        
        
        # page Header
        liEntry, liReport = self.reportHeaderDA.getEntries()
        if liReport:
            print liReport
            sDoc += "<reportHeader>\n"
            sDoc = self.addList(sDoc,  liReport)
        
        if liEntry:
            #print liEntry
            #print sDoc  
            sDoc = self.addList(sDoc,  liEntry, sEntry="entry")
            
                
            sDoc += "</reportHeader>\n"    
                
                
            #doc = self.dic2xml(doc, liEntry, "reportHeader")
            
            
         # page groups
        for k in self.reportGroupsDA:
            liEntry, liReport = k.getEntries()
            if liReport:
                print liReport
                sDoc += "<groups>\n"
                sDoc = self.addList(sDoc,  liReport)
        
            if liEntry:
                #print liEntry
                #print sDoc  
                sDoc += "<groupEntry>\n"
                sDoc += "<pageDetails>\n"
                sDoc = self.addList(sDoc,  liReport)
                
                sDoc = self.addList(sDoc,  liEntry, sEntry="entry")
                
                sDoc += "</pageDetails>\n"
                sDoc += "</groupEntry>\n"
            
                
            sDoc += "</groups>\n" 
            
         # page Footer
        liEntry, liReport = self.PageFooterDA.getEntries()
        if liReport:
            print liReport
            sDoc += "\n<pageFooter>\n"
            sDoc = self.addList(sDoc,  liReport)
        
        if liEntry:
            #print liEntry
            #print sDoc  
            sDoc = self.addList(sDoc,  liEntry, sEntry="entry")
            
                
            sDoc += "</pageFooter>\n"    
                
                
            #doc = self.dic2xml(doc, liEntry, "reportHeader")
            
            
        # report Footer
        liEntry, liReport = self.reportFooterDA.getEntries()
        if liReport:
            print liReport
            sDoc += "\n<reportFooter>\n"
            sDoc = self.addList(sDoc,  liReport)
        
        if liEntry:
            #print liEntry
            #print sDoc  
            sDoc = self.addList(sDoc,  liEntry, sEntry="entry")
            
                
            sDoc += "</reportFooter>\n"    
                
                
            #doc = self.dic2xml(doc, liEntry, "reportHeader")        
        sDoc += "</report> "
        print sDoc
        
    def addList(self, sDoc,  liReport,  sEntry=None):
        for i in liReport:
            if sEntry:
                sDoc += "\t<entry>\n"
            for key in i.keys():
                if sEntry:
                    sDoc += "\t"
                sDoc += "\t<" + key +">"
                sValue = i[key]
                sValue = self.checkXmlValue(sValue)
                sDoc += sValue
                sDoc += "</" + key +">\n"
            if sEntry:
                sDoc += "\t</entry>\n"
                
        return sDoc
        
    def checkXmlValue(self, sValue):
                            
        if not sValue:
            sValue = ""
        if isinstance(sValue, types.IntType):
            sValue = `sValue`
        elif isinstance(sValue, types.FloatType):
            sValue = `sValue`
        elif isinstance(sValue, types.DictType):
            if sValue.has_key('rColor'):
                sValue = `sValue['rColor']` + ', ' + `sValue['gColor']` + ', ' + `sValue['bColor']` 
        return sValue
        
        
    def readReportDocument(self, dicFilename):
        "Opens the file given in filename and reads it in"
        print 'dicFilename = ',  dicFilename 
        if dicFilename['TYPE'] == 'SSH':
            dicFilename['TMPNAME'] = 'tmp_editor_ssh_tab_GUI_0' 
            s1 = 'scp -P ' + dicFilename['PORT'] +  ' ' + dicFilename['USER'] + '@' + dicFilename['HOST'] + ':/' 
            s1 +=  dicFilename['NAME'] + ' ' + dicFilename['TMPNAME']
            print 's1 = ' ,  s1
            os.system(s1)
            filename = dicFilename['TMPNAME']
            
        else:
           
            filename = dicFilename['NAME']
           
        print 'filename to read xml',  filename   
        doc = self.readDocument(filename)
    
        print  `doc`
        cyRootNode = self.getRootNode(doc)
        
        self.setReportValues(cyRootNode)
            
        self.reportValues = drawingReport.drawingReport()  
       
        self.reportValues.setReportEntry({'topMargin':self.dicPage['topMargin']})
        self.reportValues.setReportEntry({'bottomMargin':self.dicPage['bottomMargin']})
        self.reportValues.setReportEntry({'rightMargin':self.dicPage['rightMargin']})
        self.reportValues.setReportEntry({'leftMargin':self.dicPage['leftMargin']})

        self.reportValues.setReportEntry({'papersizeX':self.dicPage['papersizeX']})
        self.reportValues.setReportEntry({'papersizeY':self.dicPage['papersizeY']})
        self.reportValues.setReportEntry({'orientation':self.dicPage['orientation']})

        if self.dicPage.has_key('SiteBackground_URL'):
            self.reportValues.setReportEntry({'SiteBackground_URL':self.dicPage['SiteBackground_URL']})
            self.reportValues.setReportEntry({'SiteBackgroundHeight':self.dicPage['SiteBackgroundHeight']})
            self.reportValues.setReportEntry({'SiteBackgroundWidth':self.dicPage['SiteBackgroundWidth']})
            self.reportValues.setReportEntry({'SiteBackgroundX':self.dicPage['SiteBackgroundX']})
            self.reportValues.setReportEntry({'SiteBackgroundY':self.dicPage['SiteBackgroundY']})
            
        if self.dicPage.has_key('SiteBackground_URL2'):
            self.reportValues.setReportEntry({'SiteBackground_URL2':self.dicPage['SiteBackground_URL2']})
            self.reportValues.setReportEntry({'SiteBackgroundHeight2':self.dicPage['SiteBackgroundHeight2']})
            self.reportValues.setReportEntry({'SiteBackgroundWidth2':self.dicPage['SiteBackgroundWidth2']})
            self.reportValues.setReportEntry({'SiteBackgroundX2':self.dicPage['SiteBackgroundX2']})
            self.reportValues.setReportEntry({'SiteBackgroundY2':self.dicPage['SiteBackgroundY2']})
        if self.dicPage.has_key('SiteBackground_URL3'):
            self.reportValues.setReportEntry({'SiteBackground_URL3':self.dicPage['SiteBackground_URL3']})
            self.reportValues.setReportEntry({'SiteBackgroundHeight3':self.dicPage['SiteBackgroundHeight3']})
            self.reportValues.setReportEntry({'SiteBackgroundWidth3':self.dicPage['SiteBackgroundWidth3']})
            self.reportValues.setReportEntry({'SiteBackgroundX3':self.dicPage['SiteBackgroundX3']})
            self.reportValues.setReportEntry({'SiteBackgroundY3':self.dicPage['SiteBackgroundY3']})

        cyReportHeaderNode = self.getNode(cyRootNode, 'reportHeader')
        #print 'node = ',  cyReportHeaderNode[0].toxml()
        
        cyReportHeaderEntries = self.getNodes(cyReportHeaderNode[0], 'entry')
        
        
        if cyReportHeaderEntries:
            
            width = self.dicPage['headerX2'] - self.dicPage['headerX1'] 
            height = self.dicPage['headerY2'] - self.dicPage['headerY1']
            
            self.reportHeaderDA = drawingReport.drawingReport()
            self.reportHeaderDA.createDA( self.getWidget('scReportHeader'), self.getWidget('vpReportHeader'), self.getWidget('daReportHeader'), width,  height)
            self.reportHeaderDA.setReportEntry({'posX1':self.dicPage['headerX1'] })
            self.reportHeaderDA.setReportEntry({'posX2':self.dicPage['headerX2'] })
            self.reportHeaderDA.setReportEntry({'posY1':self.dicPage['headerY1'] })
            self.reportHeaderDA.setReportEntry({'posY2':self.dicPage['headerY2'] })
            
            for i in cyReportHeaderEntries:
                
                #print i.toxml()
                self.reportHeaderDA.setEntry(self.getXmlEntry(i))
                #print 'dicEntry = ',  dicEntry
          
          
        cyReportPageHeaderNode = self.getNode(cyRootNode, 'pageHeader')
        cyPageHeaderEntries = self.getNodes(cyReportPageHeaderNode[0], 'entry')
        if cyPageHeaderEntries:
            
            width = self.dicPage['pageX2'] - self.dicPage['pageX1'] 
            height = self.dicPage['pageY2'] - self.dicPage['pageY1']
            
            self.PageHeaderDA = drawingReport.drawingReport()
            self.PageHeaderDA.createDA( self.getWidget('scPageHeader'), self.getWidget('vpPageHeader'), self.getWidget('daPageHeader'), width,  height)
            self.PageHeaderDA.setReportEntry({'posX1':self.dicPage['pageX1'] })
            self.PageHeaderDA.setReportEntry({'posX2':self.dicPage['pageX2'] })
            self.PageHeaderDA.setReportEntry({'posY1':self.dicPage['pageY1'] })
            self.PageHeaderDA.setReportEntry({'posY2':self.dicPage['pageY2'] })
            
            for i in cyPageHeaderEntries:
                
                #print i.toxml()
                self.PageHeaderDA.setEntry(self.getXmlEntry(i))
                #print 'dicEntry = ',  dicEntry
                
                
        cyReportGroupsNodes = self.getNode(cyRootNode, 'groups')
        
       
        
        if cyReportGroupsNodes:
            for k in range(len(cyReportGroupsNodes)):
                cyGroupsEntries = self.getNodes(cyReportGroupsNodes[k], 'entry')
                
    
    #            cyPageDetailsNodes = self.getNodes(cyGroupEntry, 'pageDetails')
    #            print'+++++++ cyPageDetailsNodes = ',    cyPageDetailsNodes
    #    
    #            for i in  range(len(cyPageDetailsNodes)):
                width = self.dicPage['0_detailsX2'] - self.dicPage['0_detailsX1'] 
                height = self.dicPage['0_detailsY2'] - self.dicPage['0_detailsY1']
                
                self.reportGroupsDA.append(drawingReport.drawingReport())
                self.reportGroupsDA[k].createDA( self.getWidget('scGroups'), self.getWidget('vpGroups'), self.getWidget('daGroups'), width,  height)
                self.reportGroupsDA[k].setReportEntry({'posX1':self.dicPage['0_detailsX1'] })
                self.reportGroupsDA[k].setReportEntry({'posX2':self.dicPage['0_detailsX2'] })
                self.reportGroupsDA[k].setReportEntry({'posY1':self.dicPage['0_detailsY1'] })
                self.reportGroupsDA[k].setReportEntry({'posY2':self.dicPage['0_detailsY2'] })
                
                #print cyGroupEntry.toxml()
                
                for i in cyGroupsEntries:
                    #print i.toxml()
                    self.reportGroupsDA[k].setEntry(self.getXmlEntry(i))
                    #print 'dicEntry = ',  dicEntry
          
        cyReportPageFooterNode = self.getNode(cyRootNode, 'pageFooter')
        cyPageFooterEntries = self.getNodes(cyReportPageFooterNode[0], 'entry')
        if cyPageFooterEntries:
            
            width = self.dicPage['pageFooterX2'] - self.dicPage['pageFooterX1'] 
            height = self.dicPage['pageFooterY2'] - self.dicPage['pageFooterY1']
            
            self.PageFooterDA = drawingReport.drawingReport()
            self.PageFooterDA.createDA( self.getWidget('scPageFooter'), self.getWidget('vpPageFooter'), self.getWidget('daPageFooter'), width,  height)
            self.PageFooterDA.setReportEntry({'posX1':self.dicPage['pageFooterX1'] })
            self.PageFooterDA.setReportEntry({'posX2':self.dicPage['pageFooterX2'] })
            self.PageFooterDA.setReportEntry({'posY1':self.dicPage['pageFooterY1'] })
            self.PageFooterDA.setReportEntry({'posY2':self.dicPage['pageFooterY2'] })
            
            for i in cyPageFooterEntries:
                
                #print i.toxml()
                self.PageFooterDA.setEntry(self.getXmlEntry(i))
                #print 'dicEntry = ',  dicEntry
        cyReportFooterNode = self.getNode(cyRootNode, 'reportFooter')
        
        cyReportFooterEntries = self.getNodes(cyReportFooterNode[0], 'entry')
       
        
        if cyReportFooterEntries:
            
            width = self.dicPage['footerX2'] - self.dicPage['footerX1'] 
            height = self.dicPage['footerY2'] - self.dicPage['footerY1']
            
            self.reportFooterDA = drawingReport.drawingReport()
            self.reportFooterDA.createDA( self.getWidget('scReportFooter'), self.getWidget('vpReportFooter'), self.getWidget('daReportFooter'), width,  height)
            self.reportFooterDA.setReportEntry({'posX1':self.dicPage['footerX1'] })
            self.reportFooterDA.setReportEntry({'posX2':self.dicPage['footerX2'] })
            self.reportFooterDA.setReportEntry({'posY1':self.dicPage['footerY1'] })
            self.reportFooterDA.setReportEntry({'posY2':self.dicPage['footerY2'] })

            for i in cyReportFooterEntries:
                
                #print i.toxml()
                self.reportFooterDA.setEntry(self.getXmlEntry(i))
                #print 'dicEntry = ',  dicEntry
           
         
    def getXmlEntry(self, cyNode):
        
        dicEntry = {}
        # set some defaults
        dicEntry['Property'] = '0'
        
        dicEntry['eName']  =  self.getEntrySpecification(cyNode,'name').encode('ascii')
        try:
            dicEntry['width'] =  int(self.getEntrySpecification(cyNode,'width'))
        except:
            dicEntry['width'] =  0
        try:
            dicEntry['height'] =  int(self.getEntrySpecification(cyNode,'height'))
        except:
            dicEntry['height'] =  0
            
        dicEntry['posX1'] =  int(self.getEntrySpecification(cyNode,'posX1'))
        dicEntry['posX2'] =  int(self.getEntrySpecification(cyNode,'posX2'))
        dicEntry['posY1'] =  int(self.getEntrySpecification(cyNode,'posY1'))
        dicEntry['posY2'] =  int(self.getEntrySpecification(cyNode,'posY2'))
        
        dicEntry['eType'] =  self.getEntrySpecification(cyNode,'type').encode('ascii')
        
        dicEntry['class'] =  self.getEntrySpecification(cyNode,'class').encode('ascii')
        dicEntry['value'] = self.getEntrySpecification(cyNode,'value')
        dicEntry['format'] = self.getEntrySpecification(cyNode,'format')
        if dicEntry['format']:
            dicEntry['format'] = dicEntry['format'].encode('ascii')

        dicEntry['formula'] = self.getEntrySpecification(cyNode,'formula')
        if dicEntry['formula']:
            dicEntry['formula'] = dicEntry['formula'].encode('utf-8')
        else:
            dicEntry['formula'] = None

        dicEntry['memory'] = self.getEntrySpecification(cyNode,'memory')
        if dicEntry['memory']:
            dicEntry['memory'] = dicEntry['memory'].encode('ascii')
        else:
            dicEntry['memory'] = None
            
        
        sResultSet =  self.getEntrySpecification(cyNode,'resultSet')
        if sResultSet:
            sResultSet = sResultSet.encode('ascii')
            dicEntry['resultSet'] = sResultSet
        else:
            dicEntry['resultSet'] = 'zero'

        sVariable =  self.getEntrySpecification(cyNode,'variable')
        if sVariable:
            sVariable = sVariable.encode('ascii')
            dicEntry['Variable'] = sVariable
        else:
            dicEntry['Variable'] = None 
            
        sFont = self.getEntrySpecification(cyNode,'font')
        liFont = sFont.split(';')
        
        dicEntry['font'] = liFont[0]
        if len(liFont)> 1:
            if liFont[1] == 'TTF':
                print liFont[0], type(liFont[0])
                print liFont[2], type(liFont[2])
                pdfmetrics.registerFont( TTFont( liFont[0].encode('ascii'),liFont[2].encode('ascii')))
                
        dicEntry['fontsize'] = int( self.getEntrySpecification(cyNode,'fontsize'))
        sColor = self.getEntrySpecification(cyNode,'foregroundColor').encode('ascii')
        #print sColor
        iFind = sColor.find(',')
        # print iFind
        rColor = float(sColor[0:iFind])
        iFind2 = sColor.find(',', iFind+1)
        gColor = float(sColor[iFind+1:iFind2])
        bColor = float(sColor[iFind2+1:len(sColor)])
        
        dicEntry['foregroundColor'] = {'rColor' : rColor, 'gColor' : gColor, 'bColor' : bColor}
        #print  dicEntry['foregroundColor']
        
        sColor = self.getEntrySpecification(cyNode,'backgroundColor').encode('ascii')
        #print sColor
        iFind = sColor.find(',')
        # print iFind
        rColor = float(sColor[0:iFind])
        iFind2 = sColor.find(',', iFind+1)
        gColor = float(sColor[iFind+1:iFind2])
        bColor = float(sColor[iFind2+1:len(sColor)])
        
        dicEntry['backgroundColor'] = {'rColor' : rColor, 'gColor' : gColor, 'bColor' : bColor}

        sGray = self.getEntrySpecification(cyNode,'grayScale')
        if sGray:
            dicEntry['grayScale'] = float(sGray.encode('ascii'))
        else:
            dicEntry['grayScale'] = 0.0
            
        fj = self.getEntrySpecification(cyNode,'fontJustification')
        if fj:
            fj = fj.encode('ascii')
            dicEntry['fontjustification'] = fj
        else:
            dicEntry['fontjustification'] = None

        dicEntry['Property'] =  self.getEntrySpecification(cyNode,'property')
                 
        
        return dicEntry
        
        
    def setReportValues(self, cyRootNode):

        # Papersizes
        
        self.dicPage['topMargin'] =  int(self.getEntrySpecification(cyRootNode[0],'topMargin'))
        self.dicPage['bottomMargin'] =  int(self.getEntrySpecification(cyRootNode[0],'bottomMargin'))
        self.dicPage['leftMargin'] =  int(self.getEntrySpecification(cyRootNode[0],'leftMargin'))
        self.dicPage['rightMargin'] =  int(self.getEntrySpecification(cyRootNode[0],'rightMargin'))
    
        sPapersize = 'A4'
        try:
            sPapersize =  self.getEntrySpecification(cyRootNode[0],'paperSize')
        except:
            sPapersize = 'A4'
        if sPapersize == 'A5':
            self.dicText['Papersize'] = self.pagesizes['A5']
        elif sPapersize == 'A6':
            self.dicText['Papersize'] = self.pagesizes['A6']
        else:
            self.dicText['Papersize'] = self.pagesizes['A4']
            
            
        self.dicPage['orientation'] =  self.getEntrySpecification(cyRootNode[0],'orientation').encode('ascii')
        if self.dicPage['orientation'] =='Portrait':
            self.dicPage['papersizeX'] =  int(self.getEntrySpecification(cyRootNode[0],'papersizeX'))
            self.dicPage['papersizeY'] =  int(self.getEntrySpecification(cyRootNode[0],'papersizeY'))
        elif self.dicPage['orientation'] =='Landscape':
            self.dicPage['papersizeX'] =  int(self.getEntrySpecification(cyRootNode[0],'papersizeY'))
            self.dicPage['papersizeY'] =  int(self.getEntrySpecification(cyRootNode[0],'papersizeX'))

        else:

            self.dicPage['papersizeX'] =  int(self.getEntrySpecification(cyRootNode[0],'papersizeX'))
            self.dicPage['papersizeY'] =  int(self.getEntrySpecification(cyRootNode[0],'papersizeY'))
   
        try:
            
            self.dicPage['SiteBackground_URL'] =  self.getEntrySpecification(cyRootNode[0],'sitebackground_url').encode('ascii')
            self.dicPage['SiteBackgroundX'] =  int(self.getEntrySpecification(cyRootNode[0],'sitebackground_x'))
            self.dicPage['SiteBackgroundY'] =  int(self.getEntrySpecification(cyRootNode[0],'sitebackground_y'))
            self.dicPage['SiteBackgroundWidth'] =  int(self.getEntrySpecification(cyRootNode[0],'sitebackground_width'))
            self.dicPage['SiteBackgroundHeight'] =  int(self.getEntrySpecification(cyRootNode[0],'sitebackground_height'))
            self.dicPage['PropertyBG'] =  self.getEntrySpecification(cyRootNode[0],'PropertyBG')
        except Exception, params:
            print Exception, params
            
        try:
            
            self.dicPage['SiteBackground_URL2'] =  self.getEntrySpecification(cyRootNode[0],'sitebackground_url2').encode('ascii')
            self.dicPage['SiteBackgroundX2'] =  int(self.getEntrySpecification(cyRootNode[0],'sitebackground_x2'))
            self.dicPage['SiteBackgroundY2'] =  int(self.getEntrySpecification(cyRootNode[0],'sitebackground_y2'))
            self.dicPage['SiteBackgroundWidth2'] =  int(self.getEntrySpecification(cyRootNode[0],'sitebackground_width2'))
            self.dicPage['SiteBackgroundHeight2'] =  int(self.getEntrySpecification(cyRootNode[0],'sitebackground_height2'))
            self.dicPage['PropertyBG2'] =  self.getEntrySpecification(cyRootNode[0],'PropertyBG2')
        except Exception, params:
            print Exception, params
        
        try:
            
            self.dicPage['SiteBackground_URL3'] =  self.getEntrySpecification(cyRootNode[0],'sitebackground_url3').encode('ascii')
            self.dicPage['SiteBackgroundX3'] =  int(self.getEntrySpecification(cyRootNode[0],'sitebackground_x3'))
            self.dicPage['SiteBackgroundY3'] =  int(self.getEntrySpecification(cyRootNode[0],'sitebackground_y3'))
            self.dicPage['SiteBackgroundWidth3'] =  int(self.getEntrySpecification(cyRootNode[0],'sitebackground_width3'))
            self.dicPage['SiteBackgroundHeight3'] =  int(self.getEntrySpecification(cyRootNode[0],'sitebackground_height3'))
            self.dicPage['PropertyBG3'] =  self.getEntrySpecification(cyRootNode[0],'PropertyBG3')
        except Exception, params:
            print Exception, params
            
            
            
        #
        # Report Header
        #
        cyReportHeaderNode = self.getNode(cyRootNode, 'reportHeader')
        #print '------------------'
        #print cyReportHeaderNode
        #print cyReportHeaderNode[0].toxml()
        

        cyReportHeaderEntries = self.getNodes(cyReportHeaderNode[0], 'entry')
        #print '+++++++'
        #print cyReportHeaderEntries
        liRecord = []
        self.dicPage['headerX1'] =  int(self.getEntrySpecification(cyReportHeaderNode[0],'posX1'))
        self.dicPage['headerX2'] =  int(self.getEntrySpecification(cyReportHeaderNode[0],'posX2'))
        self.dicPage['headerY1'] =  int(self.getEntrySpecification(cyReportHeaderNode[0],'posY1'))
        self.dicPage['headerY2'] =  int(self.getEntrySpecification(cyReportHeaderNode[0],'posY2'))

        self.dicPage['beginReportHeaderX'] = self.dicPage['leftMargin'] + self.dicPage['headerX1']
        self.dicPage['endReportHeaderX'] =  self.dicPage['headerX2']
        
        self.dicPage['beginReportHeaderY'] = self.dicPage['papersizeY'] - self.dicPage['topMargin'] - self.dicPage['headerY1']
        self.dicPage['endReportHeaderY'] = self.dicPage['papersizeY'] - self.dicPage['topMargin'] - self.dicPage['headerY2']


        self.dicPage['beginReportFooterX'] = self.dicPage['leftMargin'] 
        self.dicPage['endReportFooterX'] =  self.dicPage['papersizeX'] -  self.dicPage['rightMargin']
        
        self.dicPage['beginReportFooterY'] =   self.dicPage['bottomMargin'] 
        self.dicPage['endReportFooterY'] = self.dicPage['bottomMargin'] 

        #
        # PageHeader
        #
        cyReportPageNode = self.getNode(cyRootNode, 'pageHeader')
        #print '------------------'
        #print cyReportPageNode
        #print cyReportPageNode[0].toxml()
        

        cyReportPageEntries = self.getNodes(cyReportPageNode[0], 'entry')
        #print '+++++++'
        #print cyReportPageEntries
        liRecord = []
        self.dicPage['pageX1'] =  int(self.getEntrySpecification(cyReportPageNode[0],'posX1'))
        self.dicPage['pageX2'] =  int(self.getEntrySpecification(cyReportPageNode[0],'posX2'))
        self.dicPage['pageY1'] =  int(self.getEntrySpecification(cyReportPageNode[0],'posY1'))
        self.dicPage['pageY2'] =  int(self.getEntrySpecification(cyReportPageNode[0],'posY2'))


        self.dicPage['beginPageHeaderX'] =  self.dicPage['leftMargin'] +  self.dicPage['pageX1']
        self.dicPage['endPageHeaderX'] =   self.dicPage['pageX2']
        self.dicPage['beginPageHeaderY'] =  self.dicPage['endReportHeaderY'] - self.dicPage['pageY1']
        self.dicPage['endPageHeaderY'] =  self.dicPage['endReportHeaderY'] - self.dicPage['pageY2']
        
       
        #
        # Report-footer
        #

        cyReportFooterNode = self.getNode(cyRootNode, 'reportFooter')
        #print '------------------'
        #print cyReportFooterNode
        #print cyReportFooterNode[0].toxml()
        

        cyReportFooterEntries = self.getNodes(cyReportFooterNode[0], 'entry')
        #print '+++++++'
        #print cyReportFooterEntries
        liRecord = []
       
        self.dicPage['footerX1'] =  int(self.getEntrySpecification(cyReportFooterNode[0],'posX1'))
        self.dicPage['footerX2'] =  int(self.getEntrySpecification(cyReportFooterNode[0],'posX2'))
        self.dicPage['footerY1'] =  int(self.getEntrySpecification(cyReportFooterNode[0],'posY1'))
        self.dicPage['footerY2'] =  int(self.getEntrySpecification(cyReportFooterNode[0],'posY2'))
        try:
            self.dicPage['ReportFootAppendToGroup'] =  int(self.getEntrySpecification(cyReportFooterNode[0],'appendtogroup'))
        except:
            self.dicPage['ReportFootAppendToGroup'] = 0
            
        self.dicPage['beginReportFooterX'] = self.dicPage['leftMargin'] + self.dicPage['footerX1']
        self.dicPage['endReportFooterX'] =  self.dicPage['footerX2']
        
        self.dicPage['beginReportFooterY'] =  self.dicPage['bottomMargin'] + self.dicPage['footerY1']
        self.dicPage['endReportFooterY'] = self.dicPage['bottomMargin'] + self.dicPage['footerY2']
        


        #
        # Page -footer
        #

        cyReportPageNode = self.getNode(cyRootNode, 'pageFooter')
        
        #print '------------------'
        #print cyReportPageNode
        #print cyReportPageNode[0].toxml()
        

        cyReportPageEntries = self.getNodes(cyReportPageNode[0], 'entry')
        #print '+++++++'
        #print cyReportPageEntries
        liRecord = []
        self.dicPage['pageFooterX1'] =  int(self.getEntrySpecification(cyReportPageNode[0],'posX1'))
        self.dicPage['pageFooterX2'] =  int(self.getEntrySpecification(cyReportPageNode[0],'posX2'))
        self.dicPage['pageFooterY1'] =  int(self.getEntrySpecification(cyReportPageNode[0],'posY1'))
        self.dicPage['pageFooterY2'] =  int(self.getEntrySpecification(cyReportPageNode[0],'posY2'))

        try:
            self.dicPage['PageFootAppendToGroup']  = int(self.getEntrySpecification(cyReportPageNode[0],'appendtogroup'))
        except:
            self.dicPage['PageFootAppendToGroup']  = 0
            
        self.dicPage['beginPageFooterX'] =  self.dicPage['leftMargin'] +  self.dicPage['pageFooterX1']
        self.dicPage['endPageFooterX'] =   self.dicPage['pageFooterX2']
        self.dicPage['beginPageFooterY'] =  self.dicPage['pageFooterY2'] + self.dicPage['bottomMargin'] + self.dicPage['pageFooterY1']
        self.dicPage['beginPageFooterY_LastPage'] =  self.dicPage['endReportFooterY'] + self.dicPage['pageFooterY2']
        self.dicPage['endPageFooterY'] = self.dicPage['bottomMargin']  + self.dicPage['pageFooterY1']

        self.dicPage['PrintRangeFirstSite'] = self.dicPage['papersizeY'] - self.dicPage['topMargin'] - self.dicPage['bottomMargin']  -self.dicPage['headerY1'] - self.dicPage['headerY2']  - self.dicPage['pageY1']  - self.dicPage['pageY2'] - self.dicPage['pageFooterY1']  - self.dicPage['pageFooterY2'] 
        self.dicPage['PrintRangeNextSites'] = self.dicPage['papersizeY'] - self.dicPage['topMargin'] - self.dicPage['bottomMargin']  - self.dicPage['pageY1']  - self.dicPage['pageY2'] - self.dicPage['pageFooterY1']  - self.dicPage['pageFooterY2'] 
        

        self.dicPage['beginPageHeaderOtherSitesY'] = self.dicPage['papersizeY'] - self.dicPage['topMargin']  - self.dicPage['pageY1'] 
        self.dicPage['endPageHeaderOtherSitesY'] =   self.dicPage['papersizeY'] - self.dicPage['topMargin']  - self.dicPage['pageY2']


        #
        # calculate Sides
        #

        print "Side Values = ",  self.dicPage['papersizeY'] , self.dicPage['topMargin'] ,  self.dicPage['headerY2'] ,  self.dicPage['endPageFooterY'] ,  self.dicPage['bottomMargin']  , self.dicPage['pageFooterY1']
        self.dicPage['reportDetailsY'] = self.dicPage['papersizeY'] - self.dicPage['topMargin'] - self.dicPage['headerY2'] - self.dicPage['bottomMargin']  - self.dicPage['pageFooterY2']
        
        
        
        
        
        #print "appendtogroup page,  report = ",  self.dicPage['PageFootAppendToGroup']  ,  self.dicPage['ReportFootAppendToGroup'] 
        
        cyGroupNode = self.getNode(cyRootNode, 'groups')
        cyGroupEntries = self.getNodes(cyGroupNode[0], 'groupEntry')
            #print cyGroupEntries

        for k in range(len(cyGroupEntries)):
            cyGroupEntry = cyGroupEntries[k]
            self.dicPage[`k` + 'ChangeGroupBy'] = self.getEntrySpecification(cyGroupEntry,'changeGroupBy')
            self.dicPage[`k` + 'groupNumber'] = int(self.getEntrySpecification(cyGroupEntry,'number'))

    
            cyPageDetailsNodes = self.getNodes(cyGroupEntry, 'pageDetails')
            print'+++++++ cyPageDetailsNodes = ',    cyPageDetailsNodes
    
            for i in  range(len(cyPageDetailsNodes)):
                cyReportDetailsNode = cyPageDetailsNodes[i]
                cyReportDetailsEntries = self.getNodes(cyReportDetailsNode, 'entry')
    
                self.dicPage[`i` + '_detailsX1'] =  int(self.getEntrySpecification(cyReportDetailsNode,'posX1'))
                self.dicPage[`i` + '_detailsX2'] =  int(self.getEntrySpecification(cyReportDetailsNode,'posX2'))
                self.dicPage[`i` + '_detailsY1'] =  int(self.getEntrySpecification(cyReportDetailsNode,'posY1'))
                self.dicPage[`i` + '_detailsY2'] =  int(self.getEntrySpecification(cyReportDetailsNode,'posY2'))
                self.dicPage[`i` + '_lineY'] =  int(self.getEntrySpecification(cyReportDetailsNode,'lineY'))


  
