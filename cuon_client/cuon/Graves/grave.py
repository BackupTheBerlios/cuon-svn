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

    
        self.loadGlade('graves.xml', 'GraveMainwindow')

        self.setStatusBar()


        self.EntriesGraves = 'graves.xml'
        
        self.loadEntries(self.EntriesGraves)
        
        self.singleGrave.setEntries(self.getDataEntries(self.EntriesGraves) )
        self.singleGrave.setGladeXml(self.xml)
        self.singleGrave.setTreeFields( ['lastname', 'firstname'] )
        self.singleGrave.setStore( gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING,   gobject.TYPE_UINT) ) 
        self.singleGrave.setTreeOrder('lastname, firstname')
        self.singleGrave.setListHeader([_('Lastname'), _('Firstname'), _('City')])
        self.singleGrave.setTree(self.xml.get_widget('tree1') )

        self.EntriesGravesMaintenance = 'graves_maintenance.xml'
        
        self.loadEntries(self.EntriesGravesMaintenance)
        
        self.singleGraveMaintenance.setEntries(self.getDataEntries(self.EntriesGravesMaintenance) )
        self.singleGraveMaintenance.setGladeXml(self.xml)
        self.singleGraveMaintenance.setTreeFields( ['grave_service_id' ] )
        self.singleGraveMaintenance.setStore( gtk.ListStore(gobject.TYPE_UINT,  gobject.TYPE_UINT) ) 
        self.singleGraveMaintenance.setTreeOrder('grave_service_id')
        self.singleGraveMaintenance.setListHeader([_('Service-ID')])
        self.singleGraveMaintenance.setTree(self.xml.get_widget('tree1') )
        self.singleGraveMaintenance.sWhere  ='where grave_id = ' + `self.singleGrave.ID`
  

        # set values for comboBox

          

        # Menu-items
        self.initMenuItems()

        # Close Menus for Tab
        self.addEnabledMenuItems('tabs','grave1')
        self.addEnabledMenuItems('tabs','maintenance1')

               
        # seperate Menus
        self.addEnabledMenuItems('grave','grave1')
        self.addEnabledMenuItems('graveMaintenance','maintenance1')

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

    
        
       

        # tabs from notebook
        
        self.tabGrave = 0
        self.tabGraveMaintenance = 1
        
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


#Menu Schedul
        
   
    def on_SchedulSave_activate(self, event):
        self.out( "save Schedul addresses v2")
        self.singleSchedul.partnerId = self.singlePartner.ID
        self.singleSchedul.save()
        self.setEntriesEditable(self.EntriesPartnerSchedul, FALSE)
        self.tabChanged()

    def on_SchedulEdit1_activate(self, event):
        self.setEntriesEditable(self.EntriesPartnerSchedul, TRUE)
   
    def on_SchedulNew_activate(self, event):
        self.out( "new Schedul for partner v2")
        self.singleSchedul.newRecord()
        self.setEntriesEditable(self.EntriesPartnerSchedul, TRUE)

    def on_SchedulDelete_activate(self, event):
        self.out( "delete Schedul addresses v2")
        self.singleSchedul.deleteRecord()

    def on_gdeDate_date_changed(self, event ):
        print str(event)
        gdeSchedul = self.getWidget('gdeDate')
        newDate = gdeSchedul.get_time()
        print newDate
        
        
        
        

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
        
        if self.tabOption == self.tabGrave:
            self.singleGrave.connectTree()
            self.singleGrave.refreshTree()
       
        elif self.tabOption == self.tabGraveMaintenance:
            print "1 tree "
            self.singleGraveMaintenance.sWhere  ='where grave_id = ' + `int(self.singleGrave.ID)`
            self.singleGraveMaintenance.connectTree()
            self.singleGraveMaintenance.refreshTree()
        
     


         
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


        # refresh the Tree
        self.refreshTree()
        self.enableMenuItem(self.editAction)
        self.editEntries = FALSE
        
