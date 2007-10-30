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
from types import *
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import gobject

import SingleAccountInfo
import SingleAccountSentence
import time
import datetime

import logging

from cuon.Windows.windows import windows



class bookkeepingwindow(windows):

    
    def __init__(self, allTables):

        windows.__init__(self)

        self.loadGlade('bookkeeping.xml')
        self.win1 = self.getWidget('BookkeepingMainwindow','BookkeepingMainwindow')

        
        self.allTables = allTables
        self.singleAccountSentence = SingleAccountSentence.SingleAccountSentence(allTables)
        self.singleAccountInfo = SingleAccountInfo.SingleAccountInfo(allTables)
        
                      
        self.EntriesCAB = 'cashAccount.xml'
        self.loadEntries(self.EntriesCAB)
    
        self.singleAccountSentence.setEntries(self.getDataEntries(self.EntriesCAB) )
        self.singleAccountSentence.setGladeXml(self.xml)
        self.singleAccountSentence.setTreeFields( ['accounting_date','document_number1','document_number2', 'designation'] )
        self.singleAccountSentence.setStore( gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING,   gobject.TYPE_UINT) ) 
        self.singleAccountSentence.setTreeOrder('accounting_date, document_number1')
        self.singleAccountSentence.setTree(self.xml.get_widget('tree1') )
        self.singleAccountSentence.setListHeader(['date','document_number1','document_number2', 'designation'])
        
         
   
        

        # Menu-items
        self.initMenuItems()

        # Close Menus for Tab

        self.addEnabledMenuItems('tabs','cash1')
        #self.addEnabledMenuItems('tabs','mi_purchase1')
        #self.addEnabledMenuItems('tabs','mi_sales1')


        # seperate Menus
        self.addEnabledMenuItems('cash','cash1')
        #self.addEnabledMenuItems('purchase','mi_purchase1')
        #self.addEnabledMenuItems('sales','mi_sales1')

        
        # enabledMenues for CashAccountBook
        self.addEnabledMenuItems('editCash','new1')
        self.addEnabledMenuItems('editCash','clear1')
        self.addEnabledMenuItems('editCash','print1')
        self.addEnabledMenuItems('editCash','delete1')

        # enabledMenues for ArticlePurchase
        #self.addEnabledMenuItems('editPurchase','PurchaseNew1')
        #self.addEnabledMenuItems('editPurchase','PurchaseClear1')
        #self.addEnabledMenuItems('editPurchase','PurchaseEdit1')
    
 

        # tabs from notebook
        self.tabCash = 0
        
        

        # start
        
        self.tabChanged()

        # enabled menus for cash
        self.addEnabledMenuItems('editCash','new1')
        self.addEnabledMenuItems('editCash','clear1')
        self.addEnabledMenuItems('editCash','print1')

        # enabled menus for article_purchase
        #self.addEnabledMenuItems('editArticlePurchase','PurchaseNew1')
        #self.addEnabledMenuItems('editArticlePurchase','PurchaseClear1')

        # init Comboboxes
        #tax_vat =  self.rpc.callRP('src.Misc.py_getListOfTaxVat', self.dicUser)
        #cb = self.getWidget('cbVat')
        
        #for i in range(len(tax_vat)) :
        #    li = gtk.ListItem(tax_vat[i])
        #    cb.list.append_items([li])
        #    li.show()
            
    #Menu File
              
    def on_quit1_activate(self, event):
        print "exit cashAccountBook"
        self.closeWindow()
  

    #Menu Cash
  
    def on_save1_activate(self, event):
        print "save cashAccountBook"
        #self.singleAccountSentence.save()
        dicEntries = self.singleAccountSentence.readEntries()
        
        print '---------------------------------------------------------'
        print `dicEntries`
        
        print '---------------------------------------------------------'
        dicValues = self.getAccountValues(dicEntries)
        
        if self.checkAccountValues(dicValues):
            self.singleAccountSentence.saveValues(dicEntries)
            self.setEntriesEditable(self.EntriesCAB, False)
            self.tabChanged()
        else:
            self.errorMsg('Not Valid')
            
         
        
    def on_new1_activate(self, event):
        print "new cashAccountBook"
        self.singleAccountSentence.newRecord()
        cab_nr = self.rpc.callRP('Finances.get_cab_doc_number1', self.dicUser)
        print 'cab_nr = ' , cab_nr
        self.getWidget('eDocumentNumber1').set_text(`cab_nr`)
        last_date = self.rpc.callRP('Finances.getLastDate', self.dicUser)
        self.out('Last-Date = ' + `last_date`)
        last_date = time.strptime(last_date, "%d.%m.%Y",  )
        self.getWidget('eDate').set_text(time.strftime(self.dicUser['DateformatString'],last_date))
        self.getWidget('eDate').grab_focus()
        
        self.setEntriesEditable(self.EntriesCAB, True)

    def on_edit1_activate(self, event):
        self.setEntriesEditable(self.EntriesCAB, True)
        
    def on_delete1_activate(self, event):
        print "delete cashAccountBook"
        self.singleAccountSentence.deleteRecord()

    # Journal

    def on_monthly1_activate(self, event):
        month = 04
        year = 2005
        dicCab = {}
        dicCab['CabNumber'] = '1'
        
        Pdf = cuon.Finances.standard_cab_monthly.standard_cab_monthly(dicCab)

       # dicCab = self.rpc.callRP('src.Finances.py_get_cab_monthly',month,year, self.dicUser)
    #choose Manufactor button
    
    def on_bChooseManufactor_clicked(self, event):
        adr = cuon.Addresses.addresses.addresswindow(self.allTables)
        adr.setChooseEntry(_('chooseAddress'), self.getWidget( 'eManufactorNumber'))
        
    # signals from entry eCAB1
    
    def on_eCAB1_changed(self, event):
        print 'eCAB1 insertText'
        self.setInfo('eCAB1','eInfo1')
 
    def on_eCAB2_changed(self, event):
        print 'eCAB2 insertText'
        self.setInfo('eCAB2','eInfo2')

    def on_eCAB3_changed(self, event):
        print 'eCAB3 insertText'
        self.setInfo('eCAB3','eInfo3')
    
    def on_eCAB4_changed(self, event):
        print 'eCAB4 insertText'
        self.setInfo('eCAB4','eInfo4')
  

    def setInfo(self, getWidgetText, setWidgetText ):
        eAcct = self.getWidget(setWidgetText)
        cCAB1 = self.singleAccountInfo.getInfoline(self.getWidget(getWidgetText).get_text())
        if cCAB1:
            eAcct.set_text(cCAB1)
        else:
            eAcct.set_text('')
            
    

        
    def on_eDate_key_press_event(self, entry, event):
        if self.checkKey(event,'ALT','k'):
            # add one Day
            self.addOneDay(entry, event)
                        
                               
        elif self.checkKey(event,'ALT','l'):
            # remove one day
            self.removeOneDay(entry, event)
            
    def on_eShortKey_changed(self,entry):
        print 'ShortKey changed'
        if self.singleAccountSentence.isNewRecord():
            s = entry.get_text()
            if len(s) >1:
                id = self.rpc.callRP('Finances.get_cabShortKeyValues', s, self.oUser.getSqlDicUser())
                if id > 0:
                    print id
                    sDes = self.rpc.callRP('Finances.get_cab_designation', id, self.oUser.getSqlDicUser())
                    if sDes:
                        self.getWidget('eDesignation').set_text(sDes)
                else:
                    self.getWidget('eDesignation').set_text(' ')
                        
    def on_eShortKey_focus_out_event(self, entry, event):
        print 'Editing ready'
        if self.singleAccountSentence.isNewRecord():
            # fill this later
            pass
            
    # search button
    def on_bSearch_clicked(self, event):
        self.out( 'Searching ....', self.ERROR)
        sNumber = self.getWidget('eFindNumber').get_text()
        sDesignation = self.getWidget('eFindDesignation').get_text()
        self.out('Name and City = ' + sNumber + ', ' + sDesignation, self.ERROR)
        self.singleAccountSentence.sWhere = 'where number ~* \'.*' + sNumber + '.*\' and designation ~* \'.*' + sDesignation + '.*\''
        self.out(self.singleAccountSentence.sWhere, self.ERROR)
        self.refreshTree()

        
         
        
        
    def getAccountValues(self, dicEntries):
        dicValues = {}
        dicValues['d1'] = float(dicEntries['value_d1'][0]) 
        dicValues['d2'] = float(dicEntries['value_d2'][0]) 
        dicValues['d3'] = float(dicEntries['value_d3'][0]) 
        dicValues['d4'] = float(dicEntries['value_d4'][0])
        
        dicValues['c1'] = float(dicEntries['value_c1'][0]) 
        dicValues['c2'] = float(dicEntries['value_c2'][0]) 
        dicValues['c3'] = float(dicEntries['value_c3'][0]) 
        dicValues['c4'] = float(dicEntries['value_c4'][0])
        
        
        return dicValues
        
    def checkAccountValues(self, dicValues):
        ok = False
        # add all values:
        
        fDebit = float(dicValues['d1']) + float(dicValues['d2']) + \
            float(dicValues['d3']) + float(dicValues['d4'])
        fCredit = float(dicValues['c1']) + float(dicValues['c2']) + \
            float(dicValues['c3']) + float(dicValues['c4'])
        
        if fDebit - fCredit == 0.0:
            ok = True
        
        return ok
        
    def getSqlValues(self, dicValues):
        liValues = []
        dicEntry = {}
        for i in range(1,5):
            if dicValues['c' +`i`] != 0.0 and dicValues['d' + `i`] == 0.0 :
                liSql = []
                liSql.append(dicValues['c'+`i`])
                liSql.append('float')
                dicEntry['values'] = liSql
       
                liSql = []
                liSql.append('-')
                liSql.append('string')
                dicEntry['debit_credit'] = liSql
            
                liSql = []
                liSql.append(-1)
                liSql.append('int')
                dicEntry['id'] = liSql
            
                liSql = []
                liSql.append(-1)
                liSql.append('int')
                dicEntry['account_number'] = liSql
            
                
                liValues.append(dicEntry)
        
        return liValues
        

    def refreshTree(self):
        #self.singleAccountSentence.disconnectTree()
        
        if self.tabOption == self.tabCash:
            print "oo-1"
            self.singleAccountSentence.connectTree()
            print 'oo-2'
            self.singleAccountSentence.refreshTree()
            print 'oo-3'
     
     


         
    def tabChanged(self):
        print 'tab changed to :'  + str(self.tabOption)
        if self.tabOption == self.tabCash:
            #Address
            self.disableMenuItem('tabs')
            self.enableMenuItem('cash')
            print 'Seite 0'
            self.editAction = 'editCash'
            print 'oo-tc-01'
     
            
        # refresh the Tree
        self.refreshTree()
        self.enableMenuItem(self.editAction)
        self.editEntries = False
