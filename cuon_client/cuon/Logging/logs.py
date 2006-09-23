# -*- coding: utf-8 -*-

##Copyright (C) [2003]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 
import sys
import os
import time

class logs :
    

    def __init__(self):
        self.NO_LOG = -1
        self.INFO = 0
        self.WARNING = 1
        self.ERROR =  2
        self.CRITICAL = 3
        self.DEBUG = 4

        self.maxLevel = 4
        
        self.iLogLevel = self.DEBUG
        

    def setLogLevel(self, iLevel):
        self.iLogLevel = iLevel
        if iLevel > self.maxLevel:
            self.iLogLevel = self.ERROR
        else:
            self.iLogLevel = iLevel
            


    def out(self, sLog, iLogLevel = -1):
        #print 'iLoglevel = ' +  `iLogLevel`
##        iLevel = self.INFO
##        if iLogLevel != -1:
##            iLevel = iLogLevel
##        else:
##            iLogLevel = 0
##            
##        if iLevel > self.maxLevel:
##            self.iLogLevel = self.INFO
##
##        
##        if iLevel <= self.iLogLevel and self.iLogLevel > -1:
##            newTime = time.localtime()
##            f = open(os.path.normpath(os.environ['CUON_HOME'] + '/' + 'cuonLog'),'a')
##            tValue =  time.strftime("%d.%m.%Y %H:%M", newTime)
##            f.write(tValue)
##            f.write(`sLog`+ "\n")
##            f.write('---------------------------------------------------------------------------------------------------\n')
##            f.close()
        print sLog
        pass
    def printOut(self, s1,s2=None):
##        ok = True
##        if ok:
##            if s2:
##                print s1, s2
##            else:
##                print s1
      pass     
        
    
        
