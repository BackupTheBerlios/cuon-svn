import logging

class logs :
    

    def __init__(self):
        logging.basicConfig()
        self.log = logging.getLogger("cuon")
        self.log.setLevel(logging.ERROR)
        self.log.info("cuon logging startet")
        self.loglevel = [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]
        self.DEBUG = 0
        self.INFO = 1
        self.WARNING = 2
        self.ERROR =  3
        self.CRITICAL = 4
        self.iLoglevel = self.DEBUG
        

    def setLogLevel(self, iLevel):
        self.iLoglevel = iLevel
        if iLevel >= len(self.loglevel):
            self.log.setLevel(logging.ERROR)
        else:
            self.log.setLevel(self.loglevel[iLevel])
            
        #    raise Exception('The given logging level (' + str(iLevel) + ') does not exist!')
       # self.log.setLevel(self.loglevel[iLevel])


    def out(self, sLog, iLogLevel = 100):
        #print 'iLoglevel = ' +  `iLogLevel`
        iLevel = self.INFO
        if iLogLevel != 100:
            iLevel = iLogLevel
            self.log.setLevel(self.loglevel[iLevel])
#        else:
#            iLevel = self.iLoglevel

        if iLevel >= len(self.loglevel):
#            self.log.setLevel(logging.INFO)
#        else:
#            self.log.setLevel(self.loglevel[iLevel])
            if iLevel == self.DEBUG:
                self.log.debug(sLog)
            elif iLevel == self.INFO:
                self.log.info(sLog)
            elif iLevel == self.WARNING:
                self.log.warning(sLog)
            elif iLevel == self.ERROR:
                self.log.error(sLog)
            elif iLevel == self.CRITICAL:
                self.log.critical(sLog)
          
        
