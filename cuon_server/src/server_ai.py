#! /usr/bin/python
#xmlrpc-server
from twisted.web import xmlrpc, resource, static
from twisted.internet import defer
from twisted.internet import reactor
from twisted.web import server

import cuon.CuonFuncs
import cuon.ai
import cuon.basics

baseSettings = cuon.basics.basics()
print baseSettings.CUON_WEBPATH
r = cuon.CuonFuncs.CuonFuncs()
oAI = cuon.ai.ai()

print 'AI-Server start'
r.putSubHandler('AI', oAI)

reactor.listenTCP(baseSettings.PORT_AI, server.Site(r))
reactor.run()


