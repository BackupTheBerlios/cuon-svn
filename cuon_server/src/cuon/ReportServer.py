import random
import xmlrpclib
from twisted.web import xmlrpc
 
from basics import basics
import Database
import base64
import Reports.report

class ReportServer(xmlrpc.XMLRPC, basics):
    def __init__(self):
        basics.__init__(self)
        self.oDatabase = Database.Database()
        self.debugFinances = 1
        self.ReportDefs = {}
        
        self.report = Reports.report.report()
 
##    def xmlrpc_server_hibernation_incoming_document(self, dicOrder, dicUser):
##        import Reports.report_hibernation_incoming_document
##        import Garden
##        
##        print "startReport"
##        oGarden = Garden.Garden()
##        oReports = Reports.report_hibernation_incoming_document.report_hibernation_incoming_document()
##        rep = oReports.ServerStartReport(dicOrder, dicUser, oGarden, self.ReportDefs)
##        print "ok Report"
##        print len(rep)
##        en =  base64.encodestring(rep)
##        return en
##        
    def xmlrpc_createReport(self, *reportdata):
        #print reportdata
        
        rep = self.report.start(reportdata)
        #rep = oReports.ServerStartReport(dicOrder, dicUser, oGarden, self.ReportDefs)
        print "ok Report"
        print len(rep)
        en =  base64.encodestring(rep)
        return en
