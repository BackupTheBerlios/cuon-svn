# -*- coding: utf-8 -*-
##Copyright (C) [2010]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 


from basics import basics
from xmlrpclib import ServerProxy


class WebAI(basics):
    def __init__(self):
        basics.__init__(self)
        print self.XMLRPC_PROTO + '://' +self.XMLRPC_HOST + ':' +  `self.XMLRPC_PORT`

        self.sv= ServerProxy(self.XMLRPC_PROTO + '://' +self.XMLRPC_HOST + ':' +  `self.XMLRPC_PORT`,  allow_none = 1)
        print self.sv.Database.is_running()
        
    def getAuthorization(self,  Username,  Password,  ClientID):
        ok = True
        #self.XMLRPC_PORT = 7080
        #self.XMLRPC_HOST = 'localhost'
        #self.XMLRPC_PROTO = "http"
        # Authorized
        print 'Server',  self.sv
        print Username,  Password
        
        sid = self.sv.Database.createSessionID( Username, Password)
        
        
        print sid
        # Set Information for cuon
        self.dicUser={'Name':Username,'SessionID':sid,'userType':'cuon',  'client':int(ClientID)}

        return self.dicUser
        
    def getAnswer(self,  question,  dicUser):
        return self.sv.AI.getAI(question,  dicUser)
        
        