#! /usr/bin/python
#xmlrpc-server
from twisted.web import xmlrpc, resource, static
from twisted.internet import defer
from twisted.internet import reactor
from twisted.web import server
import sys
import cuon.CuonFuncs
import cuon.ReportServer


baseSettings = cuon.basics.basics()


r = cuon.CuonFuncs.CuonFuncs()
oReportServer = cuon.ReportServer.ReportServer()


r.putSubHandler('ReportServer', oReportServer)


try:    
    port = int(sys.argv[1])
except:
    port = 0
print port
print baseSettings.REPORT_PORT ,  port,  baseSettings.REPORT_PORT + port
print sys.argv

reactor.listenTCP(baseSettings.REPORT_PORT + port, server.Site(r))
reactor.run()


