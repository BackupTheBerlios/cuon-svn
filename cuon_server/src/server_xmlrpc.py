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

reactor.listenTCP(baseSettings.XMLRPC_PORT + port, server.Site(r))
if openssl:
    """Create an SSL context."""
    
    
    reactor.listenSSL(baseSettings.XMLRPC_PORT + baseSettings.SSL_OFFSET + port,  server.Site(r), maintwxmlrpc.ServerContextFactory())
    print 'HTTPS activated'

reactor.run()
