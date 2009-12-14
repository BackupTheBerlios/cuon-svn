# -*- coding: utf-8 -*-

##Copyright (C) [2003, 2004, 2005, 2006, 2007]  [Juergen Hamel, D-32584 Loehne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 


import sys
import os
import os.path
from types import *
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import base64
import bz2

from cuon.Editor.editor  import editorwindow
class sendEmail(editorwindow):

    def __init__(self, dicV=None):
        if dicV:
            self.dicValues = dicV
        else:
            self.dicValues = {}
            
        self.liAttachments = []
        
        editorwindow.__init__(self)
        table = gtk.Table(2,5)
        hbox = gtk.HBox()
        tree1 = gtk.TreeView()
        treestore = gtk.TreeStore(object)
        treestore = gtk.TreeStore(str)
##        renderer = gtk.CellRendererText()
## 
##        column = gtk.TreeViewColumn("Zweite Spalte", renderer, text=0)
##        treeview.append_column(column)
        tree1.set_model(treestore)
        
        
        label = gtk.Label('From')
        label2 = gtk.Label('To')
        label3 = gtk.Label('CC')
        label4 = gtk.Label('BCC')
        label5 = gtk.Label('Subject')
        
        self.eFrom = gtk.Entry()
        self.eTo = gtk.Entry()
        self.eCC = gtk.Entry()
        self.eBCC = gtk.Entry()
        self.eSubject = gtk.Entry()
        
        self.fcAttachment = gtk.FileChooserButton(_('Attachment'), backend=None)
        self.fcAttachment.connect('file_activated',self.on_fcAttachment_file_activated )
        self.fcAttachment.connect('selection_changed',self.on_fcAttachment_file_activated )
        
        vbox = self.getWidget('vbox2')
        vbox.hide()
        table.attach(label,0,1,0,1)
        table.attach(label2,0,1,1,2)
        table.attach(label3,0,1,2,3)
        table.attach(label4,0,1,3,4)
        table.attach(label5,0,1,4,5)

        table.attach(self.eFrom,1,2,0,1)
        table.attach(self.eTo,1,2,1,2)
        table.attach(self.eCC,1,2,2,3)
        table.attach(self.eBCC,1,2,3,4)
        table.attach(self.eSubject,1,2,4,5)

        table.attach(self.fcAttachment,2,3,0,1)
        
        vbox.pack_start(table)
        vbox.pack_start(tree1)

        #tv1 = self.getWidget('tv1')
    
        
        vbox.reorder_child(tree1,0)
        vbox.reorder_child(table,1)
        #vbox.reorder_child(tv1,2)
        vbox.show_all()
        #label.show()
        
        menubar1 = self.getWidget('menubar1')
        
        
        mEmail = gtk.Menu()
        mSend = gtk.MenuItem('Send mail')
        mSend.connect_object("activate", self.on_send_mail_activate, 'send email')
        mEmail.append(mSend)



        mSend.show()
        mEmail.show()

        iEmail = gtk.MenuItem('Email')
        iEmail.set_submenu(mEmail)
        
        iEmail.show()
        
        menubar1.append(iEmail)
        menubar1.show()
        if self.dicValues:
            if self.dicValues['To']:
                self.eTo.set_text(self.dicValues['To'])
            if self.dicValues['From']:
                self.eFrom.set_text(self.dicValues['From'])
            if self.dicValues['Signatur']:
                print 'Signatur'
                self.add2Textbuffer(self.getWidget('tv1'), self.dicValues['Signatur'],'Tail')        
            
    def on_fcAttachment_file_activated(self, event):
        print event
        self.addAttachment( event.get_filename())
        
        
    def on_send_mail_activate(self, event):
        print event
        print 'send mail '
        self.dicValues['To'] = self.eTo.get_text()
        self.dicValues['From'] = self.eFrom.get_text()
        self.dicValues['Subject'] = self.eSubject.get_text()
        
        self.dicValues['Body'] = self.readTextBuffer(self.getWidget('tv1'))
        
        em = self.rpc.callRP('Email.sendTheEmail', self.dicValues, self.liAttachments, self.dicUser)
        self.writeEmailLog(em)
        

        
    def addAttachment(self, filename):
        if filename:
            f = open(filename,'rb')
            if f:
                s = f.read()
                s = bz2.compress(s)
                s = base64.encodestring(s)
                dicAtt = {}
                dicAtt['filename'] = filename
                dicAtt['data'] = s
                
                self.liAttachments.append(dicAtt)
                print 'len liAtt', len(self.liAttachments)
                
                
