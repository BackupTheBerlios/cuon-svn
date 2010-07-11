#! /usr/bin/python
#xmlrpc-server
from twisted.web import xmlrpc, resource, static
from twisted.internet import defer
from twisted.internet import reactor
from twisted.web import server

import cuon.CuonFuncs
import cuon.basics




baseSettings = cuon.basics.basics()
print baseSettings.WEBPATH
#r = cuon.CuonFuncs.CuonFuncs()


#r.putSubHandler('iCal', oiCal)



site = server.Site(static.File(baseSettings.WEBPATH))
reactor.listenTCP(baseSettings.WEB_PORT, server.Site(site))
reactor.run()
