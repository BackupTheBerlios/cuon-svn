
import cuon.TypeDefs
from cuon.Databases.dumps import dumps




class defaultValues(dumps):
    def __init__(self):
        dumps.__init__(self)
        
        
        self.openDB()
        td = self.loadObject('td')
        self.closeDB()
        if td:
            self.td = td
            
        
        if not self.td:
            print 'td = None, Fallback to Norm'
            self.td = cuon.TypeDefs.typedefs.typedefs()
        
        
        
        
        
