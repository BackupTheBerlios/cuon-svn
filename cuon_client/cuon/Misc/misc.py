

import os
import sys
import time
import random	

import datetime

class misc:
    def __init__(self):
        pass


    def getRandomFilename(self, sPrefix='.tmp'):
    
    
        s = ''
        
        n = random.randint(0,1000000000)
        for i in range(13):
            ok = 1
            while ok:
                r = random.randint(65,122)
                if r < 91 or r > 96:
                    ok = 0
                    s = s + chr(r)
                    
        s = s + `n` + sPrefix

        return s


class Treeview:
    def __init__(self):
        pass
        
        
    def start(self,sName, sType='Text',sTitle = 'Title'):
        ts = self.getWidget(sName)
        #treeview.set_model(liststore)
 
        if sType == 'Text':
            renderer = gtk.CellRendererText()
            
        column = gtk.TreeViewColumn(sTitle, renderer, text=0)
        ts.append_column(column)
        
    def fillTree(self, sName, liGroups,liNames,sConnect):
        print 'fill Tree'
        try:
            ts = self.getWidget(sName)
            print 'ts = ', ts
            treestore = gtk.TreeStore(object)
            treestore = gtk.TreeStore(str)
            ts.set_model(treestore)
                
            if liGroups:
                lastGroup = None
                
                #iter = treestore.append(None,[_('Schedul')])
                #print 'iter = ', iter
                iter2 = None
                iter3 = None
                #liDates.reverse()
                for oneGroup in liGroups:
                    groupname = oneGroup[liNames[0]]
                    
                    iter = treestore.append(None,[groupname + '     ###' +`oneGroup['id']` ]) 
                    #print 'add iter', [groupname + '###' +`oneGroup['id']` ]
                    
                    #iter2 = treestore.insert_after(iter,None,['TESTEN'])           
                #print 'End liDates'
            ts.show()
            #self.getWidget('scrolledwindow10').show()
            EXEC (sConnect)
            print 'ts', ts
            
        except Exception, params:
            print Exception, params    
                
    
