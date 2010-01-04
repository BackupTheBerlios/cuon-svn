# -*- coding: utf-8 -*-

##Copyright (C) [2003]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 
from cuon.Databases.SingleData import SingleData
import logging
import threading

class SingleNotes(SingleData):

    
    def __init__(self, allTables):

        SingleData.__init__(self)
        # tables.dbd and address
        self.sNameOfTable =  "address_notes"
        self.xmlTableDef = 0
        self.loadTable(allTables)

        #self.athread = threading.Thread(target = self.loadTable())
        #self.athread.start()
        
        self.listHeader['names'] = []
        self.listHeader['size'] = []
        self.out( "number of Columns ")
        self.out( len(self.table.Columns))
        #
        self.addressId = 0
        self.NotesMisc = None
        self.NotesContact = None
        self.NotesRep = None
        self.NotesSalesman= None
        self.NotesOrganisation = None
        
        
    def readNonWidgetEntries(self, dicValues):
        print 'readNonWidgetEntries(self) by SingleMisc'
        dicValues['address_id'] = [self.addressId, 'int']
        dicValues['notes_misc'] = [self.NotesMisc.get_text(self.NotesMisc.get_start_iter(), self.NotesMisc.get_end_iter(), 1), 'text']
        dicValues['notes_contacter'] = [self.NotesContact.get_text(self.NotesContact.get_start_iter(), self.NotesContact.get_end_iter(), 1), 'text']
        dicValues['notes_representant'] = [self.NotesRep.get_text(self.NotesRep.get_start_iter(), self.NotesRep.get_end_iter(), 1), 'text']
        dicValues['notes_salesman'] = [self.NotesSalesman.get_text(self.NotesSalesman.get_start_iter(), self.NotesSalesman.get_end_iter(), 1), 'text']
        dicValues['notes_organisation'] = [self.NotesOrganisation.get_text(self.NotesOrganisation.get_start_iter(), self.NotesOrganisation.get_end_iter(), 1), 'text']

        return dicValues

    def fillOtherEntries(self, oneRecord):
        #print "oneRecord = ",  oneRecord['notes_misc']
        self.NotesMisc.set_text(oneRecord['notes_misc'])
        self.NotesContact.set_text(oneRecord['notes_contacter'])
        self.NotesRep.set_text(oneRecord['notes_representant'])
        self.NotesSalesman.set_text(oneRecord['notes_salesman'])
        self.NotesOrganisation.set_text(oneRecord['notes_organisation'])
        
        
    def clearAllOtherFields(self):
        self.NotesMisc.set_text('')
        self.NotesContact.set_text('')
        self.NotesRep.set_text('')
        self.NotesSalesman.set_text('')
        self.NotesOrganisation.set_text('')
