# -*- coding: utf-8 -*-
##Copyright (C) [2003]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 
import sys
import os
#sys.path.append(os.environ['CUON_PATH'])

from cuon.Databases.SingleData import SingleData
import logging
import threading

class SingleAddress(SingleData):

    
    def __init__(self, allTables):

        SingleData.__init__(self)
        # tables.dbd and address
        self.sNameOfTable =  "address"
        self.xmlTableDef = 0
        #print 'allTables = ',`allTables`
        self.loadTable(allTables)
        # self.saveTable()

        #self.athread = threading.Thread(target = self.loadTable())
        #self.athread.start()
        
        self.listHeader['names'] = ['name', 'zip', 'city', 'Street', 'ID']
        self.listHeader['size'] = [25,10,25,25,10]
        #self.out( "number of Columns ")
        #self.out( len(self.table.Columns))
        #
        self.statusfields = ['lastname', 'city']

    def getAddressPhone1(self, id):
        
        try:
            id = long(id)
            
            dicRecords = self.load(id)
        except:
            print 'Exception by getAddressPhone1-1'
            id = 0
            dicRecords = {}
        Phone = ''
        try:
            if dicRecords:
                Phone = dicRecords[0]['phone']
        except:
            print 'Exception by getAddressPhone1-2'

            Phone = ''
        
        return Phone
        
        
    def getAddress(self, id):
          
        liAddress = []
        if id > 0:
            try:
                id = long(id)
                
                dicRecords = self.load(id)
            except:
                id = 0
                dicRecords = {}
          
            if dicRecords and dicRecords not in ['ERROR', 'NONE']:
                dicRecord = dicRecords[0]
                try:
                    liAddress.append(dicRecord['lastname'])
                    liAddress.append(dicRecord['lastname2'])
                    liAddress.append(dicRecord['firstname'])
                    liAddress.append(dicRecord['street'])
                    liAddress.append(dicRecord['country'] + '-' +dicRecord['zip']+ ' ' + dicRecord['city'])
                except:
                    pass
                    
            if not liAddress:
                liAddress.append(' ')
                liAddress.append(' ')
                liAddress.append(' ')
                liAddress.append(' ')
                liAddress.append(' ')
            
        return liAddress

    def getMailAddress(self):
        
        s = None
        try:
            s = self.firstRecord['lastname'] + '\n'
            s += self.firstRecord['lastname2'] + '\n'
            s += self.firstRecord['firstname'] + '\n\n'
            s += self.firstRecord['street'] + '\n'
            s += self.firstRecord['country'] + '-' + self.firstRecord['zip'] + ' ' + self.firstRecord['city']
            
        except:
            pass
            
        return s       
    def getLastname(self):
        s = None
        try:
            s = self.firstRecord['lastname']
        except:
            pass
        if not s or s == 'NONE':
            s = ''
        return s

    def getLastname2(self):
        s = None
        try:
            s = self.firstRecord['lastname2']
        except:
            pass
        if not s or s == 'NONE':
            s = ''
        return s
        
    def getFirstname(self):
        s = None
        try:
            s = self.firstRecord['firstname']
        except:
            pass
        if not s or s == 'NONE':
            s = ''
        return s
        
    def getStreet(self):
        s = None
        try:
            s = self.firstRecord['street']
        except:
            pass
        if not s or s == 'NONE':
            s = ''
        return s
        
        
        
    def getCity(self):
        s = None
        try:
            s = self.firstRecord['city']
        except:
            pass
        if not s or s == 'NONE':
            s = ''
        return s
        
    def getZip(self):
        s = None
        try:
            s = self.firstRecord['zip']
        except:
            pass
        if not s or s == 'NONE':
            s = ''
        return s
        
        
    def getCountry(self):
        s = None
        try:
            s = self.firstRecord['country']
        except:
            pass
        if not s or s == 'NONE':
            s = ''
        return s
        
        
    def getEmail(self):
        s = None
        try:
            s = self.firstRecord['email']
        except:
            pass
        if not s or s == 'NONE':
            s = ''
        return s
        
    def getLetterAddress(self):
        s = None
        try:
            s = self.firstRecord['letter_address']
        except:
            pass
        if not s or s == 'NONE':
            s = ''
        return s
