
import os
import sys
import time


sys.path.append('/usr/lib/zope/lib/python')

from ZODB import FileStorage, DB

ZopePath = '/var/lib/zope/instance/default/var/Cuon.fs'
 
def getInfoOfTable(sNameOfTable):
    storage = FileStorage.FileStorage(ZopePath)
    db = DB(storage)
    connection = db.open()
    t2 = None
    try:
        root = connection.root()
        t2 = root[sNameOfTable]
    except StandardError:
        pass
    
    connection.close()
    db.close()
    return t2



def saveInfoOfTable(self, sNameOfTable, table ):
#    t1 = cyr_table.cyr_table()
    t1 = table
    
    storage = FileStorage.FileStorage(ZopePath)
    db = DB(storage)
    connection = db.open()
    try:
        root = connection.root()
        root[sNameOfTable] = t1
        get_transaction().commit()
    except StandardError:
        pass
    connection.close()
    db.close()


def packing(self):
    storage = FileStorage.FileStorage(ZopePath)
    db = DB(storage)
    db.pack()
    

def getInfoOfEntry(sNameOfEntry):
    storage = FileStorage.FileStorage(ZopePath)
    db = DB(storage)
    connection = db.open()
    t2 = None
    try:
        root = connection.root()
        t2 = root[sNameOfEntry]
    except StandardError:
        pass

    connection.close()
    db.close()
    return t2



def saveInfoOfEntry(self, sNameOfEntry, table ):
#    t1 = cyr_table.cyr_table()
    t1 = table
    
    storage = FileStorage.FileStorage(ZopePath)
    db = DB(storage)
    connection = db.open()
    try:
        root = connection.root()
        root[sNameOfEntry] = t1
        get_transaction().commit()
    except StandardError:
        pass
        
    connection.close()
    db.close()

def createPsql(sDatabase, sHost, sPort, sUser,  sSql):
    
    # os.system('pysql ' + '-h ' + sHost + '-p ' + sPort + ' -U ' + sUser + ' ' + sDatabase + ' < ' + sSql) 

    sysCommand = 'echo \"' + sSql + '\" | ' + 'psql  ' + '-h ' + sHost + ' -p ' + sPort + ' -U ' + sUser +   ' '  + sDatabase
    
    os.system(sysCommand)

    return sysCommand


def writeLog(sLogEntry):
    file = open('cuon_sql.log','a')
    file.write(time.ctime(time.time() ))
    file.write('\n')
    file.write(sLogEntry)
    file.write('\n')
    file.close()
    
               
    
