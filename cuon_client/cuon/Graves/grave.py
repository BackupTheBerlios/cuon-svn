# -*- coding: utf-8 -*-

##Copyright (C) [2005 - 2009]  [Jürgen Hamel, D-32584 Löhne]

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
#from gtk import True, False
import string
import logging
import SingleGrave
import SingleGraveMaintenance
import SingleGraveSpring
import SingleGraveSummer
import SingleGraveAutumn
import SingleGraveWinter
import SingleGraveHoliday
import SingleGraveYear
import SingleGraveServiceNotes
import SingleGraveSingleevent
import SingleGraveInvoices
import SingleGraveyard
import cuon.Addresses.addresses
import cuon.Addresses.SingleAddress
import cuon.PrefsFinance.prefsFinance
import cuon.PrefsFinance.SinglePrefsFinanceTop
import cuon.Misc.messages

from cuon.Windows.chooseWindows  import chooseWindows
import cPickle
#import cuon.OpenOffice.letter
# localisation
import locale, gettext
locale.setlocale (locale.LC_NUMERIC, '')
#import threading
import mx.DateTime
import graveyard
from cuon.Articles.ArticlesFastSelection import  ArticlesFastSelection
import cuon.Articles.SingleArticle
import cuon.Articles.articles
import plant_lists

