from  gladeXml import gladeXml
import cuon.TypeDefs.typedefs
import ConfigParser

class rawWindow( gladeXml):
    def __init__(self):
        gladeXml.__init__(self)
        
        self.oUser = None
        self.dicUser = None
        self.dicSqlUser = None
        self.dicUserKeys = None
        self.openDB()
        self.td = cuon.TypeDefs.typedefs.typedefs()
        self.td = self.loadObject('td')
        
        self.loadUserInfo()
        
        self.closeDB()
        self.cpParser = ConfigParser.ConfigParser()
        
        
    def loadUserInfo(self):
        self.oUser = self.loadObject('User')
        if self.oUser:
            print `self.oUser`
            self.dicUser = self.oUser.getDicUser()
            self.dicSqlUser = self.oUser.getSqlDicUser()
            print `self.dicUser`
        else:
            self.dicUser = {}
        try:
            self.dicUserKeys = self.oUser.getDicUserKeys()
        except Exception, params:
            print Exception, params
           
    def setTextbuffer(self, widget, liField):
        buffer = gtk.TextBuffer(None)
        text = ''
        print self.oUser.userEncoding
        for i in range(len(liField)):
            print type( liField[i])
            print liField[i]
            
            if isinstance(liField[i], types.StringType):
                text = text + liField[i] + '\n'
            elif isinstance(liField[i], types.UnicodeType):
                text = text + liField[i] + '\n'
                 
            elif isinstance(liField[i], types.ClassType) or isinstance(liField[i], types.InstanceType):
                text = text +  `sValue`
            elif isinstance(liField[i], types.IntType):
                text = text + `liField[i]` + '\n'
            elif isinstance(liField[i], types.FloatType):
                text = text + `liField[i]` + '\n'
                                   
            else:
                text = text + `liField[i]` + '\n'
                
        buffer.set_text(text)
        widget.set_buffer(buffer)
    

    def getConfigOption(self, section, option):
        value = None
        if self.cpParser.has_option(section,option):
            value = self.cpParser.get(section, option)
            print 'getConfigOption', section + ', ' + option + ' = ' + value
        return value   
        
    def getListOfParserItems(self, section):
        return self.cpParser.items(section)
        
    def getListOfParserSections(self):
        return self.cpParser.sections()
        
