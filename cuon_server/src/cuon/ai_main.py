
try:
    import aiml
except:
    print 'No AI'


class ai_main:

    def __init__(self):

        self.k = aiml.Kernel()
        self.os1 = 'öß'.decode('latin-1').encode('utf-7')
        self.Os1 = 'Öß'.decode('latin-1').encode('utf-7')
        self.us1 = 'üß'.decode('latin-1').encode('utf-7')
        self.Us1 = 'Üß'.decode('latin-1').encode('utf-7')
        self.as1 = 'äß'.decode('latin-1').encode('utf-7')
        self.As1 = 'Äß'.decode('latin-1').encode('utf-7')

        self.Oe = 'Ö'.decode('latin-1').encode('utf-7')
        self.Ae = 'Ä'.decode('latin-1').encode('utf-7')
        self.Ue = 'Ü'.decode('latin-1').encode('utf-7')
        self.oe = 'ö'.decode('latin-1').encode('utf-7')
        self.ae = 'ä'.decode('latin-1').encode('utf-7')
        self.ue = 'ü'.decode('latin-1').encode('utf-7')
        self.ss = 'ß'.decode('latin-1').encode('utf-7')

        try:
            ctrlFile = open('/etc/cuon/ai_subs.ini')
            s = ctrlFile.readline()
            while s:
                liS = s.split('=')
                if len(liS) > 1:
                    liS[0] = liS[0].strip()
                    liS[1] = liS[1].strip()
                    self.k.loadSubs(liS[1])
                s = ctrlFile.readline()
            ctrlFile = open('/etc/cuon/ai_aiml.ini')
            s = ctrlFile.readline()
            while s:
                liS = s.split('=')
                print liS
                if len(liS) > 1:
                    liS[0] = liS[0].strip()
                    liS[1] = liS[1].strip()
                    self.k.learn(liS[1])
                    print 'learn module' + ` liS[1]`
                s = ctrlFile.readline()

                

            print "load Modules ready"
            
        except Exception, param:
            print Exception, param
            
    def checkQ(self, question):

        print 'before:', question
    
        # German translation - later in SUBS ( at this time problems )
        #question = question.decode('latin-1').encode('utf-7')

##        question = question.replace(self.Os1,'Oess')
##        question = question.replace(self.os1,'oess')
##        question = question.replace(self.Us1,'Uess')
##        question = question.replace(self.us1,'uess')
##        question = question.replace(self.As1,'Aess')
##        question = question.replace(self.as1,'aess')
 
##        question = question.replace(self.oe,'oe')
##        question = question.replace(self.ae,'ae')
##        question = question.replace(self.ue, 'ue')
##        question = question.replace(self.Ae,'AE')
##        question = question.replace(self.Oe,'OE')
##        question = question.replace(self.Ue,'UE')
##        question = question.replace(self.ss,'ss')
        print 'after:', question

        return question
    
