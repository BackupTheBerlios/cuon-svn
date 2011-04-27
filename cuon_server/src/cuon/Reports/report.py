# -*- coding: utf-8 -*-
##Copyright (C) [2003-2004]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either verion 3 of the License, or (at your option) any later version.
##published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 


from reportlab.pdfgen import canvas
from reportlab.lib import pagesizes
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


from MyXML import MyXML
import copy
import cPickle
import os,  sys
import os.path
import string
import math
import re





class report(MyXML):
    def __init__(self):
        MyXML.__init__(self)

        print 'CUON report starts'
     
        self.pdfDoc = None
        self.pdfStory = None
        self.pdfStyles = getSampleStyleSheet()
        self.pdfStyle = None
        
        
        self.dicReportData = {}
        
        self.dicReportValues = {}
        self.dicReportFields = {}
        self.firstPage = True ;
        self.lastPage = False 
        self.beginPageX = 50
        self.beginPageY = 800
        self.lineOffset = 0
        self.dicPage = {}
        self.dicText = {}

        
        # set
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
        self.dicText['Papersize'] = pagesizes.A4
        self.dicText['Papersize_Width'], self.dicText['Papersize_Height'] = self.dicText['Papersize']
        
        self.dicText['Orientation'] = 'Portrait' #  'Landscape' # 'Portrait'
        
        self.dicPage['ReportFootAppendToGroup']  = 0 
        self.dicPage['PageFootAppendToGroup']  = 0 
        
        self.dicText['TopMargin'] = 30
        

        self.liTitle = [] 
        self.liHeader = []
        self.dicGroups = {}
        
        self.dicHeaderlist = {}
        self.dicHeaderInfo = {}
        dicPageInfo = {'x1': self.beginPageX + 400, 'x2': self.beginPageX + 480, 'y1': self.beginPageY , 'y2': self.beginPageY }
        self.dicHeaderInfo['pageinfo'] = dicPageInfo
        dicDateInfo = {'x1': self.beginPageX + 400 , 'x2': self.beginPageX + 480 , 'y1': self.beginPageY - 20, 'y2': self.beginPageY - 20}
        self.dicHeaderInfo['dateinfo'] = dicDateInfo

        self.numberOfPage = 1
        self.pdfFile = 'noname.pdf'
        self.dicResults = {}
        self.dicVariable = {}
        self.dicResult = {}
        self.endOfRegion = 0
        self.dicMemory = {}
        
        
        
    def start(self, *reportdata):
        # values in this order:
        # 1 reportname
        # 2 dicUser
        # 3 dicResults
        # 4 dicReportData
        # 5 reportDefs
        
        print len(reportdata)
        #print reportdata
        reportdata = reportdata[0][0]
        for i in range(len(reportdata)):
            #print i,'##################################'
            #print reportdata[i]
            pass
        reportname = reportdata[0]
        dicUser = reportdata[1]
        self.dicResults = reportdata[2]
        self.dicReportData = reportdata[3]
        self.reportDefs = reportdata[4]
        # set empty Value 
        self.dicMemory = {}
        self.endOfRegion = 0
        self.pdfFile = self.reportDefs['pdfFile']
        
        self.setDicUser(dicUser)
        return self.loadXmlReport(reportname)
        

    def out(self, s):
        pass
        
    def setDicUser(self, dicUser):
        self.dicUser = dicUser
        self.dicUser['Debug'] = 'NO'

        
    def loadXmlReportFile(self, sFile):
        print 'load = ',  sFile
        if sFile:
            dirNorm = os.path.dirname(sFile)
            sDirFile = os.path.basename(sFile)
            dirClient = dirNorm[0:len(dirNorm) -4] + '/client_' + `self.dicUser['client']` + '/' + sDirFile
            dirUser = dirNorm[0:len(dirNorm) -4] + '/user_' + self.dicUser['Name'] + '/' + sDirFile
                
            #print 'Pathes for dir'
            #print dirNorm
            #print dirClient
            #print dirUser
            
            
            if os.path.exists(dirUser):
                sFileName = dirUser
            elif os.path.exists(dirClient):
                sFileName = dirClient
            else:
                sFileName = sFile
                
            try:
                print 'report loaded = ', sFileName

                doc = self.readDocument(sFileName)
            except:
                print 'no valid doc found'
                doc = None
            return doc

    def loadXmlReport(self, sFile):
        
        doc = self.loadXmlReportFile(sFile)
    
        #print  `doc`
        cyRootNode = self.getRootNode(doc)

        #self.out( cyRootNode[0].toxml())
        #print  cyRootNode[0].toxml()

      

        self.setReportValues(cyRootNode)


        return self.createPdf(cyRootNode)

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
            self.dicText['Papersize'] = pagesizes.A5
        elif sPapersize == 'A6':
            self.dicText['Papersize'] = pagesizes.A6
        else:
            self.dicText['Papersize'] = pagesizes.A4
            
            
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
            
        print 'dicPage = ',  self.dicPage
            
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
        
        
        
    def getReportHeader(self, cyRootNode):

        cyReportHeaderNode = self.getNode(cyRootNode, 'reportHeader')
        #print '------------------'
        #print cyReportHeaderNode
        #print cyReportHeaderNode[0].toxml()
        

        cyReportHeaderEntries = self.getNodes(cyReportHeaderNode[0], 'entry')
        #print '+++++++'
        #print cyReportHeaderEntries
        liRecord = []
        liResults = []

        resultKey =  self.getEntrySpecification(cyReportHeaderNode[0],'resultSet')
        if resultKey and self.dicResults.has_key(resultKey):
            liResults = self.dicResults[resultKey.encode('ascii')]
            if liResults:
                self.dicResult = liResults[0]
            
   
        for i in range(len(cyReportHeaderEntries)):
            dicEntry = self.getXmlEntry(cyReportHeaderEntries[i])
            if dicEntry['resultSet'] != 'zero':
                resultKey =  dicEntry['resultSet']
                if resultKey and self.dicResults.has_key(resultKey):
                    liResults = self.dicResults[resultKey.encode('ascii')]
                    if liResults:
                        self.dicResult = liResults[0]

                        
            dicRow = self.getReportEntry(cyReportHeaderEntries[i])
            #dicRow = self. getReportRow(dicEntry) 
     
            #dicRow['text'] = dicEntry['text']
            dicRow['x1'] = self.dicPage['beginReportHeaderX'] + dicRow['x1']
            dicRow['y1'] = self.dicPage['beginReportHeaderY']  - dicRow['y1']
            liRecord = self.checkProperty(liRecord, dicRow)
            
            

        return liRecord

    def getPageHeader(self, cyRootNode):

        cyReportPageNode = self.getNode(cyRootNode, 'pageHeader')
        #print '------------------'
        #print cyReportPageNode
        #print cyReportPageNode[0].toxml()
        

        cyReportPageEntries = self.getNodes(cyReportPageNode[0], 'entry')
        #print '+++++++'
        #print cyReportPageEntries
        liRecord = []
        liResults = []
        resultKey =  self.getEntrySpecification(cyReportPageNode[0],'resultSet')
        if resultKey and self.dicResults.has_key(resultKey):
            liResults = self.dicResults[resultKey.encode('ascii')]
            self.dicResult = liResults[0]
            
        for i in range(len(cyReportPageEntries)):
            dicRow = self.getReportEntry(cyReportPageEntries[i])

            #dicRow = self. getReportRow(dicEntry) 
     
            #dicRow['text'] = dicEntry['text']
  
            if self.firstPage:
                dicRow['x1'] = self.dicPage['beginPageHeaderX']  + dicRow['x1']
                dicRow['y1'] = self.dicPage['beginPageHeaderY']  - dicRow['y1']
                dicRow['x2'] = self.dicPage['beginPageHeaderX']  + dicRow['x2']
                dicRow['y2'] = self.dicPage['beginPageHeaderY']  - dicRow['y2']

            else:
                dicRow['x1'] = self.dicPage['beginPageHeaderX']  + dicRow['x1']
                dicRow['y1'] = self.dicPage['beginPageHeaderOtherSitesY']  - dicRow['y1']
                dicRow['x2'] = self.dicPage['beginPageHeaderX']  + dicRow['x2']
                dicRow['y2'] = self.dicPage['beginPageHeaderOtherSitesY']  - dicRow['y2']
            liRecord = self.checkProperty(liRecord, dicRow)

        return liRecord


    def getPageFooter(self, cyRootNode,  x1,  y1,  x2,  y2):

        cyReportPageNode = self.getNode(cyRootNode, 'pageFooter')
        #print '------------------'
        #print cyReportPageNode
        #print cyReportPageNode[0].toxml()
        

        cyReportPageEntries = self.getNodes(cyReportPageNode[0], 'entry')
        #print '+++++++'
        #print cyReportPageEntries
        liRecord = []
        dicRow = {'x1':x1, 'x2':x2,'y1':y1,'y2':y2}
        
        for i in range(len(cyReportPageEntries)):
            dicRow = self.getReportEntry(cyReportPageEntries[i])

            #dicRow = self. getReportRow(dicEntry) 
            
            #dicRow['text'] = dicEntry['text']
            # page footer to the end of the site
            if self.dicPage['PageFootAppendToGroup'] == 0:
                if self.lastPage:
                    dicRow['x1'] = self.dicPage['beginPageFooterX']  + dicRow['x1']
                    dicRow['y1'] = self.dicPage['beginPageFooterY']  - dicRow['y1']
                    dicRow['x2'] = self.dicPage['beginPageFooterX']  + dicRow['x2']
                    dicRow['y2'] = self.dicPage['beginPageFooterY']  - dicRow['y2']
    
                else:
                
                    dicRow['x1'] = self.dicPage['beginPageFooterX']  + dicRow['x1']
                    dicRow['y1'] = self.dicPage['beginPageFooterY']  - dicRow['y1']
                    dicRow['x2'] = self.dicPage['beginPageFooterX']  + dicRow['x2']
                    dicRow['y2'] = self.dicPage['beginPageFooterY']  - dicRow['y2']

            elif self.dicPage['PageFootAppendToGroup'] == 1:
                #print "appendtogroup is 1,  y1,  y2 = ", y1, y2,   dicRow['y1'] ,  dicRow['y2']
                #print "this are x values",  x1,  x2,  dicRow['x1'],  dicRow['x2']
                footerhigh = self.dicPage['pageFooterY2']  - self.dicPage['pageFooterY1'] 
                dicRow['x1'] =  self.dicPage['beginPageFooterX'] + dicRow['x1']
                dicRow['y1'] =  y1 - dicRow['y1']
                dicRow['x2'] =  self.dicPage['beginPageFooterX'] + dicRow['x2']
                dicRow['y2'] =  y2 -  dicRow['y2']
                
                print "this are the footer  y1,  y2 = ",  dicRow['y1'] ,  dicRow['y2']
                print "this are the footer x1, x2 =   ",  x1,  x2,  dicRow['x1'],  dicRow['x2']

            else: 
                dicRow['x1'] = self.dicPage['beginPageFooterX']  + dicRow['x1']
                dicRow['y1'] = self.dicPage['beginPageFooterY']  - dicRow['y1']
                dicRow['x2'] = self.dicPage['beginPageFooterX']  + dicRow['x2']
                dicRow['y2'] = self.dicPage['beginPageFooterY']  - dicRow['y2']
                
                
            liRecord = self.checkProperty(liRecord, dicRow)
            #print 'PageFootAppend2Group= ', self.dicPage['PageFootAppendToGroup'] 
            #print 'y1, y2',  y1, y2
            
            
            #print 'PageFooterY1 = ',  self.dicPage['beginPageFooterY'] 
            #print 'PageFooterY2 = ',  self.dicPage['endPageFooterY'] 
            
            
        #sys.exit(0)    
            
        return liRecord,  dicRow

    def getReportFooter(self, cyRootNode,  x1,  y1,  x2,  y2):

        cyReportFooterNode = self.getNode(cyRootNode, 'reportFooter')
        #print '------------------'
        #print cyReportFooterNode
        #print cyReportFooterNode[0].toxml()
        

        cyReportFooterEntries = self.getNodes(cyReportFooterNode[0], 'entry')
        #print '+++++++'
        #print cyReportFooterEntries
        liRecord = []
      
        for i in range(len(cyReportFooterEntries)):
            dicEntry = self.getXmlEntry(cyReportFooterEntries[i])
            if dicEntry['resultSet'] != 'zero':
                resultKey =  dicEntry['resultSet']
                if resultKey and self.dicResults.has_key(resultKey):
                    liResults = self.dicResults[resultKey.encode('ascii')]
                    if liResults:
                        self.dicResult = liResults[0]

            dicRow = self.getReportEntry(cyReportFooterEntries[i])
            #dicRow = self. getReportRow(dicEntry) 
            if self.dicPage['ReportFootAppendToGroup'] == 0:
            #dicRow['text'] = dicEntry['text']
                dicRow['x1'] = self.dicPage['beginReportFooterX'] + dicRow['x1']
                dicRow['x2'] =  self.dicPage['beginReportFooterX'] + dicRow['x2']
                dicRow['y1'] = self.dicPage['beginReportFooterY']  -  dicRow['y1']
                dicRow['y2'] = self.dicPage['beginReportFooterY']  -  dicRow['y2']
            elif self.dicPage['ReportFootAppendToGroup'] == 1:
                dicRow['x1'] = self.dicPage['beginReportFooterX'] + dicRow['x1']
                dicRow['x2'] = self.dicPage['beginReportFooterX'] + dicRow['x2']
                dicRow['y1'] = y1 - dicRow['y1']
                dicRow['y2'] = y2 - dicRow['y2']
            else:
                dicRow['x1'] = self.dicPage['beginReportFooterX'] + dicRow['x1']
                dicRow['x2'] =  self.dicPage['beginReportFooterX'] + dicRow['x2']
                dicRow['y1'] = self.dicPage['beginReportFooterY']  -  dicRow['y1']
                dicRow['y2'] = self.dicPage['beginReportFooterY']  -  dicRow['y2']
                
            liRecord = self.checkProperty(liRecord, dicRow)

        return liRecord

    
    def startReport(self,c,  cyRootNode):
        dicRow = {}
        dicRow['x1'] = 0
        dicRow['y1']  = 0 
        dicRow['x2'] = 0
        dicRow['y2']  = 0
        self.firstPage = True
        self.setBackground(c)
        
        self.dicReportValues['reportHeader'] = self.getReportHeader(cyRootNode)
        self.printReportHeader(c)
        self.dicReportValues['pageHeader'] = self.getPageHeader(cyRootNode)
        self.printPageHeader(c)
        liRecord = []
        liResults = []
        cyGroupNode = self.getNode(cyRootNode, 'groups')
      
        resultKey =  self.getEntrySpecification(cyGroupNode[0],'resultSet')
        if resultKey and self.dicResults.has_key(resultKey):
            liResults = self.dicResults[resultKey.encode('ascii')]
       
        self.lineOffset = 0

  
        
        iGroup =  int(self.getEntrySpecification(cyGroupNode[0],'count'))
        #print 'Group'
        #print iGroup

        
        for a in range(1,  iGroup + 1):
            dicGroup = {}
            dicGroup['oldValue'] = None
            dicGroup['newValue'] = None
            self.dicGroups[`a`] = dicGroup

        #print 'dicGroups'
        #print  self.dicGroups
                
        for dicResult in liResults:

            self.dicResult = dicResult
            
            cyGroupEntries = self.getNodes(cyGroupNode[0], 'groupEntry')
            #print cyGroupEntries

            for k in range(len(cyGroupEntries)):
                cyGroupEntry = cyGroupEntries[k]
                sChangeGroupBy = self.getEntrySpecification(cyGroupEntry,'changeGroupBy')
                groupNumber = int(self.getEntrySpecification(cyGroupEntry,'number'))

                dicGroup = self.dicGroups[`groupNumber`]
                
                if sChangeGroupBy:
                    changeGroupBy = sChangeGroupBy.encode('ascii')
                    dicGroup['newValue'] = self.dicResult[changeGroupBy]
                    
                    
                #print 'Groups with id ' + `groupNumber` 
                #print self.dicGroups
                
                if ( (dicGroup['newValue'] != dicGroup['oldValue'] ) or iGroup == 1) or dicGroup['newValue'] == None :
                    dicGroup['oldValue'] = dicGroup['newValue']
                    cyPageDetailsNodes = self.getNodes(cyGroupEntry, 'pageDetails')
                    print'+++++++ cyPageDetailsNodes = ',    cyPageDetailsNodes

                    for i in  range(len(cyPageDetailsNodes)):


                        cyReportDetailsNode = cyPageDetailsNodes[i]
                       # print '------------------'
                        #print 'cyReportDetailsNode = ',  cyReportDetailsNode
                        #print 'cyReportDetailsNode toxml = ',  cyReportDetailsNode.toxml()
                        

                        cyReportDetailsEntries = self.getNodes(cyReportDetailsNode, 'entry')
                        #print '+++++++'
                        #print 'cyReportDetailsEntries = ',  cyReportDetailsEntries
                        

                        self.dicPage['detailsX1'] =  int(self.getEntrySpecification(cyReportDetailsNode,'posX1'))
                        self.dicPage['detailsX2'] =  int(self.getEntrySpecification(cyReportDetailsNode,'posX2'))
                        self.dicPage['detailsY1'] =  int(self.getEntrySpecification(cyReportDetailsNode,'posY1'))
                        self.dicPage['detailsY2'] =  int(self.getEntrySpecification(cyReportDetailsNode,'posY2'))
                        self.dicPage['lineY'] =  int(self.getEntrySpecification(cyReportDetailsNode,'lineY'))

                        self.dicPage['beginPageDetailsX'] = self.dicPage['leftMargin'] + self.dicPage['detailsX1']
                        self.dicPage['endPageDetailsX'] =   self.dicPage['detailsX2']
                        if self.firstPage:
                            self.dicPage['beginPageDetailsY'] =  self.dicPage['endPageHeaderY'] - self.dicPage['detailsY1']
                            self.dicPage['endPageDetailsY'] =  self.dicPage['endPageHeaderY'] - self.dicPage['detailsY2']
                        else:
                            self.dicPage['beginPageDetailsY'] =  self.dicPage['endPageHeaderOtherSitesY'] 
                            self.dicPage['endPageDetailsY'] =  self.dicPage['endPageHeaderOtherSitesY'] 


                        

                        for m in range(len(cyReportDetailsEntries)):
                            dicRow = self.getReportEntry(cyReportDetailsEntries[m])
                            #print '=============================================================================='

                            #print 'dicRow = ',  dicRow
                           # print dicRow['text']
                            #print '=============================================================================='
                            sq = None
                            if dicRow.has_key('fontjustification') and dicRow['fontjustification'].upper() == 'TEXT':
                                
                               # print 'dicRow at TEXT = ',  dicRow
                                
                                s = dicRow['format']
                                if dicRow['text'] and dicRow['fontsize']:
                                    #print 'text and fontsize = True'
                                    try:
                                        sq = s % dicRow['text'] 
                                        try:
                                            sq = sq.encode('utf-8')
                                        except:
                                            sq = s % dicRow['text']                
                                        #to.textOut(sq)
                                        #c.drawText(to)
                                        #print 'SQ = ', sq
                                    except Exception, params:
                                        print 'Exception utf-8, latin'
                                        print Exception, params
                                        sq = ' '
                               
                                iIndex = 0
                                x1 = dicRow['x1']
                                x2 = dicRow['x2']
                                y1 = dicRow['y1']
                                y2 = dicRow['y2']
                                
                                fontoffset = 4
                                z1 = 0
                                while iIndex > -1:
                                    #dicRow = self. getReportRow(dicEntry) 
                                    #print 'sq, iIndex = ',  sq,  iIndex 
                                    z1 += 1
                                    if sq:
                                        iIndex = sq.find('\n')
                                    else: 
                                        iIndex = -1
                                        
                                    if iIndex > -1:    
                                        dicRow['text'] = sq[:iIndex]
                                        sq = sq[iIndex+1:]
                                    else:
                                        dicRow['text'] = sq
                                        sq = None
                                       
                                      
                                    #print 'text at dicrow = ',  dicRow['text']
                                    print 'dicRow before Values = ',  dicRow['y1'] ,  dicRow['y2'] ,  self.lineOffset,  z1
                                    print 'more = ',  self.dicPage['endPageDetailsY'] 
                                    dicRow['x1'] = self.dicPage['beginPageDetailsX']  + x1
                                    dicRow['y1'] = self.dicPage['endPageDetailsY'] - self.lineOffset  -y1
                                    dicRow['x2'] = self.dicPage['beginPageDetailsX']  + x2
                                    #dicRow['y2'] = self.dicPage['endPageDetailsY']  - self.lineOffset  -y2
                                    dicRow['y2'] =  dicRow['y1'] 
                                    
                                    
                                    dicRow['fontjustification'] = 'left'
                                    dicRow['class'] = 'Label'
                                    #dicRow['value'] = dicRow['text']
                                    self.endOfRegion = dicRow['y2']
        
                                    #print dicRow
                                    #print '####################################################***'
        
        
                                    #print 'liRecord 1 = ',  len(liRecord),  liRecord[len(liRecord)-1]['text']
                                    liRecord = self.checkProperty(liRecord, dicRow)
                                    
                                    #print 'liRecord 2 = ',   len(liRecord),  liRecord[len(liRecord)-1]['text']
                                    #print 'liRecord 3 = ',   len(liRecord),  liRecord[len(liRecord)-2]['text']
                                    #print 'liRecord 4 = ',   len(liRecord),  liRecord[len(liRecord)-3]['text']
                                    self.lineOffset +=  dicRow['fontsize'] + fontoffset
                                        #print "sq = ",  sq 
                                    #print 'dicRow before end = ',  dicRow['y1'] ,  dicRow['y2'] ,  self.lineOffset,  z1
                                    if self.testEndOfPage(dicRow ,self.dicPage['reportDetailsY'] , self.lineOffset ):
                                        dicRow['y1'] -= 12
                                        dicRow['y2'] -= 12
                                        liRecord = self.doEndOfPage(liRecord,  dicRow, c, cyRootNode)
                                        self.dicPage['beginPageDetailsY'] =  self.dicPage['endPageHeaderOtherSitesY'] 
                                        self.dicPage['endPageDetailsY'] =  self.dicPage['endPageHeaderOtherSitesY'] 
                                        self.lineOffset = 30
                                       # print 'dicRow after end = ',  dicRow['y1'] ,  dicRow['y2'] ,  self.lineOffset,  z1
                                  
                                    
                                sq = None
                            else:
                                
                                #dicRow = self. getReportRow(dicEntry) 
                                #dicRow['text'] = dicEntry['text']
                                dicRow['x1'] = self.dicPage['beginPageDetailsX']  + dicRow['x1']
                                dicRow['y1'] = self.dicPage['endPageDetailsY'] - self.lineOffset - dicRow['y1']
                                dicRow['x2'] = self.dicPage['beginPageDetailsX']  + dicRow['x2']
                                dicRow['y2'] = self.dicPage['endPageDetailsY']  - self.lineOffset - dicRow['y2']
                                
                                self.endOfRegion = dicRow['y2']
    
                                #print dicRow
                                #print '####################################################***'
    
    
    
                                liRecord = self.checkProperty(liRecord, dicRow)
                            
                        if self.testEndOfPage(dicRow ,self.dicPage['reportDetailsY'] , self.lineOffset ):
                            
                           liRecord = self.doEndOfPage(liRecord,  dicRow, c,  cyRootNode)
                            
                            
                        self.lineOffset +=  self.dicPage['lineY']
                      
                        self.dicGroups[`groupNumber`] = dicGroup
        self.dicReportValues['pageDetails'] = liRecord
