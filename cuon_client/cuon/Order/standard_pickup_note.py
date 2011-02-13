# -*- coding: utf-8 -*-
##Copyright (C) [2003-2004]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 



import types
import os.path
#import cuon.PDF.report_order_standard_invoice

class standard_pickup_note:
    
    def __init__(self, dicOrder):
        
        
        #rep = cuon.PDF.report_order_standard_invoice.report_order_standard_invoice()
        self.dicReportData =  rep.dicReportData
        self.dicOrder = dicOrder
        self.openDB()
        self.oUser = self.loadObject('User')
        
        print `self.oUser`
        print `self.oUser.getDicUser()`
        
        self.closeDB()
        
        sFile = self.setFileName( self.oUser.prefPath['StandardPickup1'] +  '/' +_('pickup-') + `self.dicOrder['pickupNumber']` + '.pdf' )
        fileSelection.__init__(self, initialFilename = sFile )


        
        
    def on_ok_button1_clicked(self, event):
    

        self.on_ok_button_clicked(event)
        self.pdfFile = os.path.normpath(self.fileName)
        print self.dicOrder
        print  self.rpc.getServer()
        print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*'

        dicResult =  self.rpc.callRP('src.Address.py_getAddress', self.dicOrder['addressNumber'],  self.oUser.getDicUser() )
        for i in dicResult:
            for j in i.keys():
                if isinstance(i[j],  types.StringType):
                    i[j] = (i[j].decode('utf-7')).encode(self.oUser.userPdfEncoding)

        self.dicResults['pickup_address'] = dicResult

        dicResult2 = []
        dicResult =  self.rpc.callRP('src.Address.py_getPartnerAddress', self.dicOrder['partnerNumber'],  self.oUser.getDicUser() )
        for i in dicResult:
            for j in i.keys():
                if isinstance(i[j],  types.StringType):
                    i[j] = (i[j].decode('utf-7')).encode(self.oUser.userPdfEncoding)
            
        
        self.dicResults['partner_address'] = dicResult

        dicResult =  self.rpc.callRP('src.Address.py_getAddress', self.dicOrder['forwardingAgencyNumber'],  self.oUser.getDicUser() )
        for i in dicResult:
            for j in i.keys():
                if isinstance(i[j],  types.StringType):
                    i[j] = (i[j].decode('utf-7')).encode(self.oUser.userPdfEncoding)

        self.dicResults['forwarding_agency_address'] = dicResult



        dicResult =  self.rpc.callRP('src.Address.py_getPartnerAddress', self.dicOrder['contactPersonNumber'],  self.oUser.getDicUser() )
        for i in dicResult:
            for j in i.keys():
                if isinstance(i[j],  types.StringType):
                    i[j] = (i[j].decode('utf-7')).encode(self.oUser.userPdfEncoding)

        self.dicResults['contact_person_address'] = dicResult

        dicResult =  self.rpc.callRP('src.Order.py_getPickupData', self.dicOrder,  self.oUser.getDicUser() )
        for i in dicResult:
            for j in i.keys():
                if isinstance(i[j],  types.StringType):
                    i[j] = (i[j].decode('utf-7')).encode(self.oUser.userPdfEncoding)

        self.dicResults['pickup_data'] = dicResult

 
        dicResult =  self.rpc.callRP('src.Order.py_getStandardInvoice', self.dicOrder,  self.oUser.getDicUser() )
        print dicResult
        for i in dicResult:
            for j in i.keys():
                if isinstance(i[j],  types.StringType):
                    i[j] = (i[j].decode('utf-7')).encode(self.oUser.userPdfEncoding)
        self.out( dicResult )
        self.dicResults['positions'] = dicResult

        
        self.loadXmlReport('order_standardpickup', 'ReportStandardPickup1')
        