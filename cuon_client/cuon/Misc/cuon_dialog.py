import gtk
import pygtk


class cuon_dialog:
    def __init__(self):
        # Dialog - Flags
        # DIALOG_MODAL - make the dialog modal
        # DIALOG_DESTROY_WITH_PARENT - destroy dialog when its parent is destroyed
        # DIALOG_NO_SEPARATOR - omit the separator between the vbox and the action_area   
        #gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT
        
        self.Buttons = {}
        
        #
        
    def inputLine(self,  sTitle=None, sText=None, oParent=None):
        ok = False
        res = None
        print 'QuestionMsg'
        dialog = gtk.Dialog(sTitle, oParent, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,(gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                      gtk.STOCK_OK, gtk.RESPONSE_ACCEPT) );
        
        lLabel = gtk.Label(sText)
        dialog.vbox.pack_start(lLabel, True, True, 0)
        lLabel.show()
        
        eLine = gtk.Entry()
        dialog.vbox.pack_start(eLine, True, True, 0)
        eLine.show()
        
        response = dialog.run ();
        
        dialog.destroy ();
        print 'Response', response
        if response == gtk.RESPONSE_ACCEPT:
            ok = True
        res = eLine.get_text()
        return ok, res
        
       
