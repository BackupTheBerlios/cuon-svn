# -*- coding: utf-8 -*-
##Copyright (C) [2003]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 
##import cuon.XMLRPC.xmlrpc
##
##
##import copy
from cuon.Windows.rawWindow import rawWindow
from lists_addresses import  lists_addresses

class lists_addresses_phone12(rawWindow, lists_addresses):
    
    def __init__(self):
        rawWindow.__init__(self)
        self.loadGlade('addresses_search1.xml')
        self.win1 = self.getWidget('dialog1')

 

    def on_okbutton1_clicked(self,event):
        print 'ok'
        dicSearchfields = self.readSearchDatafields()
        Pdf = self.rpc.callRP('Report.server_address_phonelist12', dicSearchfields, self.dicUser)
        self.showPdf(Pdf, self.dicUser)
        di1 = self.getWidget('dialog1')
        di1.hide()


        
    def on_okbutton1_clicked_old(self,event):
        print 'ok'
        sFile  = self.getWidget('eFiledata').get_text()
        self.pdfFile = os.path.normpath(sFile)
        dicSearchfields = self.readSearchDatafields()
        self.out(dicSearchfields)
        di1 = self.getWidget('dialog1')
        di1.hide()

        dicResult =  self.rpc.callRP('Address.getPhonelist12', dicSearchfields, self.dicUser)
        
#        for i in dicResult:
#            for j in i.keys():
#                if isinstance(i[j],types.UnicodeType):
#                    try:
#                        i[j] = (i[j].decode('utf-8')).encode('latin-1')
#                    except:
#                        pass
#                        
            

        self.dicResults['address'] = dicResult
        self.loadXmlReport('addresses_phonelist12','ReportAddressLists' )

   
    
    
    
        
    def on_cancelbutton_clicked(self,event):
        print 'cancel'
        di1 = self.getWidget('dialog1')
        di1.hide()


    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
