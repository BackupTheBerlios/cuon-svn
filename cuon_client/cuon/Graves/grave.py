# -*- coding: utf-8 -*-

##Copyright (C) [2005]  [Jürgen Hamel, D-32584 Löhne]

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
import gobject
from gtk import TRUE, FALSE
import string
import logging
import SingleGrave
import SingleGraveMaintenance
import SingleGraveSpring
import SingleGraveSummer
import SingleGraveAutumn
import SingleGraveWinter

from cuon.Windows.chooseWindows  import chooseWindows
import cPickle
#import cuon.OpenOffice.letter
# localisation
import locale, gettext
locale.setlocale (locale.LC_NUMERIC, '')
import threading
import mx.DateTime
import graveyard

class graveswindow(chooseWindows):

    
    def __init__(self, allTables):

        chooseWindows.__init__(self)
        self.allTables = allTables
        self.singleGrave = SingleGrave.SingleGrave(allTables)
        self.singleGraveMaintenance = SingleGraveMaintenance.SingleGraveMaintenance(allTables)
        self.singleGraveSpring = SingleGraveSpring.SingleGraveSpring(allTables)
        self.singleGraveSummer = SingleGraveSummer.SingleGraveSummer(allTables)
        self.singleGraveAutumn = SingleGraveAutumn.SingleGraveAutumn(allTables)
        self.singleGraveWinter = SingleGraveWinter.SingleGraveWinter(allTables)

    
        self.loadGlade('graves.xml', 'GraveMainwindow')

        self.setStatusBar()


        self.EntriesGraves = 'graves.xml'
        
        self.loadEntries(self.EntriesGraves)
        
        self.singleGrave.setEntries(self.getDataEntries(self.EntriesGraves) )
        self.singleGrave.setGladeXml(self.xml)
        self.singleGrave.setTreeFields( ['lastname', 'firstname'] )
        self.singleGrave.setStore( gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING,   gobject.TYPE_UINT) ) 
        self.singleGrave.setTreeOrder('lastname, firstname')
        self.singleGrave.setListHeader([_('Lastname'), _('Firstname')])
        self.singleGrave.setTree(self.xml.get_widget('tree1') )

        self.EntriesGravesMaintenance = 'graves_maintenance.xml'
        
        self.loadEntries(self.EntriesGravesMaintenance)
        
        self.singleGraveMaintenance.setEntries(self.getDataEntries(self.EntriesGravesMaintenance) )
        self.singleGraveMaintenance.setGladeXml(self.xml)
        self.singleGraveMaintenance.setTreeFields( ['grave_service_id' ] )
        self.singleGraveMaintenance.setStore( gtk.ListStore(gobject.TYPE_INT,  gobject.TYPE_UINT) ) 
        self.singleGraveMaintenance.setTreeOrder('grave_service_id')
        self.singleGraveMaintenance.setListHeader([_('Service-ID')])
        self.singleGraveMaintenance.setTree(self.xml.get_widget('tree1') )
        self.singleGraveMaintenance.sWhere  ='where grave_id = ' + `self.singleGrave.ID`
  
        self.EntriesGravesSpring = 'graves_spring.xml'
        
        self.loadEntries(self.EntriesGravesSpring)
        
        self.singleGraveSpring.setEntries(self.getDataEntries(self.EntriesGravesSpring) )
        self.singleGraveSpring.setGladeXml(self.xml)
        self.singleGraveSpring.setTreeFields( ['article_id' ] )
        self.singleGraveSpring.setStore( gtk.ListStore(gobject.TYPE_INT,  gobject.TYPE_UINT) ) 
        self.singleGraveSpring.setTreeOrder('article_id')
        self.singleGraveSpring.setListHeader([_('article-ID')])
        self.singleGraveSpring.setTree(self.xml.get_widget('tree1') )
        self.singleGraveSpring.sWhere  ='where grave_id = ' + `self.singleGrave.ID`
  
        self.EntriesGravesSummer = 'graves_summer.xml'
        self.loadEntries(self.EntriesGravesSummer)
        
        self.singleGraveSummer.setEntries(self.getDataEntries(self.EntriesGravesSummer) )
        self.singleGraveSummer.setGladeXml(self.xml)
        self.singleGraveSummer.setTreeFields( ['article_id' ] )
        self.singleGraveSummer.setStore( gtk.ListStore(gobject.TYPE_INT,  gobject.TYPE_UINT) ) 
        self.singleGraveSummer.setTreeOrder('article_id')
        self.singleGraveSummer.setListHeader([_('article-ID')])
        self.singleGraveSummer.setTree(self.xml.get_widget('tree1') )
        self.singleGraveSummer.sWhere  ='where grave_id = ' + `self.singleGrave.ID`
  
  
        self.EntriesGravesAutumn = 'graves_autumn.xml'
        
        self.loadEntries(self.EntriesGravesAutumn)
        
        self.singleGraveAutumn.setEntries(self.getDataEntries(self.EntriesGravesAutumn) )
        self.singleGraveAutumn.setGladeXml(self.xml)
        self.singleGraveAutumn.setTreeFields( ['article_id' ] )
        self.singleGraveAutumn.setStore( gtk.ListStore(gobject.TYPE_INT,  gobject.TYPE_UINT) ) 
        self.singleGraveAutumn.setTreeOrder('article_id')
        self.singleGraveAutumn.setListHeader([_('article-ID')])
        self.singleGraveAutumn.setTree(self.xml.get_widget('tree1') )
        self.singleGraveAutumn.sWhere  ='where grave_id = ' + `self.singleGrave.ID`
  
        self.EntriesGravesWinter = 'graves_winter.xml'
        
        self.loadEntries(self.EntriesGravesWinter)
        
        self.singleGraveWinter.setEntries(self.getDataEntries(self.EntriesGravesWinter) )
        self.singleGraveWinter.setGladeXml(self.xml)
        self.singleGraveWinter.setTreeFields( ['article_id' ] )
        self.singleGraveWinter.setStore( gtk.ListStore(gobject.TYPE_INT,  gobject.TYPE_UINT) ) 
        self.singleGraveWinter.setTreeOrder('article_id')
        self.singleGraveWinter.setListHeader([_('article-ID')])
        self.singleGraveWinter.setTree(self.xml.get_widget('tree1') )
        self.singleGraveWinter.sWhere  ='where grave_id = ' + `self.singleGrave.ID`
  
  
        # set values for comboBox

        liService,  liTypeOfGrave, liTypeOfPaid, liPercent = self.rpc.callRP('Grave.getComboBoxEntries',self.dicUser)
        print liService   ,  liTypeOfGrave, liTypeOfPaid, liPercent
        cbService = self.getWidget('cbServiceType')
        if cbService:
            liststore = gtk.ListStore(str)
            for service in liService:
                liststore.append([service])
            cbService.set_model(liststore)
            cbService.set_text_column(0)
            cbService.show()
        
        cbTypeOfGrave = self.getWidget('cbTypeOfGrave')
        if cbTypeOfGrave:
            liststore = gtk.ListStore(str)
            for TypeOfGrave in liTypeOfGrave:
                liststore.append([TypeOfGrave])
            cbTypeOfGrave.set_model(liststore)
            cbTypeOfGrave.set_text_column(0)
            cbTypeOfGrave.show()

        cbTypeOfPaid = self.getWidget('cbTypeOfPaid')
        if cbTypeOfPaid:
            liststore = gtk.ListStore(str)
            for TypeOfPaid in liTypeOfPaid:
                liststore.append([TypeOfPaid])
            cbTypeOfPaid.set_model(liststore)
            cbTypeOfPaid.set_text_column(0)
            cbTypeOfPaid.show()

        cbPercent = self.getWidget('cbPercent')
        if cbPercent:
            liststore = gtk.ListStore(str)
            for Percent in liPercent:
                liststore.append([Percent])
            cbPercent.set_model(liststore)
            cbPercent.set_text_column(0)
            cbPercent.show()

        # Menu-items
        self.initMenuItems()

        # Close Menus for Tab
        self.addEnabledMenuItems('tabs','grave1')
        self.addEnabledMenuItems('tabs','maintenance1')
        self.addEnabledMenuItems('tabs','spring1')
        self.addEnabledMenuItems('tabs','autumn1')
        self.addEnabledMenuItems('tabs','autumn1')
        # seperate Menus
        self.addEnabledMenuItems('grave','grave1')
        self.addEnabledMenuItems('graveMaintenance','maintenance1')
        self.addEnabledMenuItems('graveSpring','spring1')
        self.addEnabledMenuItems('graveSpring','summer1')
        # enabledMenues for grave
        self.addEnabledMenuItems('editGrave','new1')
        self.addEnabledMenuItems('editGrave','clear1')
        self.addEnabledMenuItems('editGrave','print1')
        self.addEnabledMenuItems('editGrave','edit1')
 # enabledMenues for graveMaintenance
        self.addEnabledMenuItems('editGraveMaintenance','MaintenanceNew1')
        self.addEnabledMenuItems('editGraveMaintenance','MaintenanceClear1')
        self.addEnabledMenuItems('editGraveMaintenance','MaintenancePrint1')
        self.addEnabledMenuItems('editGraveMaintenance','MaintenanceEdit1')

    # enabledMenues for graveSpring
        self.addEnabledMenuItems('editGraveSpring','SpringNew1')
        self.addEnabledMenuItems('editGraveSpring','SpringClear1')
        self.addEnabledMenuItems('editGraveSpring','SpringPrint1')
        self.addEnabledMenuItems('editGraveSpring','SpringEdit1')

        
    # enabledMenues for graveSummer
        self.addEnabledMenuItems('editGraveSummer','SummerNew1')
        self.addEnabledMenuItems('editGraveSummer','SummerClear1')
        self.addEnabledMenuItems('editGraveSummer','SummerPrint1')
        self.addEnabledMenuItems('editGraveSummer','SummerEdit1')

    # enabledMenues for graveAutumn
        self.addEnabledMenuItems('editGraveAutumn','AutumnNew1')
        self.addEnabledMenuItems('editGraveAutumn','AutumnClear1')
        self.addEnabledMenuItems('editGraveAutumn','AutumnPrint1')
        self.addEnabledMenuItems('editGraveAutumn','AutumnEdit1')
        
    # enabledMenues for graveWinter
        self.addEnabledMenuItems('editGraveWinter','WinterNew1')
        self.addEnabledMenuItems('editGraveWinter','WinterClear1')
        self.addEnabledMenuItems('editGraveWinter','WinterPrint1')
        self.addEnabledMenuItems('editGraveWinter','WinterEdit1')


        # tabs from notebook
        
        self.tabGrave = 0
        self.tabGraveMaintenance = 1
        self.tabGraveSpring = 2
        self.tabGraveSummer= 3
        self.tabGraveAutumn = 4
        self.tabGraveWinter = 5
        try:
            self.win1.add_accel_group(self.accel_group)
        except Exception,  params:
            print Exception,  params
            


        self.tabChanged()
        

    #Menu File
              
    def on_quit1_activate(self, event):
        self.out( "exit clients V1")
        self.closeWindow() 
    
        


    #Menu Addressimport cuon.Login.User
  
    def on_save1_activate(self, event):
        self.out( "save grave v2")
        self.singleGrave.save()
        self.setEntriesEditable(self.EntriesGraves, FALSE)
        self.tabChanged()
        
    def on_new1_activate(self, event):
        self.out( "new grave v2")
        self.singleGrave.newRecord()
        print self.singleGrave.ID
        
        self.setEntriesEditable(self.EntriesGraves, TRUE)

    def on_edit1_activate(self, event):
        self.out( "edit grave v2")
        self.setEntriesEditable(self.EntriesGraves, TRUE)


    def on_delete1_activate(self, event):
        self.out( "delete grave v2")
        self.singleGrave.deleteRecord()

   
  #Menu maintenance
        
   
    def on_MaintenanceSave1_activate(self, event):
        self.out( "save GraveMaintenance addresses v2")
        self.singleGraveMaintenance.graveID = self.singleGrave.ID
        self.singleGraveMaintenance.save()
        self.setEntriesEditable(self.EntriesGravesMaintenance, FALSE)
        self.tabChanged()
        
    def on_MaintenanceNew1_activate(self, event):
        self.out( "new GraveMaintenance addresses v2")
        self.singleGraveMaintenance.newRecord()
        self.setEntriesEditable(self.EntriesGravesMaintenance, TRUE)

        
    def on_MaintenanceEdit1_activate(self, event):
        self.setEntriesEditable(self.EntriesGravesMaintenance, TRUE)


    def on_MaintenanceDelete1_activate(self, event):
        self.out( "delete GraveMaintenance addresses v2")
        self.singleGraveMaintenance.deleteRecord()

