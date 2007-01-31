class report_basics:
    def __init__(self):
        pass
        
    def getPdfEncoding(self, value, ReportDefs):
        retValue = None
        try:
            retValue = (value.decode('utf-7')).encode(ReportDefs['PdfEncoding'])
            print 'decode = utf-7', retValue
        except:
            try:
                retValue = (value.decode('iso-8859-15')).encode(ReportDefs['PdfEncoding']) 
                print 'decode = iso-8859-15', retValue
            except:
                try:
                    retValue = (value.decode('utf-8')).encode(ReportDefs['PdfEncoding']) 
                    print 'decode = utf-8', retValue


                 
                except Exception, params:
                    print Exception, params
                    retValue = value
        return retValue
