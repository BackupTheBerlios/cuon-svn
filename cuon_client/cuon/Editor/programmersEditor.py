from editor import editorwindow
import gtk

class programmerseditor(editorwindow):
    def __init__(self):
        editorwindow.__init__(self,prgmode=True)
        self.win1.maximize()
        self.nbEditor = self.getWidget('nbEditor')
        self.projectFolder = "/"
        self.textbuffers = []
#        Vbox = self.getWidget('vbox1')
#        Scrolledwindow = self.getWidget('scrolledwindow1')
#        Vbox.remove(Scrolledwindow)
        
            
##        if GtkSV:
##            self.textbuffer,  self.view = self.getNotesEditor(mime_type = 'text/x-ini-file')
            
##            Vbox = self.getWidget('vbox1')
##            Scrolledwindow = self.getWidget('scrolledwindow1')
##            Scrolledwindow.remove(self.getWidget('viewport1'))
##            #Vbox.remove(oldScrolledwindow)
##            #Vbox.add(self.view)
##            #Vbox.show_all()
##            Scrolledwindow.add(self.view)
##            self.view.show_all()
##            Scrolledwindow.show_all()
            
            
##        else:
            

##            self.textbuffer = self.getWidget('tv1').get_buffer()
        
        
#        self.notebook= gtk.Notebook()
#        self.notebook.set_tab_pos(gtk.POS_TOP)
         
#        self.notebook2= gtk.Notebook()
#        self.notebook2.set_tab_pos(gtk.POS_TOP)
#        label = gtk.Label('Prg-Files')
#        label.show()
#        label2 = gtk.Label('Glade Files')
#        label2.show()
#        label3 = gtk.Label('Other Files')
#        label3.show()
        
#        vbox2 = self.getWidget('vbox2')
#        self.notebook.show()
#        sc2 = gtk.ScrolledWindow()
#        tree1 = gtk.TreeView()
#        tree2 = gtk.TreeView()
#        tree3 = gtk.TreeView()
#        renderer = gtk.CellRendererText()
#        column = gtk.TreeViewColumn(_("Files"), renderer, text=0)
#        tree1.append_column(column)
        
#        self.notebook2.append_page( tree1,label) 
#        self.notebook2.append_page( tree2,label2)
#        self.notebook2.append_page( tree3,label3)  
#        sc2.add(self.notebook2)
#        hbox = gtk.HBox()
#        hbox.add(sc2)
#        hbox.add(self.notebook)
#        Vbox.add(hbox)
#        Vbox.show_all()
        #self.setNewTextbuffer('untitled')
        self.projectfiles = ['*.py','*.xml','*.glade*','*.html']
        
    def on_tbOpen_clicked(self, event):
        self.on_open1_activate(event)
        
    def on_open1_activate(self, event):
        print 'open1'
        self.selectFile(self.projectfiles)
      
        
    def on_tbQuit_clicked(self, event):
        self.on_quit1_activate(event)
        
    def on_quit1_activate(self, event):
         self.closeWindow()
         
         
    
    def disconnectPrgFilesTree(self):
        try:
             
            self.getWidget('treePrgFiles').get_selection().disconnect(self.connectPrgFilesTreeId)
        except:
            pass

    def connectPrgFilesTree(self):
        try:
            self.connectPrgFilesTreeId = self.getWidget('treePrgFiles').get_selection().connect("changed", self.PrgFilesTree_select_callback)
        except:
            pass
   
    def PrgFilesTree_select_callback(self, treeSelection):
        listStore, iter = treeSelection.get_selected()
        
        print listStore,iter
        
        if listStore and len(listStore) > 0:
           row = listStore[0]
        else:
           row = -1
   
        if iter != None:
            sNewId = listStore.get_value(iter, 0)
            print sNewId
            try:
                newID = int(sNewId[sNewId.find('###')+ 3:])
                #self.setDateValues(newID)
                
            except:
                pass
    def setPrgFiles(self):
        treestore = gtk.TreeStore(object)
        treestore = gtk.TreeStore(str)
        ts.set_model(treestore)
    
    
    def selectFile(self, liPattern = []):
        fc = gtk.FileChooserDialog(title='Open File...',
                                   parent=None,
                                   action=gtk.FILE_CHOOSER_ACTION_OPEN,
                                   buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
        fc.set_current_folder(self.projectFolder)
        fc.set_default_response(gtk.RESPONSE_OK)
        filter = gtk.FileFilter()
        filter.set_name('Project Files')
        for i in liPattern:
            print i
            filter.add_pattern(i)
       
        fc.add_filter(filter)
        response = fc.run()
        if response == gtk.RESPONSE_OK:
            print 'ok'
            print fc.get_filename()
            self.open_file( {'NAME':fc.get_filename(), 'TYPE':self.checkMimeType(fc.get_filename()) })
            self.projectFolder = fc.get_current_folder()
        else:
            print 'not ok'
        fc.destroy()

    def open_file(self, dicFilename):
        
        filename = dicFilename['NAME']
        infile = open(filename, "r")
        
        if infile:
            
            print "filename = ", filename
            self.setNewTextbuffer(filename, self.checkMimeType(filename))
            self.textbuffers[len(self.textbuffers)-1][0].set_text(infile.read())
            #self.win1.set_title(self.dicCurrentFilename['NAME'])
           
            infile.close()
           
            
    def setNewTextbuffer(self,title,mime_type= 'text/x-ini-file'):
   
        label = gtk.Label(title)
        label.show()
        textbuffer,  view = self.getNotesEditor(mime_type = mime_type)
        view.set_auto_indent(True)
        print 'styles:'
        print 'indent = ', view.get_auto_indent()
        print 'buffer = ', textbuffer
        print 'language - style = ', textbuffer.get_language()
        print 'language - style-ids = ', textbuffer.get_language().get_style_ids()

        
        Scrolledwindow =  gtk.ScrolledWindow(hadjustment=None, vadjustment=None)

        Scrolledwindow.add(view)
        view.show_all()
        Scrolledwindow.show_all()
        newPage = self.nbEditor.append_page(Scrolledwindow, label)
        self.textbuffers.append([textbuffer, view, title,newPage])

    
