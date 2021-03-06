# -*- coding: utf-8 -*-
##Copyright (C) [2003-2007]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 

import os
import types

class report_articles_pickles_standard:
    def __init__(self,  nRows = 0,  sName = 'standard'):
        self.nRows = nRows
        self.sName = sName
        self.dicReportData = {}
        
        self.dicReportData['Title'] = _('articles_pickles_' + sName + ' generatet by CUON')

        self.dicReportData['lPageNumber'] = _('Pagenumber:')
        self.dicReportData['fPageNumber'] = 1
        self.dicReportData['Designation'] = _('Designation')
        
    
    def getReportData(self, dicSearchfields, dicUser, oArticle, reportDefs):
        self.dicResults = {}
        sReportfile = reportDefs['ReportPath'] + '/articles_pickles_' + self.sName + '_' + `self.nRows` + '.xml'
        # to do
        # check, if to load pictures
        
        self.fileName = reportDefs['DocumentPathListsArticles'] + '/' +_('Pickles_' + self.sName + '-') + `dicUser['Name']` +`self.nRows` + '.pdf' 
        reportDefs['pdfFile'] = os.path.normpath(self.fileName)
        
        dicResult =  oArticle.getPickleListStandard( dicSearchfields, dicUser,  self.nRows)

    
        
        print dicResult
        print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*'
        
        self.dicResults['articles'] = dicResult
        #self.loadXmlReport('addresses_phonelist1', 'ReportAddressLists')
        #values in this order:
        # 1 reportname
        # 2 dicUser
        # 3 dicResults
        # 4 dicReportData
        # 5 reportDefs
        return sReportfile, dicUser, self.dicResults, self.dicReportData, reportDefs
                
        
        