#!/usr/bin/python
# -*- coding: utf-8 -*-
##Copyright (C) [2010]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 



import bottle
from bottle import route, run,  request,  response
from bottle import send_file, redirect, abort

from cuon.basics import basics
from xmlrpclib import ServerProxy
from cuon.gridxml import  gridxml
import types


basic = basics()

sv= ServerProxy(basic.XMLRPC_PROTO + '://' +basic.XMLRPC_HOST + ':' +  `basic.XMLRPC_PORT`,  allow_none = 1)
web3user = basic.WEB_USER3

dicUser = {}

def getAuth():
    dicUser=sv.Support.getAuthorization(basic.WEB_USER3 ,  basic.WEB_PASSWORD3,  basic.WEB_CLIENT_ID3 )
        
    return dicUser
    
    
    
@route('/hello/', method = 'GET')
def hello():
    print self.sv.Database.is_running()
    return "Hello World! " + `self.sv.Database.is_running()`


@route('/:name',  method = 'GET')
def sendFile(name):
    dicUser = getAuth()
    return send_file(name, root='/var/www/cuon/Support')
    
    
 
    

run(  port=basic.WEB_PORT3, host=basic.WEB_HOST3) # This starts the HTTP server
