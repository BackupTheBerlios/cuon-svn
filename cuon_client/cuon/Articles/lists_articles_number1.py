# -*- coding: utf-8 -*-
##Copyright (C) [2003]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 
from cuon.Windows.rawWindow import rawWindow


class lists_articles_number1(rawWindow):

    
    def __init__(self):
        rawWindow.__init__(self)
        
        self.loadGlade('articles_search1.xml')
        self.win1 = self.getWidget('dialog1')
        
        print "lists_articles_number1 start"
        
 
    def on_okbutton1_clicked(self,event):
        print 'ok'
        dicSearchfields = self.readSearchDatafields()
        Pdf = self.rpc.callRP('Report.server_articles_number1', dicSearchfields, self.dicUser)
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
            
        
##    def on_okbutton1_clicked_old(self,event):
##        print 'ok'
##        sFile  = self.getWidget('eFiledata').get_text()
##        self.pdfFile = os.path.normpath(sFile)
##        dicSearchfields = self.readSearchDatafields()
##        self.out(dicSearchfields)
##        di1 = self.getWidget('dialog1')
##        di1.hide()
##
##        dicResult =  self.rpc.callRP('Article.getArticlelist1', dicSearchfields, self.dicUser)
##        for i in dicResult:
##            for j in i.keys():
##                if isinstance(i[j],types.UnicodeType):
##                    i[j] = (i[j].decode('utf-7')).encode('latin-1')
##            
##
##    
##        self.out( dicResult )
##        print dicResult
##        print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*'
##        
##        self.dicResults['articles'] = dicResult
##        self.loadXmlReport('articles_number1', 'ReportArticleLists')
##
##
##   

##        
##    def on_cancelbutton1_clicked(self,event):
##        print 'cancel'
##        di1 = self.getWidget('dialog1')
##        di1.hide()
##
##
##    def on_bFileDialog_clicked(self, event):
##        print self.filedata
##        self.getWidget('fileselection1').set_filename(self.filedata[0])
##        self.getWidget('fileselection1').show()
##        
##  
##
##  
