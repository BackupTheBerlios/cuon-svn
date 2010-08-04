# -*- coding: utf-8 -*-
##Copyright (C) [2010]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 

import sys
import xml.dom.minidom as dom
#from xml.etree.ElementTree import ElementTree


class createHtml():
    def __init__(self,  gladeFile):
        
        self.Doc = dom.parse(gladeFile +'.glade')
        
        self.HTML = 'XUL'
        self.s = ''
        self.sEnd = []
        self.sMenuEnd = None
        self.startConvert(gladeFile)
        
    def startConvert(self,  gladeFile):

        if self.HTML == 'XUL':
            self.s= '<?xml version="1.0"?> \n<?xml-stylesheet href="chrome://global/skin/" type="text/css"?> \n<!-- Extremely recommended to keep this css include!! --> \n'
        else:
            self.s = '<HTML><BODY>\n'
            
        #print self.Doc.toxml()
        tagRoot = self.Doc.documentElement
        print 'Root = ',  tagRoot
        self.setTags(tagRoot)
        
        
#        
#        
#        
#                
#                    
        self.sEnd.reverse()
        if self.sMenuEnd:
            self.s += self.sMenuEnd
            self.sMenuEnd = None 
        for s in self.sEnd:
                self.s += s
        if self.HTML == 'XUL':   
            
            self.s += ''
        else:
            
            self.s += '\n </BODY></HTML>'
            
        print self.s
        f = open(gladeFile+'.xul', 'w')
        f.write(self.s)
        f.close()
        
                
    def setTags(self, tagRoot):
        tags = tagRoot.childNodes
        #print tags
        for tag in tags:
            try:
                #print '1-- ',  tag,  tag.nodeType
                if tag.nodeType == 1:
                    
                    val =  tag.attributes['class'].value
                    print 'val = ',  val
                    if val not in ['GtkMenuBar',  'GtkMenuItem',  'GtkMenu']:
                        if self.sMenuEnd:
                            self.s += self.sMenuEnd
                            self.sMenuEnd = None 
                    
                    if val == 'GtkWindow':
                        self.s += self.getGtkWindow(tag)
                    elif val == 'GtkVBox':
                        self.s += self.getGtkVBox(tag)
                        
                        
                    
                    elif val == 'GtkMenuBar':
                        self.s += self.getGtkMenuBar(tag)   
                    elif val == 'GtkMenuItem':
                        print 'val = ',  val
                        
                        self.s += self.getGtkMenuItem(tag)      
            except Exception,  params:
                #print Exception,  params
                pass
            
            self.setTags(tag)
            
    def getGtkWindow(self, tag):
        # set html properties from glade 
        id =  tag.attributes['id'].value
        atts = tag.childNodes
        #at1 = tag.getAttributeNode('width_request')
        #print atts
        for att in atts:
            #print 'att = ',  att                   
            childs =  att.childNodes
            try:
                if att.getAttribute('name'):
                    #print '1--- ',  att.getAttribute('name')
                    for child in childs:
                        print 'child = ', child.nodeValue
            except:
                pass
    
              
        if self.HTML == 'XUL':   
            self.s +='<window id="' + id + '" title="cuon1" xmlns="http://www.mozilla.org/keymaster/gatekeeper/there.is.only.xul">\n '
            
            self.sEnd.append( '\n</window>\n')

    def getGtkVBox(self, tag):
        # set html properties from glade 
        id =  tag.attributes['id'].value
        atts = tag.childNodes
        #at1 = tag.getAttributeNode('width_request')
        #print atts
        for att in atts:
            #print 'att = ',  att                   
            childs =  att.childNodes
            try:
                if att.getAttribute('name'):
                    #print '1--- ',  att.getAttribute('name')
                    for child in childs:
                        print 'child = ', child.nodeValue
            except:
                pass
                            
              
        if self.HTML == 'XUL':   
            self.s +='<vbox >\n '
            
            self.sEnd.append( '\n</vbox>\n')

    def getGtkMenuBar(self, tag):
        # set html properties from glade 
        id =  tag.attributes['id'].value
        atts = tag.childNodes
        #at1 = tag.getAttributeNode('width_request')
        #print atts
        for att in atts:
            #print 'att = ',  att                   
            childs =  att.childNodes
            try:
                if att.getAttribute('name'):
                    #print '1--- ',  att.getAttribute('name')
                    for child in childs:
                        print 'child = ', child.nodeValue
            except:
                pass
                            
              
        if self.HTML == 'XUL':   
            self.s +='<menubar  id="' + id + '">\n '
            
            self.sEnd.append( '\n</menubar>\n')

    def getGtkMenuItem(self, tag):
        # set html properties from glade 
        label = None
        id =  tag.attributes['id'].value
       
        #print 'find Menuitem 1'
        atts = tag.childNodes
        #print 'find Menuitem 2'
        mainmenu = False
        #print 'find Menuitem'
        #at1 = tag.getAttributeNode('width_request')
        #print atts
        for att in atts:
            print 'atts nodename = ',  att.nodeName                  
            childs =  att.childNodes
            try:
                if att.nodeName == 'property':
                    if att.getAttribute('name'):
                        
                        print '1--- ',  att.getAttribute('name')
                        for child in childs:
                            print 'child Menuitem = ', child.nodeValue
                            print 'child Menuitem2  = ', child.nodeName
                            try:
                                if att.getAttribute('name') == 'label':
                                    label =  child.nodeValue
                            except:
                                pass
                elif att.nodeName == 'signal':  
                    
                    if att.getAttribute('name'):
                        
                        print '1--- ',  att.getAttribute('name')
                        for child in childs:
                            print 'child signal 1= ', child.nodeValue
                            print 'child Signal 2  = ', child.nodeName
                            try:
                                
                                signal =  child.nodeValue
                            except:
                                pass
                    elif att.getAttribute('handler'):
                        
                        print '1--- ',  att.getAttribute('handler')
                        for child in childs:
                            print 'child handler 1= ', child.nodeValue
                            print 'child handler 2  = ', child.nodeName
                            try:
                                
                                handler =  child.nodeValue
                            except:
                                pass            
                                
            except:
                pass
            
            try:
                t2 = att.childNodes
                for t3 in t2:
                    if t3.nodeType == 1:
                        if t3.getAttribute('class'):
                            print '3--- ',  t3.getAttribute('class')
                            val =  t3.attributes['class'].value
                            print '4 ---' ,  val 
                            if val == 'GtkMenu':
                                mainmenu = True
                            
            except:
                pass
                    
                    
                    
        if id and label:            
            if self.HTML == 'XUL':  
                print 'id bymenuitem',  id
           
                if mainmenu:
                    if self.sMenuEnd:
                        self.s += self.sMenuEnd
                        self.sMenuEnd = None
                        
                    self.s +='<menu  id="' + id + '" label="'+ label  +'">\n ' 
                    self.s += '<menupopup id="' +  id +'_99">\n'  
                    self.sMenuEnd = ( '</menupopup>  \n</menu>\n')
                else:
                    self.s +='<menuitem  id="' + id + '" label="'+ label +'" />\n' 
                
                    
    
ch = createHtml(sys.argv[1])
