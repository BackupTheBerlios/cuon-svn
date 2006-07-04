#! /usr/bin/python
#xmlrpc-server
from twisted.web import xmlrpc, resource, static
from twisted.internet import defer
from twisted.internet import reactor
from twisted.web import server

import cuon.CuonFuncs
import cuon.ReportServer


baseSettings = cuon.basics.basics()
r = cuon.CuonFuncs.CuonFuncs()
oReportServer = cuon.ReportServer.ReportServer()


r.putSubHandler('ReportServer', oReportServer)

reactor.listenTCP(baseSettings.REPORT_PORT, server.Site(r))
reactor.run()


