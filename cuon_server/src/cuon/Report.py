import random
import xmlrpclib
from twisted.web import xmlrpc
 
from basics import basics
import Database


#locale.setlocale (locale.LC_ALL, '')



class Report(xmlrpc.XMLRPC, basics):
    def __init__(self):
        basics.__init__(self)
        self.oDatabase = Database.Database()
        self.debugFinances = 1
        self.ReportDefs = {}
        self.ReportDefs['ReportPath'] = self.REPORTPATH
        
        self.ReportDefs['DocumentPathHibernationIncoming'] = self.DocumentPathHibernationIncoming
        self.ReportDefs['DocumentPathListsAddresses'] = self.DocumentPathListsAddresses

        #self.report = Reports.report.report()
       

    def xmlrpc_server_hibernation_incoming_document(self, dicOrder, dicUser):
        print `self.report_server`
        import Reports.report_hibernation_incoming_document
        import Garden
        
        print "startReport"
        oGarden = Garden.Garden()
        oReports = Reports.report_hibernation_incoming_document.report_hibernation_incoming_document()
        repData = oReports.getReportData(dicOrder, dicUser, oGarden, self.ReportDefs)
        
        #return self.report_server.ReportServer.server_hibernation_incoming_document(dicOrder, dicUser)
        print repData
        
        return self.report_server.ReportServer.createReport(repData)
        
    def xmlrpc_server_address_phonelist1(self, dicSearchlist, dicUser):
        import Reports.report_addresses_phone1
        import Address
        
        print "startReport"
        oAddress=Address.Address()
        oReports = Reports.report_addresses_phone1.report_addresses_phone1()
        repData = oReports.getReportData(dicSearchlist, dicUser, oAddress, self.ReportDefs)
        print repData
        
        
        return self.report_server.ReportServer.createReport(repData)
    
