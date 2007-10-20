# -*- coding: utf-8 -*-
##Copyright (C) [2003]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 


#import xmlrpclib
#from xmlrpclib import Server
import cuon.TypeDefs
from cuon.Databases.dumps import dumps
from cuon.Logging.logs import logs
#from M2Crypto.m2xmlrpclib import  Server, SSL_Transport

import time
from xmlrpclib import ServerProxy

class myXmlRpc(dumps, logs):
    """
    @author: Jürgen Hamel
    @organization: Cyrus-Computer GmbH, D-32584 Löhne
    @copyright: by Jürgen Hamel
    @license: GPL ( GNU GENERAL PUBLIC LICENSE )
    @contact: jh@cyrus.de
    """
    def __init__(self):
        dumps.__init__(self)
        logs.__init__(self)
        
        #self.zope_server = self.getZopeServer()
        self.MyServer = self.getMyServer()
        
        
    def getMyServer(self):
        """
        if the CUON_SERVER environment-variable begins with https,
        then the server use SSL for security.
        @return: Server-Object for xmlrpc
        """
        
        sv = None
        try:
#            if self.td.server[0:5] == 'https':
#                #print "------ HTTPS ------", self.td.server
#                #sv =  Server( self.td.server  , SSL_Transport(), encoding='utf-8')
#                sv =  ServerProxy( self.td.server, allow_none = 1) 
#            else:
#                #print 'Server2 = ', self.td.server
#                #sv =  ServerProxy( self.td.server, allow_none = 1 )
            sv = ServerProxy(self.td.server,allow_none = 1)
                
        except Exception, params:
            print 'Server error by xmlrpc : ', self.td.server
            print Exception
            print params
            
        
        return sv
    
    def getZopeServer(self):
        """
        if the CUON_SERVER environment-variable begins with https,
        then the server use SSL for security.
        @return: Server-Object for xmlrpc
        """
        
        self.out( self.td.server)
        self.out( `self.td.server`)
        self.out( '++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        self.out( ' neue xmlrpclib')
        sv = None
        try:
            if self.td.server[0:5] == 'https':
                #sv =  Server( self.td.server  , SSL_Transport(), encoding='utf-8')
                sv =  ServerProxy( self.td.server,allow_none = 1 ) 
            else:
                sv =  ServerProxy( self.td.server, allow_none = 1 )
        except:
            print 'Server error'
            
        
        return sv

    def getServer(self):
        return self.MyServer
        
    def getServer2(self):
        return self.MyServer
        
    def getHelpServer(self):
        return self.MyHelpServer
        

    def test(self):
        s1 = "select * from address"
        #recordset = self.getServer().src.sql.py_executeNormalQuery(s1)
        #for record in recordset:
            #self.out( record)
            #for key in record:
                #self.out( key)
                #self.out( record[key])


    def getInfoOfTable(self, sNameOfTable):
        return self.getServer().src.Databases.py_getTable(sNameOfTable)
    

    def callRP(self, rp, *c):
        r = None
        #print 'rp',rp
        #print rp[0:3]
        s = 'r = self.getServer().' + rp + '('
        for i in c:
            s = s + `i` + ', '
            #print '-------------------------------------------------'
            #print 'i = ', `i`
            #print '-------------------------------------------------'
            
        if len(c) > 0:
            s = s[0:len(s) -2]
        s = s + ')'
        #self.out(s)
        startRP = True
        rp_tries = 0
        #print 'Server by connection: ', self.getServer()
        #print 'Servercall by Connection: ', s
        while startRP:
            try:
                exec s
                startRP = False

            except IOError, param:
                print 'IO-Error'
                print param
                
            except KeyError, param:
                print 'KEY-Error'
                print param

            except Exception, param:
                print 'unknown exception'
                print `Exception`
                print param[0:200]
                
            if startRP:
                print 'error, next try'
                
                rp_tries = rp_tries + 1
                
                if rp_tries > 5:
                    startRP = False
                else:
                    print ' wait for 2 sec. '
                    print ' Try :' + `rp_tries`
                    time.sleep(2)
        if r and r == 'NONE':
            r = None
        return    r

    
        
        
        


