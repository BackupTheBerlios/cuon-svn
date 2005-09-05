# -*- coding: utf-8 -*-
##Copyright (C) [2003-2004]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 



from cuon.PDF.standardlist import standardlist
import cuon.PDF.report_cab_monthly
from cuon.Misc.fileSelection import fileSelection
import types
import os.path

class  standard_cab_monthly(standardlist, fileSelection):
    
    def __init__(self, dicCab):
        
       standardlist.__init__(self)
        
        rep = cuon.PDF.report_cab_monthly.report_cab_monthly()
        self.dicReportData =  rep.dicReportData
        self.dicCab = dicCab
        self.openDB()
        self.oUser = self.loadObject('User')
        
        #print `self.oUser`
        #print `self.oUser.getDicUser()`
        
        self.closeDB()
        self.dicUser = self.oUser.getDicUser()
        
        sFile = self.setFileName( self.oUser.prefPath['StandardCAB1'] +  '/' +_('cabM-') + `self.dicCab['CabNumber']` + '.pdf' )
        fileSelection.__init__(self, initialFilename = sFile )


        
        
    def on_ok_button1_clicked(self, event):
    

        self.on_ok_button_clicked(event)
        self.pdfFile = os.path.normpath(self.fileName)
        print self.dicCab
        print  self.rpc.getServer()
        print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*'

        dicResult =  self.rpc.callRP('src.Finances.py_getClientAddress', self.dicUser['client'],  self.dicUser() )
        for i in dicResult:
            for j in i.keys():
                if isinstance(i[j],  types.StringType):
                    i[j] = (i[j].decode('utf-7')).encode(self.oUser.userPdfEncoding)

        self.dicResults['client'] = dicResult

        dicResult2 = []
        dicResult =  self.rpc.callRP('src.Address.py_getPartnerAddress', self.dicCab['partnerNumber'],  self.oUser.getDicUser() )
        for i in dicResult:
            for j in i.keys():
                if isinstance(i[j],  types.StringType):
                    i[j] = (i[j].decode('utf-7')).encode(self.oUser.userPdfEncoding)
            
        
        self.dicResults['partner_address'] = dicResult

        dicResult =  self.rpc.callRP('src.Address.py_getAddress', self.dicCab['forwardingAgencyNumber'],  self.oUser.getDicUser() )
        for i in dicResult:
            for j in i.keys():
                if isinstance(i[j],  types.StringType):
                    i[j] = (i[j].decode('utf-7')).encode(self.oUser.userPdfEncoding)

        self.dicResults['forwarding_agency_address'] = dicResult



        dicResult =  self.rpc.callRP('src.Address.py_getPartnerAddress', self.dicCab['contactPersonNumber'],  self.oUser.getDicUser() )
        for i in dicResult:
            for j in i.keys():
                if isinstance(i[j],  types.StringType):
                    i[j] = (i[j].decode('utf-7')).encode(self.oUser.userPdfEncoding)

        self.dicResults['contact_person_address'] = dicResult

        dicResult =  self.rpc.callRP('src.Order.py_getPickupData', self.dicCab,  self.oUser.getDicUser() )
        for i in dicResult:
            for j in i.keys():
                if isinstance(i[j],  types.StringType):
                    i[j] = (i[j].decode('utf-7')).encode(self.oUser.userPdfEncoding)

        self.dicResults['pickup_data'] = dicResult

 
        dicResult =  self.rpc.callRP('src.Order.py_getStandardInvoice', self.dicCab,  self.oUser.getDicUser() )
        print dicResult
        for i in dicResult:
            for j in i.keys():
                if isinstance(i[j],  types.StringType):
                    i[j] = (i[j].decode('utf-7')).encode(self.oUser.userPdfEncoding)
        self.out( dicResult )
        self.dicResults['positions'] = dicResult

        
        self.loadXmlReport('finances_cab_monthly', 'ReportStandardPickup1')
        

