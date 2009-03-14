# -*- coding: utf-8 -*-

##Copyright (C) [2009]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 


from twisted.web import xmlrpc
from twisted.internet import reactor
import sys,os,xmpp,string,threading,time,curses
from time import strftime

from basics import basics
from twisted.words.protocols.jabber import client, jid,   xmlstream
from twisted.words.xish import domish

class jabberBot(xmlrpc.XMLRPC, basics):
    def __init__(self):
        basics.__init__(self)
        
        
        print   'jABBER: --> ',  self.JABBERSERVER
        print self.JABBERUSERNAME   
        print self.JABBERPASSWORD
            
        self.me = jid.JID(self.JABBERUSERNAME + '@' + self.JABBERSERVER )
        self.factory = client.basicClientFactory(self.me, self.JABBERPASSWORD)
        
    def authd(self,  xmlstream):
        # need to send presence so clients know we're
        # actually online.
        presence = domish.Element(('jabber:client', 'presence'))
        presence.addElement('status').addContent('Online')
        
        xmlstream.send(presence)
        xmlstream.addObserver('/message', self.gotMessage)
        
        
        
    def gotMessage(self,  message):
        # sorry for the __str__(), makes unicode happy
        print u"from: %s" % message["from"]
        for e in message.elements():
            if e.name == "body":
                print unicode(e.__str__())
                break

    