class graveswindow(chooseWindows, ArticlesFastSelection):

    
    def __init__(self, allTables,  graveyardid=0, graveid=0,  addressid= 0, newGrave = False):

        chooseWindows.__init__(self)
        ArticlesFastSelection.__init__(self)
          
        self.allTables = allTables
        self.graveyardID = graveyardid
        self.graveID = graveid
        self.addressID = addressid
        self.pressedTypeOfInvoice = 0
        self.ModulNumber = self.MN['Grave']
        self.singleGrave = SingleGrave.SingleGrave(allTables)
        self.singleGraveMaintenance = SingleGraveMaintenance.SingleGraveMaintenance(allTables)
        self.singleGraveSpring = SingleGraveSpring.SingleGraveSpring(allTables)
        self.singleGraveSummer = SingleGraveSummer.SingleGraveSummer(allTables)
        self.singleGraveAutumn = SingleGraveAutumn.SingleGraveAutumn(allTables)
        self.singleGraveWinter = SingleGraveWinter.SingleGraveWinter(allTables)
        self.singleGraveHolidays = SingleGraveHoliday.SingleGraveHoliday(allTables)
        self.singleGraveAnnual = SingleGraveYear.SingleGraveYear(allTables)
        self.singleGraveServiceNotes = SingleGraveServiceNotes.SingleGraveServiceNotes(allTables)
        self.singleGraveUnique = SingleGraveSingleevent.SingleGraveSingleevent(allTables)
        self.singleGraveInvoices = SingleGraveInvoices.SingleGraveInvoices(allTables)
        self.singleGraveyard = SingleGraveyard.SingleGraveyard(allTables)
        self.singleAddress = cuon.Addresses.SingleAddress.SingleAddress(allTables)
        self.singlePrefsFinanceTop = cuon.PrefsFinance.SinglePrefsFinanceTop.SinglePrefsFinanceTop(allTables)
        self.fillArticlesNewID = 0
        self.singleArticle = cuon.Articles.SingleArticle.SingleArticle(allTables)
        print "load glade"
        self.loadGlade('graves.xml', 'GravesMainwindow')
        print "start fast selection"
        self.FastSelectionStart()
        self.setStatusBar()


        self.EntriesGraves = 'graves.xml'
        
        self.loadEntries(self.EntriesGraves)
        
        self.singleGrave.setEntries(self.getDataEntries(self.EntriesGraves) )
        self.singleGrave.setGladeXml(self.xml)
        self.singleGrave.setTreeFields( ['lastname', 'firstname', 'pos_number'] )
        self.singleGrave.setStore( gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING,   gobject.TYPE_UINT,   gobject.TYPE_UINT) ) 
        self.singleGrave.setTreeOrder('lastname, firstname')
        self.singleGrave.setListHeader([_('Lastname'), _('Firstname'), _('Serial Number')])
        self.singleGrave.setTree(self.getWidget('tree1') )

        self.EntriesGravesInvoices = 'graves_invoice_info.xml'
        
        self.loadEntries(self.EntriesGravesInvoices)
        
        self.singleGraveInvoices.setEntries(self.getDataEntries(self.EntriesGravesInvoices) )
        self.singleGraveInvoices.setGladeXml(self.xml)
        self.singleGraveInvoices.setTreeFields( ['address.lastname as lastname', 'address.firstname as firstname'  ] )
        self.singleGraveInvoices.setStore( gtk.ListStore( gobject.TYPE_STRING,  gobject.TYPE_STRING ,   gobject.TYPE_UINT)  )
        self.singleGraveInvoices.setTreeOrder('lastname')
        self.singleGraveInvoices.setListHeader([_('Lastname'), _('Firstname') ])
        self.singleGraveInvoices.setTree(self.getWidget('tree1') )
        self.singleGraveInvoices.sWhere  ='where grave_id = ' + `self.singleGrave.ID`+ ' and address_id = address.id '
  


        self.EntriesGravesMaintenance = 'graves_maintenance.xml'
        
        self.loadEntries(self.EntriesGravesMaintenance)
        
        self.singleGraveMaintenance.setEntries(self.getDataEntries(self.EntriesGravesMaintenance) )
        self.singleGraveMaintenance.setGladeXml(self.xml)
        self.singleGraveMaintenance.setTreeFields( ['article_id', 'grave_service_id' ] )
        self.singleGraveMaintenance.setStore( gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_INT,  gobject.TYPE_UINT) ) 
        self.singleGraveMaintenance.setTreeOrder('id desc')
        self.singleGraveMaintenance.setListHeader([_('Article-ID'),  _('Service-ID')])
        self.singleGraveMaintenance.setTree(self.getWidget('tree1') )
        self.singleGraveMaintenance.sWhere  ='where grave_id = ' + `self.singleGrave.ID`
  
  
  
  
  
        self.EntriesGravesSpring = 'graves_spring.xml'
        
        self.loadEntries(self.EntriesGravesSpring)
        
        self.singleGraveSpring.setEntries(self.getDataEntries(self.EntriesGravesSpring) )
        self.singleGraveSpring.setGladeXml(self.xml)
        self.singleGraveSpring.setTreeFields( ['service_count', 'articles.number as number', 'articles.designation as designation',  'article_id'   ] )
        self.singleGraveSpring.setStore( gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_STRING,  gobject.TYPE_STRING,gobject.TYPE_STRING, gobject.TYPE_UINT) ) 
        self.singleGraveSpring.setTreeOrder('article_id')
        self.singleGraveSpring.setListHeader([_('count'), _('number'), _('Designation'), _('article-ID')])
        self.singleGraveSpring.setTree(self.getWidget('tree1') )
        self.singleGraveSpring.sWhere  ='where grave_id = ' + `self.singleGrave.ID`+ ' and article_id = articles.id '
  
        self.EntriesGravesSummer = 'graves_summer.xml'
        self.loadEntries(self.EntriesGravesSummer)
        
        
        self.singleGraveSummer.setEntries(self.getDataEntries(self.EntriesGravesSummer) )
        self.singleGraveSummer.setGladeXml(self.xml)
        self.singleGraveSummer.setTreeFields( ['service_count', 'articles.number as number', 'articles.designation as designation',  'article_id'   ] )
        self.singleGraveSummer.setStore( gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_STRING,  gobject.TYPE_STRING,gobject.TYPE_STRING, gobject.TYPE_UINT) ) 
        self.singleGraveSummer.setTreeOrder('article_id')
        self.singleGraveSummer.setListHeader([_('count'), _('number'), _('Designation'), _('article-ID')])
        self.singleGraveSummer.setTree(self.getWidget('tree1') )
        self.singleGraveSummer.sWhere  ='where grave_id = ' + `self.singleGrave.ID`+ ' and article_id = articles.id '
  
  
        self.EntriesGravesAutumn = 'graves_autumn.xml'
        
        self.loadEntries(self.EntriesGravesAutumn)
        
        self.singleGraveAutumn.setEntries(self.getDataEntries(self.EntriesGravesAutumn) )
        self.singleGraveAutumn.setGladeXml(self.xml)
        self.singleGraveAutumn.setTreeFields( ['service_count', 'articles.number as number', 'articles.designation as designation',  'article_id'   ] )
        self.singleGraveAutumn.setStore( gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_STRING,  gobject.TYPE_STRING,gobject.TYPE_STRING, gobject.TYPE_UINT) ) 
        self.singleGraveAutumn.setTreeOrder('article_id')
        self.singleGraveSpring.setListHeader([_('count'), _('number'), _('Designation'), _('article-ID')])
        self.singleGraveAutumn.setTree(self.getWidget('tree1') )
        self.singleGraveAutumn.sWhere  ='where grave_id = ' + `self.singleGrave.ID`+ ' and article_id = articles.id '
  
        self.EntriesGravesWinter = 'graves_winter.xml'
        
        self.loadEntries(self.EntriesGravesWinter)
        
        self.singleGraveWinter.setEntries(self.getDataEntries(self.EntriesGravesWinter) )
        self.singleGraveWinter.setGladeXml(self.xml)
        self.singleGraveWinter.setTreeFields( ['service_count', 'articles.number as number', 'articles.designation as designation',  'article_id'   ] )
        self.singleGraveWinter.setStore( gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_STRING,  gobject.TYPE_STRING,gobject.TYPE_STRING, gobject.TYPE_UINT) ) 
        self.singleGraveWinter.setTreeOrder('article_id')
        self.singleGraveWinter.setListHeader([_('count'), _('number'), _('Designation'), _('article-ID')])
        self.singleGraveWinter.setTree(self.getWidget('tree1') )
        self.singleGraveWinter.sWhere  ='where grave_id = ' + `self.singleGrave.ID` + ' and article_id = articles.id '
  
  
        self.EntriesGravesHolidays = 'graves_holiday.xml'
        
        self.loadEntries(self.EntriesGravesHolidays)
       
        self.singleGraveHolidays.setEntries(self.getDataEntries(self.EntriesGravesHolidays) )
        self.singleGraveHolidays.setGladeXml(self.xml)
        self.singleGraveHolidays.setTreeFields( ['service_count', 'articles.number as number', 'articles.designation as designation',  'article_id'   ] )
        self.singleGraveHolidays.setStore( gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_STRING,  gobject.TYPE_STRING,gobject.TYPE_STRING, gobject.TYPE_UINT) ) 
        self.singleGraveHolidays.setTreeOrder('article_id')
        self.singleGraveHolidays.setListHeader([_('count'), _('number'), _('Designation'), _('article-ID')])
        self.singleGraveHolidays.setTree(self.getWidget('tree1') )
        self.singleGraveHolidays.sWhere  ='where grave_id = ' + `self.singleGrave.ID`+ ' and article_id = articles.id '
  
        
        self.EntriesGravesAnnual = 'graves_year.xml'
        
        self.loadEntries(self.EntriesGravesAnnual)     
        self.singleGraveAnnual.setEntries(self.getDataEntries(self.EntriesGravesAnnual) )
        self.singleGraveAnnual.setGladeXml(self.xml)
        self.singleGraveAnnual.setTreeFields( ['service_count', 'articles.number as number', 'articles.designation as designation',  'article_id'   ] )
        self.singleGraveAnnual.setStore( gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_STRING,  gobject.TYPE_STRING,gobject.TYPE_STRING, gobject.TYPE_UINT) ) 
        self.singleGraveAnnual.setTreeOrder('article_id')
        self.singleGraveAnnual.setListHeader([_('count'), _('number'), _('Designation'), _('article-ID')])
        self.singleGraveAnnual.setTree(self.getWidget('tree1') )
        self.singleGraveAnnual.sWhere  ='where grave_id = ' + `self.singleGrave.ID`+ ' and article_id = articles.id '
  
                
        
        self.EntriesGravesUnique = 'graves_single.xml'
        
        self.loadEntries(self.EntriesGravesUnique)
            
        self.singleGraveUnique.setEntries(self.getDataEntries(self.EntriesGravesUnique) )
        self.singleGraveUnique.setGladeXml(self.xml)
        self.singleGraveUnique.setTreeFields( ['service_count', 'articles.number as number', 'articles.designation as designation',  'article_id'   ] )
        self.singleGraveUnique.setStore( gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_STRING,  gobject.TYPE_STRING,gobject.TYPE_STRING, gobject.TYPE_UINT) ) 
        self.singleGraveUnique.setTreeOrder('article_id')
        self.singleGraveUnique.setListHeader([_('count'), _('number'), _('Designation'), _('article-ID')])
        self.singleGraveUnique.setTree(self.getWidget('tree1') )
        self.singleGraveUnique.sWhere  ='where grave_id = ' + `self.singleGrave.ID`+ ' and article_id = articles.id '
  
       
        # set values for comboBox

        liTabItem,  liTypeOfGrave, liTypeOfPaid, liPercent,  liPeriodSpring, liPeriodSummer, liPeriodAutumn, liPeriodWinter, liPeriodHolliday, liPeriodUnique, liPeriodYearly,  liSorting = self.rpc.callRP('Grave.getComboBoxEntries',self.dicUser)
        
        print   liTypeOfGrave, liTypeOfPaid, liPercent
        print liPeriodSpring, liPeriodSummer, liPeriodAutumn, liPeriodWinter, liPeriodHolliday, liPeriodUnique, liPeriodYearly
        
       
        
        cbTypeOfGrave = self.getWidget('cbTypeOfGrave')
        if cbTypeOfGrave:
            liststore = gtk.ListStore(str)
            for TypeOfGrave in liTypeOfGrave:
                liststore.append([TypeOfGrave])
            cbTypeOfGrave.set_model(liststore)
            cbTypeOfGrave.set_text_column(0)
            cbTypeOfGrave.show()

        #same for the find field 
        cbFindTypeOfGrave = self.getWidget('cbFindTypeOfGrave')
        if cbFindTypeOfGrave:
            liststore = gtk.ListStore(str)
            for TypeOfGrave in liTypeOfGrave:
                liststore.append([TypeOfGrave])
            cbFindTypeOfGrave.set_model(liststore)
            cbFindTypeOfGrave.set_text_column(0)
            cbFindTypeOfGrave.show()
            
            
            
        cbTypeOfPaid = self.getWidget('cbTypeOfPaid')
        if cbTypeOfPaid:
            liststore = gtk.ListStore(str)
            for TypeOfPaid in liTypeOfPaid:
                liststore.append([TypeOfPaid])
            cbTypeOfPaid.set_model(liststore)
            cbTypeOfPaid.set_text_column(0)
            cbTypeOfPaid.show()
        
        #same for the find field
        cbFindTypeOfPaid = self.getWidget('cbFindTypeOfPaid')
        if cbFindTypeOfPaid:
            liststore = gtk.ListStore(str)
            for TypeOfPaid in liTypeOfPaid:
                liststore.append([TypeOfPaid])
            cbFindTypeOfPaid.set_model(liststore)
            cbFindTypeOfPaid.set_text_column(0)
            cbFindTypeOfPaid.show()
            
        # same for choose paid 
        
        cbChooseTypeOfPaid = self.getWidget('cbChooseTypeOfPaid')
        if cbChooseTypeOfPaid:
            liststore = gtk.ListStore(str)
            for TypeOfPaid in liTypeOfPaid:
                liststore.append([TypeOfPaid])
            cbChooseTypeOfPaid.set_model(liststore)
            cbChooseTypeOfPaid.set_text_column(0)
            cbChooseTypeOfPaid.show()
            
        cbPercent = self.getWidget('cbPercent')
        if cbPercent:
            liststore = gtk.ListStore(str)
            for Percent in liPercent:
                liststore.append([Percent])
            cbPercent.set_model(liststore)
            cbPercent.set_text_column(0)
            cbPercent.show()
        print 'percent'
        cbPeriodSpring = self.getWidget('cbSpringPeriod')
        if cbPeriodSpring:
            liststore = gtk.ListStore(str)
            for PeriodSpring in liPeriodSpring:
                liststore.append([PeriodSpring])
            cbPeriodSpring.set_model(liststore)
            cbPeriodSpring.set_text_column(0)
            cbPeriodSpring.show()
        print 'Spring'
        
        cbPeriodSummer = self.getWidget('cbSummerPeriod')
        if cbPeriodSummer:
            liststore = gtk.ListStore(str)
            for PeriodSummer in liPeriodSummer:
                liststore.append([PeriodSummer])
            cbPeriodSummer.set_model(liststore)
            cbPeriodSummer.set_text_column(0)
            cbPeriodSummer.show()
        print 'Summer'
        
        cbPeriodAutumn = self.getWidget('cbAutumnPeriod')
        print 'Autumn',  cbPeriodAutumn
        if cbPeriodAutumn:
            print 'liPeriodAutumn',  liPeriodAutumn
            liststore = gtk.ListStore(str)
            for PeriodAutumn in liPeriodAutumn:
                liststore.append([PeriodAutumn])
            cbPeriodAutumn.set_model(liststore)
            cbPeriodAutumn.set_text_column(0)
            cbPeriodAutumn.show()
        print 'Autumn'
        
        cbPeriodWinter = self.getWidget('cbWinterPeriod')
        if cbPeriodWinter:
            liststore = gtk.ListStore(str)
            for PeriodWinter in liPeriodWinter:
                liststore.append([PeriodWinter])
            cbPeriodWinter.set_model(liststore)
            cbPeriodWinter.set_text_column(0)
            cbPeriodWinter.show()
        print 'Winter'
        cbPeriodHolliday = self.getWidget('cbHolidaysPeriod')
        if cbPeriodHolliday:
            liststore = gtk.ListStore(str)
            for PeriodHolliday in liPeriodHolliday:
                liststore.append([PeriodHolliday])
            cbPeriodHolliday.set_model(liststore)
            cbPeriodHolliday.set_text_column(0)
            cbPeriodHolliday.show()
        print 'Holliday'
        
        cbPeriodUnique = self.getWidget('cbUniquePeriod')
        if cbPeriodUnique:
            liststore = gtk.ListStore(str)
            for PeriodUnique in liPeriodUnique:
                liststore.append([PeriodUnique])
            cbPeriodUnique.set_model(liststore)
            cbPeriodUnique.set_text_column(0)
            cbPeriodUnique.show()
        print 'Unique'
        cbPeriodYearly = self.getWidget('cbYearlyPeriod')
        if cbPeriodYearly:
            liststore = gtk.ListStore(str)
            for PeriodYearly in liPeriodYearly:
                liststore.append([PeriodYearly])
            cbPeriodYearly.set_model(liststore)
            cbPeriodYearly.set_text_column(0)
            cbPeriodYearly.show()

        print 'Yearly'
        
        liGraveYard = self.rpc.callRP('Grave.getComboGraveyards',self.dicUser)
        cbGraveYard = self.getWidget('cbFindGraveyard')
        if cbGraveYard:
            liststore = gtk.ListStore(str)
            for GraveYard in liGraveYard:
                liststore.append([GraveYard])
            cbGraveYard.set_model(liststore)
            cbGraveYard.set_text_column(0)
            cbGraveYard.show()
            
        print 'Graveyard'
        # Menu-items
        self.initMenuItems()

        # Close Menus for Tab
        self.addEnabledMenuItems('tabs','grave1')
        self.addEnabledMenuItems('tabs','maintenance1')
        self.addEnabledMenuItems('tabs','invoices')
        self.addEnabledMenuItems('tabs','spring')
        self.addEnabledMenuItems('tabs','summer')
        self.addEnabledMenuItems('tabs','autumn')
        self.addEnabledMenuItems('tabs','winter')
        self.addEnabledMenuItems('tabs','holidays')
        self.addEnabledMenuItems('tabs','unique')
        self.addEnabledMenuItems('tabs','annual')
           
        # seperate Menus
        self.addEnabledMenuItems('grave','grave1')
        self.addEnabledMenuItems('graveMaintenance','maintenance1')
        self.addEnabledMenuItems('graveInvoice','invoices')
        self.addEnabledMenuItems('graveSpring','spring')
        self.addEnabledMenuItems('graveSummer','summer')
        self.addEnabledMenuItems('graveAutumn','autumn')
        self.addEnabledMenuItems('graveWinter','winter')
        self.addEnabledMenuItems('graveHolidays','holidays')
        self.addEnabledMenuItems('graveUnique','unique')
        self.addEnabledMenuItems('graveAnnual','annual')
        
        # enabledMenues for grave
        self.addEnabledMenuItems('editGrave','new1', self.dicUserKeys['grave_new'])
        self.addEnabledMenuItems('editGrave','clear1', self.dicUserKeys['grave_delete'])
        self.addEnabledMenuItems('editGrave','print1', self.dicUserKeys['grave_print'])
        self.addEnabledMenuItems('editGrave','edit1', self.dicUserKeys['grave_edit'])
 # enabledMenues for graveMaintenance
        self.addEnabledMenuItems('editGraveMaintenance','MaintenanceNew1')
        self.addEnabledMenuItems('editGraveMaintenance','MaintenanceClear1')
        self.addEnabledMenuItems('editGraveMaintenance','MaintenancePrint1')
        self.addEnabledMenuItems('editGraveMaintenance','MaintenanceEdit1')

    # enabledMenues for graveInvoice
        self.addEnabledMenuItems('editGraveInvoice','InvoicesNew1', self.dicUserKeys['graveSpring_new'])
        self.addEnabledMenuItems('editGraveInvoice','InvoicesClear1', self.dicUserKeys['graveSpring_delete'])
        #self.addEnabledMenuItems('editGraveSpring','SpringPrint1', self.dicUserKeys['graveSpring_print'])
        self.addEnabledMenuItems('editGraveInvoice','InvoicesEdit1', self.dicUserKeys['graveSpring_edit'])

    # enabledMenues for graveSpring
        self.addEnabledMenuItems('editGraveSpring','SpringNew1', self.dicUserKeys['graveSpring_new'])
        self.addEnabledMenuItems('editGraveSpring','SpringClear1', self.dicUserKeys['graveSpring_delete'])
        #self.addEnabledMenuItems('editGraveSpring','SpringPrint1', self.dicUserKeys['graveSpring_print'])
        self.addEnabledMenuItems('editGraveSpring','SpringEdit1', self.dicUserKeys['graveSpring_edit'])

    # enabledMenues for graveSummer
        self.addEnabledMenuItems('editGraveSummer','SummerNew1', self.dicUserKeys['graveSummer_new'])
        self.addEnabledMenuItems('editGraveSummer','SummerClear1', self.dicUserKeys['graveSummer_delete'])
        #self.addEnabledMenuItems('editGraveSummer','SummerPrint1', self.dicUserKeys['graveSummer_print'])
        self.addEnabledMenuItems('editGraveSummer','SummerEdit1', self.dicUserKeys['graveSummer_edit'])
