##Copyright (C) [2003]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 

import sys
from types import *
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import gobject
from gtk import TRUE, FALSE
import string

import logging
from cuon.Windows.windows  import windows
from Crypto.Cipher import AES
import cuon.Login.User

class loginwindow(windows):

    
    def __init__(self):

        windows.__init__(self)
        self.oUser = cuon.Login.User.User()
        
        self.loadGlade('login.xml')
   
        win1 = self.getWidget('UserID_Dialog')
        response = win1.run()
        
        while response == gtk.RESPONSE_DELETE_EVENT or response == gtk.RESPONSE_CANCEL:
            response = win1.run()

        while response != gtk.RESPONSE_OK:
            if response == gtk.RESPONSE_HELP:
                print "Hilfe"
            response = win1.run()
                
        ##if response == gtk.RESPONSE_OK:
        self.okButtonPressed()
        ##elif response == gtk.RESPONSE_HELP:
        ##    print "Hilfe"
            
##        elif response == gtk.RESPONSE_DELETE_EVENT:
        ##else:
        ##print "else"
            
            

    #def on_okbutton1_clicked(self, event):
    def okButtonPressed(self):
        
        obj = AES.new('Th77777777key456', AES.MODE_ECB)
        username = self.getWidget('TUserID').get_text()
        self.openDB()
        userObj = self.loadObject('User')
        self.closeDB()
        
        if userObj :
            
            print 'User found'
            #self.oUser = userObj
           
        self.oUser.setUserName(username )
        sPw = self.getWidget('TPassword').get_text()
        while(len(sPw) < 16):
            sPw= sPw +' '
        print len(sPw)    
       
        self.oUser.setUserPassword(obj.encrypt(sPw))
        
        print self.oUser.userPassword
        print  obj.decrypt(self.oUser.userPassword)

        sPw = string.replace(sPw,' ','')
        print len(sPw)
          
        self.loadProfile()
        
        self.openDB()
        self.saveObject('User', self.oUser)
        self.closeDB()
        print 'end Login'
        print str(self.oUser)
        self.quitLogin()
       
    def on_okcancel1_clicked(self, event):
        self.quitLogin()

    def quitLogin(self):
        win1 = self.getWidget('UserID_Dialog')
        win1.hide()

    def loadProfile(self, sProfile = None):
        
        if  not sProfile :
            sProfile = self.rpc.getServer().src.User.py_getNameOfStandardProfile(self.oUser.getUserName())

            print 'Profile = '
            print sProfile

        if sProfile:
            result = self.rpc.getServer().src.User.py_getStandardProfile(self.oUser.getUserName(),sProfile )
            print 'Result Profile'
            print result
            if result:
                self.oUser.userLocales ='de'
                if result.has_key('encoding'):
                    self.oUser.userEncoding = result['encoding']
                self.oUser.userPdfEncoding = 'latin-1'

                self.oUser.userDateTimeFormatString = "%d.%m.%Y"
                self.oUser.userTimeFormatString = "%H:%M"

                self.oUser.serverAddress = None
                self.oUser.userSQLDateFormat = 'DD.MM.YYYY'
                self.oUser.userSQLTimeFormat = 'HH24:MI'
                self.oUser.prefPath = {}

                self.oUser.prefPath['StandardInvoice1'] =  result['path_to_docs_invoices']
                self.oUser.prefPath['StandardSupply1'] =  result['path_to_docs_supply']
                self.oUser.prefPath['StandardPickup1'] =  result['path_to_docs_pickup']
                self.oUser.prefPath['AddressLists'] =   result['path_to_docs_address_lists']

                self.oUser.prefPath['ReportStandardInvoice1'] =   result['path_to_report_invoices']
                self.oUser.prefPath['ReportStandardSupply1'] =  result['path_to_report_supply']
                self.oUser.prefPath['ReportStandardPickup1'] =  result['path_to_report_pickup']

                self.oUser.prefPath['ReportAddressLists'] =  result['path_to_report_address_lists']

                
        else:
            print 'no standard-Profile defined'
            
        self.oUser.refreshDicUser()
