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

from twisted.web import server, resource,  static
from twisted.internet import reactor
from cuon.basics import basics
import cuon.WebAI

openssl = False
try:
    from OpenSSL import SSL
    openssl = True

except:
    pass
    
    
class ServerContextFactory:

    def getContext(self):
        """Create an SSL context.

        Similar to twisted's echoserv_ssl example, except the private key
        and certificate are in separate files."""
        ctx = SSL.Context(SSL.SSLv23_METHOD)
        ctx.use_privatekey_file('/etc/cuon/serverkey.pem')
        ctx.use_certificate_file('/etc/cuon/servercert.pem')
        return ctx

class TopLevel(resource.Resource,  basics):
    isLeaf = True
    
    def __init__(self):
        basics.__init__(self)
        self.WebAI = cuon.WebAI.WebAI()
        
    def getChild(self, name, request):
        print 'getChild',  name,  request
        if name == '':
            return self
        return Resource.getChild(self, name, request)


    def render_GET(self, request):
        print 'render',  request
        print request.prepath
        return "<html>Test</html>"
        
    def render_POST(self, request):
        print 'render',  request
        print request.prepath
        return "<html>Test</html>"
        
top = TopLevel()   
try:    
    port = int(sys.argv[1])
except:
    port = 0
print port
r = static.File("/var/cuon_www/AI/html")
r.putChild("index", static.File("index.html"))
r.putChild('newlogin',  top)
reactor.listenTCP(top.WEB_PORT4+ port, server.Site(r))
if openssl:
    """Create an SSL context."""
    
    try:
        reactor.listenSSL(top.WEB_PORT4 + top.SSL_OFFSET + port,  server.Site(r), ServerContextFactory())
        print 'HTTPS activated'
    except:
        print 'Error by activating HTTPS. Please check /etc/cuon/serverkey.pem and /etc/cuon/servercert.pem.'

reactor.run()
#
#top = TopLevel()

#site = server.Site(top)
#reactor.listenTCP(top.WEB_PORT4, site)
#reactor.run()
