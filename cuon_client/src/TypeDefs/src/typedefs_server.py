import xmlrpclib
from xmlrpclib import Server
import cuon.XML.MyXML
from typedefs import typedefs
import os
import os.path
#if len(sys.argv) > 1:
#    fname = sys.argv[1]
#else:

class typedefs_server(typedefs):

    def __init__(self):
        typedefs.__init__(self)
        # cuon glade-files
        self.main_glade_name = '/usr/share/cuon/glade/cuon.glade2'
        self.databases_glade_name =  '/usr/share/cuon/glade/databases.glade2'
        #cuon-server
        # self.server = Server ('http://sat1:9673/Cuon')
        #cuon xml-defs
        self.nameOfXmlTableFiles ={ 'tables.xml' : '/usr/share/cuon/tables.xml', 'ext1.xml' : '/usr/share/cuon/ext1.xml', 'ext2.xml' : '/usr/share/cuon/ext2.xml' }

        self.nameOfXmlEntriesFiles ={  }
        self.nameOfXmlGrantFiles ={ }
        self.nameOfGladeFiles = {}
        self.nameOfXmlSQLFiles ={ }
        self.nameOfReportFiles ={ }

        
        self.server = os.environ['CUON_SERVER']

        # read init-file
        fname = os.environ['CUON_INI']
        MyXml = cuon.XML.MyXML.MyXML()
        doc = MyXml.readDocument(fname)
        if doc:
            cyRootNode = MyXml.getRootNode(doc)
          
            cyNode = MyXml.getNode(cyRootNode,'SQLServer')
            if cyNode:
                self.SQL_HOST = MyXml.getNodeData(cyNode,'SQL-HOST')
                self.SQL_USER = MyXml.getNodeData(cyNode,'SQL-USER')
                self.SQL_PORT = MyXml.getNodeData(cyNode,'SQL-PORT')
                self.SQL_DB = MyXml.getNodeData(cyNode,'DB')

                print "sql-values"
                print self.SQL_DB
                print self.SQL_HOST
                print self.SQL_PORT
                print self.SQL_USER
                   
         
        # read xml_init-file
        fname = os.environ['CUON_INI_XML']
        MyXml = cuon.XML.MyXML.MyXML()
        doc = MyXml.readDocument(fname)
        if doc:
            cyRootNode = MyXml.getRootNode(doc)
            cyNode = MyXml.getNode(cyRootNode,'Database')
            if cyNode:
                self.nameOfXmlTableFiles[MyXml.getNodeData(cyNode,'DB-File') ] = MyXml.getNodeData(cyNode,'DB-FileValue')
                
  
            cyNodes = MyXml.getNode(cyRootNode,'Entry_Init_Files')

            cyNodes1 = MyXml.getNodes(cyRootNode[0],'Entries')

            for i in cyNodes1:

                cyFileValue = MyXml.getNodes(i,'Entry-FileValue')
                sFileValue = MyXml.getData(cyFileValue[0] )
                cyFile = MyXml.getNodes(i,'Entry-File')
                sFile = MyXml.getData(cyFile[0] )

                key = 'entry_' + sFile 
                self.nameOfXmlEntriesFiles[key ] = sFileValue
                
                
            #Glade Files
        
            cyNodes = MyXml.getNode(cyRootNode,'Glade_Init_Files')
            print "-----------------> cyNodes(glade) = " + `cyNodes`

            cyNodes1 = MyXml.getNodes(cyRootNode[0],'GladeEntries')

            for i in cyNodes1:

                cyFileValue = MyXml.getNodes(i,'Glade-FileValue')
                sFileValue = MyXml.getData(cyFileValue[0] )
                cyFile = MyXml.getNodes(i,'Glade-File')
                sFile = MyXml.getData(cyFile[0] )

                key = 'glade_' + sFile 
                self.nameOfGladeFiles[key ] = sFileValue

            # Grant-Files
            cyNodes = MyXml.getNode(cyRootNode,'Grant_Init_Files')
            print "-----------------> cyRootNode GRANT = " + `cyRootNode`
            print "-----------------> cyNodes GRANT = " + `cyNodes`
            if cyNodes:
                cyNodes1 = MyXml.getNodes(cyRootNode[0],'GrantEntries')

                for i in cyNodes1:

                    cyFileValue = MyXml.getNodes(i,'Grant-FileValue')
                    sFileValue = MyXml.getData(cyFileValue[0] )
                    cyFile = MyXml.getNodes(i,'Grant-File')
                    sFile = MyXml.getData(cyFile[0] )

                    key = 'grant_' + sFile 
                    self.nameOfXmlGrantFiles[key ] = sFileValue
                    print self.nameOfXmlGrantFiles

            # ProcedureAndTrigger-Files
            cyNodes = MyXml.getNode(cyRootNode,'SQL_Init_Files')
            print "-----------------> cyRootNode SQL = " + `cyRootNode`
            print "-----------------> cyNodes = SQL " + `cyNodes`
            if cyNodes:
                cyNodes1 = MyXml.getNodes(cyRootNode[0],'SQLEntries')

                for i in cyNodes1:

                    cyFileValue = MyXml.getNodes(i,'SQL-FileValue')
                    sFileValue = MyXml.getData(cyFileValue[0] )
                    cyFile = MyXml.getNodes(i,'SQL-File')
                    sFile = MyXml.getData(cyFile[0] )

                    key = 'grant_' + sFile 
                    self.nameOfXmlSQLFiles[key ] = sFileValue
                    print self.nameOfXmlSQLFiles
                    
            #Report Files
        
            cyNodes = MyXml.getNode(cyRootNode,'Report_Init_Files')
            print "-----------------> cyNodes(report) = " + `cyNodes`

            cyNodes1 = MyXml.getNodes(cyRootNode[0],'ReportEntries')

            for i in cyNodes1:

                cyFileValue = MyXml.getNodes(i,'Report-FileValue')
                sFileValue = MyXml.getData(cyFileValue[0] )
                cyFile = MyXml.getNodes(i,'Report-File')
                sFile = MyXml.getData(cyFile[0] )

                key = 'report_' + sFile 
                self.nameOfReportFiles[key ] = sFileValue


                
        print self.nameOfXmlGrantFiles
        print self.nameOfXmlEntriesFiles
        print self.nameOfGladeFiles
        print self.nameOfXmlSQLFiles
        print self.nameOfReportFiles
    
                    
