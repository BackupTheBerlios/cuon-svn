
# -*- coding: utf-8 -*-
##Copyright (C) [2009-2009]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 
import xmlrpclib
from twisted.web import xmlrpc
import types 
from basics import basics

try:
    import twitter
except:
    print "No twitter module found"
    
class Tweet(xmlrpc.XMLRPC, basics):
    def __init__(self):
        basics.__init__(self)
        self.encoding = "utf-8"
        self.username = None
        self.password = None
        self.message = None
        print "Tweet is starting"
        
        
    def xmlrpc_sendTwitterMessage(self, dicUser, sMessage):
        s = "Error in sending twitter"
        self.message = sMessage
        print 'start twitter message'
        #print "dicuser = ",  dicUser 
        #rc = TweetRc()
        self.username = dicUser['Twitter']['TwitterName'] 
        self.password = dicUser['Twitter']['TwitterPassword']
    
        print "username + password = ", self.username, self.password
        
        if  self.username != "TestCuon" and  self.password != "TestCuon":
    
           
            try:
                api = twitter.Api(username=self.username, password=self.password, input_encoding=self.encoding)
                status = api.PostUpdate(self.message)
                s = "%s just posted: %s" % (status.user.name, status.text)
                #print s
                print "message posted"
            except UnicodeDecodeError:
                print "Your message could not be encoded.  Perhaps it contains non-ASCII characters? "
                print "Try explicitly specifying the encoding with the  it with the --encoding flag"
    
            return s
            
    def xmlrpc_refreshUser(self, dicUser):
        self.username = dicUser['Twitter']['TwitterName'] 
        self.password = dicUser['Twitter']['TwitterPassword']
        print "username + password = ", self.username, self.password
        liReturn = []
        try:
            api = twitter.Api(username=self.username, password=self.password, input_encoding=self.encoding)
            print api
            liStatus = api.GetUserTimeline(self.username)        
            # print [s.text for s in status]
            
            for status in liStatus:
                liReturn.append(status.created_at[0:16] + ": " + status.text + '\n')
            liReturn.reverse()
        except Exception, params:
            print 'Error in getting Tweet'
            print Exception, params
            liReturn = ['NONE']   
        #print liReturn
        return liReturn

    def xmlrpc_refreshAll(self, dicUser):
        self.username = dicUser['Twitter']['TwitterName'] 
        self.password = dicUser['Twitter']['TwitterPassword']
        print "username + password = ", self.username, self.password
        liReturn = []
        try:
            api = twitter.Api(username=self.username, password=self.password, input_encoding=self.encoding)
            print api
            liStatus = api.GetPublicTimeline()        
            # print [s.text for s in status]
           
            for status in liStatus:
                liReturn.append(status.created_at[0:16]  + "-" + status.user.GetScreenName()+ ": " + status.text + '\n')
            liReturn.reverse()
        except Exception, params:
            print 'Error in getting Tweet'
            print Exception, params
            liReturn = ['NONE']
            
        #print liReturn
        return liReturn
        
    def xmlrpc_getListOfFollowers(self, dicUser):
        self.username = dicUser['Twitter']['TwitterName'] 
        self.password = dicUser['Twitter']['TwitterPassword']
        api = twitter.Api(username=self.username, password=self.password, input_encoding=self.encoding)
        liReturn = []

        try:
            liStatus = api.GetFollowers()        # print [s.text for s in status]
            numberOfFollowers = len(liStatus)
            for status in liStatus:
                liReturn.append({'name':`status.name`, 'screen_name':`status.screen_name`, 'location':`status.location`})
            #liReturn.append(status.name + " " + `status.screen_name` + " " + `status.location`)
            liReturn.reverse()
        except Exception,  params:
            print Exception,  params
            liReturn = ['NONE']

            numberOfFollowers = 0
        #print liReturn
        return liReturn,  numberOfFollowers
        
    def xmlrpc_getRepliesForUser(self, dicUser):
        self.username = dicUser['Twitter']['TwitterName'] 
        self.password = dicUser['Twitter']['TwitterPassword']
        liReturn = []
        try:
            api = twitter.Api(username=self.username, password=self.password, input_encoding=self.encoding)
            liStatus = api.GetReplies()        # print [s.text for s in status]
            
            for status in liStatus:
                liReturn.append(status.created_at[0:16] + ": " + status.text + '\n')
            liReturn.reverse()
        except Exception,  params:
            print Exception, params
            print 'Error in getting Tweet'
            liReturn = ['NONE']   
        #print liReturn
        return liReturn
    
    def xmlrpc_getUserMessages(self, dicUser):
        self.username = dicUser['Twitter']['TwitterName'] 
        self.password = dicUser['Twitter']['TwitterPassword']
        liReturn = []
        try:
            api = twitter.Api(username=self.username, password=self.password, input_encoding=self.encoding)
            #liStatus = api.GetFriends()        
            # print [s.text for s in status]
            liMessages = []
            #for user in liStatus:
                #liMessages += api.GetUserTimeline(user.name)        # print [s.text for s in status]
            liMessages += api.GetFriendsTimeline(self.username)
            for msg in liMessages:
                
                    liReturn.append(msg.GetUser().name + " " + msg.created_at[0:16] + ": " + msg.text + '\n')
            
            liReturn.reverse()
        except Exception,  params:
            print Exception, params
            print 'Error in getting Tweet'
            liReturn = ['NONE']   
        #print liReturn
        return liReturn
    def xmlrpc_getDirectMessagesForUser(self, dicUser):
        self.username = dicUser['Twitter']['TwitterName'] 
        self.password = dicUser['Twitter']['TwitterPassword']
        liReturn = []
        try:
            api = twitter.Api(username=self.username, password=self.password, input_encoding=self.encoding)
            liStatus = api.GetDirectMessages(self.username)        # print [s.text for s in status]
            
            for status in liStatus:
                liReturn.append(status.created_at[0:16] + ": " + status.text + '\n')
            liReturn.reverse()
        except:
            print 'Error in getting Tweet'
            liReturn = ['NONE']   
        #print liReturn
        return liReturn