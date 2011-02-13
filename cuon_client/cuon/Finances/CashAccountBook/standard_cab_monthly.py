# -*- coding: utf-8 -*-
##Copyright (C) [2003-2004]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 


from  cuon.Addresses.selectionDialog import selectionDialog1
#from cuon.Misc.fileSelection import fileSelection
import types
import os.path

class  standard_cab_monthly(selectionDialog1):
    
    def __init__(self, dicCab):

        selectionDialog1.__init__(self,'cab_search1.xml')
        
        rep = cuon.PDF.XML.report_cab_monthly.report_cab_monthly()
        self.dicReportData =  rep.dicReportData
        self.dicCab = dicCab
        self.openDB()
        self.oUser = self.loadObject('User')
        
        #print `self.oUser`
        #print `self.oUser.getDicUser()`
        
        self.closeDB()
        self.dicUser = self.oUser.getDicUser()
        sFile = self.getWidget('eFiledata').set_text(self.setFileName (_('stockgoods_number1.pdf') ))
        sFile = self.setFileName( self.oUser.prefPath['StandardCAB1'] +  '/' +_('cabM-') + `self.dicCab['CabNumber']` + '.pdf' )
        #fileSelection.__init__(self, initialFilename = sFile )


        
        
    def on_okbutton1_clicked(self, event):
        print 'ok to print CashaccountBook'
        sFile  = self.getWidget('eFiledata').get_text()
        #self.on_ok_button_clicked(event)
        self.pdfFile = os.path.normpath(sFile)
        print self.dicCab
        print  self.rpc.getServer()
        print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*'
        self.dicSearchfields = self.readSearchDatafields()
        print "dicSearchfields", `self.dicSearchfields`
        
        dicResults =  self.rpc.callRP('src.Finances.py_getCashAccountBook', self.dicSearchfields,  self.dicUser )
        
        #print `dicResult`
        dicResult = dicResults['cab']
        for i in dicResult:
            for j in i.keys():
                if isinstance(i[j],  types.StringType):
                    i[j] = (i[j].decode('utf-7')).encode(self.oUser.userPdfEncoding)

        self.dicResults['cab'] = dicResult
        
        dicResult = dicResults['before']
        for i in dicResult:
            for j in i.keys():
                if isinstance(i[j],  types.StringType):
                    i[j] = (i[j].decode('utf-7')).encode(self.oUser.userPdfEncoding)

        self.dicResults['before'] = dicResult

        
        di1 = self.getWidget('dialog1')
        di1.hide()

        
        self.loadXmlReport('finances_cab_monthly1', 'ReportStandardFinancesCAB')
        

    def readSearchDatafields(self):
        dicSearchfields = {}
        dicSearchfields['eMonth'] = self.getWidget('eMonth').get_text()
        dicSearchfields['eYear'] = self.getWidget('eYear').get_text()

        dicSearchfields['eAccountNumber'] = self.getWidget('eAccountNumber').get_text()
#        dicSearchfields['eDesignationTo'] = self.getWidget('eDesignationTo').get_text()
        
#        dicSearchfields['eStockFrom'] = self.getWidget('eStockFrom').get_text()
#        dicSearchfields['eStockTo'] = self.getWidget('eStockTo').get_text()

#        dicSearchfields['eActualStockFrom'] = self.getWidget('eActualStockFrom').get_text()
#        dicSearchfields['eActualStockTo'] = self.getWidget('eActualStockTo').get_text()


        return dicSearchfields
    
    def on_cancelbutton1_clicked(self,event):
        print 'cancel'
        di1 = self.getWidget('dialog1')
        di1.hide()


    def on_bFileDialog_clicked(self, event):
        print self.filedata
        self.getWidget('fileselection1').set_filename(self.filedata[0])
        self.getWidget('fileselection1').show()
        
  