#        if self.testEndOfPage(self.endOfRegion ,self.dicPage['reportDetailsY'] , self.dicPage['reportDetailsY'] ):
#            self.printNewPage(c)
#            self.printPageDetails(c)
#            self.printPageHeader(c)
#        else:     
        self.printPageDetails(c)
        self.lastPage = True 
        
        self.dicReportValues['pageFooter'],  dicRow = self.getPageFooter(cyRootNode, dicRow['x1'] , dicRow['y1'] ,dicRow['x2'] ,dicRow['y2']  )
        self.printPageFooter(c)
        self.dicReportValues['reportFooter']  = self.getReportFooter(cyRootNode,dicRow['x1'] , dicRow['y1'] ,dicRow['x2'] ,dicRow['y2'] )
        self.printReportFooter(c)
        self.closePDF(c)
        #self.pdfStory.append(c)
        



  

    
  ##  def getReportRow(self, dicEntry):
##        dicRow = copy.deepcopy(self.dicText)
##        dicRow['text'] = dicEntry['text']
##        dicRow['font'] = dicEntry['font']
##        dicRow['fontsize'] = dicEntry['fontsize']
##        dicRow['fontjustification'] = dicEntry['fontjustification']
##        dicRow['foregroundColor'] = dicEntry['foregroundColor']
##        dicRow['backgroundColor'] = dicEntry['backgroundColor']
##        dicRow['grayScale'] = dicEntry['grayScale']
##        dicRow['eType'] = dicEntry['eType']
##        dicRow['class'] = dicEntry['eClass']
##        dicRow['format'] = dicEntry['format']
##        dicRow['formula'] = dicEntry['formula']
        
