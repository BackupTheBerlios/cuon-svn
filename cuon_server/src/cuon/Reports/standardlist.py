# -*- coding: utf-8 -*-
##Copyright (C) [2003-2004]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 

import os
import os.path
from reportlab.lib import pagesizes

from report import report
import copy

class standardlist(report):

    def __init__(self):
        report.__init__(self)
        print 'ini Standardlist'
        
        self.xmlFile = ''
        
        self.filedata = []
        
        
    def setFileName(self, sName):
        
        sFile = os.path.normpath( sName )
        self.filedata.append(sFile)
        return sFile
    
    
  

 
