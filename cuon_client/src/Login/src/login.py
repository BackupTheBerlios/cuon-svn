# -*- coding: utf-8 -*-

##Copyright (C) [2003]  [J�rgen Hamel, D-32584 L�hne]

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

    
    def __init__(self, eUserName):

        windows.__init__(self)
        self.eUserName = eUserName
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
            
		##elif response == gtk.RESPONSE_DELETE_EVENT:
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

       
        sid = self.rpc.callRP('src.Databases.py_createSessionID', self.oUser.getUserName(), sPw) 
        if sid:
            self.oUser.setSessionID(sid)
            self.loadProfile()

            self.openDB()
            self.saveObject('User', self.oUser)
            self.closeDB()
            print 'end Login'
            print str(self.oUser)

            self.eUserName.set_text(self.oUser.getUserName())
            self.quitLogin()

        else:
            print "No korrekt user and/or  password !"
            self.oUser.setUserName('EMPTY')
            self.quitLogin()

       
    def on_cancelbutton1_clicked(self, event):
        self.oUser.setUserName('EMPTY')
        
        self.quitLogin()

    def quitLogin(self):
        win1 = self.getWidget('UserID_Dialog')
        win1.hide()