##        dicRow['x1'] = dicEntry['eX1']
##        dicRow['x2'] = dicEntry['eX2']
##        dicRow['y1'] = dicEntry['eY1']
##        dicRow['y2'] = dicEntry['eY2']
        
        

        
##        return dicRow
    def testEndOfPage(self, dicRow, papersizeHeight, offSet ):
        ok = False
        yRow = dicRow['y1']
        if dicRow.has_key('pagebreak'):
            return True
            
            
        #print "report17 test end of page"
        #print 'yRow', yRow
        #print 'offSet', offSet
        #print 'papersizeHeight',  papersizeHeight
        print 'sum yRow + offset', yRow + offSet
        #print 'RangeSite = ',  self.dicPage['PrintRangeFirstSite'],  self.dicPage['PrintRangeNextSites']
#        
#        if  offSet > papersizeHeight or yRow < 0:
#            #liRecord, yRow  = self.newPage(liRecord)
#            ok = True
#           
        if self.firstPage:
            if offSet + 2 * self.dicPage['lineY'] > self.dicPage['PrintRangeFirstSite']:
                ok = True
        else:
             if offSet + 2 * self.dicPage['lineY'] > self.dicPage['PrintRangeNextSites']:
                ok = True
        
        return ok
    
        #return liRecord, yRow

    def doEndOfPage(self,  liRecord,  dicRow, c,  cyRootNode):
        self.dicReportValues['pageDetails'] = liRecord
        self.dicReportValues['pageFooter'],  dicRow = self.getPageFooter(cyRootNode, dicRow['x1'] , dicRow['y1'] ,dicRow['x2'] ,dicRow['y2'] )
        self.printPageDetails(c)
        self.printPageFooter(c)
        # begin new page
        liRecord = []
        #self.numberOfPage = self.numberOfPage + 1
        self.lineOffset = 0
        
        self.firstPage = False
       
        self.printNewPage(c)
        try:
            self.setBackground(c)
        except:
            pass
        self.dicReportValues['pageHeader'] = self.getPageHeader(cyRootNode)
        self.printPageHeader(c)
        
        return liRecord
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

    def getReportEntry(self, cyNode):
        eValue = ''
        dicEntry = self.getXmlEntry(cyNode)
        if dicEntry['class'] == 'Label':
            if self.dicReportData.has_key( dicEntry['eName']):
                eValue =  self.dicReportData[dicEntry['eName']]
            else:
                eValue =  dicEntry['value']
                #print eValue

        elif dicEntry['class'] == 'ImageURL':
            if self.dicReportData.has_key( dicEntry['eName']):
                eValue =  self.dicReportData[dicEntry['eName']]
            else:
                eValue =  dicEntry['value']
            eValue = eValue.strip()
            #print "pictureDMS 001", eValue
            if eValue[0:9] == 'dms_print':
                sNewImage = eValue
                #print "pictureDMS 002", eValue
                #print self.dicResult
                    
                if self.dicResult.has_key(sNewImage):
                    eValue =  self.dicResult[sNewImage]
                    #print "pictureDMS 003", eValue
                else:
                    eValue = ''
            #print "pictureDMS 004", eValue       
            
        elif dicEntry['class'] == 'Field':
            if self.dicReportData.has_key(dicEntry['eName']):
                eValue =  self.dicReportData[dicEntry['eName']]
            else:
                eValue = ''
        elif dicEntry['class'] == 'Python':
            if dicEntry['formula']:
                formula = dicEntry['formula']
                try:
                    #print 'Formula1 = ', formula
                    exec formula
                    #print 'Result of the formula = ', a
                    eValue = a
                except:
                    eValue = None
            else:
                eValue = None
                
        elif dicEntry['class'] == 'Function':
            if dicEntry['formula']:
                # Parse formula
                liFormula = string.split(dicEntry['formula'],' ')
                formula = 'a = '
                checkTrigger = True
                #print liFormula
                if liFormula:
                    z = 0
                    ok = True
                    for fw in range(len(liFormula)):
                        #print self.dicVariable
                        #print fw
                        
                        if z > 0:
                            z = z -1
                        elif ok:

                            if checkTrigger:
                                if  liFormula[fw] == '!IF':
                                     #print self.dicMemory
                                     if self.dicMemory.has_key(liFormula[fw + 1]):
                                          #print 'Value by key'
                                          
                                          #print liFormula[fw + 1], self.dicMemory[liFormula[fw + 1]]
                                          if self.dicMemory[liFormula[fw + 1]] not in ['NONE','ERROR'] and self.dicMemory[liFormula[fw + 1]][0]:
                                            ''' !THEN sequence'''

                                            #print "Value bei !IF", self.dicMemory[liFormula[fw + 1]][-1]
                                            if self.dicMemory.has_key(liFormula[fw + 3]):
                                                #print 'fw +3 '    
                                                #print liFormula[fw + 3], self.dicMemory[liFormula[fw + 3]]
                                                 
                                                formula += `self.dicMemory[liFormula[fw + 3]][-1]`
                                            else:
                                                formula +=  liFormula[fw + 3]
                                          else:
                                            ''' !ELSE sequence '''
                                            if self.dicMemory.has_key(liFormula[fw + 5]):
                                                 
                                                formula += `self.dicMemory[liFormula[fw + 5]][-1]`
                                            else:
                                                formula +=  liFormula[fw + 5]
                                     #print 'FW =',  liFormula[fw]    
                                     #print ok , formula
                                     checkTrigger = False
                                     ok = False
                                elif  liFormula[fw] == '!SUM':
                                     if self.dicMemory.has_key(liFormula[fw + 2]):
                                         liVar = self.dicMemory[liFormula[fw + 2]]
                                         #print 'liVar = ' + `liVar`
                                         for v in liVar:
                                             #print v
                                             formula = formula + "+" + " " + `v`
                                     #print 'Function***********************************************1'
                                     #print formula
                                     #print 'Function***********************************************2'
                                     checkTrigger = False
                                     z = 1

                                elif liFormula[fw] == '!Var':
                                    formula = formula + ' ' + `self.dicVariable[liFormula[fw + 1]]`
                                    #print 'Function***********************************************3'
                                    #print formula
                                    #print 'Function***********************************************4'
                                    checkTrigger = False

                                else:
                                    #print liFormula[fw]
                                    formula = formula + ' ' + liFormula[fw]
                                    #print 'Function***********************************************5'
                                    #print formula
                                    #print 'Function***********************************************6' 

                            else:
                                checkTrigger = True
                            
                if formula:
                    try:
                        #print 'Formula1 = ', formula
                        exec formula
                        #print 'Result of the formula = ', a
                        eValue = a
                    except:
                        eValue = None
                else:
                    eValue = None


                    
        elif dicEntry['class'] == 'DatabaseField':
            #print self.dicResult
            #print '2***********************************************2'
            try:
                if self.dicResult.has_key(dicEntry['eName']) :
                    eValue = self.dicResult[dicEntry['eName']]
            except:
                print "Exception at ",  dicEntry['eName']
                evalue = 0
                #print 'eValue = ' + `eValue`
            

        
    
        dicEntry['text'] = eValue
        # add-ons
        if dicEntry['Variable']:
            self.dicVariable[dicEntry['Variable']] = eValue


        if dicEntry['memory']:
            liVar = []
            if self.dicMemory.has_key(dicEntry['memory']):
                liVar = self.dicMemory[dicEntry['memory']]

            liVar.append(eValue)
            self.dicMemory[dicEntry['memory']] = liVar
            #print 'Memory = ' + `liVar`
            
        return dicEntry
    
    def createTestSite(self, c):
        grids = []
        for i in range(0,55):
            grids.append(i/2*inch)
            
        c.grid(grids, grids)
        for i in grids:
            for j in grids:
                
                c.drawString(i,j,'' + `i` + ',' +`j`)
                

        return c
  
        
     
        
    def createPdf(self, cyRootNode):
        #self.out( 'createPdf')
       
        self.pdfDoc = SimpleDocTemplate(self.pdfFile)
        self.pdfStory = [Spacer(1, 1 * inch)]
        self.pdfStyle = self.pdfStyles['Normal']

        
        c = canvas.Canvas(self.pdfFile, pagesize = self.dicText['Papersize'] )
                 
       
    
        if self.dicUser['Debug'] == 'YES':
            print 'DebugMode'
            c = self.createTestSite(c)
        else:
            print 'No Debug Mode'
        
        self.startReport(c, cyRootNode)   
        #self.pdfDoc.build(self.pdfStory)
        
        #os.system('gpdf  ' + self.pdfFile + ' &')
        f = open(self.pdfFile,'rb')
        s = f.read()
        f.close()
        return s
        
    def printNewPage(self, c) :
        print "report15 new page"
        self.setLatestSiteInformations(c)
        #c.save()
        #self.pdfStory.append(c)
        self.dicReportData['fPageNumber'] += 1
        
    def closePDF(self, c):
        print "report16 close page"
        self.setLatestSiteInformations(c)

        c.save()
        
    def setLatestSiteInformations(self, c):
        
            
        c.showPage()
        
        
        
    def printReportHeader(self, c) :

        if self.dicReportValues.has_key('reportHeader'):
            liRecord = self.dicReportValues['reportHeader']

            for dicField in liRecord:
                self.printPdfField(c, dicField)
                
    def printPageHeader(self, c) :

        print 'starting Page Header'
        if self.dicReportValues.has_key('pageHeader'):
            liRecord = self.dicReportValues['pageHeader']

            for dicField in liRecord:
                self.printPdfField(c, dicField)


    def printPageDetails(self, c) :
        print 'starting Page Details'
        if  self.dicReportValues.has_key('pageDetails'):
             liRecord = self.dicReportValues['pageDetails']
             for dicField in liRecord:
                try:
                    #print 'dicField = ',  dicField
                    self.printPdfField(c, dicField)
                except:
                    print 'Error at ',  c,  dicField
                    

    def printPageFooter(self, c) :
        print 'starting Page footer'

        if self.dicReportValues.has_key('pageFooter'):
            liRecord = self.dicReportValues['pageFooter']

            for dicField in liRecord:
                self.printPdfField(c, dicField)

    def printReportFooter(self, c) :
        
        print 'starting Report footer'
                   
        if self.dicReportValues.has_key('reportFooter'):
            liRecord = self.dicReportValues['reportFooter']
            #rint 'liRecord by ReportFooter = '
            for dicField in liRecord:
                #print dicField
                #print '-------------------------------------------------------------------------------------------'
                self.printPdfField(c, dicField)


                
        


    def printPdfField(self, c, dicField):
        #print dicField
        #print '::::::::::::::::::::::::::::::::::::::::::::::::::::::'
      

        if dicField['class'] == 'Line'  :
            
            c.setLineWidth( dicField['fontsize'])
            c.setStrokeColorRGB(dicField['foregroundColor']['rColor'], dicField['foregroundColor']['gColor'], dicField['foregroundColor']['bColor'])
            p = c.beginPath()
            p.moveTo(dicField['x1'],dicField['y1'])
            p.lineTo(dicField['x2'],dicField['y2'])
            c.drawPath(p, stroke = 1)
            print 'Line = ',  dicField['eName'],  dicField['x1'],dicField['y1'],  ' to ', dicField['x2'],dicField['y2']
        elif dicField['class'] == 'Rectangle'  :
            
            c.setLineWidth( dicField['fontsize'])
            c.setStrokeColorRGB(dicField['foregroundColor']['rColor'], dicField['foregroundColor']['gColor'], dicField['foregroundColor']['bColor'])
            c.setFillColorRGB(dicField['backgroundColor']['rColor'], dicField['backgroundColor']['gColor'], dicField['backgroundColor']['bColor'])