# enabledMenues for graveAutumn
        self.addEnabledMenuItems('editGraveAutumn','AutumnNew1', self.dicUserKeys['graveAutumn_new'])
        self.addEnabledMenuItems('editGraveAutumn','AutumnClear1', self.dicUserKeys['graveAutumn_delete'])
        #self.addEnabledMenuItems('editGraveAutumn','AutumnPrint1', self.dicUserKeys['graveAutumn_print'])
        self.addEnabledMenuItems('editGraveAutumn','AutumnEdit1', self.dicUserKeys['graveAutumn_edit'])
# enabledMenues for graveWinter
        self.addEnabledMenuItems('editGraveWinter','WinterNew1', self.dicUserKeys['graveWinter_new'])
        self.addEnabledMenuItems('editGraveWinter','WinterClear1', self.dicUserKeys['graveWinter_delete'])
        #self.addEnabledMenuItems('editGraveWinter','WinterPrint1', self.dicUserKeys['graveWinter_print'])
        self.addEnabledMenuItems('editGraveWinter','WinterEdit1', self.dicUserKeys['graveWinter_edit'])

       # enabledMenues for graveHolidays
        self.addEnabledMenuItems('editGraveHolidays','HolidaysNew1', self.dicUserKeys['graveHolidays_new'])
        self.addEnabledMenuItems('editGraveHolidays','HolidaysClear1', self.dicUserKeys['graveHolidays_delete'])
        #self.addEnabledMenuItems('editGraveHolidays','HolidaysPrint1', self.dicUserKeys['graveHolidays_print'])
        self.addEnabledMenuItems('editGraveHolidays','HolidaysEdit1', self.dicUserKeys['graveHolidays_edit'])
 # enabledMenues for graveUnique
        self.addEnabledMenuItems('editGraveUnique','UniqueNew1', self.dicUserKeys['graveUnique_new'])
        self.addEnabledMenuItems('editGraveUnique','UniqueClear1', self.dicUserKeys['graveUnique_delete'])
        #self.addEnabledMenuItems('editGraveUnique','UniquePrint1', self.dicUserKeys['graveUnique_print'])
        self.addEnabledMenuItems('editGraveUnique','UniqueEdit1', self.dicUserKeys['graveUnique_edit'])
