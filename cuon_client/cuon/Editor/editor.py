import gtk.glade
import sys, os
import os.path

import string
try:
    import gtksourceview
    GtkSV = True 
except:
    print 'No gtksourceview import possible. Please install gtksourceview for python!!'
    GtkSV = False
    

from cuon.Windows.windows  import windows 

class editorwindow(windows):
    def __init__(self, dicFilename=None, servermod=False):
        windows.__init__(self)
        
        self.close_dialog = None
        self.clipboard = gtk.clipboard_get()
        self.ModulNumber = 0
        print dicFilename, servermod
        self.openDB()
        self.oUser = self.loadObject('User')
        self.closeDB()
        if servermod:
            self.xml = gtk.glade.XML('../usr/share/cuon/glade/editor.glade2')
            self.setXmlAutoconnect()
        else:
            self.loadGlade('editor.xml')
        self.win1 = self.getWidget('EditorMainwindow')
        
        if GtkSV:
            lm = gtksourceview.SourceLanguagesManager()
            self.textbuffer = gtksourceview.SourceBuffer()
            self.textbuffer.set_data('languages-manager', lm)
            manager = self.textbuffer.get_data('languages-manager')
            mime_type = 'text/x-tex'
            language = manager.get_language_from_mime_type(mime_type)
            self.textbuffer.set_highlight(True)
            self.textbuffer.set_language(language)
            self.view = gtksourceview.SourceView(self.textbuffer)
            self.view.set_show_line_numbers(True)
            Vbox = self.getWidget('vbox1')
            Scrolledwindow = self.getWidget('scrolledwindow1')
            Scrolledwindow.remove(self.getWidget('viewport1'))
            #Vbox.remove(oldScrolledwindow)
            #Vbox.add(self.view)
            #Vbox.show_all()
            Scrolledwindow.add(self.view)
            self.view.show_all()
            Scrolledwindow.show_all()
            
            
        else:
            

            self.textbuffer = self.getWidget('tv1').get_buffer()
        
        
        self.actualTab = 0
        
        
        if dicFilename:
            self.dicCurrentFilename = dicFilename
            self.open_file(dicFilename)
        else:
            self.dicCurrentFilename = {'TYPE':'FILE','NAME':'./new.txt'}
    
    def on_quit1_activate(self, event):
        print 'quit editor'
        os.system('find -name "tmp_editor_ssh_tab_*" -exec rm {} \;')
        self.closeWindow()
        
    def on_save1_activate(self, event):
        self.save_current_file()
        
    def get_text(self):
        "Returns the current text in the text area"
        return self.textbuffer.get_text(self.textbuffer.get_start_iter(), self.textbuffer.get_end_iter())
    
    def delete(self, widget, data=None):
        "Put up dialog box, asking user if they're sure they want to quit. If so, quit"
        #Since we allow people to do other things while deciding whether to save
        #we'd better not let them accumulate these dialog boxes
        if self.close_dialog:
            return True
    
        if self.textview.get_buffer().get_modified():
            self.close_dialog=gtk.Dialog("Save changes to file before closing?",
                    None,0,
                    ("Close without saving",0,
                     gtk.STOCK_CANCEL,1,
                     gtk.STOCK_SAVE,2))
            answer=self.close_dialog.run()
    
            if answer==1:
                self.close_dialog.destroy()
                self.close_dialog=None
                return True
            if answer==2:
                self.save_current_file()
    
        Ged.number_of_instances = Ged.number_of_instances - 1
        self.window.destroy()
        if __name__ == "__main__":
                if Ged.number_of_instances == 0:
                    gtk.main_quit()
        return False
    
    def open_item_clicked(self, data=None):
        "Creates a file chooser and allows user to open a file with it"
        self.filesel = gtk.FileSelection("Select file to open...")
        self.filesel.ok_button.connect_object("clicked", self.open_selected_file, None)
        self.filesel.cancel_button.connect("clicked", lambda w: self.filesel.destroy())
        self.filesel.show()
    
    
    def open_selected_file(self, data=None):
        "Opens the selected file and reads it in"
        self.open_file(self.filesel.get_filename())
        self.filesel.destroy()  
    
    def open_file(self, dicFilename):
        "Opens the file given in filename and reads it in"
        if dicFilename['TYPE'] == 'SSH':
            dicFilename['TMPNAME'] = 'tmp_editor_ssh_tab_' + `self.actualTab` 
            s1 = 'scp -P ' + dicFilename['PORT'] +  ' ' + dicFilename['USER'] + '@' + dicFilename['HOST'] + '://' 
            s1 +=  dicFilename['NAME'] + ' ' + dicFilename['TMPNAME']
            os.system(s1)
            filename = dicFilename['TMPNAME']
            
        else:
           
           filename = dicFilename['NAME']
            
            
        infile = open(filename, "r")
        if infile:
            self.textbuffer.set_text(infile.read())
            infile.close()
            #self.dicCurrentFilename = filename
            self.win1.set_title(self.dicCurrentFilename['NAME'])
    
    def save_as_item_clicked(self, data=None):
        "Creates a file chooser and allows the user to save to it"
        self.filesel = gtk.FileSelection("Save As...")
        self.filesel.ok_button.connect_object("clicked", self.save_selected_file, None)
        self.filesel.cancel_button.connect("clicked", lambda w: self.filesel.destroy())
        self.filesel.show()
    
    def save_selected_file(self, data=None):
        "Saves the selected file"
        self.save_file(self.filesel.get_filename(), self.get_text())
        self.dicCurrentFilename = self.filesel.get_filename()
        self.window.set_title(self.dicCurrentFilename)
        self.filesel.destroy()
        
    def save_file(self, dicFilename, data):
        "Saves the data to the file located by the filename"
        print 'save this ', dicFilename
        
        if dicFilename['TYPE'] == 'SSH':
            sFile = dicFilename['TMPNAME']
        else:
            sFile = dicFilename['NAME']
        outfile = open(sFile, "w")
        if outfile:
            outfile.write(data)
            outfile.close() 
            #mark as unmodified since last save
            self.textbuffer.set_modified(False)
            
        if dicFilename['TYPE'] == 'SSH':
            os.system('cp -f ' + dicFilename['TMPNAME']  +' ' + os.path.basename(dicFilename['NAME'] ) )
            s1 = 'scp -P ' + dicFilename['PORT'] +   ' ' + os.path.basename(dicFilename['NAME'] )  + ' '  + dicFilename['USER'] + '@' + dicFilename['HOST'] + '://' 
            s1 +=  os.path.dirname(dicFilename['NAME'] )
            print s1
            
            os.system(s1)
            os.system('rm ' +  os.path.basename(dicFilename['NAME'] ) )
            print 'Files saved'
            
    def save_current_file(self, data=None):
        "Saves the text to the current file"
        if self.dicCurrentFilename['NAME'] != "/new":
            self.save_file(self.dicCurrentFilename, self.get_text())
        else:
            self.save_as_item_clicked()
    
    # edit menu
    def on_undo1_activate(self,  event):
        self.textbuffer.undo ()
        
    def on_redo1_activate(self,  event):
        self.textbuffer.redo ()
            
    def on_cut1_activate(self, event):
        self.textbuffer.cut_clipboard(self.clipboard, self.view.get_editable())

    def on_copy1_activate(self, event):
        self.textbuffer.copy_clipboard(self.clipboard)
        
    def on_paste1_activate(self, event):
        self.textbuffer.paste_clipboard(self.clipboard,None,  self.view.get_editable())

        
    # toolbar buttons
    def on_tbUndo_clicked(self, event):
        self.activateClick('undo1')
        
    def on_tbRedo_clicked(self, event):
        self.activateClick('redo1')
        
    def on_tbCut_clicked(self, event):
        self.activateClick('cut1')
    
    def on_tbCopy_clicked(self, event):
        self.activateClick('copy1')
    
    def on_tbPaste_clicked(self, event):
        self.activateClick('paste1')
           
        
    def plugin_item_clicked(self, data=None):
        "Creates a file chooser and allows user to open a file with it"
        self.filesel = gtk.FileSelection("Select plugin to open...")
        self.filesel.ok_button.connect_object("clicked", self.open_selected_plugin, None)
        self.filesel.cancel_button.connect("clicked", lambda w: self.filesel.destroy())
        self.filesel.show()
    
    
    def setLanguage(self,  mType):
        manager = self.textbuffer.get_data('languages-manager')
        #print manager.get_available_languages()
        mime_type = mType
        language = manager.get_language_from_mime_type(mime_type)
        self.textbuffer.set_highlight(True)
        self.textbuffer.set_language(language)

    def open_selected_plugin(self, data=None):
        "Opens the selected plugin file and reads it in"
        self.open_plugin(self.filesel.get_filename())
        self.filesel.destroy()  
    
    def open_plugin(self, filename):
        "Opens the file given in filename and reads it in"
        infile = open(filename, "r")
        if infile:
            command = infile.read()
            infile.close()
            exec(command)
    
    
    def enable_wrap(self,data=None):
        "Enables word wrap and changes menu item appropriately"
        self.textview.set_wrap_mode(gtk.WRAP_WORD)
        self.word_wrap_item.destroy()
        self.word_wrap_item=gtk.MenuItem("Disable _Word Wrap")
        self.word_wrap_item.connect_object("activate",self.disable_wrap,None)
        self.edit_menu.append(self.word_wrap_item)  
        self.word_wrap_item.show()
    
    def disable_wrap(self,data=None):
        "Disables word wrap and changes menu item appropriately"
        self.textview.set_wrap_mode(gtk.WRAP_NONE)
        self.word_wrap_item.destroy()
        self.word_wrap_item=gtk.MenuItem("Enable _Word Wrap")
        self.word_wrap_item.connect_object("activate",self.enable_wrap,None)
        self.edit_menu.append(self.word_wrap_item)  
        self.word_wrap_item.show()

