# -*- coding: utf-8 -*-
##Copyright (C) [2003]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 

import shelve
import sys
import os
import pickle
import base64

#import os.path

class dumps:
    def __init__(self):
        self.dbase = None

    def openDB(self):
        print 'OS.ENViron', os.environ['CUON_HOME']
        self.dbase = shelve.open(os.path.normpath(os.environ['CUON_HOME'] + '/' + 'cuonObjects'))

    def closeDB(self):
        self.dbase.close()
        
    def saveObject(self, key, oValue):
        # print "Save = " + `key` + ", " + os.environ['CUON_HOME'] + '/' + 'cuonObjects'

        self.dbase[key] = oValue

    def loadObject(self, key):
        # print "Home = " + os.environ['CUON_HOME'] + '/' + 'cuonObjects'
        # print key
        oValue = None
        # dbase  = shelve.open(os.path.normpath(os.environ['CUON_HOME'] + '/' + 'cuonObjects'))
        try:
            oValue = self.dbase[key]
        except:
            oValue = None
            
        # dbase.close()
        return oValue
    

    def pickleObject(self, key, obj):
        # print key
        pkey = os.path.normpath(os.environ['CUON_HOME'] +'/' + `key`)
        fkey = open(pkey,'w')
        pickle.dump(obj,fkey, 1)
        fkey.close()
        

    def unpickleObject(self, key):
        print key
        pkey = os.path.normpath(os.environ['CUON_HOME'] +'/' + `key`)
        fkey = open(pkey)
        obj =  pickle.load(fkey)
        fkey.close()
        return obj
    
        
    
    def doEncode(self, s):
        return base64.encodestring(s)

    def doDecode(self, s):
        return  base64.decodestring(s)
