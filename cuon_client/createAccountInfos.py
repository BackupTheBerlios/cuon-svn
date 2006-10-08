
def setXml(nr, art, eg, des):
    s = '    <account>\n'
    s = s + '        <account_number>' + nr.strip() + '</account_number>\n'
    s = s + '        <type>' + art.strip() + '</type>\n'
    s = s + '        <eg>' + eg.strip() + '</eg>\n'
    s = s + '        <designation>' + des.strip() + '</designation>\n'
    s = s + '    </account>\n'
    print s
    return s

ch = raw_input('XSane, Tastatur, 4 (x/t/4,U) :')
    
if ch == 'd':

    f = open('test.acc','a')
    ok = True
    oldS = False
    des = ' '

    inf = open('0001.txt','r')
    if inf:
        while ok:
            s1 = inf.readline()
            if s1:
                print s1
                print '-----------------'
                liS = s1.split('  ')
                print liS
                i = len(liS)
                if i >= 1:
                    
                    try:
                        iAcc = int(liS[0].strip())
                        print '################################################'
                        print 'iAcc', iAcc
                        if iAcc > 0:
                            # Account-Number found
                            if oldS:
                                s = setXml(nr, art, eg, des)
                                f.write(s)    
                                
                            nr = liS[0]
                            des = liS[i-1].strip()
                            art = liS[1].strip()
                            eg = ''
                        
                            oldS = True
                    except:
                        print 'Integer Error - set strings'
                        for iB in liS:
                            des = des +' ' + iB.strip()
                        
                
                
            else:
                ok = False
                s = setXml(nr, art, eg, des)
                f.write(s)    
    f.close()
    inf.close()
    
elif ch == '4':
    fIn = open('SKR04.txt')
    fOut = open('sk04.xml','w')
    s = '<Account_Info'
    s += '    plan_number = "SK04" >\n'
    fOut.write(s)
    s = fIn.readline()
    ok = True
    while ok:
        liS = s.split('\t')
        des = ''
        if len(liS) > 1:
            nr = liS[0]
            des = liS[1].decode('latin-1').encode('utf-8') 
            eg = ''
            art = ''
            xml = setXml(nr,art,eg,des)
            fOut.write(xml)
            
        s = fIn.readline()
        if not s:
            ok = False
            
    fIn.close()
    s = '</Account_Info>\n'
    fOut.write(s)
    fOut.close()
    
elif ch == 'U':
    f = open('finance_account_datev_03.xml','r')
    f2 = open('t1.xml','a')
    s = f.readline()
    s2 = None
    z = 0
    while s:
        z = z + 1
        try:
            s2 = s.decode('latin-1')
            s2 = s2.encode('utf-8')
            print s2
            f2.write(s2)
        except:
            print 'error - line = ' , z
        s = f.readline()
    f.close()
    f2.close()
    
else:
    
    while ok:
        nr =  raw_input('Kontonummer  : ')
        art = raw_input('Art          : ')
        eg  = raw_input('EG           : ')
        des = raw_input('Beschreibung : ')

        s = setXml(nr, art, eg, des)

        f.write(s)
        o = raw_input('Weiter (j/n) :')
        if o != 'j':
            ok = False
        

