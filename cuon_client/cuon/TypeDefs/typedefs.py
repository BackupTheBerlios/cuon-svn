# -*- coding: utf-8 -*-

##Copyright (C) [2003]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 

import xmlrpclib
from xmlrpclib import Server
import cuon.XML.MyXML
import sys
import os
import ConfigParser
#if len(sys.argv) > 1:
#    fname = sys.argv[1]
#else:

class typedefs:

    def __init__(self):

        # initial-Values
        self.server = None
        self.cuon_path = None
        self.help_server = None
        self.cpParser = None
        try:
            self.cuon_path = os.environ(['CUON_PATH'])
            
        except:
            pass
        
        try:
            self.server = os.environ(['CUON_SERVER'])
            
        except:
            pass            
            
            
            
        try:
            self.help_server = os.environ(['CUON_HELPSERVER'])
            
        except:
            pass            
            
            
            
        try:
            pass
        except:
            pass
        
        # start read /etc/cuon/cuon.ini
        self.getConfigParser('/etc/cuon/cuon.ini')
        if self.cpParser:
            value = self.getConfigOption('PATH','CUON_PATH')
            if value:
              self.cuon_path = value
              
            value = self.getConfigOption('SERVER','CUON_SERVER')
            if value:
              self.server = value
              
            value = self.getConfigOption('SERVER','CUON_HELPSERVER')
            if value:
              self.help_server = value
              
        try:
            
            # start read /etc/cuon/cuon.ini
            self.getConfigParser(os.environ['HOME'] + '/.cuon.ini')
            if self.cpParser:
                value = self.getConfigOption('PATH','CUON_PATH')
                if value:
                  self.cuon_path = value
                  
                value = self.getConfigOption('SERVER','CUON_SERVER')
                if value:
                  self.server = value
                  
                value = self.getConfigOption('SERVER','CUON_HELPSERVER')
                if value:
                  self.help_server = value
              
        except Exception, params:
            print Exception, params
            
                 
          
        # If noc config-Options found, fallback to defaults   
        if not self.cuon_path:    
            self.cuon_path = os.environ['HOME'] +'/cuon'
        
        if not self.server:
            self.server = 'http://localhost:7080'
        
##        if not self.homePath:
##            self.homePath = os.environ['HOME'] + '/cuon'
##            
            
        #self.server = os.environ['CUON_SERVER']
        #self.homePath = os.environ['CUON_HOME']        
        if not self.help_server:
            self.help_server = 'http://84.244.7.139:7084/?action=xmlrpc2'
            
            
        
        print 'Server by typedef : ' + self.server
        
    def getConfigParser(self, sFile):
        try:
            self.cpParser = ConfigParser.ConfigParser()
            f = open(sFile, 'rw')
            if f:    
                self.cpParser.readfp(f)
                f.close()
        except:
            print 'no file ' + sFile + 'found '
            self.cpParser = None
            
        
    def getConfigOption(self, section, option):
        value = None
        if self.cpParser.has_option(section,option):
            value = self.cpParser.get(section, option)
            print 'getConfigOption', section + ', ' + option + ' = ' + value
        return value       
