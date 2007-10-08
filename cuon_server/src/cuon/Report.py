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

        self.ReportDefs['DocumentPathOrderInvoice'] = self.DocumentPathOrderInvoice


        self.ReportDefs['DocumentPathHibernationIncoming'] = self.DocumentPathHibernationIncoming
        self.ReportDefs['DocumentPathHibernationPickup'] = self.DocumentPathHibernationPickup
        self.ReportDefs['DocumentPathHibernationInvoice'] = self.DocumentPathHibernationInvoice
        
        self.ReportDefs['DocumentPathListsAddresses'] = self.DocumentPathListsAddresses
        self.ReportDefs['DocumentPathListsArticles'] = self.DocumentPathListsAddresses

        self.ReportDefs['PdfEncoding'] = self.PdfEncoding

    
        #self.report = Reports.report.report()
       

    
    def xmlrpc_server_address_phonelist1(self, dicSearchlist, dicUser):
        import Reports.report_addresses_phone1
        import Address
        
        print "startReport"
        oAddress=Address.Address()
        oReports = Reports.report_addresses_phone1.report_addresses_phone1()
        repData = oReports.getReportData(dicSearchlist, dicUser, oAddress, self.ReportDefs)
        #print repData
        
        
        return self.report_server.ReportServer.createReport(repData)
        
    def xmlrpc_server_address_phonelist11(self, dicSearchlist, dicUser):
        import Reports.report_addresses_phone11
        import Address
        
        print "startReport"
        oAddress=Address.Address()
        oReports = Reports.report_addresses_phone11.report_addresses_phone11()
        repData = oReports.getReportData(dicSearchlist, dicUser, oAddress, self.ReportDefs)
        #print repData
        
        
        return self.report_server.ReportServer.createReport(repData)        
    
    def xmlrpc_server_articles_number1(self, dicSearchlist, dicUser):
        import Reports.report_articles_number1
        import Article
        
        print "startReport"
        oArticles = Article.Article()
        oReports = Reports.report_articles_number1.report_articles_number1()
        repData = oReports.getReportData(dicSearchlist, dicUser, oArticles, self.ReportDefs)
        print repData
        
        
        return self.report_server.ReportServer.createReport(repData)
        
        
    def xmlrpc_server_articles_pickles_standard(self, dicSearchlist, dicUser,  nRows):
        import Reports.report_articles_pickles_standard
        import Article
        
        print "startReport"
        oArticles = Article.Article()
        oReports = Reports.report_articles_pickles_standard.report_articles_pickles_standard(nRows)
        repData = oReports.getReportData(dicSearchlist, dicUser, oArticles, self.ReportDefs)
        print repData
        
        
        return self.report_server.ReportServer.createReport(repData)
        
    def xmlrpc_server_hibernation_incoming_document(self, dicOrder, dicUser):
        print `self.report_server`
        import Reports.report_hibernation_incoming_document
        import Garden
        
        print "startReport"
        oGarden = Garden.Garden()
        oReports = Reports.report_hibernation_incoming_document.report_hibernation_incoming_document()
        repData = oReports.getReportData(dicOrder, dicUser, oGarden, self.ReportDefs)
        
        #return self.report_server.ReportServer.server_hibernation_incoming_document(dicOrder, dicUser)
        #print repData
        
        return self.report_server.ReportServer.createReport(repData)
        
    def xmlrpc_server_hibernation_pickup_document(self, dicOrder, dicUser):
        print `self.report_server`
        import Reports.report_hibernation_pickup_document
        import Garden
        
        print "startReport"
        oGarden = Garden.Garden()
        oReports = Reports.report_hibernation_pickup_document.report_hibernation_pickup_document()
        repData = oReports.getReportData(dicOrder, dicUser, oGarden, self.ReportDefs)
        
        #return self.report_server.ReportServer.server_hibernation_incoming_document(dicOrder, dicUser)
        #print repData
        
        return self.report_server.ReportServer.createReport(repData)
        
    def xmlrpc_server_hibernation_invoice(self, dicOrder, dicUser):
        print `self.report_server`
        import Reports.report_hibernation_invoice
        import Garden
        
        print "startReport"
        oGarden = Garden.Garden()
        oReports = Reports.report_hibernation_invoice.report_hibernation_invoice()
        repData = oReports.getReportData(dicOrder, dicUser, oGarden, self.ReportDefs)
        
        #return self.report_server.ReportServer.server_hibernation_incoming_document(dicOrder, dicUser)
        #print repData
        
        return self.report_server.ReportServer.createReport(repData)
        
        
    def xmlrpc_server_order_invoice_document(self, dicOrder, dicUser):
        print 'report-server = ', `self.report_server`
        import Reports.report_order_standard_invoice
        import Order
        
        print "startReport"
        oOrder = Order.Order()
        oReports = Reports.report_order_standard_invoice.report_order_standard_invoice()
        repData = oReports.getReportData(dicOrder, dicUser, oOrder, self.ReportDefs)
        #print '\n\n'
        #print 'get repData'
        #print '\n'
        #return self.report_server.ReportServer.server_hibernation_incoming_document(dicOrder, dicUser)
        #print '--> Rep-Data = ', repData
        
        return self.report_server.ReportServer.createReport(repData)
            
    def xmlrpc_server_list_list_of_invoices(self, dicExtraData, dicUser):
        print 'report-server = ', `self.report_server`
        import Reports.report_list_list_of_invoices
        import Order
        oOrder = Order.Order()
        
        print "startReport"
        oReports = Reports.report_list_list_of_invoices.report_list_list_of_invoices()
        repData = oReports.getReportData(dicExtraData, dicUser, oOrder, self.ReportDefs)
        #print '\n\n'
        #print 'get repData'
        #print '\n'
        #return self.report_server.ReportServer.server_hibernation_incoming_document(dicExtraData, dicUser)
        #print '--> Rep-Data = ', repData
        
        return self.report_server.ReportServer.createReport(repData)
            
    def xmlrpc_server_list_of_inpayment(self, dicExtraData, dicUser):
        print 'report-server = ', `self.report_server`
        import Reports.report_list_of_inpayment
        import Order
        oOrder = Order.Order()
        
        print "startReport"
        oOrder = Order.Order()
        oReports = Reports.report_list_of_inpayment.report_list_of_inpayment()
        repData = oReports.getReportData(dicExtraData, dicUser, oOrder, self.ReportDefs)
        #print '\n\n'
        #print 'get repData'
        #print '\n'
        #return self.report_server.ReportServer.server_hibernation_incoming_document(dicExtraData, dicUser)
        #print '--> Rep-Data = ', repData
        
        return self.report_server.ReportServer.createReport(repData)
        
        
    def xmlrpc_server_list_of_residue(self, dicExtraData, dicUser):
        print 'report-server = ', `self.report_server`
        import Reports.report_list_of_residue
        import Order
        oOrder = Order.Order()
        
        print "startReport"
        oReports = Reports.report_list_of_residue.report_list_of_residue()
        repData = oReports.getReportData(dicExtraData, dicUser, oOrder, self.ReportDefs)
        #print '\n\n'
        #print 'get repData'
        #print '\n'
        #return self.report_server.ReportServer.server_hibernation_incoming_document(dicExtraData, dicUser)
        #print '--> Rep-Data = ', repData
        
        return self.report_server.ReportServer.createReport(repData)
        
    def xmlrpc_server_list_of_reminder(self, dicExtraData, dicUser):
        print 'report-server = ', `self.report_server`
        import Reports.report_list_of_reminder
        import Order
        oOrder = Order.Order()
        
        print "startReport"
        oReports = Reports.report_list_of_reminder.report_list_of_reminder()
        repData = oReports.getReportData(dicExtraData, dicUser, oOrder, self.ReportDefs)
        #print '\n\n'
        #print 'get repData'
        #print '\n'
        #return self.report_server.ReportServer.server_hibernation_incoming_document(dicExtraData, dicUser)
        #print '--> Rep-Data = ', repData
        
        return self.report_server.ReportServer.createReport(repData)
                                    
