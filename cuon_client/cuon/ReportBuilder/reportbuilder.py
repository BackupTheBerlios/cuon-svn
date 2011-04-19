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
from types import *
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

from cuon.Windows.chooseWindows  import chooseWindows
class reportbuilderwindow(chooseWindows):

    
    def __init__(self, dicFilename = None):

        chooseWindows.__init__(self)
        
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
           
        self.drawReportHeader = {}
        self.drawPageHeader = {}
        self.drawGroup = {}
        self.drawPageFooter = {}
        self.drawReportFooter = {}
        
        fname = '../usr/share/cuon/glade/reportbuilder.glade2'
        try:
            self.xml = gtk.Builder()
            self.xml.add_from_file(fname)
        except Exception, params:
            print Exception, params
            
        
            
        try:
            self.xml.connect_signals(self)
        except Exception, params:
            print Exception, params
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
            
            
        cyReportHeaderNode = self.getNode(cyRootNode, 'reportHeader')
        print 'node = ',  cyReportHeaderNode[0].toxml()
        cyReportHeaderEntries = self.getNodes(cyReportHeaderNode[0], 'entry')
       
        
        if cyReportHeaderEntries:
            self.dicPage['RheaderX1'] =  int(self.getEntrySpecification(cyReportHeaderNode[0],'posX1'))
            self.dicPage['RheaderX2'] =  int(self.getEntrySpecification(cyReportHeaderNode[0],'posX2'))
            self.dicPage['RheaderY1'] =  int(self.getEntrySpecification(cyReportHeaderNode[0],'posY1'))
            self.dicPage['RheaderY2'] =  int(self.getEntrySpecification(cyReportHeaderNode[0],'posY2'))
            width = self.dicPage['RheaderX2'] - self.dicPage['RheaderX1'] 
            height = self.dicPage['RheaderY2'] - self.dicPage['RheaderY1']
            
            self.reportHeaderDA = drawingReport.drawingReport()
            self.reportHeaderDA.createDA( self.getWidget('scReportHeader'), self.getWidget('vpReportHeader'), self.getWidget('daReportHeader'), width,  height)
            for i in cyReportHeaderEntries:
                
                #print i.toxml()
                self.reportHeaderDA.drawObjects.append(self.getXmlEntry(i))
                #print 'dicEntry = ',  dicEntry
          
          
        cyReportPageHeaderNode = self.getNode(cyRootNode, 'pageHeader')
        cyPageHeaderEntries = self.getNodes(cyReportPageHeaderNode[0], 'entry')
        if cyPageHeaderEntries:
            self.dicPage['PheaderX1'] =  int(self.getEntrySpecification(cyReportPageHeaderNode[0],'posX1'))
            self.dicPage['PheaderX2'] =  int(self.getEntrySpecification(cyReportPageHeaderNode[0],'posX2'))
            self.dicPage['PheaderY1'] =  int(self.getEntrySpecification(cyReportPageHeaderNode[0],'posY1'))
            self.dicPage['PheaderY2'] =  int(self.getEntrySpecification(cyReportPageHeaderNode[0],'posY2'))
            width = self.dicPage['PheaderX2'] - self.dicPage['PheaderX1'] 
            height = self.dicPage['PheaderY2'] - self.dicPage['PheaderY1']
            
            self.PageHeaderDA = drawingReport.drawingReport()
            self.PageHeaderDA.createDA( self.getWidget('scPageHeader'), self.getWidget('vpPageHeader'), self.getWidget('daPageHeader'), width,  height)
            for i in cyPageHeaderEntries:
                
                #print i.toxml()
                self.PageHeaderDA.drawObjects.append(self.getXmlEntry(i))
                #print 'dicEntry = ',  dicEntry
        cyGroupNode = self.getNode(cyRootNode, 'groups')
        
        cyReportPageFooterNode = self.getNode(cyRootNode, 'pageFooter')
         
        cyReportFooterNode = self.getNode(cyRootNode, 'reportFooter')
        
         
         
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
            
        dicEntry['x1'] =  int(self.getEntrySpecification(cyNode,'posX1'))
        dicEntry['x2'] =  int(self.getEntrySpecification(cyNode,'posX2'))
        dicEntry['y1'] =  int(self.getEntrySpecification(cyNode,'posY1'))
        dicEntry['y2'] =  int(self.getEntrySpecification(cyNode,'posY2'))
        
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
            
            
        self.dicPage['orientation'] =  self.getEntrySpecification(cyRootNode[0],'papersizeX').encode('ascii')
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
   
