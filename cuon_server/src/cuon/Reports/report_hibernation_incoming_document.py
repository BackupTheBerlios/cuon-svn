# -*- coding: utf-8 -*-
##Copyright (C) [2003-2004]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 


import os
import types
from report_basics import report_basics



class report_hibernation_incoming_document(report_basics):
    def __init__(self):
        report_basics.__init__(self)
        
        self.dicReportData = {}
        self.dicResults = {}
        
        
        self.dicReportData['Title'] = _('Hibernation Incoming generatet by CUON')

        self.dicReportData['lPageNumber'] = _('Pagenumber:')
        self.dicReportData['fPageNumber'] = 1
        self.dicReportData['Designation'] = _('Designation')
        self.dicReportData['lIncoming'] = _('Incoming Document')
        self.dicReportData['lPickUpBy'] = _('Pick up by:')
        self.dicReportData['lPickupNumber'] = _('Pickup-Nr.:')
        self.dicReportData['lOrderNumber'] = _('Order-Number:')
        self.dicReportData['lBeginData'] = _('Begin at:')
        self.dicReportData['lPlantNumber'] = _('Plant:')
        self.dicReportData['lPlantName'] = _('Botany name:')
        
    
    
    def getReportData(self, dicOrder, dicUser, oGarden, reportDefs ):
        
        
        self.fileName = reportDefs['DocumentPathHibernationIncoming'] + '/' +_('Incoming_Document-') + `dicOrder['incomingNumber']` + '.pdf' 
        reportDefs['pdfFile'] = os.path.normpath(self.fileName)
        print dicOrder
        print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*'

        dicResult =  oGarden.xmlrpc_getIncomingAddress( dicOrder, dicUser )
        print "result by address: ", dicResult
        for i in dicResult:
            for j in i.keys():
                if isinstance(i[j],  types.StringType):
                    i[j] = self.getPdfEncoding(i[j],reportDefs )
                    
                                
                            
                            

        self.dicResults['address'] = dicResult   
        dicResult =  oGarden.xmlrpc_getHibernationIncoming( dicOrder,  dicUser )
        print "result by positions", dicResult
        

        for i in dicResult:
            for j in i.keys():
                if isinstance(i[j],  types.StringType):
                    i[j] = self.getPdfEncoding(i[j],reportDefs )
            

    
        print  dicResult 
        self.dicResults['positions'] = dicResult
        # values in this order:
        # 1 reportname
        # 2 dicUser
        # 3 dicResults
        # 4 dicReportData
        # 5 reportDefs
        return reportDefs['ReportPath'] + '/hibernation_incoming_document.xml', dicUser, self.dicResults, self.dicReportData, reportDefs
        
        
        
        