#Menu Spring
        
   
    def on_SpringSave1_activate(self, event):
        self.out( "save GraveSpring addresses v2")
        self.singleGraveSpring.graveID = self.singleGrave.ID
        self.singleGraveSpring.save()
        self.setEntriesEditable(self.EntriesGravesSpring, FALSE)
        self.tabChanged()
        
    def on_SpringNew1_activate(self, event):
        self.out( "new GraveSpring addresses v2")
        self.singleGraveSpring.newRecord()
        self.setEntriesEditable(self.EntriesGravesSpring, TRUE)

        
    def on_SpringEdit1_activate(self, event):
        self.setEntriesEditable(self.EntriesGravesSpring, TRUE)


    def on_SpringDelete1_activate(self, event):
        self.out( "delete GraveSpring addresses v2")
        self.singleGraveSpring.deleteRecord()



        #Menu Summer
        
   
    def on_SummerSave1_activate(self, event):
        self.out( "save GraveSummer addresses v2")
        self.singleGraveSummer.graveID = self.singleGrave.ID
        self.singleGraveSummer.save()
        self.setEntriesEditable(self.EntriesGravesSummer, FALSE)
        self.tabChanged()
        
    def on_SummerNew1_activate(self, event):
        self.out( "new GraveSummer addresses v2")
        self.singleGraveSummer.newRecord()
        self.setEntriesEditable(self.EntriesGravesSummer, TRUE)

        
    def on_SummerEdit1_activate(self, event):
        self.setEntriesEditable(self.EntriesGravesSummer, TRUE)


    def on_SummerDelete1_activate(self, event):
        self.out( "delete GraveSummer addresses v2")
        self.singleGraveSummer.deleteRecord()



        
        #Menu Autumn
        
   
    def on_AutumnSave1_activate(self, event):
        self.out( "save GraveAutumn addresses v2")
        self.singleGraveAutumn.graveID = self.singleGrave.ID
        self.singleGraveAutumn.save()
        self.setEntriesEditable(self.EntriesGravesAutumn, FALSE)
        self.tabChanged()
        
    def on_AutumnNew1_activate(self, event):
        self.out( "new GraveAutumn addresses v2")
        self.singleGraveAutumn.newRecord()
        self.setEntriesEditable(self.EntriesGravesAutumn, TRUE)

        
    def on_AutumnEdit1_activate(self, event):
        self.setEntriesEditable(self.EntriesGravesAutumn, TRUE)


    def on_AutumnDelete1_activate(self, event):
        self.out( "delete GraveAutumn addresses v2")
        self.singleGraveAutumn.deleteRecord()

        #Menu Winter
        
   
    def on_WinterSave1_activate(self, event):
        self.out( "save GraveWinter addresses v2")
        self.singleGraveWinter.graveID = self.singleGrave.ID
        self.singleGraveWinter.save()
        self.setEntriesEditable(self.EntriesGravesWinter, FALSE)
        self.tabChanged()
        
    def on_WinterNew1_activate(self, event):
        self.out( "new GraveWinter addresses v2")
        self.singleGraveWinter.newRecord()
        self.setEntriesEditable(self.EntriesGravesWinter, TRUE)

        
    def on_WinterEdit1_activate(self, event):
        self.setEntriesEditable(self.EntriesGravesWinter, TRUE)


    def on_WinterDelete1_activate(self, event):
        self.out( "delete GraveWinter addresses v2")
        self.singleGraveWinter.deleteRecord()

        