#            print dicField
            
            c.setFillGray(dicField['grayScale'])
            p = c.beginPath()
            p.rect(dicField['x1'],dicField['y1'], dicField['x2'] - dicField['x1']  , dicField['y2'] -  dicField['y1'])
            c.drawPath(p, stroke = 1, fill = 1)

        elif dicField['class'] == 'ImageURL'  :
            sImage = str(dicField['text'])
            
            
            #print 'ImageURL = ', sImage
            nWidth = dicField['width'] 
            nHeight =dicField['height'] 
            #print 'ImageURL values'
            #print 'x1', dicField['x1']
            #print 'x2', dicField['x2']
            #print 'y1', dicField['y1']
            #print 'y2', dicField['y2']
            try:
                if nWidth > 0 and nHeight > 0:
                    c.drawImage(sImage, dicField['x1'] ,dicField['y1'], width = nWidth, height = nHeight)
                else:
                    c.drawImage(sImage, dicField['x1'] ,dicField['y1'])
            except:
                print 'no image found'
                
        else:
                
            #            if dicField['eType'] == 'int':
            #                dicField['text'] = `dicField['text']`

            s = dicField['format']

            
##            to = c.beginText()
##            to.setTextOrigin(dicField['x1'],dicField['y1'])
##            to.setFont(dicField['font'].encode('ascii'), dicField['fontsize'], 0)
##            to.setFillColorRGB(dicField['foregroundColor']['rColor'], dicField['foregroundColor']['gColor'], dicField['foregroundColor']['bColor'] )
##            to.setTextOrigin(dicField['x1'],dicField['y1'])
            x1 = dicField['x1']
            y1 = dicField['y1']
            x2 = dicField['x2']
            y2 = dicField['y2']
            c.setFont(dicField['font'].encode('ascii'), dicField['fontsize'], 0)
            c.setFillColorRGB(dicField['foregroundColor']['rColor'], dicField['foregroundColor']['gColor'], dicField['foregroundColor']['bColor'] )
            
            if dicField['text'] and dicField['fontsize']:
                try:
                    sq = s % dicField['text'] 
                    try:
                        sq = sq.encode('utf-8')
                    except:
                        sq = s % dicField['text']                
                    #to.textOut(sq)
                    #c.drawText(to)
                    #print 'SQ = ', sq
                except Exception, params:
                    print 'Exception utf-8, latin'
                    print Exception, params
                    sq = ' '
                
                    
                try:
                   
                    
                    if dicField['fontjustification']:
                        #print 'Justification' + dicField['fontjustification']
                        try:
                            if dicField['fontjustification'] == 'left':
                                c.drawString(x1,y1,sq)
                            elif dicField['fontjustification'] == 'right':
                                c.drawRightString(x2,y1,sq)
                            elif dicField['fontjustification'] == 'center':
                                c.drawCenteredString( (int(x1+x2)/2),y1,sq)
                            elif dicField['fontjustification'] == 'blocktext':
                                textobject = c.beginText()
                                textobject.setTextOrigin(x1, y1)
                                textobject.setFont(dicField['font'].encode('ascii'), dicField['fontsize'])
                                
                                
                                textobject.textLines(sq)
                                
                                c.drawText(textobject)
                                
                        except:
                            print 'error draw string'
                    else:
                        try:
                            c.drawString(x1,y1,sq)
                        except:
                            print 'error draw string 2'
                    
