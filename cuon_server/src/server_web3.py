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


@route('/hello/', method = 'GET')
def hello():
    return "Hello World!"
    

@route('/cuon/Glade/:name', method = 'GET')
def AllGlades(name):
    
    return send_file(name,  root='/var/www/cuon/Glade')
    

@route('/cuon/mimic/:name', method = 'GET')
def MimicLibs(name):
    
    return send_file(name,  root='/var/www/cuon/mimic')
    

@route('/cuon/:name', method = 'GET')
def AllSites(name):
    
    return send_file(name,  root='/var/www/cuon/')
    
@route('/RPC/', method = 'POST')
def AllXMLRPC():
    result = None
    print 'get xmlrpc'
    #print request 
    print request.environ
    #print 'end'
    env22  = request.environ['wsgi.input'].read(int(request.environ['CONTENT_LENGTH']))
    #print env22
    args = gridxml().xmltodict(env22)
    print 'args = ',  args
    #liFunction = args['methodName'].split()
    s = "result = sv." + args['methodName'][0] + "("
                                             
    if args['params']:
        print 'args[params] = ',  args['params']
        for par in args['params']:
            print 'par = ',  par
            liPars = par['param']
            for value in liPars:
                print 'value = ',  value
                keys =  value.keys()
                print 'keys = ',  keys
                for key in keys:
                    x1 = value[key]
                    print 'x1 = ',  x1
                    print 'x1[0] = ',  x1[0]
                    
                    
                    if x1[0].has_key('string'):
                        
                        s += "'" + x1[0]['string'][0] + "'" + ", "
        i = s.rfind(',')
        if i>0:
            s = s[:i]
            
    s += ")"
    print 'exe = ',  s
    print sv
    
    exec s
    print 'result = ',  result
    
    xml1 = "<?xml version='1.0'?><methodResponse><params><param><value>"
    
    if isinstance(result, types.StringType):
        print '1'
        xml1 += "<string>" + result + "</string>"
        #xml1 += "<int>" + `55` + "</int>"
        
        print '2'
        
    xml1 += "</value></param></params></methodResponse>"
    
    print "return xml1 = " ,  xml1
    #return "<?xml version='1.0'?><methodResponse><params><param><value><int>42</int></value></param></params></methodResponse>"
    return xml1
    
    
basic.WEB_HOST4 = "cuonsim1.de"


run(  port=basic.WEB_PORT4, host=basic.WEB_HOST4) # This starts the HTTP server






