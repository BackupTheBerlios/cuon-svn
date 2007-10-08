#! /usr/bin/python
#xmlrpc-server
from twisted.web import xmlrpc, resource
#from twisted.web.resource import Resource
from twisted.internet import defer
from twisted.internet import reactor
from twisted.web import server
from twisted.application import internet
from twisted.application import service

from nevow import livepage,  loaders, appserver
from nevow import inevow, static, url, rend 
from nevow import accessors, tags as T
from twisted.python.components import registerAdapter


from zope.interface import implements



import cuon.CuonFuncs
import cuon.basics
import cuon.Web2
import sys
import os 
import commands

baseSettings = cuon.basics.basics()
print baseSettings.WEBPATH

oWeb2 = cuon.Web2.Web2()
commands.getstatusoutput('mkdir ' + baseSettings.WEBPATH + 'counter')
# 0 = Root-site
# 1 = Linked-Site
# 2 = Python code
# 3 = Directory structure
TypeRootSite = 0
TypeLinkedSite = 1
TypePython = 2
TypeDir = 3
TypeImage = 4
TypeFile = 5
        
class Image:
    """An image consisting of a filename and some comments.
    """
    def __init__(self, filename, comments):
        self.filename = filename
        self.comments = comments
  


        
# Register the adapter so Nevow can access Image instance attributes.
registerAdapter(accessors.ObjectContainer, Image, inevow.IContainer)


# Just a list of images to render in the page.
images = [Image('/var/cuon_www/images/screenshots/Screenshot-1.jpg', ['Meeow', 'Purrrrrrrr']) ]
    
oDirs = {}
dirs = []
def start():
    # create data structure
    liResult = oWeb2.getDirectoryStructure()
    if liResult and liResult not in ['NONE','ERROR']:
        for result in liResult:
            result['data'] = baseSettings.rebuild(result['data'])
            liDirs = result['data'].split(',')
            for sDir in liDirs:
                sDir = sDir.strip()
                sKey = sDir[sDir.rfind('/')+1:]
                sDir = baseSettings.WEBPATH + sDir
                print 'sDir = ', sDir
                sCommand = 'if [ ! -d ' + sDir + ' ] ; then mkdir ' + sDir + ' ; fi '
                print sCommand
                status,output = commands.getstatusoutput(sCommand)
                oDirs[sKey] = sDir
    #now save Images
    liResult = oWeb2.getImageIDs()
    if liResult and liResult not in ['NONE','ERROR']:
        for result in liResult:
            try:
                id = result['id']
                print id
                image = oWeb2.getSiteElementByID(id)[0]
                sDir = image['save_to_dir'].strip()
                name = image['name'].strip()
                if not sDir[len(sDir)-1] == '/':
                    sDir += '/'
                print name
                print sDir
                filename = baseSettings.WEBPATH + sDir + name
                print filename
                f = open(filename,'wb')
                f.write(baseSettings.rebuild(image['data']))
                f.close
            except Exception, params:
                print Exception,  params
                
            
def getRootSite():
    #child_images = static.File('images/')
    roots = oWeb2.getRootElement()
    liRootChilds = []
    rootSite = baseSettings.rebuild(roots['data'])
    rootChilds = roots['linked_keys']
    if rootChilds:
        liRootChilds = rootChilds.split(',')
        
    
    for newDir in oDirs.keys():
        liRootChilds.append(newDir)
    print liRootChilds
    
    rootClass = 'class Root(object):\n'
    rootClass +='\timplements(inevow.IResource)\n'
    rootClass +='\n'
    #rootClass += "\tchild_images = static.File('/images')\n"

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
    print 'dicHtmlSite', dicHtmlSite
    htmlClass = None
    liChilds = []
    if dicHtmlSite and dicHtmlSite not in ['NONE','ERROR'] :
        try:
            Childs = dicHtmlSite['linked_keys']
            if Childs:
                liChilds = Childs.split(',')
        except:
            pass
    
        
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
        htmlClass +='\t\tcounter(\'' + dicHtmlSite['name'].strip() +'\')\n'
    
        htmlClass +='\t\treturn """' + baseSettings.rebuild(dicHtmlSite['data']) + '""" \n'
        #print '-------------------------------------------------------------------'
        #print htmlClass
        #print '-------------------------------------------------------------------'
        
    return htmlClass 



    
