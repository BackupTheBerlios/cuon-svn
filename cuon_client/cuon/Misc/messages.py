import gtk
import pygtk


class messages:
    def __init__(self):
        # Dialog - Flags
        # DIALOG_MODAL - make the dialog modal
        # DIALOG_DESTROY_WITH_PARENT - destroy dialog when its parent is destroyed
        # DIALOG_NO_SEPARATOR - omit the separator between the vbox and the action_area   
        self.Buttons = {}
        
        #
        
    def errorMsg(self, sText):
        # gtk
        ok = False
        print 'errorMsg'
        dialog = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR,gtk.BUTTONS_CLOSE, sText);
        dialog.run ();
        dialog.destroy ();
        
        return ok