##    def on_calendar1_day_selected(self, cal):
##        print cal
##        date  = cal.get_date()
##        print date
##        print date[0]
##        print date[1]
##        print date[2]
##        eSchedulDate = self.getWidget('eSchedulDate')
##        newDate = mx.DateTime.DateTime(date[0], date[1] + 1, date[2])
##        sDate = newDate.strftime(self.oUser.userDateTimeFormatString)
##        eSchedulDate.set_text(sDate)
        
##    def on_eSchedulDate_changed(self, event):
##        pass

##    def on_hscale1_value_changed(self, hScale):
##        tTime = None
##        hourValue =  hScale.get_value()
##        eSchedulTime = self.getWidget('eSchedulTime')
##        sTime = eSchedulTime.get_text()
##        if sTime:
##            tTime = mx.DateTime.strptime(sTime,self.oUser.userTimeFormatString)
##            oldHour = tTime.hour
##            oldMinute = tTime.minute
            
##            print 'oldHour = ' + `oldHour`
            
##            tTime = mx.DateTime.today(hourValue, oldMinute)
##        else:
##            tTime = mx.DateTime.today(hourValue, 0)
            
##        sTime = tTime.strftime(self.oUser.userTimeFormatString)
##        eSchedulTime.set_text(sTime)
            
