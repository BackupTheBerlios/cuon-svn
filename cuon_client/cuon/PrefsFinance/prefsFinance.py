# -*- coding: utf-8 -*-
##Copyright (C) [2003]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

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
from gtk import TRUE, FALSE
import cuon.XMLRPC.xmlrpc

from cuon.Databases.SingleData import SingleData
import SinglePrefsFinanceVat
import SinglePrefsFinanceTop
import SinglePrefsFinanceAcctInfo
import cuon.Finances.SingleAccountInfo

import logging
from cuon.Windows.windows  import windows


class prefsFinancewindow(windows):

    
    def __init__(self, allTables):

        windows.__init__(self)
        self.rpc = cuon.XMLRPC.xmlrpc.myXmlRpc()

        self.loadGlade('prefs_finance.xml')
        self.win1 = self.getWidget('PreferencesFinancesMainwindow')
        self.filesel = gtk.FileSelection(title=None)
  
        
        self.allTables = allTables
        self.singlePrefsFinanceVat = SinglePrefsFinanceVat.SinglePrefsFinanceVat(allTables)
        self.singlePrefsFinanceTop = SinglePrefsFinanceTop.SinglePrefsFinanceTop(allTables)
        self.singlePrefsFinanceAcctInfo = SinglePrefsFinanceAcctInfo.SinglePrefsFinanceAcctInfo(allTables)
        # finances
        #self.sai = cuon.Finances.SingleAccountInfo.SingleAccountInfo(allTables)
        
        # self.singlePrefsFinance.loadTable()
              
        self.EntriesPrefsFinanceVat = 'prefs_finance_vat.xml'
        self.EntriesPrefsFinanceTop = 'prefs_finance_top.xml'
        self.EntriesPrefsFinanceAcctInfo = 'prefs_finance_acctinfo.xml'
                
        
        #singlePrefsFinanceVat
 
 
        self.loadEntries(self.EntriesPrefsFinanceVat)
        self.singlePrefsFinanceVat.setEntries(self.getDataEntries(self.EntriesPrefsFinanceVat) )
        self.singlePrefsFinanceVat.setGladeXml(self.xml)
        self.singlePrefsFinanceVat.setTreeFields( ['vat_name', 'vat_designation'] )
        self.singlePrefsFinanceVat.setStore( gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING,   gobject.TYPE_UINT) ) 
        self.singlePrefsFinanceVat.setTreeOrder('vat_name')
        self.singlePrefsFinanceVat.setTree(self.xml.get_widget('tree1') )
        #self.singlePrefsFinanceVat.setListHeader(['vat_name', 'designation', ])
        
        #singlePrefsFinanceTermsOfPayment(TOP)
 
 
        self.loadEntries(self.EntriesPrefsFinanceTop)
        self.singlePrefsFinanceTop.setEntries(self.getDataEntries(self.EntriesPrefsFinanceTop) )
        self.singlePrefsFinanceTop.setGladeXml(self.xml)
        self.singlePrefsFinanceTop.setTreeFields( ['number', 'designation'] )
        self.singlePrefsFinanceTop.setStore( gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING,   gobject.TYPE_UINT) ) 
        self.singlePrefsFinanceTop.setTreeOrder('number')
        self.singlePrefsFinanceTop.setTree(self.xml.get_widget('tree1') )
        #self.singlePrefsFinanceTop.setListHeader(['top_name', 'designation', ])

   
     #singlePrefsFinanceAcctInfo
        
        self.loadEntries(self.EntriesPrefsFinanceAcctInfo)
        self.singlePrefsFinanceAcctInfo.setEntries(self.getDataEntries(self.EntriesPrefsFinanceAcctInfo) )
        self.singlePrefsFinanceAcctInfo.setGladeXml(self.xml)
        self.singlePrefsFinanceAcctInfo.setTreeFields( ['account_number', 'designation'] )
        self.singlePrefsFinanceAcctInfo.setStore( gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING,  gobject.TYPE_UINT) ) 
        self.singlePrefsFinanceAcctInfo.setTreeOrder('account_number')
        self.singlePrefsFinanceAcctInfo.setListHeader([_('Account-Number'), _('Designation')])

        #self.singlePrefsFinanceAcctInfo.sWhere  ='where articles_number = ' + `self.singlePrefsFinance.ID`
        self.singlePrefsFinanceAcctInfo.setTree(self.xml.get_widget('tree1') )
  

        

        # Menu-items
        self.initMenuItems()

        # Close Menus for Tab

        self.addEnabledMenuItems('tabs','mi_vat1')
        self.addEnabledMenuItems('tabs','mi_top11')
        self.addEnabledMenuItems('tabs','mi_acct1')


        # seperate Menus
        self.addEnabledMenuItems('vat','mi_vat1')
        self.addEnabledMenuItems('top','mi_top1')
        self.addEnabledMenuItems('acct','mi_acct1')

        
        # enabledMenues for Vat
        self.addEnabledMenuItems('editVat','new1')
        self.addEnabledMenuItems('editVat','clear1')
        self.addEnabledMenuItems('editVat','print1')
        self.addEnabledMenuItems('editVat','edit1')

        # enabledMenues for Terms of Payment
        self.addEnabledMenuItems('editTop','TopNew1')
        self.addEnabledMenuItems('editTop','TopClear1')
        self.addEnabledMenuItems('editTop','TopEdit1')
    
       # enabledMenues for Account Info
        self.addEnabledMenuItems('editAcct','SalesNew1')
        self.addEnabledMenuItems('editAcct','SalesClear1')
        self.addEnabledMenuItems('editAcct','SalesEdit1')



        # tabs from notebook
        self.tabVat = 0
        self.tabTop = 1
        self.tabAcct = 2
        self.tabAcctPlan = 3
        
        
        print self.tabVat
        
        # start
        
        self.tabChanged()

  

    #Menu File
              
    def on_quit1_activate(self, event):
        print "exit tops v2"
        self.closeWindow()




  #Menu Vat
        
   
    def on_VatSave1_activate(self, event):
        print "save VAT  v2"
        self.singlePrefsFinanceVat.save()
        self.setEntriesEditable(self.EntriesPrefsFinanceVat, FALSE)

        self.tabChanged()
        
    def on_VatNew1_activate(self, event):
        print "new VAT  v2"
        self.singlePrefsFinanceVat.newRecord()
        self.setEntriesEditable(self.EntriesPrefsFinanceVat, TRUE)

    def on_VatEdit1_activate(self, event):
        self.setEntriesEditable(self.EntriesPrefsFinanceVat, TRUE)

    def on_VatClear1_activate(self, event):
        print "delete VAT  v2"
        self.singlePrefsFinanceVat.deleteRecord()

  #Menu Terms of Payment
        
   
    def on_TopSave1_activate(self, event):
        print "save TOP  v2"
        self.singlePrefsFinanceTop.save()
        self.setEntriesEditable(self.EntriesPrefsFinanceTop, FALSE)

        self.tabChanged()
        
    def on_TopNew1_activate(self, event):
        print "new TOP  v2"
        self.singlePrefsFinanceTop.newRecord()
        self.setEntriesEditable(self.EntriesPrefsFinanceTop, TRUE)

    def on_TopEdit1_activate(self, event):
        self.setEntriesEditable(self.EntriesPrefsFinanceTop, TRUE)

    def on_TopClear1_activate(self, event):
        print "delete TOP  v2"
        self.singlePrefsFinanceTop.deleteRecord()



    def on_bImportAcct_clicked(self, event):
        self.importAcct()
    # signals from entry eAddressNumber
    
    def on_eAddressNumber_changed(self, event):
        print 'eAdrnbr changed'
        eAdrField = self.getWidget('eAddressField1')
        liAdr = self.singleAddress.getAddress(long(self.getWidget( 'eAddressNumber').get_text()))
        eAdrField.set_text(liAdr[0] + ', ' + liAdr[4])


    # search button
    def on_bSearch_clicked(self, event):
        self.out( 'Searching ....', self.ERROR)
        sNumber = self.getWidget('eFindNumber').get_text()
        sDesignation = self.getWidget('eFindDesignation').get_text()
        self.out('Name and City = ' + sNumber + ', ' + sDesignation, self.ERROR)
        self.singlePrefsFinance.sWhere = 'where number ~* \'.*' + sNumber + '.*\' and designation ~* \'.*' + sDesignation + '.*\''
        self.out(self.singlePrefsFinance.sWhere, self.ERROR)
        self.refreshTree()

                     

    def refreshTree(self):
        self.singlePrefsFinanceVat.disconnectTree()
        self.singlePrefsFinanceTop.disconnectTree()
        self.singlePrefsFinanceAcctInfo.disconnectTree()
        
        if self.tabOption == self.tabVat:
            
            self.singlePrefsFinanceVat.connectTree()
            self.singlePrefsFinanceVat.refreshTree()


        elif self.tabOption == self.tabTop:
            #self.singlePrefsFinanceTop.sWhere  ='where articles_number = ' + `int(self.singlePrefsFinance.ID)`
            self.singlePrefsFinanceTop.connectTree()
            self.singlePrefsFinanceTop.refreshTree()


        elif self.tabOption == self.tabAcct:
            self.singlePrefsFinanceAcctInfo.connectTree()
            self.singlePrefsFinanceAcctInfo.refreshTree()
 
 
    def filesel_destroy(self,w):
        self.filesel.destroy()
  
     
    def filesel_ok(self, w):
        sFile =  self.filesel.get_filename()
        self.filesel_destroy(w)
        if sFile:
            print "%s" % sFile
            doc = self.readDocument(sFile)
            if doc:
                #print doc.toxml()
                rn = self.getRootNode(doc)
                if rn:
                    #print rn[0].toxml()
                    acctNodes = self.getNodes(rn[0],'account')
                    if acctNodes:
                        plan_number = 'SK-03'
                        for an in acctNodes:
                            #print '-----------------------------'
                            #print an.toxml()
                            dicAcct = {}
                            dictAcct['account_plan_number'] = [plan_number,'string']

                            dicAcct['account_number'] = [self.getData(self.getNodes(an,'account_number')[0]),'string']
                            dicAcct['type'] = [self.getData(self.getNodes(an,'type')[0]),'string']
                            dicAcct['eg'] = [self.getData(self.getNodes(an,'eg')[0]),'string']
                            dicAcct['designation'] = [self.getData(self.getNodes(an,'designation')[0]),'string']
                            print `dicAcct`
                            if dicAcct:
                                if dicAcct['account_number'][0] == 'EMPTY':
                                    dicAcct = {}
                                elif dicAcct['type'][0] == 'EMPTY': 
                                    dicAcct['type'] = [' ', 'string']
                                elif dicAcct['eg'][0] == 'EMPTY': 
                                    dicAcct['eg'] = [' ', 'string']
                                elif dicAcct['designation'][0] == 'EMPTY': 
                                    dicAcct['type'] = {}
                                elif dicAcct['account_plan_number'][0] == 'EMPTY': 
                                    dicAcct = {}
                              
                            #dicAcct = {'eg': ' ', 'type': [u'V', 'string'], 'account_number': [u'1', 'string'], 'designation': [u'Aufwendungen fuer die Ingangsetzung und Erweiterung des Geschaeftsbetriebes', 'string']}
                            print 'After: ', `dicAcct`         
                            if dicAcct:
                                self.rpc.callRP('src.Finances.py_updateAccountInfo',dicAcct, self.dicUser)
                                #print self.rpc.callRP('src.sql.py_test', self.dicUser)
                                
                                
    def importAcct(self):
       
        
        self.filesel.connect("destroy", self.filesel_destroy)
        
        # Connect the ok_button to file_ok_sel method
        self.filesel.ok_button.connect("clicked", self.filesel_ok)
    
        # Connect the cancel_button to destroy the widget
        self.filesel.cancel_button.connect("clicked",self.filesel_destroy )
    
  
        self.filesel.show()
         
    def tabChanged(self):
        print 'tab changed to :'  + str(self.tabOption)
        if self.tabOption == self.tabVat:
            #Address
            self.disableMenuItem('tabs')
            self.enableMenuItem('vat')
            print 'Seite 0'
            self.editAction = 'editVat'
            
        elif self.tabOption == self.tabTop:
            #Partner
            self.disableMenuItem('tabs')
            self.enableMenuItem('top')
            self.editAction = 'editTop'
            print 'Seite 1'
            
        elif self.tabOption == self.tabAcct:
            self.disableMenuItem('tabs')
            self.enableMenuItem('sales')
            self.editAction = 'editSales'
            # fill box_entry
            
            print 'Seite 2'
            
        # refresh the Tree
        self.refreshTree()
        self.enableMenuItem(self.editAction)
        self.editEntries = FALSE
