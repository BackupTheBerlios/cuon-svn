import os
import sys
sys.path.append(os.environ['CUON_PATH'])
import uno
from cuon.Databases.dumps import dumps
class ooconnect(dumps):

    def __init__(self):
        dumps.__init__(self)
        
        # get the uno component context from the PyUNO runtime
        localContext = uno.getComponentContext()

        # create the UnoUrlResolver 
        resolver = localContext.ServiceManager.createInstanceWithContext(
                                    "com.sun.star.bridge.UnoUrlResolver", localContext )

        # connect to the running office 				
        self.ctx = resolver.resolve( "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext" )
        self.smgr = self.ctx.ServiceManager
