# -*- coding: utf-8 -*-
##Copyright (C) [2003-2005]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 

import sys
from types import *
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import gobject
import string

import logging

#import cuon.Login.User
import SingleDMS
import cuon.Misc.misc
import os
try:
    import sane
except:
    print 'No Sane found --> No scanner !'
    
import Image
import bz2
import re
import binascii



class documentTools:

    def __init__(self):
        pass


    def viewDocument(self, singleDMS,dicUser):
                             
        exe = None
        if singleDMS.fileFormat:
            if singleDMS.fileFormat == dicUser['prefDMS']['fileformat']['scanImage']['format']:
                print 'show'
                s = bz2.decompress( singleDMS.imageData)
              
                newIm = Image.fromstring('RGB',[singleDMS.size_x, singleDMS.size_y], s)
                newIm.show()
            else:
                for key in  dicUser['prefDMS']['fileformat'].keys():
                    print singleDMS.fileFormat
                    print dicUser['prefDMS']['fileformat'][key]['format']
                    if singleDMS.fileFormat ==  dicUser['prefDMS']['fileformat'][key]['format']:
                        exe =  dicUser['prefDMS']['fileformat'][key]['executable']
                        if singleDMS.fileSuffix and singleDMS.fileSuffix != 'NONE':
                            sEXT = singleDMS.fileSuffix
                        else:   
                            sEXT =  dicUser['prefDMS']['fileformat'][key]['suffix'][0]

            if exe:
                singleDMS.createTmpFile(sEXT)
                os.system(exe + ' ' + singleDMS.tmpFile)
                        

    def scanDocument(self, singleDMS, dicUser):
        ##       misc = cuon.Misc.misc.misc()
        
##        sc = dicUser['prefDMS']['scan_program']
##        sc = sc + ' --mode ' + dicUser['prefDMS']['scan_mode']
##        sc = sc + ' --resolution ' + dicUser['prefDMS']['scan_resolution']
        
##        print sc
##        self.scanfile = dicUser['prefPath']['tmp'] +  misc.getRandomFilename('_scan.tmp')
##        print self.scanfile
##        sc = sc + ' >> ' + self.scanfile

##        print sc
##        ok = os.system(sc)
##        print ok
        
        scanner=sane.open(dicUser['prefDMS']['scan_device'])
        print 'SaneDev object=', scanner
        print 'Device parameters:', scanner.get_parameters()
        
        # Set scan parameters
        scanner.mode = dicUser['prefDMS']['scan_mode']
        scanner.contrast=dicUser['prefDMS']['scan_contrast']
        scanner.brightness=dicUser['prefDMS']['scan_brightness']
        #scanner.white_level=dicUser['prefDMS']['scan_white_level']
        scanner.depth=dicUser['prefDMS']['scan_depth']
        scanner.br_x=dicUser['prefDMS']['scan_r']['x']
        scanner.br_y=dicUser['prefDMS']['scan_r']['y']
        scanner.resolution = dicUser['prefDMS']['scan_resolution']
        
        print 'Device parameters after setting:', scanner.get_parameters()
        print scanner.contrast
        print scanner.brightness
        #print scanner.white_level
        
        # Initiate the scan
        scanner.start()
        
        # Get an Image object
        # (For my B&W QuickCam, this is a grey-scale image.  Other scanning devices
        #  may return a
        im=scanner.snap()
        print 'Device parameters after snap:', scanner.get_parameters()

        # Write the image out as a GIF file
        #im.save('/home/jhamel/foo.png')
        
        im.show()
        if (im.mode != "RGB"):
            im = im.convert("RGB")

        singleDMS.size_x = im.size[0]
        singleDMS.size_y = im.size[1]
        
        s = im.tostring('raw','RGB')
        print len(s)
        s2 = bz2.compress(s)
        print len(s2)
        singleDMS.imageData = s2
        

        #newIm = Image.fromstring('RGB',[1024.0,768.0], s)
        #newIm.show()

    def importDocument(self, singleDMS, dicUser, sFile):
        
                
        
        if sFile:
            print sFile
            f = file(sFile,'rb')
            b = f.read()
            singleDMS.imageData = bz2.compress(b)
            suffix =  string.lower(sFile[string.rfind(sFile,'.')+1:len(sFile)])
            for key in  dicUser['prefDMS']['fileformat'].keys():
                for i in dicUser['prefDMS']['fileformat'][key]['suffix']:
                    print i
                    print suffix
                    if i == suffix:
                        print 'suffix found'
                        singleDMS.fileFormat = singleDMS.fileFormat = dicUser['prefDMS']['fileformat'][key]['format']
                        singleDMS.fileSuffix = suffix
                        print 'singleDMS -f-format', `singleDMS.fileFormat`
                        print 'singleDMS -f-suffix', `singleDMS.fileSuffix`
                        
            f.close()
            
