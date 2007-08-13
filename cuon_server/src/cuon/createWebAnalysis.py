import os
import time 
import sys
sys.path.append('/usr/share/cuon/cuon_server/src/cuon')
import SVG

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
            
# now create the htmlside per day
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

# now create the htmlside per month
actualYear = {2007:{1:{},2:{},3:{},4:{},5:{},6:{},7:{},8:{},9:{},10:{},11:{},12:{} },2008:{1:{},2:{},3:{},4:{},5:{},6:{},7:{},8:{},9:{},10:{},11:{},12:{}},2009:{1:{},2:{},3:{},4:{},5:{},6:{},7:{},8:{},9:{},10:{},11:{},12:{}},2010:{1:{},2:{},3:{},4:{},5:{},6:{},7:{},8:{},9:{},10:{},11:{},12:{}},2011:{1:{},2:{},3:{},4:{},5:{},6:{},7:{},8:{},9:{},10:{},11:{},12:{}} }

actualSite = ''

##fDay = open('webalyser_days2.html','r')
##s = fDay.readline()
##while s:
##    s = s.strip()
##    if s.find('<H4>') > 0:
##        print s
##        print 'h4', s.find('<H4>')
##        print '/h4', s.find('</H4>')
##        actualSite = s[s.find('<H4>')+4:s.find('</H4>')]
##        print actualSite
##        actualYear[iYear][iMonth][actualSite] = []
##    s = fDay.readline()
##
##fDay.close()

fDay = open('webalyser_days.html','r')
        
s = fDay.readline()
iYear = 0
iMonth = 0
iDay = 0
iValue = 0
lastYear = 0
lastMonth = 0
lastSite = ''
while s:
    s = s.strip()
    if s.find('<H4>') > 0:
        print s
        print 'h4', s.find('<H4>')
        print '/h4', s.find('</H4>')
        actualSite = s[s.find('<H4>')+4:s.find('</H4>')]
        print actualSite
        
    liS = s.split(' ')
    print 'liS = ', liS
    if len(liS) == 2:
        sDate = liS[0]
        sValue = liS[1]
        if len(sDate) > 1 :
            if len(sDate) > 9 :
                #print 'try'
                try:
                    iTest = int(sDate[0:4])
                    #print 'iTest', iTest
                    iYear = int(sDate[0:4]) 
                    #print 'iYear', iYear
                    iMonth = int(sDate[5:7])
                    #print 'iMonth', iMonth
                    #print sDate[8:10]
                    iDay = int(sDate[8:10])
                    #print sDate[8:11], sValue[0:sValue.find('<')]
                    iValue = int(sValue[0:sValue.find('<')])
                    #print iYear,iMonth,iDay,iValue
                    if actualSite != lastSite:
                        actualYear[iYear][iMonth][actualSite] = []
                        print 'new site = ', actualSite
                        lastSite = actualSite
                    
                    
                    

                    print '------------------ actualSite',iYear,iMonth,actualSite
                    if  not actualYear[iYear][iMonth].has_key(actualSite):
                         actualYear[iYear][iMonth][actualSite] = []
                    actualYear[iYear][iMonth][actualSite].append((iDay,iValue))
                    print 'aY = ', actualYear[iYear][iMonth][actualSite]
                    #print actualYear
                    
                except Exception, param:
                    print Exception, param
                    
                
    s = fDay.readline()            

fDay.close()
print actualYear


liYear = actualYear.keys()
liYear.sort()
HTML_SIDE = open('web_year.html','w')
sHTML = '<html><body>\n'
print liYear
for iYear in liYear:
    liMonth = actualYear[iYear].keys()
    liMonth.sort()
    for iMonth in liMonth:
        print iYear, iMonth
        liSites = actualYear[iYear][iMonth].keys()
        liSites.sort()
        sHTML += '<H3>' + `iMonth` + ' ' + `iYear` + '</H3>\n'
        
        print liSites
        if liSites:
            for sSite in liSites:
                
                liValues = actualYear[iYear][iMonth][sSite]
                
                dicScene = {}
                dicScene['title'] = sSite + '_' + `iYear` + `iMonth`
                dicScene['height'] = 1150
                dicScene['width'] = 1150
                dicScene['xMargin'] = 60
                dicScene['yMargin'] = 20
                dicScene['colorMargin'] = (122,25,215)
                dicScene['colorFill'] = (187,255,215)
                dicScene['xFontSize'] = 20
                dicScene['yFontSize'] = 20
                dicScene['Axis'] = {}    
                dicScene['Axis']['xAxisMargin'] = 20
                dicScene['Axis']['yAxisMargin'] = 20
                dicScene['Axis']['colorMargin'] = (222,125,15)
                dicScene['Axis']['colorFill'] = (21,20,145)
                dicScene['Axis']['colorTextFG'] = (22,125,15)
                dicScene['Axis']['colorTextBG'] = (225,225,215)
            
                svg = SVG.SVG()
                #print dicScene['title']
                svg.BarChart(dicScene,liValues)
                os.system('convert ' + dicScene['title'] + '.svg '  +dicScene['title'] + '.png ')
                sHTML += '<img src="' + dicScene['title'] + '.png" width="90%" height="90%" alt="" /><br>\n'
                sHTML += 'Zugriffe ' + `iMonth` + ' ' + `iYear` + ' ' + dicScene['title'] + '<br><br>\n'
sHTML += '\n</body></html>\n'
HTML_SIDE.write(sHTML)
HTML_SIDE.close()
                
            




