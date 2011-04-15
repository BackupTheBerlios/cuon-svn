#! /usr/bin/python
#xmlrpc-server

from twisted.web import xmlrpc, resource, static
from twisted.internet import defer
from twisted.internet import reactor
from twisted.web import server
import maintwxmlrpc    
import cuon.basics
import sys

baseSettings = cuon.basics.basics()

openssl = False
try:
    from OpenSSL import SSL
    openssl = True

except:
    pass
    
print 'Openssl = ', openssl
import locale, gettext
m = maintwxmlrpc.ServerData()
r = m.getSite()
try:    
    port = int(sys.argv[1])
except:
    port = 0
print port


if baseSettings.XMLRPC_ALLOW_HTTP :
    reactor.listenTCP(baseSettings.XMLRPC_HTTP_PORT + port, server.Site(r))


if openssl:
    """Create an SSL context."""
    
    try:
        reactor.listenSSL(baseSettings.XMLRPC_HTTPS_PORT +  port,  server.Site(r), maintwxmlrpc.ServerContextFactory())
        print 'HTTPS activated'
    except:
        print 'Error by activating HTTPS. Please check /etc/cuon/serverkey.pem and /etc/cuon/servercert.pem.'

reactor.run()
