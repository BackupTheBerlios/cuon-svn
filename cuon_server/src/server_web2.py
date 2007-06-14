#! /usr/bin/python
#xmlrpc-server
from twisted.web import xmlrpc, resource, static
from twisted.internet import defer
from twisted.internet import reactor
from twisted.web import server
from nevow import livepage, tags, loaders, appserver

from twisted.application import internet
from twisted.application import service

from zope.interface import implements

from nevow import inevow

import cuon.CuonFuncs
import cuon.basics

baseSettings = cuon.basics.basics()
print baseSettings.WEBPATH
#r = cuon.CuonFuncs.CuonFuncs()


#r.putSubHandler('iCal', oiCal)

##class LiveExamplePage(livepage.LivePage):
##    docFactory = loaders.stan(
##        tags.html[
##            tags.head[
##                livepage.glue],
##            tags.body[
##                tags.input(
##                    type="text",
##                    onchange="server.handle('change', this.value)")]])
##
##    def handle_change(self, ctx, value):
##        return livepage.alert(value)
##
##site = appserver.NevowSite(LiveExamplePage())
##reactor.listenTCP(baseSettings.WEB_PORT2, site)
from zope.interface import implements

from nevow import inevow

##
## How does a request come to the Page?
##
## or How to use Nevow without all the fancy automations
##


s1 = 'class Root(object):\n'
s1 +='\timplements(inevow.IResource)\n'
s1 +='\n'
s1 +='\tdef locateChild(self, ctx, segments):\n'
s1 +='\t\tif segments[0] == \'\':\n'
s1 +='\t\t\treturn self, ()\n'
s1 +='\t\telif segments[0] == \'foo\':\n'
s1 +='\t\t\treturn self.foo, segments[1:]\n'
s1 +='\t\telse:\n'
s1 +='\t\t\treturn None, ()\n'
s1 +='\t\t\n'
s1 +='\tdef renderHTTP(self, ctx):\n'
s1 +='\t\treturn """<html><body>Hello world!<br />\n'
s1 +='\t\t<a href="./foo" id="foo">foo</a></body></html>\n'
s1 += '""" \n'

print s1 
exec (s1)

class Foo(object):
    implements(inevow.IResource)
    
    def locateChild(self, ctx, segments):
        # segments is the remaining segments returned by the root locateChild
        # see segments[1:]
        if segments[0] == 'baz':
            return self.baz, segments[1:]
        else:
            return None, ()
    
    def renderHTTP(self, ctx):
        return """<html><body><h1 id="heading">You are in Foo</h1>
        <a href="./foo/baz" id="baz">baz</a></body></html>
"""

class Baz(object):
    implements(inevow.IResource)
    def locateChild(self, ctx, segments):
        return None, ()
    def renderHTTP(self, ctx):
        return '<html><body><h1 id="heading">You are in Baz</h1></body></html>'

# We are adding children to the pages.
# This could also happen inside the class.
exec (s1)
exec('root = Root()') 
root.foo = Foo()
root.foo.baz = Baz()
#internet.TCPServer(baseSettings.WEB_PORT2, appserver.NevowSite(RootPage())).setServiceParent(application)

site = appserver.NevowSite(root)
reactor.listenTCP(baseSettings.WEB_PORT2, site)

reactor.run()



