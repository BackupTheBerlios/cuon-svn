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
from zope.interface import implements

from nevow import inevow

import cuon.CuonFuncs
import cuon.basics
import cuon.Web2

baseSettings = cuon.basics.basics()
print baseSettings.WEBPATH

oWeb2 = cuon.Web2.Web2()


def getRootSite():
    roots = oWeb2.getRootElement()
    liRootChilds = []
    rootSite = roots['data']
    rootChilds = roots['linked_keys']
    if rootChilds:
        liRootChilds = rootChilds.split(',')
        
    
    
    
    rootClass = 'class Root(object):\n'
    rootClass +='\timplements(inevow.IResource)\n'
    rootClass +='\n'
    rootClass +='\tdef locateChild(self, ctx, segments):\n'
    rootClass +='\t\tif segments[0] == \'\':\n'
    rootClass +='\t\t\treturn self, ()\n'
    if liRootChilds:
        z = 0
        for child in liRootChilds:
            if z == 0:
                rootClass +='\t\tif segments[0] == \'' + child + '\':\n'
            else:
                rootClass +='\t\telif segments[0] == \'' + child + '\':\n'
            rootClass +='\t\t\treturn self.' + child.strip() + ', segments[1:]\n'
            z += 1
        rootClass +='\t\telse:\n'
        rootClass +='\t\t\treturn None, ()\n'
    else:
        rootClass +='\t\treturn None, ()\n'
    rootClass +='\t\t\n'
    rootClass +='\tdef renderHTTP(self, ctx):\n'
    rootClass +='\t\treturn """' + rootSite + '""" \n'
    print '-------------------------------------------------------------------'
    print rootClass
    print '-------------------------------------------------------------------'
    
    return rootClass 

def getHtmlSite(dicHtmlSite):
    
    liChilds = []
    Childs = dicHtmlSite['linked_keys']
    if Childs:
        liChilds = Childs.split(',')
        
    
    htmlClass = 'class ' + dicHtmlSite['name'].strip() + '(object):\n'
    htmlClass +='\timplements(inevow.IResource)\n'
    htmlClass +='\n'
    htmlClass +='\tdef locateChild(self, ctx, segments):\n'
    if liChilds:
        z = 0
        for child in liChilds:
            if z == 0:
                htmlClass +='\t\tif segments[0] == \'' + child + '\':\n'
            else:
                htmlClass +='\t\telif segments[0] == \'' + child + '\':\n'
            htmlClass +='\t\t\treturn self.' + child.strip() + ', segments[1:]\n'
            z += 1
        htmlClass +='\t\telse:\n'
        htmlClass +='\t\t\treturn None, ()\n'
    else:
        htmlClass +='\t\treturn None, ()\n'
    
    htmlClass +='\t\t\n'
    htmlClass +='\tdef renderHTTP(self, ctx):\n'
    htmlClass +='\t\treturn """' + dicHtmlSite['data'] + '""" \n'
    print '-------------------------------------------------------------------'
    print htmlClass
    print '-------------------------------------------------------------------'
    
    return htmlClass 
    
#First save Images
    
# begin consdtruct websites    
    
    
rootClass = getRootSite()

exec (rootClass)
exec('root = Root()') 

liSites = ['root','MainLeft']
for sName in liSites:
    IDs = oWeb2.getAllSiteElementIDs(sName)
    if IDs and IDs != 'NONE':
        for id in IDs:
            dicHtmlSite = oWeb2.getSiteElementByID(id['id'])
            if dicHtmlSite and dicHtmlSite != 'NONE':
                print 'dicHtmlSite = ', dicHtmlSite
                htmlClass = getHtmlSite(dicHtmlSite[0])
                exec (htmlClass)
                liRootKeys = dicHtmlSite[0]['root_keys'].split(',')
                if liRootKeys:
                    for key in liRootKeys:
                        s =  key.strip() +"." + dicHtmlSite[0]['name'].strip() + " = " + dicHtmlSite[0]['name'].strip() + "()"
                        print 's-root = ', s
                        exec ( s)
# We are adding children to the pages.
# This could also happen inside the class.


#root.foo = Foo()
#root.foo.baz = Baz()
#internet.TCPServer(baseSettings.WEB_PORT2, appserver.NevowSite(RootPage())).setServiceParent(application)

site = appserver.NevowSite(root)
reactor.listenTCP(baseSettings.WEB_PORT2, site)

reactor.run()

#<html><body>Hello world!<br />\n'
#rootClass +='\t\t<a href="./foo" id="foo">foo</a></body></html>

##class TabbedPage(rend.Page):
##    addSlash = True
##    docFactory = loaders.stan(
##        t.html[
##            t.head[
##                t.title["Tabbed Page Example"],
##                tabbedPane.tabbedPaneGlue.inlineGlue
##            ],
##            t.body[
##                t.invisible(data=t.directive("pages"),
##                            render=tabbedPane.tabbedPane)
##            ]
##        ]
##    )
##    
##    def data_pages(self, ctx, data):
##        return {"name": "outer",
##                "selected": 1,
##                "pages": (("One", t.p["First One"]),
##                          ("Two", t.p["Second One"]),
##                          ("Three", t.p[t.invisible(
##                            render = tabbedPane.tabbedPane,
##                            data = {"name":  "inner",
##                                    "pages": (("Four", t.p["Fourth One"]),
##                                              ("Five", t.p["Fifth One"])) })]
##                           ))}
##
##class Foo(object):
##    implements(inevow.IResource)
##    
##    def locateChild(self, ctx, segments):
##        # segments is the remaining segments returned by the root locateChild
##        # see segments[1:]
##        if segments[0] == 'baz':
##            return self.baz, segments[1:]
##        else:
##            return None, ()
##    
##    def renderHTTP(self, ctx):
##        return """<html><body><h1 id="heading">You are in Foo</h1>
##        <a href="./foo/baz" id="baz">baz</a></body></html>
##"""
##
##class Baz(object):
##    implements(inevow.IResource)
##    def locateChild(self, ctx, segments):
##        return None, ()
##    def renderHTTP(self, ctx):
##        return '<html><body><h1 id="heading">You are in Baz</h1></body></html>'
