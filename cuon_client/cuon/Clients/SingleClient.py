# -*- coding: utf-8 -*-
##Copyright (C) [2005]  [Juergen Hamel, D-32584 Loehne]

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

class SingleClient(SingleData):

    
    def __init__(self, allTables):

        SingleData.__init__(self)
        self.sqlDicUser['noWhereClient'] = 'YES'
        self.dicUser['noWhereClient'] = 'YES'
        self.dicInternetUser['noWhereClient'] = 'YES'
        # tables.dbd and address
        self.sNameOfTable =  "clients"
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
        #self.statusfields = ['lastname', 'city']
        dicClients = self.rpc.callRP('User.getClientInfo', self.sqlDicUser )
        self.out(dicClients)
        
        liClientIds = dicClients['clientsID']
        s = ''
        for iZ in range(len(liClientIds)-1):
            s += liClientIds[iZ]
            s += ' or id = '
        s += `liClientIds[len(liClientIds)-1]`
        
        self.sWhere = 'where id = ' + s
        self.out('sWhere by clients: ' + `self.sWhere`)
        
    def getAddress(self, id):
        dicRecords = self.load(id)
        liAddress = []
        if dicRecords:
            dicRecord = dicRecords[0]
            liAddress.append(dicRecord['name'])
            liAddress.append(dicRecord['name2'])
            liAddress.append(dicRecord['firstname'])
            liAddress.append(dicRecord['street'])
            liAddress.append(dicRecord['country'] + '-' +dicRecord['zip']+ ' ' + dicRecord['city'])
        if not liAddress:
            liAddress.append(' ')
            liAddress.append(' ')
            liAddress.append(' ')
            liAddress.append(' ')
            liAddress.append(' ')
            
        return liAddress

        
    def getName(self,  id):
        name = 'NONE'
        try:
            print "1"
            dicRecords = self.load(id)
            print "2", dicRecords
            dicRecord = dicRecords[0]
            print "3",  dicRecord
            name = dicRecord['name']
            print "4"
        except:
            print 'client name error'
        return name
        
