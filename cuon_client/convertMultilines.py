import sys


def writeValues(f_out, liS1,liForbidden):
    #print liS1
    s = ''
    bOK = True
    for forbidden in liForbidden:
        #forbidden = forbidden.decode('ISO-8859-15')
        #print forbidden
        sL2 = liS1[2].decode('ISO-8859-15').encode('utf-8')
        sL3 = liS1[3].decode('ISO-8859-15').encode('utf-8')
        sL16 = liS1[16].decode('ISO-8859-15').encode('utf-8')
        #print sL2
        
        if sL2.find(forbidden) >= 0:
            bOK = False
        if sL3.find(forbidden) >= 0:
            bOK = False
        if sL16.find(forbidden) >= 0:
            bOK = False    
    if bOK:
        for i in liS1:
            
            if len(i) > 49:
                i=i[0:49]
            s += i.strip() + ';'
            
        s = s[:len(s)-1]
        #print 's = ', s
    
        f_out.write(s+'\n')
    else:
        print 'This is erase:'
        print liS1
        

print sys.argv
sFile = sys.argv[1]
f_in = open(sFile)
f_out = open(sFile +'_conv','a')
s1 = f_in.readline()
while s1:
    s2 = s1.replace('","','";"')
    f_out.write(s2)
    
    s1 = f_in.readline()

f_in.close()
f_out.close()

f_in = open(sFile +'_conv')
f_out = open(sFile +'_out','a')
s1 = None
ok = False

s1 = f_in.readline()
liAll = []
while s1:
    #print '----------------------------------------------------------------'
    #print s1
    liS1 = s1.split(';')
    liS1.append('\"\"')
    liS1.append('\"\"')
    liS1.append('\"\"')
    
    if len(liAll) > 0:
        lastIndex = len(liAll) -1
        liS2 = liAll[lastIndex]
        #print liS1
        #print '::::::'
        #print liS2
        #print 
        
        if liS1[11].strip() == 'Telefax':
            #print 'set Telefax'
            
            liS1[20] = liS1[15]
            #print liS1
        elif liS1[11].strip() == 'Mobil':
            liS1[21] = liS1[15]
        else:
            #print 'Normal'
            liS1[19] = liS1[15]
        #print liS1
        #print '::::::'
        #print liS2
        #print 
        
        if liS1[1] == liS2[1] and liS1[2] == liS2[2] and  liS1[4] == liS2[4] and liS1[7] == liS2[7] and liS1[10] == liS2[10]:
            #print liS1[1], liS2[1]
            #print liS1[2], liS2[2]
            #print liS1[4], liS2[4]
            #print liS1[7], liS2[7]
            #print liS1[10], liS2[10]
        
            #print 'len liS1', len(liS1)
            if liS1[11].strip() == '"Telefax"':
                liS2[20] = liS1[15]
            elif liS1[11].strip() == '"Mobil"':
                liS2[21] = liS1[15]
            else:
                liS2[19] = liS1[15]
            liAll[lastIndex] = liS2
            
        else:
            liAll.append(liS1)
            
    else:
        liAll.append(liS1)
        
    s1 = f_in.readline()
    #print '################################################################'
    #print 
#print len(liAll)
liForb = []
try:
  f = open('forbidden.txt','r')
  s = f.readline()
  while s:
    sEncode = 'latin-1'
    sDescode = 'latin-1'
    #s = s.decode(sDescode)
    #s = s.encode(sEncode)
    
    print sDescode + ' ' + sEncode, s
    liForb.append(s.strip()[:-1])
    s = f.readline()
except Exception, params:
    print Exception, params
print liForb

f_in.close()
for liS in liAll:
    writeValues(f_out,liS, liForb)
f_out.close()


    
