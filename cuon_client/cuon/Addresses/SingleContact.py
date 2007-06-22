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
import cuon.Addresses.SingleAddress
import cuon.Addresses.SinglePartner

class SingleContact(SingleData):

    
    def __init__(self, allTables):
        
        SingleData.__init__(self)
        # tables.dbd and address
        self.sNameOfTable =  "contact"
        self.xmlTableDef = 0
        self.loadTable(allTables)
        # self.saveTable()
        self.allTables = allTables

        #self.athread = threading.Thread(target = self.loadTable())
        #self.athread.start()
        
        self.listHeader['names'] = ['name', 'zip', 'city', 'Street', 'ID']
        self.listHeader['size'] = [25,10,25,25,10]
        self.out( "number of Columns ")
        self.out( len(self.table.Columns))
        #
        self.addressId = 0
        self.partnerId = 0
        
        
        #self.statusfields = ['lastname', 'firstname']

            
##    def readNonWidgetEntries(self, dicValues):
##        print 'readNonWidgetEntries(self) by SingleBank'
##        dicValues['addres_sid'] = [self.addressId, 'int']
##        return dicValues

    def getAddress(self, address_id):
        print address_id
        singleAddress = cuon.Addresses.SingleAddress.SingleAddress(self.allTables)
        
        liAddress = singleAddress.getAddress(address_id)
        print 'liAddress', liAddress
        
        return liAddress
        
    def getPhone(self, address_id):
        print address_id
        singleAddress = cuon.Addresses.SingleAddress.SingleAddress(self.allTables)
        
        Phone = singleAddress.getAddressPhone1(address_id)
        
        return Phone
        
    def getPhonePartner(self, partnerid):
        print partnerid
        
        singlePartner = cuon.Addresses.SinglePartner.SinglePartner(self.allTables)
        
        Phone = singlePartner.getPartnerPhone1(partnerid)
        
        return Phone
        
        
    def fillOtherEntries(self, oneRecord):
        print 'fill tvAddress'
        if oneRecord['address_id'] > 0:
            liAddr = self.getAddress(oneRecord['address_id'])
            print liAddr
            self.setTextbuffer(self.getWidget('tvAddress'),liAddr)
            self.getWidget('ePhoneAddress1').set_text(self.getPhone(oneRecord['address_id']))
            self.addressId = oneRecord['address_id']
        if oneRecord['partnerid'] > 0:
            self.getWidget('ePhonePartner').set_text(self.getPhonePartner(oneRecord['partnerid']))
            
    def readNonWidgetEntries(self, dicValues):
        print 'readNonWidgetEntries(self) by SinglePartner'
        dicValues['address_id'] = [self.addressId, 'int']
        dicValues['partnerid'] = [self.partnerId, 'int']
        try:
            sSql = self.getStaffID(self.dicUser, False)
            result = self.rpc.callRP('Database.executeNormalQuery',sSql,self.dicUser)
            print result
            cID = result[0]['id']
            
        except Exception, param:
            print Exception, param
            cID = 0
            
            
        print 'cID = ', cID
        dicValues['contacter_id'] = [cID,'int']
        return dicValues