# enabledMenues for graveAnnual
        self.addEnabledMenuItems('editGraveAnnual','AnnualNew1', self.dicUserKeys['graveAnnual_new'])
        self.addEnabledMenuItems('editGraveAnnual','AnnualClear1', self.dicUserKeys['graveAnnual_delete'])
        #self.addEnabledMenuItems('editGraveAnnual','AnnualPrint1', self.dicUserKeys['graveAnnual_print'])
        self.addEnabledMenuItems('editGraveAnnual','AnnualEdit1', self.dicUserKeys['graveAnnual_edit'])

 

    # enabledMenues for Save 
        self.addEnabledMenuItems('editSave','save1', self.dicUserKeys['address_save'])
        self.addEnabledMenuItems('editSave','InvoicesSave1', self.dicUserKeys['address_save'])
        self.addEnabledMenuItems('editSave','MaintenanceSave1', self.dicUserKeys['address_save'])
        self.addEnabledMenuItems('editSave','SpringSave1', self.dicUserKeys['address_save'])
        self.addEnabledMenuItems('editSave','SummerSave1', self.dicUserKeys['address_save'])
        self.addEnabledMenuItems('editSave','AutumnSave1', self.dicUserKeys['address_save'])
        self.addEnabledMenuItems('editSave','WinterSave1', self.dicUserKeys['address_save'])
        self.addEnabledMenuItems('editSave','HolidaysSave1', self.dicUserKeys['address_save'])
        self.addEnabledMenuItems('editSave','UniqueSave1', self.dicUserKeys['address_save'])
        self.addEnabledMenuItems('editSave','AnnualSave1', self.dicUserKeys['address_save'])
        # tabs from notebook
        print 'Menus enabled'
        self.tabGrave = 0
        self.tabGraveInvoice = 1
        self.tabGraveMaintenance = 2
        self.tabGraveSpring = 3
        self.tabGraveSummer= 4
        self.tabGraveAutumn = 5
        self.tabGraveHollidays = 6
        self.tabGraveWinter = 7
        self.tabGraveAnnual = 8
        self.tabGraveUnique = 9
        
        


        try:
            self.win1.add_accel_group(self.accel_group)
        except Exception,  params:
            print Exception,  params
            

        if newGrave:
            # create a new grave
            self.dicGrave = {'addressid':self.addressID}
            newID = self.rpc.callRP('Grave.createNewGrave', self.dicUser,self.dicGrave)
        elif self.addressID > 0:
            self.singleGrave.sWhere = " where addressid = " + `self.addressID`
            
        
        print 'now tab changed'
        self.tabChanged()
        

    #Menu File
              
    def on_quit1_activate(self, event):
        self.out( "exit clients V1")
        self.closeWindow() 
    
        


    #Menu Grave
  
    def on_save1_activate(self, event):
        self.out( "save grave v2")
        self.singleGrave.save()
        self.setEntriesEditable(self.EntriesGraves, False)
        self.tabChanged()
        
    def on_new1_activate(self, event):
        self.out( "new grave v2")
        self.singleGrave.newRecord()
        print self.singleGrave.ID
        
        self.setEntriesEditable(self.EntriesGraves, True)

    def on_edit1_activate(self, event):
        self.out( "edit grave v2")
        self.setEntriesEditable(self.EntriesGraves, True)

        # sub menu lists
    def on_plant_lists_activate(self, event):
        pl = plant_lists.plantlists()

    def on_clear1_activate(self, event):
        self.out( "delete grave v2")
        self.singleGrave.deleteRecord()


    def on_calcPrices_activate(self,  event):
        print 'calc all prices'
        wMessage = cuon.Misc.messages.messages()
        if wMessage.QuestionMsg('Would you really calc all Prices ???') == True:
            bOK = self.rpc.callRP('Grave.calcAllPrices',self.dicUser )
            print 'calc all prices = ',  bOK

        else:
            print 'cancel calc prices '
   #Menu Invoice Info
        
   
    def on_InvoicesSave1_activate(self, event):
        self.out( "save GraveInvoices addresses v2")
        print "Grave invoices save"
        self.singleGraveInvoices.graveID = self.singleGrave.ID
        self.singleGraveInvoices.singleGrave = self.singleGrave
        self.singleGraveInvoices.save()
        self.setEntriesEditable(self.EntriesGravesInvoices, False)
        self.setEntriesEditable(self.EntriesGraves, False)
        self.tabChanged()
        
    def on_InvoicesNew1_activate(self, event):
        self.out( "new GraveInvoices addresses v2")
        self.singleGraveInvoices.newRecord()
        self.setEntriesEditable(self.EntriesGravesInvoices, True)
        self.setEntriesEditable(self.EntriesGraves, True)
        
    def on_InvoicesEdit1_activate(self, event):
        self.setEntriesEditable(self.EntriesGravesInvoices, True)
        self.setEntriesEditable(self.EntriesGraves, True)

    def on_InvoicesClear1_activate(self, event):
        self.out( "delete GraveInvoices addresses v2")
        self.singleGraveInvoices.deleteRecord()


  #Menu maintenance
        
   
    def on_MaintenanceSave1_activate(self, event):
        self.out( "save GraveMaintenance addresses v2")
        
       
        # set the price from a pricegroup if no price is setting
        # modul,artikelwidget,pricewidget,singleID
        self.setArticlePrice('grave','eServiceArticleID', 'eServicePrice',  self.singleGrave.ID)
        
        
        self.singleGraveMaintenance.graveID = self.singleGrave.ID
        self.singleGraveMaintenance.graveServiceID =  self.MN['GraveServiceNotesService'] 
        self.singleGraveMaintenance.singleGrave = self.singleGrave
        self.singleGraveMaintenance.save()
        
        
        
        self.singleGraveServiceNotes.graveID = self.singleGrave.ID
        self.singleGraveServiceNotes.graveServiceID =  self.MN['GraveServiceNotesService'] 
        self.singleGraveServiceNotes.save()
        
        
        self.setEntriesEditable(self.EntriesGravesMaintenance, False)
        self.tabChanged()
        
    def on_MaintenanceNew1_activate(self, event):
        self.out( "new GraveMaintenance addresses v2")
        self.singleGraveMaintenance.newRecord()
        self.setEntriesEditable(self.EntriesGravesMaintenance, True)

        
    def on_MaintenanceEdit1_activate(self, event):
        self.setEntriesEditable(self.EntriesGravesMaintenance, True)


    def on_MaintenanceClear1_activate(self, event):
        self.out( "delete GraveMaintenance addresses v2")
        self.singleGraveMaintenance.deleteRecord()

#Menu Spring
        
   
    def on_SpringSave1_activate(self, event):
        self.out( "save GraveSpring addresses v2")
        
         # set the price from a pricegroup if no price is setting
        self.setArticlePrice('grave','eSpringArticleID', 'eSpringPrice',  self.singleGrave.ID)
       

        self.singleGraveSpring.graveID = self.singleGrave.ID
        self.singleGraveSpring.graveServiceID =  self.MN['GraveServiceNotesSpring'] 
        self.singleGraveSpring.singleGrave = self.singleGrave
        self.singleGraveSpring.save()
        
        self.singleGraveServiceNotes.graveID = self.singleGrave.ID
        self.singleGraveServiceNotes.graveServiceID =  self.MN['GraveServiceNotesSpring'] 
        self.singleGraveServiceNotes.save()
        
        self.setEntriesEditable(self.EntriesGravesSpring, False)
        self.setEntriesEditable(self.EntriesGraves, False)
        self.tabChanged()
        
    def on_SpringNew1_activate(self, event):
        self.out( "new GraveSpring addresses v2")
        self.singleGraveSpring.newRecord()
        self.setEntriesEditable(self.EntriesGravesSpring, True)
        self.setEntriesEditable(self.EntriesGraves, True)
        
    def on_SpringEdit1_activate(self, event):
        self.setEntriesEditable(self.EntriesGravesSpring, True)
        self.setEntriesEditable(self.EntriesGraves, True)

    def on_SpringClear1_activate(self, event):
        self.out( "delete GraveSpring addresses v2")
        self.singleGraveSpring.deleteRecord()



        #Menu Summer
        
   
    def on_SummerSave1_activate(self, event):
        self.out( "save GraveSummer addresses v2")
        
          # set the price from a pricegroup if no price is setting
        self.setArticlePrice('grave','eSummerArticleID', 'eSummerPrice',  self.singleGrave.ID)
        
      
      
        
        self.singleGraveSummer.graveID = self.singleGrave.ID
        self.singleGraveSummer.graveServiceID =  self.MN['GraveServiceNotesSummer'] 
        self.singleGraveSummer.singleGrave = self.singleGrave
        self.singleGraveSummer.save()
        
        self.singleGraveServiceNotes.graveID = self.singleGrave.ID
        self.singleGraveServiceNotes.graveServiceID =  self.MN['GraveServiceNotesSummer'] 
        self.singleGraveServiceNotes.save()
        
        
        self.setEntriesEditable(self.EntriesGravesSummer, False)
        self.setEntriesEditable(self.EntriesGraves, False)
        self.tabChanged()
        
        
    def on_SummerNew1_activate(self, event):
        self.out( "new GraveSummer addresses v2")
        self.singleGraveSummer.newRecord()
        self.setEntriesEditable(self.EntriesGravesSummer, True)
        self.setEntriesEditable(self.EntriesGraves, True)
        
    def on_SummerEdit1_activate(self, event):
        self.setEntriesEditable(self.EntriesGravesSummer, True)
        self.setEntriesEditable(self.EntriesGraves, True)

    def on_SummerClear1_activate(self, event):
        self.out( "delete GraveSummer addresses v2")
        self.singleGraveSummer.deleteRecord()



        
        #Menu Autumn
        
   
    def on_AutumnSave1_activate(self, event):
        
        
          # set the price from a pricegroup if no price is setting
        self.setArticlePrice('grave','eAutumnArticleID', 'eAutumnPrice',  self.singleGrave.ID)


        self.singleGraveAutumn.graveID = self.singleGrave.ID
        self.singleGraveAutumn.graveServiceID =  self.MN['GraveServiceNotesAutumn'] 
        self.singleGraveAutumn.singleGrave = self.singleGrave
        self.singleGraveAutumn.save()
        
        self.singleGraveServiceNotes.graveID = self.singleGrave.ID
        self.singleGraveServiceNotes.graveServiceID =  self.MN['GraveServiceNotesAutumn'] 
        self.singleGraveServiceNotes.save()
        
        
        self.setEntriesEditable(self.EntriesGravesAutumn, False)
        self.setEntriesEditable(self.EntriesGraves, False)
        self.tabChanged()
        
    def on_AutumnNew1_activate(self, event):
        print  "new GraveAutumn addresses v2"
        self.singleGraveAutumn.newRecord()
        self.setEntriesEditable(self.EntriesGravesAutumn, True)
        self.setEntriesEditable(self.EntriesGraves, True)
        
    def on_AutumnEdit1_activate(self, event):
        self.setEntriesEditable(self.EntriesGravesAutumn, True)
        self.setEntriesEditable(self.EntriesGraves, True)

    def on_AutumnClear1_activate(self, event):
        self.out( "delete GraveAutumn addresses v2")
        self.singleGraveAutumn.deleteRecord()

        #Menu Winter
        
   
    def on_WinterSave1_activate(self, event):
        self.out( "save GraveWinter addresses v2")
        
          # set the price from a pricegroup if no price is setting
        self.setArticlePrice('grave','eWinterArticleID', 'eWinterPrice',  self.singleGrave.ID)
    

        self.singleGraveWinter.graveID = self.singleGrave.ID
        self.singleGraveWinter.graveServiceID =  self.MN['GraveServiceNotesWinter'] 
        self.singleGraveWinter.singleGrave = self.singleGrave
        self.singleGraveWinter.save()
        
        self.singleGraveServiceNotes.graveID = self.singleGrave.ID
        self.singleGraveServiceNotes.graveServiceID =  self.MN['GraveServiceNotesWinter'] 
        self.singleGraveServiceNotes.save()
        
        self.setEntriesEditable(self.EntriesGravesWinter, False)
        self.setEntriesEditable(self.EntriesGraves, False)
        self.tabChanged()
        
    def on_WinterNew1_activate(self, event):
        self.out( "new GraveWinter addresses v2")
        self.singleGraveWinter.newRecord()
        self.setEntriesEditable(self.EntriesGravesWinter, True)
        self.setEntriesEditable(self.EntriesGraves, True)
        
    def on_WinterEdit1_activate(self, event):
        self.setEntriesEditable(self.EntriesGravesWinter, True)
        self.setEntriesEditable(self.EntriesGraves, True)

    def on_WinterClear1_activate(self, event):
        self.out( "delete GraveWinter addresses v2")
        self.singleGraveWinter.deleteRecord()

        
        
    #Menu Holidays
        
   
    def on_HolidaysSave1_activate(self, event):
        print "save GraveHolidays addresses v2"
        
          # set the price from a pricegroup if no price is setting
        self.setArticlePrice('grave','eHolidaysArticleID', 'eHolidaysPrice',  self.singleGrave.ID)
       

        self.singleGraveHolidays.graveID = self.singleGrave.ID
        self.singleGraveHolidays.graveServiceID =  self.MN['GraveServiceNotesHolliday'] 
        self.singleGraveHolidays.singleGrave = self.singleGrave
        self.singleGraveHolidays.save()
        
        self.singleGraveServiceNotes.graveID = self.singleGrave.ID
        self.singleGraveServiceNotes.graveServiceID =  self.MN['GraveServiceNotesHolliday'] 
        self.singleGraveServiceNotes.save()
        
        
        self.setEntriesEditable(self.EntriesGravesHolidays, False)
        self.setEntriesEditable(self.EntriesGraves, False)
        self.tabChanged()
        
    def on_HolidaysNew1_activate(self, event):
        print "new GraveHolidays addresses v2"
        self.singleGraveHolidays.newRecord()
        self.setEntriesEditable(self.EntriesGravesHolidays, True)
        self.setEntriesEditable(self.EntriesGraves, True)
        
    def on_HolidaysEdit1_activate(self, event):
        print "print GraveHolidays addresses v2"
        self.setEntriesEditable(self.EntriesGravesHolidays, True)
        self.setEntriesEditable(self.EntriesGraves, True)

    def on_HolidaysClear1_activate(self, event):
        self.out( "delete GraveHolidays addresses v2")
        self.singleGraveHolidays.deleteRecord()

