import xmlrpclib
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import ConfigParser

class simpleGlade:
    def __init__(self):
        self.xml = None
        self.dicKeys = {}
        self.dicKeys['CTRL'] = gtk.gdk.CONTROL_MASK 
        self.dicKeys['SHIFT'] = gtk.gdk.SHIFT_MASK 
        self.dicKeys['ALT'] = gtk.gdk.MOD1_MASK
        self.dicKeys['NONE'] = 0 

    def loadGlade(self, filename):
        self.xml = gtk.glade.XML(filename)
        self.setXmlAutoconnect()
        print 'xml = ', self.xml
    def getWidget(self, sName):
        return self.xml.get_widget(sName )

    def setXmlAutoconnect(self):

        nameFuncMap = {}
        for key in dir(self.__class__):
            nameFuncMap[key] = getattr(self, key)
            
            if  nameFuncMap:
                               
                self.xml.signal_autoconnect(nameFuncMap)

    def checkKey(self, event,sState, cKey):
        ok = False
        #print 'keyval', event.keyval
        #print 'keyval-name', gtk.gdk.keyval_name(event.keyval)
        #print 'state', event.state
        if (event.state and self.dicKeys[sState])  or sState == 'NONE':
            #print 'state is found'
            
            if gtk.gdk.keyval_name(event.keyval) == cKey :
                ok = True
        #print 'ok = ', ok
        return ok
          

class gtkMiniClient(simpleGlade):
    def __init__(self):
        simpleGlade.__init__(self)
    
        # connection-Data
        cpServer = ConfigParser.ConfigParser()
            
        cpServer.readfp(open('cuon_mini_client.ini'))
    
        CUON_SERVER = self.getConfigOption('USER','host',cpServer)
        Username = self.getConfigOption('USER','user',cpServer)
        Password = self.getConfigOption('USER','password',cpServer)
        # connect to Server
        self.Server = xmlrpclib.ServerProxy(CUON_SERVER)
        # Authorized
        sid = self.Server.src.Databases.py_createSessionID( Username, Password)
        
        print sid
        # Set Information for cuon
        self.dicUser={'Name':Username,'SessionID':sid,'userType':'cuon'}
        self.loadGlade('gtkMiniClient.glade')
        
        self.wQuestion =   self.getWidget('tvQuestion')
        self.wAnswer =   self.getWidget('tvAnswer')
        self.qBuffer = gtk.TextBuffer(None)
        self.aBuffer = gtk.TextBuffer(None)
  
        self.wQuestion.grab_focus()        
   
        
        
    def getConfigOption(self, section, option, configParser = None):
        value = None
        if configParser:
            cps = configParser
        else:
           cps = self.cpServer
           
        if cps.has_option(section,option):
            value = cps.get(section, option)
            print 'getConfigOption', section + ', ' + option + ' = ' + value
        return value    

    def on_quit1_activate(self, event):
        self.out( "exit ai v2")
        self.gtk_main_quit()
    
    def on_bSend_clicked(self, event):
        self.sendToAi(event)

    def on_tvQuestion_key_press_event(self, entry,event):
        if self.checkKey(event,'CTRL','Return'):
            self.sendToAi(event)
       
    def sendToAi(self, event):
        print "AI send"
        buffer = self.wQuestion.get_buffer()
        q1 = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), 1)
        if q1:
            print 'Question', q1
            a1 = self.Server.src.AI.py_getAI(q1.decode('iso-8859-1').encode('utf-7'),self.dicUser)
                        
            if a1:
                a1 = a1.decode('utf-7').encode('iso-8859-1')
                a1 = a1 + '\n'
            
                q1 = q1 + '\n'
                self.aBuffer = self.wAnswer.get_buffer()
                self.aBuffer.insert(self.aBuffer.get_end_iter(), q1, len(q1) )
                self.wAnswer.set_buffer(self.aBuffer)

                
            
                
                print "Answer", a1
        
                self.aBuffer = self.wAnswer.get_buffer()
                self.aBuffer.insert(self.aBuffer.get_end_iter(), a1, len(a1) )
                self.wAnswer.set_buffer(self.aBuffer)
                self.aBuffer = self.wAnswer.get_buffer()
                self.wAnswer.scroll_to_iter(self.aBuffer.get_end_iter(),0.0,False,0.0,0.0)
        
        self.qBuffer.set_text('')
        self.wQuestion.set_buffer(self.qBuffer)
        self.wQuestion.scroll_to_iter(self.qBuffer.get_start_iter(),0.0,False,0.0,0.0)
        
        self.wQuestion.grab_focus()        




m = gtkMiniClient()
gtk.main()
  
