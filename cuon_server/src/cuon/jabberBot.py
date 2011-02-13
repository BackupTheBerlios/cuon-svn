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
import xmlrpclib
from basics import basics
from twisted.words.protocols.jabber import client, jid,   xmlstream
from twisted.words.xish import domish
import shelve

class jabberBot(xmlrpc.XMLRPC, basics):
    def __init__(self):
        basics.__init__(self)
        
        
        print   'jABBER: --> ',  self.JABBERSERVER
        print self.JABBERUSERNAME   
        print self.JABBERPASSWORD
        self.filename = 'dic_jabberusers'
        self.me = jid.JID(self.JABBERUSERNAME + '@' + self.JABBERSERVER )
        self.factory = client.basicClientFactory(self.me, self.JABBERPASSWORD)
        self.Server = xmlrpclib.ServerProxy(self.XMLRPC_PROTO + '://' + self.XMLRPC_HOST + ':' + `self.XMLRPC_PORT`)
        self.theXmlstream = None
        self.dicUsers = {}
        
        # Authorized
    def authd(self,  xmlstream):
        # need to send presence so clients know we're
        # actually online.
        presence = domish.Element(('jabber:client', 'presence'))
        presence.addElement('status').addContent('Online')
        self.theXmlstream = xmlstream
        self.theXmlstream.send(presence)
        self.theXmlstream.addObserver('/message', self.gotMessage)
        
    
    def create_reply(self,  elem):
        """ switch the 'to' and 'from' attributes to reply to this element """
        # NOTE - see domish.Element class to view more methods 
        
        msg_frm = elem['from']
        msg_to = elem['to']
        
        message = domish.Element(('jabber:client','message'))
        message["to"] = msg_frm
        message["from"] = msg_to
        message["type"] = "chat"
        
        return message

    
    def send(self,  msg0,  newMsg):
        msg = self.create_reply(msg0)
        #print `msg`,  newMsg
        #for e in msg.elements():
          #  print e.name, unicode(e.__str__())
            
        #msg['body'] = newMsg
        msg.addElement('body', content = newMsg)

        #for e in msg.elements():
          #  print e.name,  unicode(e.__str__())
        
        
        print `msg`
        self.theXmlstream.send(msg)    


    def gotMessage(self,  message):
        # sorry for the __str__(), makes unicode happy
        print u"from1: %s" % message["from"]
        send_from = message["from"].strip()
        
        #print unicode(message.__str__())
        for e in message.elements():
            if e.name == "body":
                #print unicode(e.__str__())
                msg_body = unicode(e.__str__())
                if msg_body.strip().lower()[0:5]  == 'login':
                    print 'login found'
                    liUser = msg_body[5:].split(',')
                    print liUser
                    username = liUser[0].strip()
                    sPw = liUser[1].strip()
                    iClient = 1
                    try:
                        iClient = int(liUser[2].strip())
                    except Exception, param:
                        print Exception, param
                        iClient = 0
                                          
                    sid = self.Server.Database.createSessionID( username, sPw)
                    print sid
                    self.dicUsers = shelve.open(self.filename)
                    self.dicUsers[message['from'].__str__()] = {'Name':username, 'SessionID':sid,'userType':'cuon', 'client':iClient}
                    self.dicUsers.close()
                    
                    if sid not in ['TEST']:
                        return_msg = 'Authentication successful'
                    else:
                        return_msg = 'Authentication failed'
                    self.send(message,  return_msg)
                else:
                    # send to AI
                    try:
                        self.dicUsers = shelve.open(self.filename)
                        one_user =  self.dicUsers[message['from'].__str__()]
                        self.dicUsers.close()
                    except Exception, param:
                        print Exception,  param
                        self.dicUsers = shelve.open(self.filename)
                        self.dicUsers[message['from'].__str__()] = {'Name':'testuser', 'SessionID':'TEST','userType':'cuon', 'client':0}
                        one_user =  self.dicUsers[message['from'].__str__()]
                        self.dicUsers.close()
                    try:
                        a1 = self.Server.AI.getAI(msg_body,one_user)
                    except Exception,  param:
                        print Exception,  param
                        a1 = 'Sorry,  perhaps you are not authorizes'
                    if one_user['SessionID'] in ['TEST'] or one_user['client'] == 0:
                        prefix_a1 = 'Failed: '
                    else:
                        prefix_a1 = u'OK: '
                        
                    #print "Answer", a1
                    self.send(message,  prefix_a1 + a1)
                
                
                break

    