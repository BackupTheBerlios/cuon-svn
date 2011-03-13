#! /usr/bin/python
#xmlrpc-server

from twisted.web import xmlrpc, resource, static
from twisted.internet import defer
from twisted.internet import reactor
from twisted.web import server
    
        

import cuon.CuonFuncs
import cuon.Web
import cuon.basics
import cuon.Database
import cuon.User
import cuon.AI
import cuon.Address
import cuon.Article
import cuon.Stock
import cuon.Order
import cuon.Projects
import cuon.Finances
import cuon.Misc
import cuon.Garden
import cuon.Report
import cuon.WebShop
import cuon.Email
import cuon.Grave
#import cuon.Tweet
import cuon.Support


openssl = False
try:
    from OpenSSL import SSL
    openssl = True

except:
    pass
    

import locale, gettext

class ServerContextFactory:

    def getContext(self):
        """Create an SSL context.

        Similar to twisted's echoserv_ssl example, except the private key
        and certificate are in separate files."""
        ctx = SSL.Context(SSL.SSLv23_METHOD)
        ctx.use_privatekey_file('/etc/cuon/serverkey.pem')
        ctx.use_certificate_file('/etc/cuon/servercert.pem')
        return ctx


class ServerData:
    def __init__(self):
        pass
        
    def getSite(self):

        
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
        oWeb = cuon.Web.Web()
        oDatabase = cuon.Database.Database()
        oUser = cuon.User.User()
        oStock = cuon.Stock.Stock()
        oAI = cuon.AI.AI()
        
        oAddress = cuon.Address.Address()
        oArticle = cuon.Article.Article()
        oOrder = cuon.Order.Order()
        oProjects = cuon.Projects.Projects()
        oFinances = cuon.Finances.Finances()
        oMisc = cuon.Misc.Misc()
        oGarden = cuon.Garden.Garden()
        oReport = cuon.Report.Report()
        oWebShop = cuon.WebShop.WebShop()
        oEmail = cuon.Email.cuonemail()
        oGrave = cuon.Grave.Grave()
        #oTweet = cuon.Tweet.Tweet()
        oSupport = cuon.Support.Support()
        
        r.putSubHandler('Web', oWeb)
        r.putSubHandler('Database', oDatabase)
        r.putSubHandler('User', oUser)
        r.putSubHandler('AI', oAI)
        r.putSubHandler('Stock', oStock)
        r.putSubHandler('Article', oArticle)
        r.putSubHandler('Address', oAddress)
        r.putSubHandler('Order', oOrder)
        r.putSubHandler('Projects', oProjects)
        r.putSubHandler('Finances', oFinances)
        r.putSubHandler('Misc', oMisc)
        r.putSubHandler('Garden', oGarden)
        r.putSubHandler('Report', oReport)
        r.putSubHandler('WebShop', oWebShop)
        r.putSubHandler('Email', oEmail)
        r.putSubHandler('Grave', oGrave)
        #r.putSubHandler('Tweet', oTweet)
        r.putSubHandler('Support', oSupport)
        return r 

##reactor.listenTCP(baseSettings.XMLRPC_PORT, server.Site(r))
##if openssl:
##   """Create an SSL context."""
##    
##    
##    reactor.listenSSL(baseSettings.XMLRPC_PORT + baseSettings.SSL_OFFSET,  server.Site(r), ServerContextFactory())
##    print 'HTTPS activated'
##
##reactor.run()
