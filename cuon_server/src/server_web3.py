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
from bottle import route, run,  request,  response,  send_file
from cuon.basics import basics
from cuon.WebAI import WebAI


basic = basics()
webai = WebAI()


#
#
##PUT /inventory/fb65174f-2dde-4c1e-ba13-1a776d6864fd
#@route('/inventory/:ID', method='PUT')
#def insertIntoInventory(ID):
#    # perhaps update ?, no answer ?
#    print 'Put Inventory,  hat to program soon',  ID
#    
#    return '<?xml version="1.0" encoding="utf-8"?><boolean>false</boolean>'
#    

rootsite = '/var/cuon_www/AI'
roothtml = rootsite + '/html/'

@route('/hello/', method = 'GET')
def hello():
    return "Hello World!"
   
@route('/')
def setRootSite():
    print 'Get cookies= ',  request.COOKIES
    return send_file('index.html', root=roothtml)
 

@route('/menu_navigation.js')
def setJSSite():
    return send_file('/menu_navigation.js', root=roothtml)
 
@route('/Login.html')
def setLoginSite():
    return send_file('Login.html', root=roothtml)
 
@route('/newlogin/' , method='POST')
def setCookie():
    
    env22  = request.environ['wsgi.input'].read(int(request.environ['CONTENT_LENGTH']))
    #xml_dict = dicxml.xml_to_dict(env22)[1]
    print 'Data = ',  env22
    dicAddress = {}
    if env22:
        print env22
        liValue = env22.split('&')
        for value in liValue:
            liAddress = value.split('=')
            if liAddress:
                dicAddress[liAddress[0].strip()] = liAddress[1].strip()
    for key in dicAddress.keys():
        print key,dicAddress[key]
        response.set_cookie(key,dicAddress[key], path='/', domain='localhost',  secure=False )

    #print response.COOKIES
    return '''<html><body>User login ok:  </br>'''+ dicAddress['Username'] +  '''</body></html>'''
    
    

@route('/:file')
def setSite(file):
    return send_file(file, root=roothtml)
 
 

run(  port=basic.WEB_PORT4, host=basic.WEB_HOST4) # This starts the HTTP server
