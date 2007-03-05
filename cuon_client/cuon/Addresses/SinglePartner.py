# -*- coding: utf-8 -*-

##Copyright (C) [2003]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 


from cuon.Databases.SingleData import SingleData
import logging
import threading

class SinglePartner(SingleData):

    
    def __init__(self, allTables):

        SingleData.__init__(self)
        # tables.dbd and address
        self.sNameOfTable =  "partner"
        self.xmlTableDef = 0
        self.loadTable(allTables)
        # self.saveTable()

        #self.athread = threading.Thread(target = self.loadTable())
        #self.athread.start()
        
        self.listHeader['names'] = ['name', 'zip', 'city', 'Street', 'ID']
        self.listHeader['size'] = [25,10,25,25,10]
        self.out( "number of Columns ")
        self.out( len(self.table.Columns))
        #
        self.addressId = 0
        self.statusfields = ['lastname', 'firstname']

    def getPartnerPhone1(self, id):
        Phone = ''
        assert id > 0
        try:
            id = long(id)
            
            dicRecords = self.load(id)
        except:
            print 'Exception by getAddressPhone1-1'
            id = 0
            dicRecords = {}
        try:
            if dicRecords:
                Phone = dicRecords[0]['phone']
        except:
            print 'Exception by getAddressPhone1-2'

            Phone = ''
        
        return Phone        
        
    def readNonWidgetEntries(self, dicValues):
        print 'readNonWidgetEntries(self) by SinglePartner'
        dicValues['addressid'] = [self.addressId, 'int']
        return dicValues

    def getAddress(self, id):
        dicRecords = self.load(id)
        liAddress = []
        if dicRecords:
            dicRecord = dicRecords[0]
            liAddress.append(dicRecord['lastname'])
            liAddress.append(dicRecord['lastname2'])
            liAddress.append(dicRecord['firstname'])
            liAddress.append(dicRecord['street'])
            liAddress.append(dicRecord['country'] + '-' +dicRecord['zip'] + ' ' + dicRecord['city'])
        if not liAddress:
            liAddress.append(' ')
            liAddress.append(' ')
            liAddress.append(' ')
            liAddress.append(' ')
            liAddress.append(' ')
            
        return liAddress
        
        
    def getAddressID(self):
        id = 0
        if self.firstRecord.has_key('addressid'):
             id = self.firstRecord['addressid']
        return id 
        
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
        
    def getEmail(self):
        s = None
        try:
            s = self.firstRecord['email']
        except:
            pass
        if not s or s == 'NONE':
            s = ''
        return s        