#Menu Annual
        
   
    def on_AnnualSave1_activate(self, event):
        self.out( "save GraveAnnual addresses v2")
        
          # set the price from a pricegroup if no price is setting
        self.setArticlePrice('grave','eAnnualArticleID', 'eAnnualPrice',  self.singleGrave.ID)
       
        self.singleGraveAnnual.graveID = self.singleGrave.ID
        self.singleGraveAnnual.graveServiceID =  self.MN['GraveServiceNotesAnnual'] 
        self.singleGraveAnnual.singleGrave = self.singleGrave
        self.singleGraveAnnual.save()
        
        
        self.singleGraveServiceNotes.graveID = self.singleGrave.ID
        self.singleGraveServiceNotes.graveServiceID =  self.MN['GraveServiceNotesAnnual'] 
        self.singleGraveServiceNotes.save()
        
        
        self.setEntriesEditable(self.EntriesGravesAnnual, False)
        self.setEntriesEditable(self.EntriesGraves, False)
        self.tabChanged()
        
    def on_AnnualNew1_activate(self, event):
        self.out( "new GraveAnnual addresses v2")
        self.singleGraveAnnual.newRecord()
        self.setEntriesEditable(self.EntriesGravesAnnual, True)
        self.setEntriesEditable(self.EntriesGraves, True)
        
    def on_AnnualEdit1_activate(self, event):
        self.setEntriesEditable(self.EntriesGravesAnnual, True)
        self.setEntriesEditable(self.EntriesGraves, True)

    def on_AnnualClear1_activate(self, event):
        self.out( "delete GraveAnnual addresses v2")
        self.singleGraveAnnual.deleteRecord()

