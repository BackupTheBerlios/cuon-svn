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
from bottle import route, run,  request,  response,  template
from bottle import send_file, redirect, abort

from cuon.basics import basics
from xmlrpclib import ServerProxy
from cuon.gridxml import  gridxml
import types


basic = basics()

sv= ServerProxy(basic.XMLRPC_PROTO + '://' +basic.XMLRPC_HOST + ':' +  `basic.XMLRPC_PORT`,  allow_none = 1)
web3user = basic.WEB_USER3

dicUser = {}
rootDir = '/var/cuon_www/SupportTicket/'
print bottle.TEMPLATE_PATH 
bottle.TEMPLATE_PATH = [rootDir +'views/']
bottle.TEMPLATES.clear()

def getAuth():
    print 'get Auth'
    dicUser=sv.Support.getAuthorization(basic.WEB_USER3 ,  basic.WEB_PASSWORD3,  basic.WEB_CLIENT_ID3 )
    #print request.environ
    
    #env22  = request.environ['wsgi.input'].read(int(request.environ['CONTENT_LENGTH']))
    #print env22
    #args = gridxml().xmltodict(env22)   
    #print args
    
    return dicUser
    
    
    
@route('/hello/', method = 'GET')
def hello():
    print "test the db"
    print sv
    print sv.Database.is_running()
    print request.environ
    return "Hello World! " + `sv.Database.is_running()`

@route('/index.html',  method = 'GET')
@route('/',  method = 'GET')
def sendIndexFile():
    bottle.TEMPLATES.clear()
    dicUser = getAuth()
    print dicUser
    
    print bottle.TEMPLATE_PATH 
    result = sv.Support.getProjects(dicUser)
    print result
    
    output = template('index_example',   rows=result)

    
    
    return output
    
    
@route('/show_tickets/:id',  method = 'GET')
def showTicketsForProject(id):
    bottle.TEMPLATES.clear()
    dicUser = getAuth()
    print dicUser
    response.set_cookie("SupportProjectID", id)
    
    result = sv.Support.getTickets(dicUser,  id )
    print result
    
    output = template('showTickets_example',   rows=result)

    
    
    return output
    
      
@route('/show_ticket_details/:id',  method = 'GET')
def showTicket_details(id):
    bottle.TEMPLATES.clear()
    dicUser = getAuth()
    print dicUser
    prID = request.get_cookie("SupportProjectID")
    print 'Cookie ID = ',  prID
    
    
    result = sv.Support.getTicketDetails(dicUser,  id )
    print result
    
    output = template('showTicketDetails_example',   rows=result)

    
    
    return output
     
    
@route('/:name',  method = 'GET')
def sendOtherFiles(name):
    print "sendfile called"
    return send_file(name, root=rootDir)
    

run(  port=basic.WEB_PORT3, host=basic.WEB_HOST3, reloader=True) # This starts the HTTP server
