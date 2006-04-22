
from types import *
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade



import string


from cuon.Windows.windows  import windows 

class aiwindow(windows):
    def __init__(self, allTables, module = 0, sep_info = None):
        
        windows.__init__(self)

        self.ModulNumber = self.MN['AI']
        
        self.openDB()
        self.oUser = self.loadObject('User')
        self.closeDB()
        
        self.loadGlade('ai.xml')
        self.win1 = self.getWidget('AIMainwindow')

        #self.rpc.callRP('src.XML.py_readDocument','cuon_addresses')

        self.wQuestion =   self.getWidget('tvQuestion')
        self.wAnswer =   self.getWidget('tvAnswer')
        self.qBuffer = gtk.TextBuffer(None)
        self.aBuffer = gtk.TextBuffer(None)


        self.wQuestion.grab_focus()
                

    def on_quit1_activate(self, event):
        self.out( "exit ai v2")
        self.closeWindow() 
    
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
            ##try:
##                q1 = q1.decode('latin-1')
##            except:
##                pass
##            try:
##                q1 = q1.encode('utf-8')
##            except:
##                pass
            
            print 'Question', q1
            a1 = self.rpc.callRP('src.AI.py_getAI',q1.encode('utf-8'), self.dicSqlUser)
            if a1:
                a1 = a1.decode('utf-7').encode('utf-8')
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
