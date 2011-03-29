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

class report_grave_plant_lists:
    def __init__(self,  nRows = 0,  sName = 'standard', iOrderSort=0):
        self.nRows = nRows
        self.sName = sName
        self.iOrderSort = iOrderSort
        
        self.dicReportData = {}
        
        self.dicReportData['Title'] = _(sName + ' generatet by CUON')

        self.dicReportData['lPageNumber'] = _('Pagenumber:')
        self.dicReportData['fPageNumber'] = 1
        self.dicReportData['Designation'] = _('Designation')
        
    
    def getReportData(self, dicSearchfields, dicUser, oGrave, reportDefs):
        self.dicResults = {}
        sReportfile = reportDefs['ReportPath'] + '/' + self.sName
        # to do
        # check, if to load pictures
        
        self.fileName = reportDefs['DocumentPathListsGraves'] + '/' +_( self.sName + '-') + `dicUser['Name']` +`self.nRows` + '.pdf' 
        reportDefs['pdfFile'] = os.path.normpath(self.fileName)
        dicUser['iOrderSort'] = self.iOrderSort
        dicResult =  oGrave.getGravePlantListValues( dicSearchfields, dicUser,  self.nRows)

    
        
        #print dicResult
        #print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*'
        
        self.dicResults['grave'] = dicResult
        dicResult =  oGrave.getGravePlantListArticles( dicSearchfields, dicUser,  self.nRows)
        self.dicResults['articles'] = dicResult
        print 'Grave-Aricticle = ',  dicResult
        #self.loadXmlReport('addresses_phonelist1', 'ReportAddressLists')
        #values in this order:
        # 1 reportname
        # 2 dicUser
        # 3 dicResults
        # 4 dicReportData
        # 5 reportDefs
        return sReportfile, dicUser, self.dicResults, self.dicReportData, reportDefs
                
        
        
