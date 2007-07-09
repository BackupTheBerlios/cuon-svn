import os
import time 

liDir = os.listdir('./')
if liDir:
    for fName in liDir:
        
        #print 'fname = ', fName,fName.find('.counter')
        if fName.find('.counter') > 0:
            try:
                f = open(fName,'r')
            
                z1 = int(f.readline().strip())
                
            except:
                z1 = 0
            try:
                f.close()
            except:
                pass
            try:
                f = open(fName,'w')
            
                f.write('0')
                f.close()
            except:
                pass
            try:
                f.close()
            except:
                pass
            f = open(fName[0:fName.find('counter')] + 'daily','a')    
            print 'z1 = ', z1
            f.write(time.strftime('%Y.%m.%d', time.localtime()) + ' ' + `z1` + '\n')
            f.close()
            
# now create the htmlside
liDir = os.listdir('./')
fDay = open('webalyser_days.html','w')    
fDay.write('<html><body><H2>Hits per Day</H2>\n')
f = None
if liDir:
    for fName in liDir:
        
        if fName.find('.daily') > 0:
            fDay.write('<H4>' + fName[0:fName.find('.daily')] + '</H4>\n')
            try:
                f = open(fName,'r')
            
                s1 = f.readline().strip()
                while s1:
                   fDay.write(s1 + '<br>\n') 
                   s1 = f.readline().strip()
                f.close()
            except:
                if f:
                    f.close()
                
            fDay.write('<br><br>')
    
    
fDay.write('</body></html>')
fDay.close()
