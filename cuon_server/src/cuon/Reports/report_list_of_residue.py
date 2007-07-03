# -*- coding: utf-8 -*-
##Copyright (C) [2003-2004]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 


import os
import types
from report_basics import report_basics



class report_list_of_residue(report_basics):
    def __init__(self):
        report_basics.__init__(self)
        
        self.dicReportData = {}
        self.dicResults = {}
        
        
        self.dicReportData['Title'] = _('List of Residue generated by CUON')

        self.dicReportData['lPageNumber'] = _('Pagenumber:')
        self.dicReportData['fPageNumber'] = 1
        self.dicReportData['Designation'] = _('Designation')
        self.dicReportData['lOrderNumber'] = _('Order-Number:')
        
    
    
    def getReportData(self, dicExtraData, dicUser, oOrder, reportDefs ):
        
        
        self.fileName = reportDefs['DocumentPathOrderInvoice'] + '/' +_('ListOfResidue-') + `dicExtraData['dBegin']`  + '.pdf' 
        reportDefs['pdfFile'] = os.path.normpath(self.fileName)
        print dicExtraData
        print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*'
        self.dicResults['Info'] = dicExtraData
        dicResult =  oOrder.getResidue(  dicUser )
        print "result by OrderListInvoices: ", dicResult
        if dicResult != 'NONE':
##            for i in dicResult:
##                for j in i.keys():
##                    if isinstance(i[j],  types.StringType):
##                        i[j] = self.getPdfEncoding(i[j],reportDefs )
##                        
                                    
                            
                            

            self.dicResults['listOfResidue'] = dicResult   
            print self.dicResults
            
            print 'ReportPath = ', reportDefs['ReportPath'] + '/list_list_of_invoices.xml'
            
            # values in this order:
            # 1 reportname
            # 2 dicUser
            # 3 dicResults
            # 4 dicReportData
            # 5 reportDefs
        return reportDefs['ReportPath'] + '/list_of_residue.xml', dicUser, self.dicResults, self.dicReportData, reportDefs
        
        
        
        