##    def on_vscale1_value_changed(self, vScale):
##        tTime = None
##        minuteValue =  vScale.get_value()
##        eSchedulTime = self.getWidget('eSchedulTime')
##        sTime = eSchedulTime.get_text()
##        if sTime:
##            tTime = mx.DateTime.strptime(sTime,self.oUser.userTimeFormatString)
##            oldHour = tTime.hour
##            oldMinute = tTime.minute
            
##            tTime = mx.DateTime.today(oldHour, minuteValue)
##        else:
##            tTime = mx.DateTime.today(0, minuteValue)
            
##        sTime = tTime.strftime(self.oUser.userTimeFormatString)
##        eSchedulTime.set_text(sTime)
            
        
        
    


    # Menu Lists

    def on_liAddressesPhone1_activate(self, event):
        self.out( "lists startet")
        Pdf = lists_addresses_phone1.lists_addresses_phone1()


    def on_liAddressesPhone11_activate(self, event):
        self.out( "lists startet")
        Pdf = lists_addresses_phone11.lists_addresses_phone11()



    #Menu Writer
    def on_newletter1_activate(self, event):
        self.out("writer startet ")

        fkey = 'cuonAddress' + `self.singleGrave.ID`
        self.out( fkey)
        self.pickleObject(fkey , self.singleGrave.getAddress(self.singleGrave.ID))

        sExec = os.environ['CUON_OOEXEC']
        os.system(sExec + ' cuon/OpenOffice/ooMain.py ' + fkey )
        #letter1 = cuon.OpenOffice.letter.letter()
        #letter1.createAddress(singleGrave.ID)


        
    def on_chooseAddress_activate(self, event):
        # choose Address from other Modul
        if self.tabOption == self.tabGrave:
            print '############### Address choose ID ###################'
            self.setChooseValue(self.singleGrave.ID)
            self.closeWindow()
        elif self.tabOption == self.tabPartner:
            print '############### Address choose ID ###################'
            self.setChooseValue(self.singlePartner.ID)
            self.closeWindow()

        else:
            print '############### No ID found,  choose ID -1 ###################'
            self.setChooseValue('-1')
            self.closeWindow()
 
              
    def on_bSearchGraveyard_clicked(self,  event):
        adr = graveyard.graveyardMainwindow(self.allTables)
        adr.setChooseEntry('chooseGraveyard', self.getWidget( 'eGraveyardID'))

    # signals from entry eAddressNumber
    
    def on_eGraveyardID_changed(self, event):
        print 'eAdrnbr changed'
        iAdrNumber = self.getChangedValue('eGraveyardID')
        eAdrField = self.getWidget('eGraveyardShortname')
        #iAdr = self.singleAddress.getAddress(iAdrNumber)
        #self.setTextbuffer(eAdrField,liAdr) 
        
    # search button
    def on_bSearch_clicked(self, event):
        self.out( 'Searching ....', self.ERROR)
        sName = self.getWidget('eFindName').get_text()
        sCity = self.getWidget('eFindCity').get_text()
        self.out('Name and City = ' + sName + ', ' + sCity, self.ERROR)
        self.singleGrave.sWhere = 'where lastname ~* \'.*' + sName + '.*\' and city ~* \'.*' + sCity + '.*\''
        self.out(self.singleGrave.sWhere, self.ERROR)
        self.refreshTree()

    def refreshTree(self):
        self.singleGrave.disconnectTree()
        self.singleGraveMaintenance.disconnectTree()
        self.singleGraveSpring.disconnectTree()
        self.singleGraveSummer.disconnectTree()
        self.singleGraveAutumn.disconnectTree()
        self.singleGraveWinter.disconnectTree()
        
        if self.tabOption == self.tabGrave:
            self.singleGrave.connectTree()
            self.singleGrave.refreshTree()
       
        elif self.tabOption == self.tabGraveMaintenance:
            print "1 tree "
            self.singleGraveMaintenance.sWhere  ='where grave_id = ' + `int(self.singleGrave.ID)`
            self.singleGraveMaintenance.connectTree()
            self.singleGraveMaintenance.refreshTree()
        
        elif self.tabOption == self.tabGraveSpring:
            print "1 tree "
            self.singleGraveSpring.sWhere  ='where grave_id = ' + `int(self.singleGrave.ID)`
            self.singleGraveSpring.connectTree()
            self.singleGraveSpring.refreshTree()
            
        
        elif self.tabOption == self.tabGraveSummer:
            print "1 tree "
            self.singleGraveSummer.sWhere  ='where grave_id = ' + `int(self.singleGrave.ID)`
            self.singleGraveSummer.connectTree()
            self.singleGraveSummer.refreshTree()
        
        elif self.tabOption == self.tabGraveAutumn:
            print "1 tree "
            self.singleGraveAutumn.sWhere  ='where grave_id = ' + `int(self.singleGrave.ID)`
            self.singleGraveAutumn.connectTree()
            self.singleGraveAutumn.refreshTree()
            
        elif self.tabOption == self.tabGraveWinter:
            print "1 tree "
            self.singleGraveWinter.sWhere  ='where grave_id = ' + `int(self.singleGrave.ID)`
            self.singleGraveWinter.connectTree()
            self.singleGraveWinter.refreshTree()
            

         
    def tabChanged(self):
        self.out( 'tab changed to :'  + str(self.tabOption))
        
        if self.tabOption == self.tabGrave:
            #Address
            self.disableMenuItem('tabs')
            self.enableMenuItem('grave')

            self.actualEntries = self.singleGrave.getEntries()
            self.editAction = 'editGrave'
            self.setStatusbarText([''])
          
            self.setTreeVisible(True)
            

            self.out( 'Seite 0')


        elif self.tabOption == self.tabGraveMaintenance:
            self.out( 'Seite 2')
            self.disableMenuItem('tabs')
            self.enableMenuItem('graveMaintenance')
           
            self.editAction = 'editGraveMaintenance'
            self.setTreeVisible(True)
            self.setStatusbarText([self.singleGrave.sStatus])

        elif self.tabOption == self.tabGraveSpring:
            self.out( 'Seite 2')
            self.disableMenuItem('tabs')
            self.enableMenuItem('graveSpring')
           
            self.editAction = 'editGraveSpring'
            self.setTreeVisible(True)
            self.setStatusbarText([self.singleGrave.sStatus])
            
        elif self.tabOption == self.tabGraveSummer:
            self.out( 'Seite 2')
            self.disableMenuItem('tabs')
            self.enableMenuItem('graveSummer')
           
            self.editAction = 'editGraveSummer'
            self.setTreeVisible(True)
            self.setStatusbarText([self.singleGrave.sStatus])   
            
            
            
        elif self.tabOption == self.tabGraveAutumn:
            self.out( 'Seite 2')
            self.disableMenuItem('tabs')
            self.enableMenuItem('graveAutumn')
           
            self.editAction = 'editGraveAutumn'
            self.setTreeVisible(True)
            self.setStatusbarText([self.singleGrave.sStatus])
        
        
        elif self.tabOption == self.tabGrave:
            self.out( 'Seite 2')
            self.disableMenuItem('tabs')
            self.enableMenuItem('grave')
           
            self.editAction = 'editGrave'
            self.setTreeVisible(True)
            self.setStatusbarText([self.singleGrave.sStatus])
    
    
        # refresh the Tree
        self.refreshTree()
        self.enableMenuItem(self.editAction)
        self.editEntries = FALSE
        