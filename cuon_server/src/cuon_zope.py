
import os
import sys
import time
import random	
import xmlrpclib

CUON_FS = None
CUON_AI_SERVER="http://localhost:8765"
#sys.path.append('/usr/lib/zope/lib/python')
f = open('/etc/cuon/cuon_zope.ini')
if f:
    s1 = f.readline()
    while s1:
        liIni = s1.split('=')
        if liIni[0].strip() == 'ZOPE_PYTHON':
            sys.path.append(liIni[1].strip())
        if liIni[0].strip() == 'CUON_FS':
            CUON_FS = liIni[1].strip()
        if liIni[0].strip() == 'CUON_AI_SERVER':
            CUON_AI_SERVER = liIni[1].strip()

        
        s1 = f.readline()
        
    f.close()

ai_server = xmlrpclib.ServerProxy(CUON_AI_SERVER)

    
from ZODB import FileStorage, DB

#CUON_FS = '/var/lib/zope/instance/default/var/Cuon.fs'
#CUON_FS = os.environ['CUON_FS']
 
def getInfoOfTable(sNameOfTable):
    storage = FileStorage.FileStorage(CUON_FS)
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

def packing():
    storage = FileStorage.FileStorage(CUON_FS)
    db = DB(storage)
    db.pack()


def saveInfoOfTable(sNameOfTable, table ):
#    t1 = cyr_table.cyr_table()
    t1 = table
    writeLog('ST1' + `t1`)
    writeLog('ST2'  + `CUON_FS`)
    storage = FileStorage.FileStorage(CUON_FS)
    writeLog(`'ST3' + storage`)
    
    db = DB(storage)
    writeLog('ST4' + `db`)
    connection = db.open()
    try:
        root = connection.root()
        root[sNameOfTable] = t1
        get_transaction().commit()
    except :
        writeLog('ST5' + 'saveInfoOfTable - ERROR')
        writeLog('ST6' + `exception`)
    connection.close()
    db.close()
    packing()


    

def getInfoOfEntry(sNameOfEntry):
    storage = FileStorage.FileStorage(CUON_FS)
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



def saveInfoOfEntry( sNameOfEntry, table ):
#    t1 = cyr_table.cyr_table()
    t1 = table
    
    storage = FileStorage.FileStorage(CUON_FS)
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
    packing()

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
    
               
def createSessionID(secValue = 36000):
    
    s = ''
	
    n = random.randint(0,1000000000)
    for i in range(27):
        ok = 1
    while ok:
        r = random.randint(65,122)
        if r < 91 or r > 96:
            ok = 0
            s = s + chr(r)
	
            s = s + `n`
            writeLog(s)
        return {'SessionID':s, 'endTime': time.time() + secValue}
	
def checkEndTime(fTime):
    writeLog('checkEndTime : ' + `fTime`)
    ok = 0
    try:
        if time.time() < fTime:
            ok = 1
    except:
        writeLog('Error in time-routine')
                
    return ok
	


def getAI(question):
    return ai_server.getAnswer(question)
