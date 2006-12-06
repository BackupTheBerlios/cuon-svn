from  gladeXml import gladeXml
import cuon.TypeDefs.typedefs
import ConfigParser
import gtk
import types

class rawWindow( gladeXml):
    def __init__(self):
        gladeXml.__init__(self)
        
        self.oUser = None
        self.dicUser = None
        self.dicSqlUser = None
        self.dicUserKeys = None
        self.openDB()
        #self.td = cuon.TypeDefs.typedefs.typedefs()
        
        
        
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
        
