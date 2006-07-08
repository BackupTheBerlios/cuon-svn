#! /usr/bin/python
#xmlrpc-server
from twisted.web import xmlrpc, resource, static
from twisted.internet import defer
from twisted.internet import reactor
from twisted.web import server

import cuon.CuonFuncs
import cuon.iCal
import cuon.basics
import cuon.Database
import cuon.User
import cuon.AI
import cuon.Address
import cuon.Article
import cuon.Stock
import cuon.Order
import cuon.Finances
import cuon.Misc
import cuon.Garden
import cuon.Report

import locale, gettext

print 'Start'
# localisation
APP = 'cuon_server'
DIR = '/usr/share/locale'
#locale.setlocale (locale.LC_ALL, '')

gettext.bindtextdomain (APP, DIR)
gettext.textdomain (APP)
gettext.install (APP,DIR,unicode=1)
_ = gettext.gettext 
s = gettext.find(APP)

print 'Gettext', s

s = _('Lastname')
print s

baseSettings = cuon.basics.basics()
print baseSettings.WEBPATH
r = cuon.CuonFuncs.CuonFuncs()
oiCal = cuon.iCal.iCal()
oDatabase = cuon.Database.Database()
oUser = cuon.User.User()
oStock = cuon.Stock.Stock()
oAI = cuon.AI.AI()

oAddress = cuon.Address.Address()
oArticle = cuon.Article.Article()
oOrder = cuon.Order.Order()
oFinances = cuon.Finances.Finances()
oMisc = cuon.Misc.Misc()
oGarden = cuon.Garden.Garden()
oReport = cuon.Report.Report()


r.putSubHandler('iCal', oiCal)
r.putSubHandler('Database', oDatabase)
r.putSubHandler('User', oUser)
r.putSubHandler('AI', oAI)
r.putSubHandler('Stock', oStock)
r.putSubHandler('Article', oArticle)
r.putSubHandler('Address', oAddress)
r.putSubHandler('Order', oOrder)
r.putSubHandler('Finances', oFinances)
r.putSubHandler('Misc', oMisc)
r.putSubHandler('Garden', oGarden)
r.putSubHandler('Report', oReport)

reactor.listenTCP(baseSettings.XMLRPC_PORT, server.Site(r))
reactor.run()


