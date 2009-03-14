#! /usr/bin/python
#xmlrpc-server
from twisted.web import xmlrpc, resource, static
from twisted.internet import defer
from twisted.internet import reactor
from twisted.web import server
from twisted.words.protocols.jabber import  xmlstream
import cuon.basics

baseSettings = cuon.basics.basics()
import cuon.jabberBot

jb = cuon.jabberBot.jabberBot()



        
jb.factory.addBootstrap(xmlstream.STREAM_AUTHD_EVENT, jb.authd)
reactor.connectTCP(baseSettings.JABBERSERVER, 5222, jb.factory)
reactor.run()
        