#from twisted.web import server, resource,  static
#from twisted.internet import reactor
#from cuon.basics import basics
#import cuon.WebAI
#
#openssl = False
#try:
#    from OpenSSL import SSL
#    openssl = True
#
#except:
#    pass
#    
#dicSession = {}
#
#def setAISite(request):
#    s = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">  
#    <html> <head> <title>Cyrus-Computer GmbH freie Software, Warenwirtschaft unter LINUX</title> <meta name="ROBOTS" content="NOINDEX, NOFOLLOW"> <meta http-equiv="content-type" content="text/html; charset=UTF-8"> 
#    <meta http-equiv="content-type" content="application/xhtml+xml; charset=UTF-8"> 
#    <meta http-equiv="content-style-type" content="text/css"> 
#    <meta http-equiv="expires" content="0"> 
#    <link rel="stylesheet" type="text/css" href="/cuon_ai.css" />  
#    </head> 
#    <body> 
#    <div id="page"> 
#    <div id="welcome">C.U.O.N. AI Connection</div> 
#    <div id="introtext">Please enter  your Question below :</div> 
#    <div id="login-block">      
#    <FORM ACTION="/aiquestion/" METHOD=POST> 
#    <div id="introtext"><p class="label">Question &nbsp;:<input class="txtInput" name="Question" type="text" size="60" maxlength="532"></p> </div>
#    <INPUT type="submit" value="Send"> 
#    </FORM> """ 
#    
#    s += dicSession[request.getSession().uid ]['AI_Session'] 
#        
#    s += """ <br /> <br />
#    </div> 
#    </div> 
#    </body> 
#    </html> """
#    return s
#
#def errorSite():
#    s = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">  
#    <html> <head> <title>Cyrus-Computer GmbH freie Software, Warenwirtschaft unter LINUX</title> <meta name="ROBOTS" content="NOINDEX, NOFOLLOW"> <meta http-equiv="content-type" content="text/html; charset=UTF-8"> 
#    <meta http-equiv="content-type" content="application/xhtml+xml; charset=UTF-8"> 
#    <meta http-equiv="content-style-type" content="text/css"> 
#    <meta http-equiv="expires" content="0"> 
#    <link rel="stylesheet" type="text/css" href="/var/cuon_www/AI/html/cuon_ai.css" />  
#    </head> 
#    <body> 
#    <div id="page"> 
#    <div id="welcome">Connection error</div> 
#    <div id="introtext">Please go back to the <a href="/">main site</a> and login again</div> 
#      </div> 
#    </div> 
#    </body> 
#    </html> """
#    return s
#def htmlConvert(sValue):
#    if sValue:
#        sValue = sValue.encode('utf-8')
#        sValue = sValue.replace('&', '&amp;')
#  
#        sValue = sValue.replace('\'', '&apos;')
#        sValue = sValue.replace('\"', '&quot; ')
#        sValue = sValue.replace('<', '&lt;')
#        sValue = sValue.replace('>', '&gt;')
#        
#        # for testing:
#        #sValue = sValue.replace('/', '')
#    return sValue
#class ServerContextFactory:
#
#    def getContext(self):
#        """Create an SSL context.
#
#        Similar to twisted's echoserv_ssl example, except the private key
#        and certificate are in separate files."""
#        ctx = SSL.Context(SSL.SSLv23_METHOD)
#        ctx.use_privatekey_file('/etc/cuon/serverkey.pem')
#        ctx.use_certificate_file('/etc/cuon/servercert.pem')
#        return ctx
#
#class TopLevel(resource.Resource,  basics):
#    isLeaf = True
#    
#    def __init__(self):
#        basics.__init__(self)
#        self.webAI = cuon.WebAI.WebAI()
#        
#    def getChild(self, name, request):
#        print 'getChild',  name,  request
#        if name == '':
#            return self
#        return Resource.getChild(self, name, request)
#    
#        
#    def render_GET(self, request):
#        print 'render',  request
#        print request.prepath
#        return "<html>Test</html>"
#        
#    def render_POST(self, request):
#        print 'render',  request
#        for field in request.args.keys():
#            print field,  request.args[field]
#        print 'Session',  request.getSession()
#        
#        print 'ID = ',  request.getSession().uid
#        print 'Path',  request.prepath
#        
#        Params = request.args
#        if request.prepath == ['newlogin']:
#            dicUser = self.webAI.getAuthorization(Params['Username'][0],  Params['Password'][0],  Params['ClientID'][0])
#            dicSession[request.getSession().uid ] = {}
#            dicSession[request.getSession().uid ]['CuonUser'] = dicUser
#            dicSession[request.getSession().uid ]['AI_Session'] = 'Begin Session'
#            return setAISite(request)
#            
#class AILevel(resource.Resource,  basics):
#    isLeaf = True
#    
#    def __init__(self):
#        basics.__init__(self)
#        self.webAI = cuon.WebAI.WebAI()
#        
#    
#        
#    def getChild(self, name, request):
#        print 'getChild',  name,  request
#        if name == '':
#            return self
#        return Resource.getChild(self, name, request)
#
#
#    def render_GET(self, request):
#        print 'render',  request
#        print request.prepath
#        return "<html>Test</html>"
#        
#    def render_POST(self, request):
#        print 'render',  request
#        for field in request.args.keys():
#            print field,  request.args[field]
#        print 'Session',  request.getSession()
#        print 'ID = ',  request.getSession().uid
#        print 'Path',  request.prepath
#        
#        
#        if request.prepath == ['aiquestion']:
#            print 'AI = ',  request.args
#            if dicSession.has_key(request.getSession().uid ):
#                aiAnswer =  self.webAI.getAnswer(request.args['Question'][0], dicSession[request.getSession().uid ]['CuonUser']  )
#                #print 'AI answer total = ',  aiAnswer
#                
#                
#                aiAnswer = htmlConvert(aiAnswer)
#                print aiAnswer
#                aiAnswer = """<div id="answer">""" + aiAnswer + """</div> \n  <div id="question">"""  + request.args['Question'][0] + """</div> \n\n"""
#                print aiAnswer
#                aiAnswer = aiAnswer.replace('\n', '<br />')
#                print aiAnswer
#                dicSession[request.getSession().uid ]['AI_Session']  = aiAnswer +  dicSession[request.getSession().uid ]['AI_Session'] 
#                return setAISite(request)
#            else:
#                return errorSite()
#
#    
#top = TopLevel()   
#ai = AILevel()
#
#try:    
#    port = int(sys.argv[1])
#except:
#    port = 0
#print port
#
#r = static.File("/var/cuon_www/")
##r.putChild("index", static.File("index.html"))
#r.putChild("login", static.File("top"))
#r.putChild("aiquestion", ai)
#
#
#reactor.listenTCP(top.WEB_PORT4+ port, server.Site(r))
#if openssl:
#    """Create an SSL context."""
#    
#    try:
#        reactor.listenSSL(top.WEB_PORT4 + top.SSL_OFFSET + port,  server.Site(r), ServerContextFactory())
#        print 'HTTPS activated'
#    except:
#        print 'Error by activating HTTPS. Please check /etc/cuon/serverkey.pem and /etc/cuon/servercert.pem.'
#
#reactor.run()
##
##top = TopLevel()
#
##site = server.Site(top)
##reactor.listenTCP(top.WEB_PORT4, site)
##reactor.run()
