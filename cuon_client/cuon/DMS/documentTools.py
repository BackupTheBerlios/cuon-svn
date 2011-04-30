# -*- coding: utf-8 -*-
##Copyright (C) [2003-2005]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

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
import zipfile
import logging

#import cuon.Login.User
import SingleDMS
import cuon.Misc.misc
import os
import types
from PIL import Image
try:
    import sane
    #from _sane import *
except Exception, param:
    
    print 'No Sane found --> No scanner !'
    print Exception, param
    
import bz2
import re
import binascii
import cuon.XMLRPC.xmlrpc
import base64
from cuon.Databases.dumps import dumps
import SingleDMS

class documentTools(dumps):

    def __init__(self):
        dumps.__init__(self)
        self.rpc = cuon.XMLRPC.xmlrpc.myXmlRpc()

    def viewDocument(self, singleDMS,dicUser, dicVars,Action=None, liEmailAddresses = None):
        print 'dicVars1 ', dicVars
        print 'Action = ', Action
        print singleDMS.ID, singleDMS.fileFormat
        singleDMS.loadDocument()
        print singleDMS.ID, singleDMS.fileFormat
        print 'len Image = ', len(singleDMS.imageData)
        exe = None
        sEXT = 'txt'
        if singleDMS.fileFormat:
            print 'Format = ', singleDMS.fileFormat
            if singleDMS.fileFormat == dicUser['prefDMS']['fileformat']['scanImage']['format']:
                print 'show'
                s = bz2.decompress( singleDMS.imageData)
                #sys.exit(0)
                newIm = Image.fromstring('RGB',[singleDMS.size_x, singleDMS.size_y], s)
                newIm.show()
            elif singleDMS.fileFormat == dicUser['prefDMS']['fileformat']['LINK']['format']:
                print 'Link'
                s = singleDMS.imageData
                print 's = ', s
                
                os.system(dicUser['prefDMS']['exe']['internet'] + ' ' + `s` )
                
            else:
                for key in  dicUser['prefDMS']['fileformat'].keys():
                    print 'file-format', singleDMS.fileFormat
                    print 'User-fileformat', dicUser['prefDMS']['fileformat'][key]['format']
                    if singleDMS.fileFormat ==  dicUser['prefDMS']['fileformat'][key]['format']:
                        print 'dicUser-prefDMS', dicUser['prefDMS']['fileformat'][key]
                        exe =  dicUser['prefDMS']['fileformat'][key]['executable']
                        print '-------------------------------------------------------------------'
                        print 'exe = ', exe
                        print '-------------------------------------------------------------------'
                        #sys.exit(0)
                        
                        if singleDMS.fileSuffix and singleDMS.fileSuffix not in ['NONE','ERROR']:
                            sEXT = singleDMS.fileSuffix
                        else:   
                            sEXT =  dicUser['prefDMS']['fileformat'][key]['suffix'][0]
        else:
            exe = None
        
        print 'exe 1 = ', exe
        if exe or Action != None:
            singleDMS.createTmpFile(sEXT)
            if dicVars:
                #print ' '
                #print 'dicVars = ', dicVars
                try:
                    if zipfile.is_zipfile(singleDMS.tmpFile):
                        print 'zipfile found'
                        z1 = zipfile.ZipFile(singleDMS.tmpFile,'a')
                        print z1.namelist()
                        for f1 in ['content.xml', 'styles.xml']:
                            f_in = str(z1.read(f1))
                            #print 'content.xml', f_in
                            
                            f_in = self.replaceValues(dicVars,f_in, dicUser)
                            #print 'replaced Content', f_in
                            z1.writestr(f1,f_in)
                            
                        z1.close()

                    else:
                        
                        f_out = open(singleDMS.tmpFile + '_w1','a')
                                                    
                        f_in = open(singleDMS.tmpFile,'r')
                        if f_in and f_out:
                            s = f_in.readline()
                            while s:
                                s = self.replaceValues(dicVars,s)                                 
                                
                                f_out.write(s)
                                s = f_in.readline()
                                
                            singleDMS.tmpFile = singleDMS.tmpFile + '_w1'
                        else:
                            'error read/create tmp-file'
                except Exception, param:
                    print Exception
                    print param
                    
        print 'exe2 = ', exe
        if Action == 'PrintNewsletter':
            sExe = dicUser['prefApps']['printNewsletter']
            print 'sExe', sExe, singleDMS.tmpFile 
            os.system(sExe + ' ' + singleDMS.tmpFile)
        elif Action == 'sentAutomaticEmail':
            print 'sentAutomaticEmail'
            print dicUser
            if dicUser.has_key('Email'):
                liAttachments = []
                filename = singleDMS.tmpFile
                f = open(filename,'rb')
                if f:
                    s = f.read()
                    s = bz2.compress(s)
                    s = base64.encodestring(s)
                    dicAtt = {}
                    dicAtt['filename'] = filename
                    dicAtt['data'] = s
        
                    liAttachments.append(dicAtt)
                f.close()
                
                for emailTo in liEmailAddresses:
                    dicV = {}
                    dicV['From'] = dicUser['Email']['From']
                    dicV['To'] = emailTo
                    dicV['Subject'] = dicVars['email_subject']
                    dicV['Body'] = dicVars['Body']
                    print 'dicV = ', dicV
                    em = self.rpc.callRP('Email.sendTheEmail', dicV, liAttachments, dicUser)
                    self.writeEmailLog(em)
                    
        else:
            print 'else execute ', exe 
            #os.system(exe + ' ' + singleDMS.tmpFile )
            self.startExternalPrg(exe,singleDMS.tmpFile)

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
        # SANE for scan images
        
        print 'SANE version:', sane.init()
        print 'Available devices=', sane.get_devices()
        
        if dicUser['prefDMS']['scan_device']:
            try:
                scanner=sane.open(dicUser['prefDMS']['scan_device'])
            except:
                scanner = sane.open(sane.get_devices()[0][0])
        else:
            scanner = sane.open(sane.get_devices()[0][0])
         
        try:
            print 'SaneDev object=', scanner
            print 'Device parameters:', scanner.get_parameters()
            print 'mode', scanner.mode
            print 'contrast', scanner.contrast
            print 'brightness', scanner.brightness
            print 'depth', scanner.depth
            print 'br_x', scanner.br_x
            print 'br_y', scanner.br_y
            print 'resolution', scanner.resolution
        except:
            pass
            
        # Set scan parameters
        scanner.mode = dicUser['prefDMS']['scan_mode']
        try:
            if isinstance(scanner.contrast, types.IntType):
                scanner.contrast= int(dicUser['prefDMS']['scan_contrast'])
            else:
                scanner.contrast= dicUser['prefDMS']['scan_contrast']
        except:
            pass
        try:    
            if isinstance(scanner.brightness, types.IntType):
                
                scanner.brightness= int(dicUser['prefDMS']['scan_brightness'])
            else:
                scanner.brightness= dicUser['prefDMS']['scan_brightness']
        except:
            pass
            
            #scanner.white_level=dicUser['prefDMS']['scan_white_level']
        try:
            if isinstance(scanner.depth, types.IntType):
                scanner.depth= int(dicUser['prefDMS']['scan_depth'])
            else:
                scanner.depth= dicUser['prefDMS']['scan_depth']
        except:
            pass
            
        try:
            if isinstance(scanner.br_x, types.IntType):
                
                scanner.br_x= int(dicUser['prefDMS']['scan_r']['x'])
            else:
                scanner.br_x= dicUser['prefDMS']['scan_r']['x']
        except:
            pass
    
        try:
            if isinstance(scanner.br_y, types.IntType):
                scanner.br_y = int(dicUser['prefDMS']['scan_r']['y'])
            else:
                scanner.br_y=dicUser['prefDMS']['scan_r']['y']
        except:
            pass
    
        try:
            if isinstance(scanner.resolution, types.IntType):
                scanner.resolution = int(dicUser['prefDMS']['scan_resolution'])
            else:
                scanner.resolution = dicUser['prefDMS']['scan_resolution']
        except:
            pass
            
        print 'Device parameters after setting:', scanner.get_parameters()
        #print scanner.contrast
        #print scanner.brightness
        #print scanner.white_level
        
        # Initiate the scan
        scanner.start()
        
        # Get an Image object
        im=scanner.snap()
        #print 'Device parameters after snap:', scanner.get_parameters()

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
        #del scanner
        #sane.exit()
        

    def importDocument(self, singleDMS, dicUser, sFile):
       
        if sFile:
            #print sFile
            f = open(sFile,'rb')
            #print f
            #f.seek(0)
            #b = f.readline()
            b = f.read()
            #print 'len of b', len(b)
            #print b
            
            singleDMS.imageData = bz2.compress(b)
            suffix =  string.lower(sFile[string.rfind(sFile,'.')+1:len(sFile)])
            for key in  dicUser['prefDMS']['fileformat'].keys():
                for i in dicUser['prefDMS']['fileformat'][key]['suffix']:
                    #print i
                    #print suffix
                    if i == suffix:
                        print 'suffix found'
                        singleDMS.fileFormat = singleDMS.fileFormat = dicUser['prefDMS']['fileformat'][key]['format']
                        singleDMS.fileSuffix = suffix
                        print 'singleDMS -f-format', `singleDMS.fileFormat`
                        print 'singleDMS -f-suffix', `singleDMS.fileSuffix`
                        
            f.close()
    def load_mainwindow_logo(self,  allTables):        
        self.singleDMS = SingleDMS.SingleDMS(allTables)
        self.singleDMS.loadMainLogo()
        return  self.singleDMS.createTmpFile(self.singleDMS.firstRecord['file_suffix'])
        
        
    def replaceValues(self, dicVars, s, dicUser):
        #print 'replace this in document: ',  dicVars
        for key in dicVars.keys():
            try:
                if isinstance(dicVars[key], types.UnicodeType): 
                    if dicUser['Locales'] == 'de':
                        dicVars[key] = dicVars[key].encode('utf-8')
                        #print 'de and unicode'
                        #print dicVars[key]
                    
                if self.checkType( dicVars[key], 'string'):
                    dicVars[key]  = dicVars[key].replace('&','&amp;' )
                
                #print key, dicVars[key]
                #print '\n'
                
            except Exception, params:
                print Exception, params
                    
            try:
                #print 'try to replace this ', key,  dicVars[key]
                if dicVars[key] == 'NONE' or dicVars[key] ==None:
                    s = s.replace('##'+ key + ';;','')
                elif self.checkType(dicVars[key], 'string') :
                    s = s.replace('##'+ key + ';;',dicVars[key] )
                
                else:
                    s = s.replace('##'+ key + ';;',`dicVars[key]` )
            except:
                pass
        return s