#Menu Unique
        
   
    def on_UniqueSave1_activate(self, event):
        self.out( "save GraveUnique addresses v2")
        
          # set the price from a pricegroup if no price is setting
        self.setArticlePrice('grave','eUniqueArticleID', 'eUniquePrice',  self.singleGrave.ID)
      


        self.singleGraveUnique.graveID = self.singleGrave.ID
        self.singleGraveUnique.graveServiceID =  self.MN['GraveServiceNotesUnique'] 
        self.singleGraveUnique.singleGrave = self.singleGrave
        self.singleGraveUnique.save()
        
        
        self.singleGraveServiceNotes.graveID = self.singleGrave.ID
        self.singleGraveServiceNotes.graveServiceID =  self.MN['GraveServiceNotesUnique'] 
        self.singleGraveServiceNotes.save()
        
        
        self.setEntriesEditable(self.EntriesGravesUnique, False)
        self.setEntriesEditable(self.EntriesGraves, False)
        self.tabChanged()
        
    def on_UniqueNew1_activate(self, event):
        self.out( "new GraveUnique addresses v2")
        self.singleGraveUnique.newRecord()
        self.setEntriesEditable(self.EntriesGravesUnique, True)
        self.setEntriesEditable(self.EntriesGraves, True)
        
    def on_UniqueEdit1_activate(self, event):
        self.setEntriesEditable(self.EntriesGravesUnique, True)
        self.setEntriesEditable(self.EntriesGraves, True)

    def on_UniqueClear1_activate(self, event):
        self.out( "delete GraveUnique addresses v2")
        self.singleGraveUnique.deleteRecord()



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


    def on_tbNew_clicked(self,  event):
        if self.tabOption == self.tabGrave:
            self.activateClick('new1')
        elif self.tabOption == self.tabGraveMaintenance:
            self.activateClick('MaintenanceNew1')           
        elif self.tabOption == self.tabGraveInvoice:
            self.activateClick('InvoicesNew1')            
        elif self.tabOption == self.tabGraveSpring:
            self.activateClick('SpringNew1')
        elif self.tabOption == self.tabGraveSummer:
            self.activateClick('SummerNew1')
        elif self.tabOption == self.tabGraveAutumn:
            self.activateClick('AutumnNew1')
        elif self.tabOption == self.tabGraveWinter:
            self.activateClick('WinterNew1')
        elif self.tabOption == self.tabGraveHollidays:
            self.activateClick('HolidaysNew1')
        elif self.tabOption == self.tabGraveAnnual:
            self.activateClick('AnnualNew1')
        elif self.tabOption == self.tabGraveUnique:
            self.activateClick('UniqueNew1')            
            
    def on_tbEdit_clicked(self,  event):
        if self.tabOption == self.tabGrave:
            self.activateClick('edit1')
        if self.tabOption == self.tabGraveMaintenance:
            self.activateClick('MaintenanceEdit1')    
        elif self.tabOption == self.tabGraveInvoice:
            self.activateClick('InvoicesEdit1')
        elif self.tabOption == self.tabGraveSpring:
            self.activateClick('SpringEdit1')
        elif self.tabOption == self.tabGraveSummer:
            self.activateClick('SummerEdit1')
        elif self.tabOption == self.tabGraveAutumn:
            self.activateClick('AutumnEdit1')
        elif self.tabOption == self.tabGraveWinter:
            self.activateClick('WinterEdit1')
        elif self.tabOption == self.tabGraveHollidays:
            self.activateClick('HolidaysEdit1')
        elif self.tabOption == self.tabGraveAnnual:
            self.activateClick('AnnualEdit1')
        elif self.tabOption == self.tabGraveUnique:
            self.activateClick('UniqueEdit1')
         
         
            
    def on_tbSave_clicked(self,  event):
        if self.tabOption == self.tabGrave:
            self.activateClick('save1')
        if self.tabOption == self.tabGraveMaintenance:
            self.activateClick('MaintenanceSave1')    
        elif self.tabOption == self.tabGraveInvoice:
            self.activateClick('InvoicesSave1')
        elif self.tabOption == self.tabGraveSpring:
            self.activateClick('SpringSave1')
        elif self.tabOption == self.tabGraveSummer:
            self.activateClick('SummerSave1')
        elif self.tabOption == self.tabGraveAutumn:
            self.activateClick('AutumnSave1')
        elif self.tabOption == self.tabGraveWinter:
            self.activateClick('WinterSave1')
        elif self.tabOption == self.tabGraveHollidays:
            self.activateClick('HolidaysSave1')
        elif self.tabOption == self.tabGraveAnnual:
            self.activateClick('AnnualSave1')
        elif self.tabOption == self.tabGraveUnique:
            self.activateClick('UniqueSave1')
                
    def on_tbDelete_clicked(self,  event):
        if self.tabOption == self.tabGrave:
            self.activateClick('clear1')
        if self.tabOption == self.tabGraveMaintenance:
            self.activateClick('MaintenanceClear1')    
        elif self.tabOption == self.tabGraveInvoice:
            self.activateClick('InvoicesClear1')
        elif self.tabOption == self.tabGraveSpring:
            self.activateClick('SpringClear1')
        elif self.tabOption == self.tabGraveSummer:
            self.activateClick('SummerClear1')
        elif self.tabOption == self.tabGraveAutumn:
            self.activateClick('AutumnClear1')
        elif self.tabOption == self.tabGraveWinter:
            self.activateClick('WinterClear1')
        elif self.tabOption == self.tabGraveHollidays:
            self.activateClick('HolidaysClear1')
        elif self.tabOption == self.tabGraveAnnual:
            self.activateClick('AnnualClear1')
        elif self.tabOption == self.tabGraveUnique:
            self.activateClick('UniqueClear1')
                  
                 
              
    def on_bChooseAddress_clicked(self, event):
        adr = cuon.Addresses.addresses.addresswindow(self.allTables)
        adr.setChooseEntry('chooseAddress', self.getWidget( 'eAddressNumber'))

    def on_eAddressNumber_changed(self, event):
        print 'eAddressNumber changed'
        iAdrNumber = self.getChangedValue('eAddressNumber')
        eAdrField = self.getWidget('tvAddress')
        liAdr = self.singleAddress.getAddress(iAdrNumber)
        self.setTextbuffer(eAdrField,liAdr)


    def on_bGotoAddress_clicked(self,  event):
        adr = cuon.Addresses.addresses.addresswindow(self.allTables, self.singleAddress.ID)
        
    def on_bInvoiceChooseAddress_clicked(self, event):
        adr = cuon.Addresses.addresses.addresswindow(self.allTables)
        adr.setChooseEntry('chooseAddress', self.getWidget( 'eInvoiceAddressID'))

    def on_eInvoiceAddressID_changed(self, event):
        print 'eAddressNumber changed'
        iAdrNumber = self.getChangedValue('eInvoiceAddressID')
        eAdrField = self.getWidget('tvInvoicesAddress')
        liAdr = self.singleAddress.getAddress(iAdrNumber)
        self.setTextbuffer(eAdrField,liAdr)

        
       
    def on_bInvoiceChooseTOP_clicked(self, event):
        print 'choose TOP'
        top = cuon.PrefsFinance.prefsFinance.prefsFinancewindow(self.allTables, preparedTab = 1 )
        top.setChooseEntry('chooseTOP', self.getWidget( 'eInvoiceTOPID'))
        
    def on_eInvoiceTOPID_changed(self, event):
        print 'eTOPID changed'
        eTopField = self.getWidget('tvInvoicesTOP')
        try:
            liTop = self.singlePrefsFinanceTop.getTOP(long(self.getWidget( 'eInvoiceTOPID').get_text()))
            self.setTextbuffer(eTopField, liTop)
            
        except Exception,param:
            self.setTextbuffer(eTopField, ' ')
            print Exception,param

        
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
 
    def on_bChooseArticle_clicked(self,  event):
        art =  cuon.Articles.articles.articleswindow(self.allTables)
        if self.tabOption == self.tabGraveSpring:
            art.setChooseEntry('chooseArticle', self.getWidget( 'eSpringArticleID'))

        elif self.tabOption == self.tabGraveSummer:
            art.setChooseEntry('chooseArticle', self.getWidget( 'eSummerArticleID'))
            
        elif self.tabOption == self.tabGraveAutumn:
            art.setChooseEntry('chooseArticle', self.getWidget( 'eAutumnArticleID'))
            
        elif self.tabOption == self.tabGraveWinter:
            art.setChooseEntry('chooseArticle', self.getWidget( 'eWinterArticleID'))
            
        elif self.tabOption == self.tabGraveHollidays:
            art.setChooseEntry('chooseArticle', self.getWidget( 'eHolidaysArticleID'))
            
        elif self.tabOption == self.tabGraveUnique:
            art.setChooseEntry('chooseArticle', self.getWidget( 'eUniqueArticleID'))
            
        elif self.tabOption == self.tabGraveAnnual:
            art.setChooseEntry('chooseArticle', self.getWidget( 'eAnnualArticleID'))
    
    
    def on_bSearchGraveyard_clicked(self,  event):
        adr = graveyard.graveyardMainwindow(self.allTables)
        adr.setChooseEntry('chooseGraveyard', self.getWidget( 'eGraveyardID'))

    # signals from entry eAddressNumber
    
    def on_eGraveyardID_changed(self, event):
        print 'eAdrnbr changed'
        iAdrNumber = self.getChangedValue('eGraveyardID')
        eAdrField = self.getWidget('tvGraveyard')
        
        liAdr,  addressid = self.singleGraveyard.getAddress(iAdrNumber)
        liAdr2 = self.singleAddress.getAddress(addressid)
        
        self.setTextbuffer(eAdrField,liAdr + liAdr2) 
        
    # search button
    def on_bSearch_clicked(self, event):
       self.findGrave()
        
    def on_eFindButton_key_press_event(self,entry,  event):
        print 'eSearch_key_press_event'
        if self.checkKey(event,'NONE','Return'):
            self.findGrave()
    def on_cbFindGraveyard_changed(self,  event):
        self.findGrave()
        
        
    def findGrave(self):
        print 'findGrave'
        iGraveyardId = 0
        iTypeOfPaid = -1
        iTypeOfGrave = -1
        self.singleGrave.setTreeOrder('lastname, firstname')
        sName = self.getWidget('eFindNameOfGrave').get_text()
        sFirstname = self.getWidget('eFindFirstname').get_text()
        sSerialNumber = self.getWidget('eFindSerialNumber').get_text()
        
        try:
            sGY = self.getWidget('cbFindGraveyard').get_active_text()
            print 'Graveyard = ',  sGY
            iGraveyardId = int( sGY[sGY.find('###')+3:])
            print 'graveyardID = ',  iGraveyardId
        except:
            pass
            
            
        try:
            sGP = self.getWidget('cbFindTypeOfPaid').get_active_text()
            print 'Grave paid = ',  sGP
            iTypeOfPaid = int( sGP[sGP.find('###')+3:])
            print 'graveyardID = ',  iTypeOfPaid
        except:
            pass
            
            
        try:
            sGT = self.getWidget('cbFindTypeOfGrave').get_active_text()
            print 'Grave Type = ',  sGT
            iTypeOfGrave = int( sGT[sGT.find('###')+3:])
            print 'iTypeOfGrave = ',  iTypeOfGrave
        except:
            pass    
        liSearch = []
        if sName:
            liSearch.append('lastname')
            liSearch.append(sName)
      
        if sSerialNumber:
            liSearch.append('pos_number')
            print 'liSearch 01 = ',  liSearch
            try:
                if sSerialNumber.find('-') > 0:
                    liPos = sSerialNumber.split('-')
                    liSearch.append('# between ' + liPos[0].strip() + ' and ' + liPos[1].strip() )
                    self.singleGrave.setTreeOrder('pos_number, lastname')
                else:
                    print 'else ',  liSearch
                    liSearch.append(int(sSerialNumber.strip()))
            except Exception,  params:
                print Exception,  params
                print 'error in find'
                liSearch.append(0)
        print 'liSearch 02 = ',  liSearch    
        if sFirstname:
            liSearch.append('firstname')
            liSearch.append(sFirstname)
        print 'liSearch 04 = ',  liSearch
        
        if iGraveyardId > 0:
            liSearch.append('graveyardid')
            liSearch.append(iGraveyardId)
            
        if iTypeOfPaid > -1:
            liSearch.append('type_of_paid')
            liSearch.append(iTypeOfPaid)
        
        if iTypeOfGrave > -1:
            liSearch.append('type_of_grave')
            liSearch.append(iTypeOfGrave)
            
        print 'liSearch 05 = ',  liSearch   
        if liSearch:
            self.singleGrave.sWhere = self.getWhere(liSearch) 
        print 'liSearch 10= ',  liSearch
        print  self.singleGrave.sWhere
        self.refreshTree()

                
    def on_bQuickAppend_clicked(self, event):
        print "bQuickappend activated"
        self.AutoInsert = False
       # Modul,iModulID,   iArticleID,  dicUser)
        if self.tabOption == self.tabGraveMaintenance:
            self.activateClick('MaintenanceNew1')
            self.AutoInsert = True 
            #self.getWidget('eSpringArticleID').set_text(' ')
            print "article ID = " ,  self.fillArticlesNewID
            self.getWidget('eServiceCounts').set_text(self.getCheckedValue('1.00', 'toStringFloat') )
            self.getWidget('eServicePrice').set_text(self.getCheckedValue(self.rpc.callRP('Article.getPrice', 'grave', self.singleGrave.ID,  self.fillArticlesNewID,self.dicUser),'toStringFloat'))
            self.getWidget('eServiceArticleID').set_text(`self.fillArticlesNewID`)
        elif self.tabOption == self.tabGraveSpring:
            self.activateClick('SpringNew1')
            self.AutoInsert = True 
            #self.getWidget('eSpringArticleID').set_text(' ')
            print "article ID = " ,  self.fillArticlesNewID
            self.getWidget('eSpringCounts').set_text(self.getCheckedValue('1.00', 'toStringFloat') )
            self.getWidget('eSpringPrice').set_text(self.getCheckedValue(self.rpc.callRP('Article.getPrice','grave', self.singleGrave.ID,   self.fillArticlesNewID,self.dicUser),'toStringFloat'))
            self.getWidget('eSpringArticleID').set_text(`self.fillArticlesNewID`)
        elif self.tabOption == self.tabGraveSummer:
            self.activateClick('SummerNew1')
            self.AutoInsert = True 
            #self.getWidget('eSummerArticleID').set_text(' ')
            print "article ID = " ,  self.fillArticlesNewID
            self.getWidget('eSummerCounts').set_text(self.getCheckedValue('1.00', 'toStringFloat') )
            self.getWidget('eSummerPrice').set_text(self.getCheckedValue(self.rpc.callRP('Article.getPrice','grave', self.singleGrave.ID,   self.fillArticlesNewID,self.dicUser),'toStringFloat'))
            self.getWidget('eSummerArticleID').set_text(`self.fillArticlesNewID`)

        elif self.tabOption == self.tabGraveAutumn:
            self.activateClick('AutumnNew1')
            self.AutoInsert = True 
            #self.getWidget('eAutumnArticleID').set_text(' ')
            print "article ID = " ,  self.fillArticlesNewID
            self.getWidget('eAutumnCounts').set_text(self.getCheckedValue('1.00', 'toStringFloat') )
            self.getWidget('eAutumnPrice').set_text(self.getCheckedValue(self.rpc.callRP('Article.getPrice', 'grave', self.singleGrave.ID,  self.fillArticlesNewID,self.dicUser),'toStringFloat'))
            self.getWidget('eAutumnArticleID').set_text(`self.fillArticlesNewID`)

        elif self.tabOption == self.tabGraveHollidays:
            self.activateClick('HolidaysNew1')
            self.AutoInsert = True 
            #self.getWidget('eWinterArticleID').set_text(' ')
            print "article ID = " ,  self.fillArticlesNewID
            self.getWidget('eHolidaysCounts').set_text(self.getCheckedValue('1.00', 'toStringFloat') )
            self.getWidget('eHolidaysPrice').set_text(self.getCheckedValue(self.rpc.callRP('Article.getPrice', 'grave', self.singleGrave.ID,  self.fillArticlesNewID,self.dicUser),'toStringFloat'))
            self.getWidget('eHolidaysArticleID').set_text(`self.fillArticlesNewID`)

        elif self.tabOption == self.tabGraveWinter:
            self.activateClick('WinterNew1')
            self.AutoInsert = True 
            #self.getWidget('eWinterArticleID').set_text(' ')
            print "article ID = " ,  self.fillArticlesNewID
            self.getWidget('eWinterCounts').set_text(self.getCheckedValue('1.00', 'toStringFloat') )
            self.getWidget('eWinterPrice').set_text(self.getCheckedValue(self.rpc.callRP('Article.getPrice', 'grave', self.singleGrave.ID,  self.fillArticlesNewID,self.dicUser),'toStringFloat'))
            self.getWidget('eWinterArticleID').set_text(`self.fillArticlesNewID`)

        elif self.tabOption == self.tabGraveUnique:
            self.activateClick('UniqueNew1')
            self.AutoInsert = True 
            #self.getWidget('eWinterArticleID').set_text(' ')
            print "article ID = " ,  self.fillArticlesNewID
            self.getWidget('eUniqueCounts').set_text(self.getCheckedValue('1.00', 'toStringFloat') )
            self.getWidget('eUniquePrice').set_text(self.getCheckedValue(self.rpc.callRP('Article.getPrice',  'grave', self.singleGrave.ID, self.fillArticlesNewID,self.dicUser),'toStringFloat'))
            self.getWidget('eUniqueArticleID').set_text(`self.fillArticlesNewID`)

        elif self.tabOption == self.tabGraveAnnual:
            self.activateClick('AnnualNew1')
            self.AutoInsert = True 
            #self.getWidget('eWinterArticleID').set_text(' ')
            print "article ID = " ,  self.fillArticlesNewID
            self.getWidget('eAnnualCounts').set_text(self.getCheckedValue('1.00', 'toStringFloat') )
            self.getWidget('eAnnualPrice').set_text(self.getCheckedValue(self.rpc.callRP('Article.getPrice',  'grave', self.singleGrave.ID,  self.fillArticlesNewID,self.dicUser),'toStringFloat'))
            self.getWidget('eAnnualArticleID').set_text(`self.fillArticlesNewID`)

            #
    def on_eArticleID_changed(self, event):
        print "eArticleID changed"
        #self.singleArticle.load(self.fillArticlesNewID)
        if self.tabOption == self.tabGraveMaintenance:
            try:
                self.getWidget('eServiceArticleDesignation').set_text(self.singleArticle.getArticleDesignation(int(self.getWidget('eServiceArticleID').get_text())) )
                
            except:
                self.getWidget('eServiceArticleDesignation').set_text(' ') 
            if self.AutoInsert:
               
                self.AutoInsert = False
                self.activateClick('MaintenanceSave1')
            
        elif self.tabOption == self.tabGraveSpring:
            try:
                self.getWidget('eSpringArticleDesignation').set_text(self.singleArticle.getArticleDesignation(int(self.getWidget('eSpringArticleID').get_text())) )
            except:
                self.getWidget('eSpringArticleDesignation').set_text(' ') 
            if self.AutoInsert:
                self.AutoInsert = False
                self.activateClick('SpringSave1')
            
        elif self.tabOption == self.tabGraveSummer:
            try:
                self.getWidget('eSummerArticleDesignation').set_text(self.singleArticle.getArticleDesignation(int(self.getWidget('eSummerArticleID').get_text())) )
            except:
                self.getWidget('eSummerArticleDesignation').set_text(' ') 
            if self.AutoInsert:
                self.AutoInsert = False
                self.activateClick('SummerSave1')
            
        elif self.tabOption == self.tabGraveAutumn:
            try:
                self.getWidget('eAutumnArticleDesignation').set_text(self.singleArticle.getArticleDesignation(int(self.getWidget('eAutumnArticleID').get_text())) )
            except:
                self.getWidget('eAutumnArticleDesignation').set_text(' ') 
            if self.AutoInsert:
                self.AutoInsert = False
                self.activateClick('AutumnSave1')
        elif self.tabOption == self.tabGraveWinter:
            try:
                self.getWidget('eWinterArticleDesignation').set_text(self.singleArticle.getArticleDesignation(int(self.getWidget('eWinterArticleID').get_text())) )
            except:
                self.getWidget('eWinterArticleDesignation').set_text(' ') 
            if self.AutoInsert:
                self.AutoInsert = False
                self.activateClick('WinterSave1')
        elif self.tabOption == self.tabGraveHollidays:
            try:
                self.getWidget('eHolidaysArticleDesignation').set_text(self.singleArticle.getArticleDesignation(int(self.getWidget('eHolidaysArticleID').get_text())) )
            except:
                self.getWidget('eHolidaysArticleDesignation').set_text(' ') 
            if self.AutoInsert:
                self.AutoInsert = False
                self.activateClick('HolidaysSave1')
        elif self.tabOption == self.tabGraveAnnual:
            try:
                self.getWidget('eAnnualArticleDesignation').set_text(self.singleArticle.getArticleDesignation(int(self.getWidget('eAnnualArticleID').get_text())) )
            except:
                self.getWidget('eAnnualArticleDesignation').set_text(' ') 
            if self.AutoInsert:
                self.AutoInsert = False
                self.activateClick('AnnualSave1')
                
        elif self.tabOption == self.tabGraveUnique:
            try:
                self.getWidget('eUniqueArticleDesignation').set_text(self.singleArticle.getArticleDesignation(int(self.getWidget('eUniqueArticleID').get_text())) )
            except:
                self.getWidget('eUniqueArticleDesignation').set_text(' ') 
            if self.AutoInsert:
                self.AutoInsert = False
                self.activateClick('UniqueSave1')
                         
    def on_bDMS_clicked(self, event):
        print 'dms clicked'
        if self.singleGrave.ID > 0:
            print 'ModulNumber', self.ModulNumber
            Dms = cuon.DMS.dms.dmswindow(self.allTables, self.ModulNumber, {'1':self.singleGrave.ID})
       
       
    def on_bAddressDMS_clicked(self, event):
        print 'Addressdms clicked'
        if self.singleGrave.ID > 0:
            print 'ModulNumber', self.ModulNumber
