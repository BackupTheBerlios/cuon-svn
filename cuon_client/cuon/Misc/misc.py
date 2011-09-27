# fix a bug in uuid, import it first !!

import uuid

import os
import sys
import time
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import datetime
import types 
import cuon.DMS.documentTools


class misc:
    def __init__(self):
        pass


    def getRandomFilename(self, sPrefix='.tmp'):
    
    
       return str(uuid.uuid4())+ sPrefix
        
#        n = random.randint(0,1000000000)
#        for i in range(13):
#            ok = 1
#            while ok:
#                r = random.randint(65,122)
#                if r < 91 or r > 96:
#                    ok = 0
#                    s = s + chr(r)
#                    
#        s = s + `n` + sPrefix
#
#        return s
#

class sendAsEmail():
    def __init__(self):
        pass
        
        
    def sendNormal(self, Type, sTo,  dicUser,  singleDMS,  dicVars ):
        sSubject = 'email'
        sText = 'information below'
        print 'Path for ',  Type, dicUser['prefPath']['templates']+'/supply_subject.tpl'
        if Type == 'Supply':
            try:
                
                f = open(dicUser['prefPath']['templates']+'/supply_subject.tpl')
                sSubject = f.read()
                f.close()
            except:
                print 'error read supply subject'
                
            try:
                f = open(dicUser['prefPath']['templates']+'/supply_text.tpl')
                sText = f.read()
                f.close()
            except:
                print 'error read supply Text'
                    
        
        
        dicVars['From'] = dicUser['Email']['From']
        dicVars['To'] = sTo
        
        dicVars['Body'] = sText + '\n\n -- \n' + dicUser['Email']['Signatur']
        dicVars['email_subject'] = sSubject
        
        print dicVars
        
        dt = cuon.DMS.documentTools.documentTools()
        dt.viewDocument(singleDMS,dicUser, dicVars,'sentAutomaticEmail', sTo)         
            
class Treeview:
    def __init__(self):
        pass
        
        
    def start(self,ts, sType='Text',sTitle = 'Title'):
        #ts = self.getWidget(sName)
        #treeview.set_model(liststore)
 
        if sType == 'Text':
            renderer = gtk.CellRendererText()
            
        column = gtk.TreeViewColumn(sTitle, renderer, text=0)
        ts.append_column(column)
        
    def fillTree(self, ts, liGroups,liNames,sConnect):
        ''' ts = Widget, '''
        print 'fill Tree'
        try:
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
                    groupname = ''
                    for name in liNames:
                        if isinstance(oneGroup[name], types.StringType):
                            groupname += oneGroup[name] + ', '
                        else:
                            groupname += `oneGroup[name]` + ', '
                    
                    iter = treestore.append(None,[groupname + '     ###' +`oneGroup['id']` ]) 
                    #print 'add iter', [groupname + '###' +`oneGroup['id']` ]
                    #iter2 = treestore.insert_after(iter,None,['TESTEN'])           
                #print 'End liDates'
            ts.show()
            #self.getWidget('scrolledwindow10').show()
            #exec (sConnect)
            print 'ts', ts
            
        except Exception, params:
            print Exception, params    
                
    
