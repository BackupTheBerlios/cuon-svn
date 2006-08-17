import pygtk
import gtk
import os, sys
import time
from xmlrpclib import ServerProxy


class startCuon:
    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title('Cuon-Installer')
        self.window.show()
        self.sv =  ServerProxy( 'http:84.244.7.139:7080',allow_none = 1 )
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.button = gtk.Button("Hello World")
        self.button.connect("clicked", self.hello, None) 
        self.Linux = (0,'linux')
        self.Windows = (1,'win32')
        self.Mac = (2,'mac')
        
    def main(self):
         gtk.main()
    
    def gtk_main_quit(self):
        gtk.main_quit()
    def delete_event(self, widget, event, data=None):
        return False
    def destroy(self, widget, data=None):
        gtk.main_quit()    
    def checkOS(self):
        Os = -1
        s = sys.platform
        if s.find(self.Linux[1]) >= 0:
            Os = self.Linux[0]
        elif s.find(self.Windows[1]) >= 0:
            Os = self.Windows[0]
     
        return Os
        
    def startRsync(self):
        if Os == self.Linux[0]:
            # Linux rsync startet
            pass

    def hello(self):
        pass

if __name__ == "__main__":
    stc = startCuon()
    stc.main()