#            iGraveyardId = self.singleGrave.getGraveyardID(self.singleGrave.ID)
#            print 'GraveyardID = ',  iGraveyardId
#            liAdr,  addressid = self.singleGraveyard.getAddress(iGraveyardId)
#            print liAdr,  addressid
            addressid = self.singleGrave.getAddressID(self.singleGrave.ID)
            if addressid > 0:
                Dms = cuon.DMS.dms.dmswindow(self.allTables, self.MN['Address'], {'1':addressid})
    
    
    
    def  on_CreateSingleInvoice_activate(self,  event):
        self.pressedTypeOfInvoice = 1
        if self.tabOption == self.tabGrave:
            self.getWidget('chooseInvoices').show()
            
            
        elif self.tabOption == self.tabGraveMaintenance:
            print 'create Single Invoice'
            newOrderNumber = self.rpc.callRP('Grave.createNewInvoice',self.dicUser, ['Service'],  self.singleGrave.ID )
            print 'newOrderNumber = ',  newOrderNumber
            
            
           
    def on_CreateAllInvoices_activate(self,  event):
        self.pressedTypeOfInvoice = 2
        self.getWidget('chooseInvoices').show()
   
    def on_bCIOK_clicked(self, event):
        liInvoices = []
        
        if  self.getWidget('chService').get_active() :
            liInvoices.append('Service')
        if  self.getWidget('chSpring').get_active() :
            liInvoices.append('Spring')
        if  self.getWidget('chSummer').get_active() :
            liInvoices.append('Summer')
        if  self.getWidget('chAutumn').get_active() :
            liInvoices.append('Autumn')
        if  self.getWidget('chWinter').get_active() :
            liInvoices.append('Winter')
        if  self.getWidget('chHolliday').get_active() :
            liInvoices.append('Holliday')
        if  self.getWidget('chUnique').get_active() :
            liInvoices.append('Unique')
        if  self.getWidget('chYearly').get_active() :
            liInvoices.append('Yearly')
        if  self.getWidget('chAllTogether').get_active() :
            liInvoices = [] 
            liInvoices.append('Service')
            liInvoices.append('Spring')
            liInvoices.append('Summer')
            liInvoices.append('Autumn')
            liInvoices.append('Winter')
            liInvoices.append('Holliday')
            liInvoices.append('Unique')
            liInvoices.append('Yearly')
 
 
        
        liValues = []
        liValues.append(liInvoices)
        liValues.append(self.getWidget('cbChooseTypeOfPaid').get_active())
 
 
 
 
        print 'create Single Invoice',  liInvoices
        if self.pressedTypeOfInvoice == 1:
            newOrderNumber = self.rpc.callRP('Grave.createNewInvoice',self.dicUser, liValues,  self.singleGrave.ID )
            print 'newOrderNumber = ',  newOrderNumber
        elif self.pressedTypeOfInvoice == 2:
            bOK = self.rpc.callRP('Grave.createAllNewInvoice',self.dicUser, liValues )
            
        self.getWidget('chooseInvoices').hide()
        
    def on_bCICancel_clicked(self, event):
        self.getWidget('chooseInvoices').hide()   
        
    def refreshTree(self):
        self.singleGrave.disconnectTree()
        self.singleGraveMaintenance.disconnectTree()
        self.singleGraveInvoices.disconnectTree()
        self.singleGraveSpring.disconnectTree()
        self.singleGraveSummer.disconnectTree()
        self.singleGraveAutumn.disconnectTree()
        self.singleGraveWinter.disconnectTree()
        self.singleGraveHolidays.disconnectTree()
        self.singleGraveAnnual.disconnectTree()
        self.singleGraveUnique.disconnectTree()
        if self.tabOption == self.tabGrave:
            self.singleGrave.connectTree()
            self.singleGrave.refreshTree()
            
        elif self.tabOption == self.tabGraveInvoice:
            print "1 tree "
            self.singleGraveInvoices.sWhere  ='where grave_id = ' + `int(self.singleGrave.ID)`+ ' and address_id = address.id '
            self.singleGraveInvoices.connectTree()
            self.singleGraveInvoices.refreshTree()
            
        elif self.tabOption == self.tabGraveMaintenance:
            print "1 tree "
            self.singleGraveMaintenance.sWhere  ='where grave_id = ' + `int(self.singleGrave.ID)`
            self.singleGraveMaintenance.connectTree()
            self.singleGraveMaintenance.refreshTree()
        
        elif self.tabOption == self.tabGraveSpring:
            print "1 tree "
            self.singleGraveSpring.sWhere  ='where grave_id = ' + `int(self.singleGrave.ID)`+ ' and article_id = articles.id '
            self.singleGraveSpring.connectTree()
            self.singleGraveSpring.refreshTree()
            
        
        elif self.tabOption == self.tabGraveSummer:
            print "1 tree "
            self.singleGraveSummer.sWhere  ='where grave_id = ' + `int(self.singleGrave.ID)`+ ' and article_id = articles.id '
            self.singleGraveSummer.connectTree()
            self.singleGraveSummer.refreshTree()
        
        elif self.tabOption == self.tabGraveAutumn:
            print "1 tree "
            self.singleGraveAutumn.sWhere  ='where grave_id = ' + `int(self.singleGrave.ID)`+ ' and article_id = articles.id '
            self.singleGraveAutumn.connectTree()
            self.singleGraveAutumn.refreshTree()
            
        elif self.tabOption == self.tabGraveWinter:
            print "1 tree "
            self.singleGraveWinter.sWhere  ='where grave_id = ' + `int(self.singleGrave.ID)`+ ' and article_id = articles.id '
            self.singleGraveWinter.connectTree()
            self.singleGraveWinter.refreshTree()
            
        elif self.tabOption == self.tabGraveHollidays:
            print "1 tree "
            self.singleGraveHolidays.sWhere  ='where grave_id = ' + `int(self.singleGrave.ID)`+ ' and article_id = articles.id '
            self.singleGraveHolidays.connectTree()
            self.singleGraveHolidays.refreshTree()
            
        elif self.tabOption == self.tabGraveAnnual:
            print "1 tree "
            self.singleGraveAnnual.sWhere  ='where grave_id = ' + `int(self.singleGrave.ID)`+ ' and article_id = articles.id '
            self.singleGraveAnnual.connectTree()
            self.singleGraveAnnual.refreshTree()
            
        elif self.tabOption == self.tabGraveUnique:
            print "1 tree "
            self.singleGraveUnique.sWhere  ='where grave_id = ' + `int(self.singleGrave.ID)`+ ' and article_id = articles.id '
            self.singleGraveUnique.connectTree()
            self.singleGraveUnique.refreshTree()
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
            

            print  'Seite 0' 

        elif self.tabOption == self.tabGraveMaintenance:
            self.out( 'Seite 2')
            self.disableMenuItem('tabs')
            self.enableMenuItem('graveMaintenance')
            self.singleGraveMaintenance.graveID = self.singleGrave.ID   
            self.singleGraveMaintenance.graveServiceID =  self.MN['GraveServiceNotesService'] 
            self.singleGraveMaintenance.singleGrave = self.singleGrave
        
            self.editAction = 'editGraveMaintenance'
            self.setTreeVisible(True)
            self.setStatusbarText([self.singleGrave.sStatus])
            
            
        elif self.tabOption == self.tabGraveInvoice:
            self.out( 'Seite 2')
            self.disableMenuItem('tabs')
            self.enableMenuItem('graveInvoice')
           
            self.editAction = 'editGraveInvoice'
            self.setTreeVisible(True)
            self.setStatusbarText([self.singleGrave.sStatus])
            
        elif self.tabOption == self.tabGraveSpring:
            self.out( 'Seite 2')
            self.disableMenuItem('tabs')
            self.enableMenuItem('graveSpring')
            self.singleGraveSpring.graveID = self.singleGrave.ID   
            self.singleGraveSpring.graveServiceID =  self.MN['GraveServiceNotesSpring'] 
            self.singleGraveSpring.singleGrave = self.singleGrave
        
            self.editAction = 'editGraveSpring'
            self.setTreeVisible(True)
            self.setStatusbarText([self.singleGrave.sStatus])
            
        elif self.tabOption == self.tabGraveSummer:
            self.out( 'Seite 2')
            self.disableMenuItem('tabs')
            self.enableMenuItem('graveSummer')
             
            self.singleGraveSummer.graveID = self.singleGrave.ID   
            self.singleGraveSummer.graveServiceID =  self.MN['GraveServiceNotesSummer'] 
            self.singleGraveSummer.singleGrave = self.singleGrave
       
            self.editAction = 'editGraveSummer'
            self.setTreeVisible(True)
            self.setStatusbarText([self.singleGrave.sStatus])   
            
            
            
        elif self.tabOption == self.tabGraveAutumn:
            self.out( 'Seite 2')
            self.disableMenuItem('tabs')
            self.enableMenuItem('graveAutumn')
            self.singleGraveAutumn.graveID = self.singleGrave.ID  
            self.singleGraveAutumn.graveServiceID =  self.MN['GraveServiceNotesAutumn'] 
            self.singleGraveAutumn.singleGrave = self.singleGrave    
            
            self.editAction = 'editGraveAutumn'
            self.setTreeVisible(True)
            self.setStatusbarText([self.singleGrave.sStatus])
        
        elif self.tabOption == self.tabGraveWinter:
            self.out( 'Seite 2')
            self.disableMenuItem('tabs')
            self.enableMenuItem('graveWinter')
              
            self.singleGraveWinter.graveID = self.singleGrave.ID   
            self.singleGraveWinter.graveServiceID =  self.MN['GraveServiceNotesWinter'] 
            self.singleGraveWinter.singleGrave = self.singleGrave
     
            self.editAction = 'editGraveWinter'
            self.setTreeVisible(True)
            self.setStatusbarText([self.singleGrave.sStatus])
        
        elif self.tabOption == self.tabGraveHollidays:
            self.out( 'Seite 2')
            self.disableMenuItem('tabs')
            self.enableMenuItem('graveHolidays')
           
     
            self.singleGraveHolidays.graveID = self.singleGrave.ID   
            self.singleGraveHolidays.graveServiceID =  self.MN['GraveServiceNotesHolliday'] 
            self.singleGraveHolidays.singleGrave = self.singleGrave
     
            self.editAction = 'editGraveHolidays'
            self.setTreeVisible(True)
            self.setStatusbarText([self.singleGrave.sStatus]) 
            
            
        elif self.tabOption == self.tabGraveAnnual:
            self.out( 'Seite 2')
            self.disableMenuItem('tabs')
            self.enableMenuItem('graveAnnual')
                  
            self.singleGraveAnnual.graveID = self.singleGrave.ID   
            self.singleGraveAnnual.graveServiceID =  self.MN['GraveServiceNotesAnnual'] 
            self.singleGraveAnnual.singleGrave = self.singleGrave

            self.editAction = 'editGraveAnnual'
            self.setTreeVisible(True)
            self.setStatusbarText([self.singleGrave.sStatus])
         
        elif self.tabOption == self.tabGraveUnique:
            self.out( 'Seite 2')
            self.disableMenuItem('tabs')
            self.enableMenuItem('graveUnique')
           
            self.singleGraveUnique.graveID = self.singleGrave.ID   
            self.singleGraveUnique.graveServiceID =  self.MN['GraveServiceNotesUnique'] 
            self.singleGraveUnique.singleGrave = self.singleGrave
    
        
            self.editAction = 'editGraveUnique'
            self.setTreeVisible(True)
            self.setStatusbarText([self.singleGrave.sStatus])
            
        if self.tabOption ==2:
            liService = self.rpc.callRP('Grave.getService',self.dicUser,  self.tabOption -2)
                                        
            cbService = self.getWidget('cbServiceType')
            if cbService:
                liststore = gtk.ListStore(str)
                for service in liService:
                    liststore.append([service])
                cbService.set_model(liststore)
                cbService.set_text_column(0)
                cbService.show()
          
       
        
           # refresh the Tree
      
        self.refreshTree()
        self.enableMenuItem(self.editAction)
        self.editEntries = False
        
