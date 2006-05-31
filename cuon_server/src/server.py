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
import cuon.Order
import cuon.Finances

baseSettings = cuon.basics.basics()
print baseSettings.CUON_WEBPATH
r = cuon.CuonFuncs.CuonFuncs()
oiCal = cuon.iCal.iCal()
oDatabase = cuon.Database.Database()
oUser = cuon.User.User()
oAI = cuon.AI.AI()
oAddress = cuon.Address.Address()
oArticle = cuon.Article.Article()
oOrder = cuon.Order.Order()
oFinances = cuon.Finances.Finances()


r.putSubHandler('iCal', oiCal)
r.putSubHandler('Database', oDatabase)
r.putSubHandler('User', oUser)
r.putSubHandler('AI', oAI)
r.putSubHandler('Article', oArticle)
r.putSubHandler('Address', oAddress)
r.putSubHandler('Order', oOrder)
r.putSubHandler('Finances', oFinances)


reactor.listenTCP(7080, server.Site(r))
#reactor.run()

site = server.Site(static.File(baseSettings.CUON_WEBPATH))
reactor.listenTCP(7081, server.Site(site))
reactor.run()