class ImagePage(rend.Page):
    """A simple page that renders a list of images. We registered an adapter
    earlier so that the data= directives inside the pattern can look inside
    Image instances.
    """
    
    addSlash = True
    
    def render_images(self, ctx, data):
        """Render a list of images.
        """
        tag = T.div(data=images, render=rend.sequence)[
            T.div(pattern='item')[
                T.p(data=T.directive('filename'), render=T.directive('data')),
                T.ul(data=T.directive('comments'), render=rend.sequence)[
                    T.li(pattern='item', render=T.directive('data')),
                    ],
                ],
            ]
        return tag
        
    docFactory = loaders.stan( T.html[T.body[T.directive('images')]] )
        
# init server data
start()

# begin consdtruct websites    
    
def counter(sName):
    print 'sName =',sName
    fName = baseSettings.WEBPATH + 'counter/' + sName +'.counter'
    print 'fname = ', fName
    try:
        f = open(fName,'r')

        z1 = int(f.readline().strip())
        
    except:
        z1 = 0
    try:
        f.close()
    except:
        pass
    f = open(fName,'w')    
    z1 += 1
    f.write(`z1`)
    f.close()
    
    
    
rootClass = getRootSite()

exec (rootClass)
exec('root = Root()') 



#liSites = ['root','MainLeft']
liSites = oWeb2.getLinkedStructure()
print 'lisites = ', liSites
for sName in liSites:
    IDs = oWeb2.getAllSiteElementIDs(sName)
    if IDs and IDs not in ['NONE','ERROR']:
        for id in IDs:
            dicHtmlSite = oWeb2.getSiteElementByID(id['id'],  TypeLinkedSite)
            if dicHtmlSite and dicHtmlSite not in ['NONE','ERROR']:
                #print 'dicHtmlSite = ', dicHtmlSite
                htmlClass = getHtmlSite(dicHtmlSite[0])
                if htmlClass:
                    exec (htmlClass)
                    liRootKeys = dicHtmlSite[0]['root_keys'].split(',')
                    if liRootKeys:
                        for key in liRootKeys:
                            s =  key.strip() +"." + dicHtmlSite[0]['name'].strip() + " = " + dicHtmlSite[0]['name'].strip() + "()"
                            print 's-root = ', s
                            try:
                                exec (s)
                            except Exception, params:
                                print Exception,params
                                
            dicHtmlSite = oWeb2.getSiteElementByID(id['id'],  TypePython)
            if dicHtmlSite and dicHtmlSite not in ['NONE','ERROR']:
                #print 'dicHtmlSite = ', dicHtmlSite
                dicPython = dicHtmlSite[0]
                pythonClass = dicPython['data']
                if pythonClass:
                    exec (pythonClass)
                    liRootKeys = dicPython['root_keys'].split(',')
                    if liRootKeys:
                        for key in liRootKeys:
                            s =  key.strip() +"." + dicPython['name'].strip() + " = " + dicPython[0]['name'].strip() + "()"
                            print 's-root = ', s
                            try:
                                exec (s)
                            except Exception, params:
                                print Exception,params
                                
                                    

# We are adding children to the pages.
# This could also happen inside the class.
##class ADir(rend.Page):
##    def locateChild(self, request, segments):
##        path = '/'.join(segments)
##        return static.File(path), ()
##
#root.images = static.File('/var/cuon_www/images')
print 'oDirs = ', oDirs
for newDir in oDirs.keys():
    s = 'root.'+ newDir +' = static.File("' + oDirs[newDir] +'")'
    print s
    exec(s)
    
static_site = appserver.NevowSite(static.File("/var/cuon_www/images"))

#sites = appserver.NevowSite(root)

#root.foo = Foo()
#root.foo.baz = Baz()
#internet.TCPServer(baseSettings.WEB_PORT2, appserver.NevowSite(RootPage())).setServiceParent(application)
#application = service.Application('static')
#site2 = server.Site(static.File(baseSettings.WEBPATH))
site = appserver.NevowSite(root)


#webServer = internet.TCPServer(baseSettings.WEB_PORT2,appserver.NevowSite(root))
#webServer = internet.TCPServer(baseSettings.WEB_PORT2,sites)

#webServer.setServiceParent(application)

reactor.listenTCP(baseSettings.WEB_PORT2, site)
#webServer.startService()
#webServer.run()
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
