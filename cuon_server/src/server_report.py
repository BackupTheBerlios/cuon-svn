#! /usr/bin/python
#xmlrpc-server
from twisted.web import xmlrpc, resource, static
from twisted.internet import defer
from twisted.internet import reactor
from twisted.web import server

import cuon.CuonFuncs
import cuon.ReportServer
# localisation
import locale, gettext


locale.setlocale (locale.LC_ALL, '')
APP = 'cuon_report'
DIR = '/usr/share/locale'

gettext.bindtextdomain (APP, DIR)
gettext.textdomain (APP)
gettext.install (APP, DIR, unicode=1)


baseSettings = cuon.basics.basics()
r = cuon.CuonFuncs.CuonFuncs()
oReportServer = cuon.ReportServer.ReportServer()


r.putSubHandler('ReportServer', oReportServer)

reactor.listenTCP(baseSettings.REPORT_PORT, server.Site(r))
reactor.run()


