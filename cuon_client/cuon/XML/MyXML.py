# -*- coding: utf-8 -*-

##Copyright (C) [2003]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 

from xml.dom import minidom
#from xml.dom.ext.reader import Sax2
#from xml.dom import ext
from xml.dom import Node
#from xml.dom.ext.reader import PyExpat
from cuon.Logging.logs import logs
import string
# from amara import *

class MyXML(logs):
    """
    @author: Juergen Hamel
    @organization: Cyrus-Computer GmbH, D-32584 Loehne
    @copyright: by Juergen Hamel
    @license: GPL ( GNU GENERAL PUBLIC LICENSE )
    @contact: jh@cyrus.de
    """
    def __init__(self):
        logs.__init__(self) 
     
        self.setLogLevel(1)
        self.out("MyXML startet")
        

    def NotTextNodeError(self):
        pass

    def getTextFromNode(self, node):
        """
        scans through all children of node and gathers the
        text. if node has non-text child-nodes, then
        NotTextNodeError is raised.
        """
        t = ""
        for n in node.childNodes:
            if n.nodeType == n.TEXT_NODE:
                t += n.nodeValue
            else:
                raise NotTextNodeError
        return t
    
    
    def nodeToDic(self, node):
        """
        nodeToDic() scans through the children of node and makes a
        dictionary from the content.
            1. three cases are differentiated.
                  - if the node contains no other nodes, it is a text-node
                    and {nodeName:text} is merged into the dictionary.
                  - if the node has the attribute "method" set to "true",
                    then it's children will be appended to a list and this
                    list is merged to the dictionary in the form: {nodeName:list}.
                  - else, nodeToDic() will call itself recursively on
                    the nodes children (merging {nodeName:nodeToDic()} to
                    the dictionary).
        """
        print "nodeToDic"
        dic = {} 
        for n in node.childNodes:
            if n.nodeType != n.ELEMENT_NODE:
                continue
            if n.getAttribute("multiple") == "true":
                # node with multiple children:
                # put them in a list
                l = []
                for c in n.childNodes:
                    if c.nodeType != n.ELEMENT_NODE:
                        continue
                    l.append(nodeToDic(c))
                    dic.update({n.nodeName:l })
                    continue
        
                try:
                    text = getTextFromNode(n)
                except NotTextNodeError:
                    # 'normal' node
                    dic.update({n.nodeName:nodeToDic(n)})
                    continue
                
                # text node
                dic.update({n.nodeName:text})
                continue
            return dic
        
        
    def readDocument(self, filename):
        #    reader = PyExpat.Reader()
        #    doc = reader.fromUri(filename)
        #build a DOM tree from the file
        #self.out("filename = " + `filename`)
        doc = None
        try:
            doc = minidom.parse(filename)
        except Exception, param:
                print 'unknown exception by read XML-document'
                print `Exception`
                print `param`
        
        #self.out("Document =  " + doc.toxml() )


        return  doc
              
        
    def getRootNode(self, doc):
        return doc.childNodes
      
    def getSingleNode(self,  cyNode,  cyValue):
        return cyNode.getElementsByTagName(cyValue)  
        
        
    def getListOfTables(self, cyNode):
        allTable = cyNode.getElementsByTagName("table")
        allNames = []
        for iNode in allTable:
            allName = iNode.getElementsByTagName("nameOfTable")
            for oneName in allName:
                rc = oneName.firstChild
                if rc.nodeType == Node.TEXT_NODE:
                    self.out("rc.data = " +  rc.data)
                    allNames.append( rc.data) 
            
        return allNames

    def getListOfSequences(self, cyNode):
        allTable = cyNode.getElementsByTagName("database_sequence")
        allNames = []
        for iNode in allTable:
            allName = iNode.getElementsByTagName("nameOfSequence")
            for oneName in allName:
                rc = oneName.firstChild
                if rc.nodeType == Node.TEXT_NODE:
                    self.out("rc.data = " +  rc.data)
                    allNames.append( rc.data) 
        print "sequences allNames", allNames 
        return allNames
        
    def getListOfForeignKeys(self, cyNode):
        allTable = cyNode.getElementsByTagName("foreign_key")
        allNames = []
        for iNode in allTable:
            allName = iNode.getElementsByTagName("foreign_key_name")
            for oneName in allName:
                rc = oneName.firstChild
                if rc.nodeType == Node.TEXT_NODE:
                    self.out("rc.data = " +  rc.data)
                    allNames.append( rc.data) 
        print "foreign_key allNames", allNames 
        return allNames

    def getTable(self, cyNode, cyName, cyValue):

        allTable = cyNode.getElementsByTagName("table")
        for iNode in allTable:
            allName = iNode.getElementsByTagName("nameOfTable")
            for oneName in allName:
                rc = oneName.firstChild
                if rc.nodeType == Node.TEXT_NODE:
                    self.out("rc.data = " +  rc.data)
                    if(cyValue == rc.data):
                        self.out( iNode.toxml())
                        self.out("rc.data found = " +  rc.data)
                        return iNode

                    
    def getSequence(self, cyNode, cyName, cyValue):

        allTable = cyNode.getElementsByTagName("database_sequence")
        for iNode in allTable:
            allName = iNode.getElementsByTagName("nameOfSequence")
            for oneName in allName:
                rc = oneName.firstChild
                if rc.nodeType == Node.TEXT_NODE:
                    self.out("rc.data = " +  rc.data)
                    if(cyValue == rc.data):
                        self.out( iNode.toxml())
                        self.out("rc.data found = " +  rc.data)
                        return iNode
                                     
    def getForeignKey(self, cyNode, cyName, cyValue):

        allTable = cyNode.getElementsByTagName("foreign_key")
        for iNode in allTable:
            allName = iNode.getElementsByTagName("foreign_key_name")
            for oneName in allName:
                rc = oneName.firstChild
                if rc.nodeType == Node.TEXT_NODE:
                    self.out("rc.data = " +  rc.data)
                    if(cyValue == rc.data):
                        self.out( iNode.toxml())
                        self.out("rc.data found = " +  rc.data)
                        return iNode
                        
    def getNumberOfFields(self, cyTable):
        self.out("cyTable =  " + cyTable.toxml() )

        allColumns = cyTable.getElementsByTagName("field")
        return len(allColumns)
    

    def getColumnAt(self, cyTable, iIndex):
        allColumns = cyTable.getElementsByTagName("field")
        self.out( allColumns[iIndex].toxml())
        return allColumns[iIndex]


    def getTableSpecification(self, cyTable, sValue):
        self.out("cyTable =  = " + cyTable.toxml() )
        nameTag = cyTable.getElementsByTagName(sValue)
        for oneName in nameTag:
            rc = oneName.firstChild
            if rc.nodeType == Node.TEXT_NODE:
                return rc.data
            else:
                return "EMPTY"
          

    def getColumnSpecification(self, cyColumn, sValue):
        nameTag = cyColumn.getElementsByTagName(sValue)
        for oneName in nameTag:
            rc = oneName.firstChild
            if rc:
                if rc.nodeType == Node.TEXT_NODE:
                    return rc.data
            else:
                return None
            
                        
        
    def test(self):
        import pprint
        doc = self.readDocument("/etc/cuon/tables.dbd")
        for n in doc.childNodes :
            print  n.nodeName
            for n2 in n.childNodes :
                print n2.nodeName
                

        cyRootNode = self.getRootNode(doc)
        print "----------------------------------------------------------------------------------"
        for n in cyRootNode :
            print  n.nodeName
        print cyRootNode[0].nodeName

        
        cyTestNode = self.getTable(cyRootNode[0], "table", "articles")
        table.createTable(cyTestNode)
        

    def getListOfEntries(self, cyNode):
        allEntries = cyNode.getElementsByTagName("table")
        allNames = []
        print cyNode.toxml()
        print '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
        
        for iNode in allEntries:
            print iNode.toxml()
            ent =  iNode.getElementsByTagName("entry")
           
            for eNode in ent:
                eName = eNode.getElementsByTagName("name")
                rc = eName[0].firstChild
                if rc.nodeType == Node.TEXT_NODE:
                    self.out("rc.data = " +  rc.data)
                    allNames.append( rc.data) 
        print '###########################################################################'
        print allNames
        print '###########################################################################'
        
        return allNames
    
    def getEntries(self, sFileName):
        doc = self.readDocument(sFileName)
        

    def getEntry(self, cyNode, cyName, cyValue):
        
        for tNode in cyNode:
            oneTable = tNode.getElementsByTagName("table")
            print 'oneTable = ' + oneTable[0].toxml()
            for oneTableEntry  in oneTable:
                te = oneTableEntry.getElementsByTagName("entry")
              ##  print '**************************************************'
