<?xml version="1.0" encoding="UTF-8"?>
<leo_file>
<leo_header file_format="2" tnodes="0" max_tnode_index="0" clone_windows="0"/>
<globals body_outline_ratio="0.5">
	<global_window_position top="0" left="0" height="742" width="1137"/>
	<global_log_window_position top="0" left="0" height="0" width="0"/>
</globals>
<preferences>
</preferences>
<find_panel_settings>
	<find_string></find_string>
	<change_string></change_string>
</find_panel_settings>
<vnodes>
<v t="jhamel.111403174330" a="V"><vh>Login</vh>
<v t="jhamel.111403174330.1" tnodeList="jhamel.111403174330.1"><vh>@file __init__.py</vh></v>
<v t="jhamel.111403174330.2" tnodeList="jhamel.111403174330.2,jhamel.111403174330.3,jhamel.111403174330.4,jhamel.111403174330.5,jhamel.111403174330.6,jhamel.111403174330.7,jhamel.111403174330.8"><vh>@file login.py</vh>
<v t="jhamel.111403174330.3"><vh>&lt;&lt; login declarations &gt;&gt;</vh></v>
<v t="jhamel.111403174330.4"><vh>class loginwindow</vh>
<v t="jhamel.111403174330.5"><vh>__init__</vh></v>
<v t="jhamel.111403174330.6"><vh>okButtonPressed</vh></v>
<v t="jhamel.111403174330.7"><vh>on_okcancel1_clicked</vh></v>
<v t="jhamel.111403174330.8"><vh>quitLogin</vh></v>
</v>
</v>
<v t="jhamel.111403174330.9" tnodeList="jhamel.111403174330.9,jhamel.111403174330.10,jhamel.111403174330.11,jhamel.111403174330.12,jhamel.111403174330.13,jhamel.111403174330.14,jhamel.111403174330.15,jhamel.111403174330.16"><vh>@file User.py</vh>
<v t="jhamel.111403174330.10"><vh>&lt;&lt; User declarations &gt;&gt;</vh></v>
<v t="jhamel.111403174330.11"><vh>class User</vh>
<v t="jhamel.111403174330.12"><vh>__init__</vh></v>
<v t="jhamel.111403174330.13"><vh>refreshDicUser</vh></v>
<v t="jhamel.111403174330.14"><vh>getDicUser</vh></v>
<v t="jhamel.111403174330.15"><vh>setUserName</vh></v>
<v t="jhamel.111403174330.16"><vh>setUserPassword</vh></v>
</v>
</v>
</v>
</vnodes>
<tnodes>
<t tx="jhamel.111403174330"></t>
<t tx="jhamel.111403174330.1">@root src/Login/src/__init__.py
@language python
__all__ = ['User' 'login']
</t>
<t tx="jhamel.111403174330.2">@root src/Login/src/login.py
@language python
&lt;&lt; login declarations &gt;&gt;
@others
</t>
<t tx="jhamel.111403174330.3">##Copyright (C) [2003]  [Jürgen Hamel, D-32584 Löhne]

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

</t>
<t tx="jhamel.111403174330.4">class loginwindow(windows):
	@others
</t>
<t tx="jhamel.111403174330.5">def __init__(self):

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
</t>
<t tx="jhamel.111403174330.6">    ##elif response == gtk.RESPONSE_HELP:
    ##    print "Hilfe"
        
##        elif response == gtk.RESPONSE_DELETE_EVENT:
    ##else:
    ##print "else"
        
        

#def on_okbutton1_clicked(self, event):
def okButtonPressed(self):
    
    obj = AES.new('Th77777777key456', AES.MODE_ECB)

    self.oUser.setUserName( self.getWidget('TUserID').get_text())
    sPw = self.getWidget('TPassword').get_text()
    while(len(sPw) &lt; 16):
        sPw= sPw +' '
    print len(sPw)    
   
    self.oUser.setUserPassword(obj.encrypt(sPw))
    
    print self.oUser.userPassword
    print  obj.decrypt(self.oUser.userPassword)

    sPw = string.replace(sPw,' ','')
    print len(sPw)
    self.saveObject('User', self.oUser)
    self.quitLogin()
</t>
<t tx="jhamel.111403174330.7">def on_okcancel1_clicked(self, event):
    self.quitLogin()
</t>
<t tx="jhamel.111403174330.8">def quitLogin(self):
    win1 = self.getWidget('UserID_Dialog')
    win1.hide()
</t>
<t tx="jhamel.111403174330.9">@root src/Login/src/User.py
@language python
&lt;&lt; User declarations &gt;&gt;
@others
</t>
<t tx="jhamel.111403174330.10">##Copyright (C) [2003]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 
import os.path

from cuon.Windows.windows import windows


</t>
<t tx="jhamel.111403174330.11">class User:
	@others
</t>
<t tx="jhamel.111403174330.12">def __init__(self):
    
    self.userName = 'EMPTY'
    self.userPassword = 'EMPTY'
    
    # setting for locales
    self.userLocales ='de'
    self.userEncoding = 'utf-7'
    self.userDateTimeFormatString = "%d.%m.%Y"
    self.serverAddress = None
    self.userSQLDateFormat = 'DD.MM.YYYY'
    self.userSQLTimeFormat = 'HH24:MI'

    self.dicUser = {}
    
    
    
    # setting for files and path
    self.pathAddressPhoneListing1 = os.path.abspath('.')
    print  self.pathAddressPhoneListing1
</t>
<t tx="jhamel.111403174330.13">def refreshDicUser(self):
    self.dicUser['Locales'] = self.userLocales
    self.dicUser['Encoding'] = self.userEncoding
    self.dicUser['DateTimeformatString'] = self.userDateTimeFormatString
    #self.dicUser['serverAddress'] = self.serverAddress
    self.dicUser['SQLDateFormat'] = self.userSQLDateFormat
    self.dicUser['SQLTimeFormat'] = self.userSQLTimeFormat
    self.dicUser['Name'] = self.userName
</t>
<t tx="jhamel.111403174330.14">    #self.dicUser['Password'] = self.userPassword

def getDicUser(self):
    return self.dicUser
</t>
<t tx="jhamel.111403174330.15">def setUserName(self, s):
    self.userName = s
    self.refreshDicUser()
</t>
<t tx="jhamel.111403174330.16">def setUserPassword(self, s):
    self.userPassword = s
    self.refreshDicUser()
</t>
</tnodes>
</leo_file>