#                    if dicField['fontjustification']:
#                        #print 'Justification' + dicField['fontjustification']
#                        if dicField['fontjustification'] == 'left':
#                            c.drawString(x1,y1,sq)
#                        elif dicField['fontjustification'] == 'right':
#                            c.drawRightString(x1,y1,sq)
#                        elif dicField['fontjustification'] == 'center':
#                            c.drawCenteredString(x1,y1,sq)
#                            
#                    else:
#                        c.drawString(x1,y1,sq)
                except Exception, params:
                    print 'Exception utf-8, latin 2'
    
                    print Exception, params

            
            
            #c.drawString(dicField['x1'],dicField['y1'],dicField['text'] )

            
    def printTitle(self, c):
        for i in self.liTitle:
            c.drawString(i['x1'],i['y1'],i['text'] )


    def printHeader(self,c):
        for i in self.liHeader:
            c.drawString(i['x1'],i['y1'],i['text'] )
        
         

    def createHeader(self, dicHeaderInfo):

    
        liHeaderLocal = dicHeaderInfo['Headerline']
        print liHeaderLocal
        for i in range(0,len(liHeaderLocal)):
            dicHeaderline = liHeaderLocal[i]
            dicHeader = copy.deepcopy(self.dicText)
            dicHeader['text'] = dicHeaderline['text'] # .encode('latin-1')
            dicHeader['x1'] = dicHeaderline['x1']
            dicHeader['y1'] = dicHeaderline['y1']
            self.liHeader.append(dicHeader)

            
        return self.liHeader

    def createStandardPageHeader(self,  liRecord):
        liRows = []
        #print 'numberOfPage : ' + `numberOfPage`
        dicPageInfo = self.dicHeaderInfo['pageinfo']
        dicHeader = copy.deepcopy(self.dicText)
       #dicHeader['text'] = 'Pagenumber: '
        dicHeader['x1'] = dicPageInfo['x1']
        dicHeader['y1'] = dicPageInfo['y1']
        liRows.append(dicHeader)

        dicHeader = copy.deepcopy(self.dicText)
        #dicHeader['text'] = `numberOfPage`
        dicHeader['x1'] = dicPageInfo['x2']
        dicHeader['y1'] = dicPageInfo['y2']
        liRows.append(dicHeader)



        dicDateInfo = self.dicHeaderInfo['dateinfo']
        dicHeader = copy.deepcopy(self.dicText)
        dicHeader['text'] = 'Date: ' 
        dicHeader['x1'] = dicDateInfo['x1']
        dicHeader['y1'] = dicDateInfo['y1']

        liRows.append(dicHeader)

        liRecord.append(liRows)
        return liRecord
    
    
    def createPdfPages(self,dicResult):
        pass

    
   
    def firstPage(self, liRecord):
        #self.numberOfPage = self.numberOfPage + 1
        liRecord = self.createStandardPageHeader(liRecord)
        return liRecord
    
    
    
    def newPage(self, liRecord):
    
        yRow = self.dicText['TopMargin']
        #self.numberOfPage = self.numberOfPage + 1
        liRecord = self.createStandardPageHeader(liRecord)
        liRecord.append('Pagebreak')
        
        return liRecord, yRow
        
        
        
    def setBackground(self,c):
        