##                for te1 in te:
##                    print self.getEntrySpecification( te1, cyValue)
            
                

        return oneTableEntry
        

    
    
    def getNumberOfEntries(self, cyEntries):
            all = cyEntries.getElementsByTagName("entry")
            return len(all)
    

    def getEntryAt(self, cyEntries, iIndex):
        all = cyEntries.getElementsByTagName("entry")
        self.out( all[iIndex].toxml())
        return all[iIndex]



    def getEntrySpecification(self, cyEntry, sValue):
        try:
            nameTag = cyEntry.getElementsByTagName(sValue)
            for oneName in nameTag:
                rc = oneName.firstChild
                if rc:
                    if rc.nodeType == Node.TEXT_NODE:
                        return rc.data
                    else:
                        return "EMPTY"
                else:
                    return "EMPTY"
        except:
            return "EMPTY"
            

    def getNode(self, cyNode, cyValue):
        #print cyNode[0].toxml()
        OneNode = cyNode[0]
        element1 = OneNode.getElementsByTagName(cyValue)
        return element1
                             

    def getNodeData(self, cyNode, sValue):
        nameTag = cyNode[0]
        oneName = nameTag.getElementsByTagName(sValue)
        for oneElement in oneName:
            rc = oneElement.firstChild
            if rc.nodeType == Node.TEXT_NODE:
                return rc.data
            else:
                return "EMPTY"   

    def getNodes(self, cyNode, cyValue):
        #print cyNode[0].toxml()
        elements = cyNode.getElementsByTagName(cyValue)
        return elements

    def getData(self, cyNode):
        rc = cyNode.firstChild
        if rc and rc.nodeType == Node.TEXT_NODE:
            return rc.data
        else:
            return "EMPTY"   

            
    def getAttributValue(self, node, sName):
        s = None
        #print 'getAttributValue'
        #print node.toxml()
        #print '------------------------------------------------------'
        if node.hasAttributes():
            #print `node.attributes`
            #print '+++++++++++++++++++++++++++++++++++++++++++++++++++'
            s = node.getAttribute(sName)
            #print s
        return s
        
    def createDoc(self,  sDTD='super_special.dtd',sDTD2='super_special2.dtd',   encoding = 'utf-8',  sRoot='test'  ):
        impl = minidom.getDOMImplementation()
        #dt = impl.createDocumentType(sRoot , None, None)
        doc = impl.createDocument(None, sRoot, None)
        print doc.toxml()
        return doc
        
        
    def readXmlString(self,  sXml):    
        return parseString(sXml)
        
    def dic2xml(self,  doc, liParams, sTag=None):
        print 'liParams = ',  liParams
        if sTag:
            rootNode = self.getRootElement(doc)
            tag = self.getSingleNode(rootNode, sTag)[0]
        else:
            tag = None
        for dicParams in liParams:
            doc = self.append2doc(doc,  dicParams,  tag)
        return doc
    
    def getDoc2String(self, doc):
        return doc.toxml("UTF-8")
        
    def append2doc(self, doc, dicParams,  tag = None):

        if tag is None:
            root = doc.documentElement
        else:
            root = tag
        
        #print 'dicParams = ',   dicParams
        for key, value in dicParams.iteritems():
            tag = doc.createElement(key)
            root.appendChild(tag)
            if isinstance(value, dict):
                self.append2doc(doc, value, tag)
            else:
                root.appendChild(tag)
                print key,  value
                if value:
                    if isinstance(value, int):
                       tag_txt = doc.createTextNode(`value`) 
                    elif isinstance(value, float):
                       tag_txt = doc.createTextNode(`value`)
                    else:
                        tag_txt = doc.createTextNode(value)
                else:
                    tag_txt = doc.createTextNode("")
                tag.appendChild(tag_txt)
     
        return doc
    def xmltodict(self,  xmlstring):
        doc = minidom.parseString(xmlstring)
        self.remove_whilespace_nodes(doc.documentElement)
        return self.elementtodict(doc.documentElement)
    
    def elementtodict(self,  parent):
        child = parent.firstChild
        if (not child):
            return None
        elif (child.nodeType == minidom.Node.TEXT_NODE):
            return child.nodeValue
        
        d={}
        while child is not None:
            if (child.nodeType == minidom.Node.ELEMENT_NODE):
                try:
                    d[child.tagName]
                except KeyError:
                    d[child.tagName]=[]
                d[child.tagName].append(self.elementtodict(child))
            child = child.nextSibling
        return d
    
    def remove_whilespace_nodes(self,  node, unlink=True):
        remove_list = []
        for child in node.childNodes:
            if child.nodeType == minidom.Node.TEXT_NODE and not child.data.strip():
                remove_list.append(child)
            elif child.hasChildNodes():
                self.remove_whilespace_nodes(child, unlink)
        for node in remove_list:
            node.parentNode.removeChild(node)
            if unlink:
                node.unlink()
        
    def getRootElement(self, doc):
        return doc.documentElement
        
    def addElementToNode(self, Node, sName):
        x = Node.createElement(sName)
        print x
        self.Node.appendChild(x)
        return Node 
        
    def addElement(self, doc,  sName ):
        x = doc.createElement(sName)
        print x
        self.getRootElement(doc).appendChild(x)
        return doc       
        
##        pprint.pprint(dic)
##        print dic["database"]["name"]
##        print
##        for item in dic["database"]["table"]:
##            print "table Name:", item["name"]
##            print "Item's Value:", item["x"]
            
                


##import pprint
##import xml.dom.minidom
##from xml.dom.minidom import Node
##doc = xml.dom.minidom.parse("books.xml")
##mapping = {}
##for node in doc.getElementsByTagName("book"):
##  isbn = node.getAttribute("isbn")
##  L = node.getElementsByTagName("title")
##  for node2 in L:
##    title = ""
##    for node3 in node2.childNodes:
##      if node3.nodeType == Node.TEXT_NODE:
##        title += node3.data
##    mapping[isbn] = title

### New Classes with AMARA-Object-Bindings
##
##    def getXmlDocument(self, filename)
##        assert filename
##        try:
##            doc = binderytools.bind_file('tables.xml')
##        exception:
##            doc = None
##            
##        return doc
##        
##        
