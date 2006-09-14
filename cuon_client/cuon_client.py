#!/usr/bin/env python

import os, sys
import shutil
import ConfigParser
# create cuon_home
#iCHome=~/cuon
#iCHomeReports=~/cuon/Reports
#iCHomeDocs=~/cuon/Docs
#iCHomeInvoice=~/cuon/Invoice
#iCHomePickup=~/cuon/Pickup
#iCHomeDelivery=~/cuon/Delivery
#iCHomeOO=~/cuon/OO


if len(sys.argv) > 1:
    server =  sys.argv[1]
    print "Server = ", server
    print "-------------####################--------------"

if len(sys.argv) > 2:
    Locale =  sys.argv[2]
    print "Locale = ", Locale
    print "-------------####################--------------"

print os.environ['HOME']
cuon_home = os.environ['HOME'] + '/cuon_newclient'
cuon_bin = cuon_home + '/bin'

try:
    os.removedirs(cuon_home)
except:
    pass
try:
    os.mkdir(cuon_home)
except Exception, params:
    print Exception, params
    
try:   
    os.mkdir(cuon_bin)
except Exception, params:
    print Exception, params
# bin dir
try:
    #shutil.copytree('Client/CUON/cuon',cuon_bin )
    os.system('cp -R Client/CUON/* ' + cuon_bin)
    os.system('cp -R Client/cuonObjects ' + cuon_home)
    
except Exception, params:
    print 'shutil'
    print Exception, params

# copy glade-files
dirGlade = 'Client/usr/share/cuon/glade'
liGlade = os.listdir(dirGlade)
print liGlade
for i in liGlade:
    s = 'glade_' + i[0:i.find('.glade')] + '.xml'
    print s
    shutil.copyfile(dirGlade + '/' + i,cuon_home + '/' + s)
    
# copy locale
os.system('cp -R Client/locale ' +  cuon_home)

# Todo 
# icon


# create startFile

f = open(cuon_bin + '/startcuon','w')
s = '#!/usr/bin/sh \n'
s += 'python Cuon.py ' + server + ' client NO ' + cuon_home + '/locale/' +  Locale

f.write(s)
f.close()

# create tar-files
cpParser = ConfigParser.ConfigParser()
f = file('Client/CUON/version.cfg','r')

cpParser.readfp(f)
f.close()

print cpParser.sections()
try:
            
    n1 = cpParser.get('version', 'Name')
    v1 = cpParser.get('version', 'Major') + '.' + cpParser.get('version', 'Minor') + '-' + cpParser.get('version', 'Rev')
    #sFile = self.cpParser.get('version', 'File')
except Exception, param:
    print "Error read version-configfile" 
    print Exception
    print param
os.system('rm cuon_client-' + v1 + 'tar.bz2 ')
print os.system('S1=`pwd` ; cd ' + cuon_home + ' ; tar -cjf $S1/cuon_client-' + v1 + 'tar.bz2 *' )







