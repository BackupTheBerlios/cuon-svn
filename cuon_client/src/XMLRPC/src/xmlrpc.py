##Copyright (C) [2003]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 


import xmlrpclib
from xmlrpclib import Server
import cuon.TypeDefs
from cuon.Databases.dumps import dumps
from cuon.Logging.logs import logs

class myXmlRpc(dumps, logs):
    def __init__(self):
        dumps.__init__(self)
        logs.__init__(self)
        self.openDB()
        self.td = self.loadObject('td')
        self.closeDB()
        

    def getServer(self):
        self.out( self.td.server)
        self.out( 'http://' + `self.td.server`)
        self.out( '++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        self.out( ' ')
        
        return Server('http://' + self.td.server)

    def test(self):
        s1 = "select * from address"
        recordset = self.getServer().src.sql.py_executeNormalQuery(s1)
        for record in recordset:
            self.out( record)
            for key in record:
                self.out( key)
                self.out( record[key])


    def getInfoOfTable(self, sNameOfTable):
        return self.getServer().src.Databases.py_getTable(sNameOfTable)
    

        
# wert = server.py_parseResult(recordset, 0, "id" )
# self.out( wert