##        print '######################### Start BackgroundImage ##################################'
##        print self.dicPage['SiteBackground_URL']
##        print self.dicPage['SiteBackgroundX']
##        print self.dicPage['SiteBackgroundX']
##        print self.dicPage['SiteBackgroundWidth']
##        print self.dicPage['SiteBackgroundHeight']
##        
        try:
            if self.dicPage.has_key('SiteBackground_URL'):
                
                
                sImage = str(self.dicPage['SiteBackground_URL'])
                #print 'ImageURL = ', sImage
                nWidth = self.dicPage['SiteBackgroundWidth'] 
                nHeight = self.dicPage['SiteBackgroundHeight'] 
                x1 = self.dicPage['SiteBackgroundX']
                y1 = self.dicPage['SiteBackgroundY']
                dicRow = {'PropertyBG':self.dicPage['PropertyBG']}
                if self.doPrintPart(dicRow, 'BG'):
                    if nWidth > 0 and nHeight > 0:
                        c.drawImage(sImage, x1, y1, width = nWidth, height = nHeight)
                    else:
                        c.drawImage(sImage, x1, y1)
                        
                
        except Exception, params:
            print Exception, params
            
        try:
            if self.dicPage.has_key('SiteBackground_URL2'):
                
                
                sImage = str(self.dicPage['SiteBackground_URL2'])
                #print 'ImageURL = ', sImage
                nWidth = self.dicPage['SiteBackgroundWidth2'] 
                nHeight = self.dicPage['SiteBackgroundHeight2'] 
                x1 = self.dicPage['SiteBackgroundX2']
                y1 = self.dicPage['SiteBackgroundY2']
                dicRow = {'PropertyBG2':self.dicPage['PropertyBG2']}
                if self.doPrintPart(dicRow, 'BG2'):
                    if nWidth > 0 and nHeight > 0:
                        c.drawImage(sImage, x1, y1, width = nWidth, height = nHeight)
                    else:
                        c.drawImage(sImage, x1, y1)
                        
                
        except Exception, params:
            print Exception, params   
            
            
        try:
            if self.dicPage.has_key('SiteBackground_URL3'):
                
                
                sImage = str(self.dicPage['SiteBackground_URL3'])
                #print 'ImageURL = ', sImage
                nWidth = self.dicPage['SiteBackgroundWidth3'] 
                nHeight = self.dicPage['SiteBackgroundHeight3'] 
                x1 = self.dicPage['SiteBackgroundX3']
                y1 = self.dicPage['SiteBackgroundY3']
                dicRow = {'PropertyBG3':self.dicPage['PropertyBG3']}
                if self.doPrintPart(dicRow, 'BG3'):
                    if nWidth > 0 and nHeight > 0:
                        c.drawImage(sImage, x1, y1, width = nWidth, height = nHeight)
                    else:
                        c.drawImage(sImage, x1, y1)
                        
                
        except Exception, params:
            print Exception, params
            
            
            
    def doPrintPart(self, dicRow,  Suffix = ''):
        doPrint = False
        printSite = None
        if dicRow.has_key('Property'+Suffix) and dicRow['Property'+Suffix]:
            #print "sProperty = " ,  Suffix,  dicRow['Property'+Suffix]
            sProperty = dicRow['Property'+Suffix]
            printSite = sProperty[0].strip().upper()
            if printSite == 'A':
                # all sites
                doPrint = True
            elif printSite == 'F' and self.firstPage:
                #only first site
                doPrint = True    
            elif printSite == 'N' and not self.firstPage:
                #all but not the first page
                doPrint = True  
            elif printSite == 'L' and self.lastPage:
                #only the last page
                doPrint = True    
            elif printSite == 'B' and not self.firstPage and not self.lastPage:
                # all sites but not the first and not the last
                doPrint = True    
            elif printSite == 'C'  and not self.lastPage:
                # all sites but not the last page
                doPrint = True      
                
        else:
            doPrint = True 
        #print 'do Print = ',   printSite,  Suffix, doPrint
        #print dicRow
        
        return doPrint
        
        
    def checkProperty(self,  liRecord, dicRow) :
        
        doPrint = self.doPrintPart(dicRow)
        
        if doPrint:
            
            liRecord.append(copy.deepcopy(dicRow))
        
        return liRecord
        
        
        
