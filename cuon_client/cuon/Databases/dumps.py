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
import time
import datetime as DateTime
import random
import types
import cuon.TypeDefs.typedefs
import bz2


#import os.path

class dumps:
    def __init__(self, td=None):
        self.dbase = None
        self.decimalLocale = {}
        self.decimalLocale['coma'] = ['de','nl','it','pl','au','ch']
        self.td = None
        #print '------------------------------------------------'
        if td:
            #print 'td is not None'
            self.td = td
        else:
            #print 'set td new'
            self.td = cuon.TypeDefs.typedefs.typedefs()
        #print 'td', self.td
        #print '------------------------------------------------'
        
    def openDB(self):
        #print 'PATH = ', self.td.cuon_path
        self.dbase = shelve.open(os.path.normpath(self.td.cuon_path + '/' + 'cuonObjects'))

    def closeDB(self):
        self.dbase.close()
        
    def saveObject(self, key, oValue):
        # print "Save = " + `key` + ", " + self.td.cuon_path + '/' + 'cuonObjects'

        self.dbase[key] = oValue

    def loadObject(self, key):
        # print "Home = " + self.td.cuon_path + '/' + 'cuonObjects'
        # print key
        oValue = None
        # dbase  = shelve.open(os.path.normpath(self.td.cuon_path + '/' + 'cuonObjects'))
        try:
            oValue = self.dbase[key]
        except:
            oValue = None
            
        # dbase.close()
        return oValue
    

    def pickleObject(self, key, obj):
        # print key
        pkey = os.path.normpath(self.td.cuon_path +'/' + `key`)
        fkey = open(pkey,'w')
        pickle.dump(obj,fkey, 1)
        fkey.close()
        

    def unpickleObject(self, key):
        print key
        pkey = os.path.normpath(self.td.cuon_path +'/' + `key`)
        fkey = open(pkey)
        obj =  pickle.load(fkey)
        fkey.close()
        return obj
    
        
    
    def doEncode(self, s):
        return base64.encodestring(s)

    def doDecode(self, s):
        return  base64.decodestring(s)


    def doCompress(self,s):
        return bz2.compress( s)
    def doUncompress(self,s):
        return bz2.decompress( s)
        
    def saveTmpData(self, data, typ):
        s = ''
        if not typ:
            typ = 'pdf'
            
        n = random.randint(0,1000000000)
        for i in range(27):
            ok = True
            while ok:
                r = random.randint(65,122)
                if r < 91 or r > 96:
                    ok = False
                    s = s + chr(r)
    
        s = s + `n`
        s =  os.path.normpath(self.td.cuon_path + '/cuon__' +  s + `time.time()` + '.' + typ)
        f = open(s,'wb')
        f.write(data)
        f.close()
        return s
        
    def showPdf(self, Pdf, dicUser):
        #print "PDF", Pdf
        
        s = self.doDecode(Pdf)
        fname = self.saveTmpData(s, 'pdf')
        print 'PDF-App = ', dicUser['prefApps']['PDF']
        print os.system(dicUser['prefApps']['PDF'] + ' ' + fname + ' &')
        

    def getCheckedValue(self, value, type, min = None, max = None):
        retValue = None
        try:
            assert type
            if type == 'int':
                if isinstance(value, types.IntType) or isinstance(value, types.LongType) :
                
                
                    try:
                        retValue = int(value)
                    except:
                        retValue = 0
                    

                else:
                    try:
                        assert value != None
                        if isinstance(value, types.StringType):
                            value = value.strip()
                            if value[0] == 'L'  or value[0] == 'l':
                                value = value[1:]
                            
                        retValue = int(value)
                    except:
                        retValue = 0
                
                        
            elif type == 'float':
                if not isinstance(value, types.FloatType):
                    try:
                        assert value != None

                        if isinstance(value, types.StringType):
                            
                            value = value.strip()
                            convert = False
                            print 'convert userlocales = ', self.dicUser['Locales']
                            for sLocale in self.decimalLocale['coma']:
                                #print sLocale
                                if sLocale == self.dicUser['Locales']:
                                    convert = True
                            if convert:
                                #print 'convert to normal float'
                                value = value.replace('.','')
                                value = value.replace(',','.')
                                
                                    
                            if value[0] == 'L'  or value[0] == 'l':
                                value = value[1:]
                        retValue = float(value)
                    except:
                        retValue = 0.0
                else:
                    retValue =  value 
            elif type == 'toStringFloat':
                if isinstance(value, types.StringType):
                    if value == 'NONE':
                        value = '0.00'
                    elif value == 'None':
                        value = '0.00'
                        
                        
                    convert = False
                    print 'convert userlocales = ', self.dicUser['Locales']
                    for sLocale in self.decimalLocale['coma']:
                        #print sLocale
                        if sLocale == self.dicUser['Locales']:
                            convert = True
                    if convert:
                        #print 'convert to normal float'
                        value = value.replace('.',',')
                        #value = value.replace(',','.')
                         
                retValue = value 
                
            elif type == 'date':
                #print 'value by date', value
                retvalue = time.strptime(value, self.dicUser['DateformatString'])
                self.printOut( 'dt2 = ', retvalue)
                
                        
                    #elif entry.getVerifyType() == 'date' and isinstance(sValue, types.StringType):
                    #    dt = DateTime.DateTimeFrom(sValue)
                    #dt = DateTime.strptime(sValue, "YYYY-MM-DD HH:MM:SS.ss")
                    #dt = DateTime.DateTime(1999)
                    #    # self.out( dt)
                    #    sValue = dt.strftime(self.sDateFormat)
                    
            elif type == 'formatedDate':
                #print 'value by formatedDate', value
                checkvalue = time.strptime(value, self.dicUser['DateformatString'])
                self.printOut( 'dtFormated2 = ', checkvalue)
                if checkvalue[0] == 1900 and checkvalue[1] == 1 and checkvalue[2] == 1:
                    # 1900/1/1 --> set to empty
                    retvalue = ''
                else:
                    retValue = value
                    
            elif type == 'toStringDate':
                #print 'value by toStringDate', value
                retValue = time.strftime(self.dicUser['DateformatString'],value)
                self.printOut( 'dt5 = ', retValue) 
                
            elif type == 'string':    
                #print 'check string = ', value
                
                if not isinstance(value, types.StringType):
                    value = `value`
                if value == 'NONE':
                    value = ''
                elif value == 'None':
                    value = ''
                
                retValue = value
                
                
                
            else:
                retValue = value
        
        except AssertionError:
            print 'No type set '
            retValue = value
        except Exception,params:
            print Exception, params
            retValue = value
        
        #print 'retvalue = ', retValue
        
        return retValue
        
    
    def getTime(self,s ):
        Hour,Minute = divmod(s,4)
        Minute = Minute * 15
        
        
        return Hour, Minute
