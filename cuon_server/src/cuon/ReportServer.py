import random
import xmlrpclib
from twisted.web import xmlrpc
 
from basics import basics
import Database
import base64
import Reports.report
#import Reports.report2

class ReportServer(xmlrpc.XMLRPC, basics):
    def __init__(self):
        basics.__init__(self)
        self.oDatabase = Database.Database()
        self.debugFinances = 1
        self.ReportDefs = {}
        
        self.report = Reports.report.report()
        #self.report2 = Reports.report2.report2()
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
        print 'start ReportServer --> createReport : reportdata', reportdata
        
        rep = self.report.start(reportdata)
        #rep = oReports.ServerStartReport(dicOrder, dicUser, oGarden, self.ReportDefs)
        print "ok Report"
        print len(rep)
        en =  base64.encodestring(rep)
        return en

#    def xmlrpc_createReport2(self, *reportdata):
#        print 'start ReportServer --> createReport : reportdata', reportdata
#        
#        rep = self.report2.start(reportdata)
#        #rep = oReports.ServerStartReport(dicOrder, dicUser, oGarden, self.ReportDefs)
#        print "ok Report"
#        print len(rep)
#        en =  base64.encodestring(rep)
#        return en
