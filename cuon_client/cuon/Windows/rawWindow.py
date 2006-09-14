from  gladeXml import gladeXml
import cuon.TypeDefs.typedefs

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
           
    
