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

#if len(sys.argv) > 1:
#    fname = sys.argv[1]
#else:

class typedefs:

    def __init__(self):
       
        self.server = os.environ['CUON_SERVER']
        self.homePath = os.environ['CUON_HOME']        
        self.help_server = 'http://84.244.7.139:7084/?action=xmlrpc2'
        
        print 'Server by typedef : ' + self.server
        
    
