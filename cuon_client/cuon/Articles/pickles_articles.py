# -*- coding: utf-8 -*-
##Copyright (C) [2003 -2007]  [Juergen Hamel, D-32584 Loehne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 
from cuon.Windows.rawWindow import rawWindow


class pickles_articles(rawWindow):

    
    def __init__(self, nRows):
        rawWindow.__init__(self)
        self.nRows = nRows
        self.loadGlade('articles_search1.xml')
        self.win1 = self.getWidget('dialog1')
        
        print "pickles_articles start",  self.nRows
        
 
    def on_okbutton1_clicked(self,event):
        print 'ok'
        dicSearchfields = self.readSearchDatafields()
        Pdf = self.rpc.callRP('Report.server_articles_pickles_standard', dicSearchfields, self.dicUser,  self.nRows)
        self.showPdf(Pdf, self.dicUser)
        di1 = self.getWidget('dialog1')
        di1.hide()
    
    def on_cancelbutton1_clicked(self,event):
        print 'cancel'
        di1 = self.getWidget('dialog1')
        di1.hide()
        
    def readSearchDatafields(self):
        dicSearchfields = {}
        dicSearchfields['eNumberFrom'] = self.getWidget('eNumberFrom').get_text()
        dicSearchfields['eNumberTo'] = self.getWidget('eNumberTo').get_text()

        dicSearchfields['eDesignationFrom'] = self.getWidget('eDesignationFrom').get_text()
        dicSearchfields['eDesignationTo'] = self.getWidget('eDesignationTo').get_text()
        
 

        return dicSearchfields
            
        
