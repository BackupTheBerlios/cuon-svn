import gtkhtml2
import sys
from types import *
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import gobject
import cuon.XMLRPC.xmlrpc
from cuon.Windows.windows  import windows
import gtkmozembed as moz


class helpwindow(windows):

    
    def __init__(self):

        windows.__init__(self)

        self.loadGlade('help.xml')
        self.win1 = self.getWidget('HelpMainwindow')
        

        s = self.rpc.callRP('Misc.getHelpBook')
        s = s.decode('utf-8').encode('latin-1')
        document = gtkhtml2.Document()
        
        document.clear()
        document.open_stream('text/html')
        document.write_stream(s)
        document.close_stream()
        
        

        sw1 = self.getWidget('swHelp')
        view = gtkhtml2.View()
        view.set_document(document)
        sw1.add(view)
        self.win1.show_all()
##        
##        moz.set_profile_path("/tmp/","foo")
##
##        gtkmoz = moz.MozEmbed()
##        gtkmoz.load_url("http://www.pro-linux.de")
##        sw1 = self.getWidget('swHelp')
##        
##        sw1.add(gtkmoz)
##        self.win1.show_all()
##        

    def on_quit1_activate(self, event):
        print "exit help v2"
        self.closeWindow()



