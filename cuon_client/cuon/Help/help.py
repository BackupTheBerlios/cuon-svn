try:
    import gtkhtml2
except:
    print 'gtkhtml not found'
    
    
import sys
from types import *
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import gobject
import cuon.XMLRPC.xmlrpc
from cuon.Windows.windows  import windows

try:
    import gtkmozembed as moz
except:
    print ' No Module self.helpmozembed found'
    print ' search to python-gnome-extras '
    print ' SuSE 10.1 has problems'
    print ' No Online-Help avaible '


class helpwindow(windows):

    
    def __init__(self):

        windows.__init__(self)

        self.loadGlade('help.xml')
        self.win1 = self.getWidget('HelpMainwindow')


        

        self.helpmoz = moz.MozEmbed()
        #sw1 = self.getWidget('swHelp')
        self.vbox = self.getWidget('vbox2')
        self.vbox.add(self.helpmoz)
        self.helpmoz.load_url("http://85.214.52.49:8000/cuontrac/wiki/Documentation")
        self.helpmoz.set_size_request(816,600)
        self.helpmoz.show()
        self.win1.show_all()
        
    def on_tBack_clicked(self, event):
        self.helpmoz.go_back()
    
    def on_tForward_clicked(self, event):
        self.helpmoz.go_forward()
        
    def on_tRelaod_clicked(self, event):
        self.helpmoz.reload(moz.GTK_MOZ_EMBED_FLAG_RELOADNORMAL)
        
    def on_tQuit_clicked(self, event):
        self.closeWindow()
        
    def on_quit1_activate(self, event):
        print "exit help v2"
        self.closeWindow()



