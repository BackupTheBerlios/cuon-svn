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



class report_order_standard_invoice(report_basics):
    def __init__(self):
        report_basics.__init__(self)
        
        self.dicReportData = {}
        self.dicResults = {}
        
        
        self.dicReportData['Title'] = _('Invoice generatet by CUON')

        self.dicReportData['lPageNumber'] = _('Pagenumber:')
        self.dicReportData['fPageNumber'] = 1
        self.dicReportData['Designation'] = _('Designation')
        self.dicReportData['lOrderNumber'] = _('Order-Number:')
        
    
    
    def getReportData(self, dicOrder, dicUser, oOrder, reportDefs ):
        
        
        self.fileName = reportDefs['DocumentPathOrderInvoice'] + '/' +_('Invoice-') + `dicOrder['invoiceNumber']` + '.pdf' 
        reportDefs['pdfFile'] = os.path.normpath(self.fileName)
        print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*'
        dicOrder['invoiceDate'] = oOrder.xmlrpc_getInvoiceDate(dicOrder['orderid'], dicUser)
        dicResult = oOrder.xmlrpc_getOrderValues(dicOrder['orderid'], dicUser)
        if dicResult and dicResult not in ['NONE','ERROR']:
            for key in dicResult[0].keys():
                dicOrder[key] = dicResult[0][key]
        
        self.dicResults['Order'] = [dicOrder]
        
        print dicOrder
        
        dicResult =  oOrder.xmlrpc_getInvoiceAddress( dicOrder, dicUser )
        print "result by address: ", dicResult
        if dicResult not in ['NONE','ERROR']:
##            for i in dicResult:
##                for j in i.keys():
##                    if isinstance(i[j],  types.StringType):
##                        i[j] = self.getPdfEncoding(i[j],reportDefs )
##                        
                                    
                            
                            
            #for key in dicOrder.keys():
            #    dicResult[0][key] = dicOrder[key]
                
            self.dicResults['address'] = dicResult   
            #dicResult =  oOrder.xmlrpc_getOrderPositions( dicOrder,  dicUser )
            dicResult =  oOrder.xmlrpc_getStandardInvoice( dicOrder,  dicUser )

            print "result by positions", dicResult
            
##    
##            for i in dicResult:
##                for j in i.keys():
##                    if isinstance(i[j],  types.StringType):
##                        i[j] = self.getPdfEncoding(i[j],reportDefs )
##                
##    
        
            print  dicResult 
            self.dicResults['positions'] = dicResult
            print 'ReportPath = ', reportDefs['ReportPath'] + '/order_standardinvoice.xml'
            
            dicResult =  oOrder.xmlrpc_getToP( dicOrder, dicUser )

            print "result by top", dicResult
            
##    
##            for i in dicResult:
##                for j in i.keys():
##                    if isinstance(i[j],  types.StringType):
##                        i[j] = self.getPdfEncoding(i[j],reportDefs )
##                
##    
        
            print  dicResult 
            self.dicResults['terms_of_payment'] = dicResult
            
            dicResult =  oOrder.xmlrpc_getUserInfoInvoice( dicOrder, dicUser )
            self.dicResults['user_info'] = dicResult
            # values in this order:
            # 1 reportname
            # 2 dicUser
            # 3 dicResults
            # 4 dicReportData
            # 5 reportDefs
        return reportDefs['ReportPath'] + '/order_standardinvoice.xml', dicUser, self.dicResults, self.dicReportData, reportDefs
        
        
        
        