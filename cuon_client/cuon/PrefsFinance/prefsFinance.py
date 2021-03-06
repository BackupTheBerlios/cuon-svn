# -*- coding: utf-8 -*-
##Copyright (C) [2003]  [Jürgen Hamel, D-32584 Löhne]

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
#from gtk import True, False
import cuon.XMLRPC.xmlrpc

from cuon.Databases.SingleData import SingleData
import SinglePrefsFinanceVat
import SinglePrefsFinanceTop
import cuon.Finances.SingleAccountInfo
import cuon.Finances.SingleAccountPlan

import logging
from cuon.Windows.chooseWindows  import chooseWindows


class prefsFinancewindow(chooseWindows):

    
    def __init__(self, allTables, preparedTab = 0):

        chooseWindows.__init__(self)
        self.rpc = cuon.XMLRPC.xmlrpc.myXmlRpc()

        self.loadGlade('prefs_finance.xml')
        self.win1 = self.getWidget('PreferencesFinancesMainwindow')
        self.filesel = gtk.FileSelection(title=None)
  
        
        self.allTables = allTables
        self.singlePrefsFinanceVat = SinglePrefsFinanceVat.SinglePrefsFinanceVat(allTables)
        self.singlePrefsFinanceTop = SinglePrefsFinanceTop.SinglePrefsFinanceTop(allTables)
        self.singleFinanceAccountInfo = cuon.Finances.SingleAccountInfo.SingleAccountInfo(allTables)
        self.singleFinanceAccountPlan = cuon.Finances.SingleAccountPlan.SingleAccountPlan(allTables)
        # finances
        #self.sai = cuon.Finances.SingleAccountInfo.SingleAccountInfo(allTables)
        
        # self.singlePrefsFinance.loadTable()
              
        self.EntriesPrefsFinanceVat = 'prefs_finance_vat.xml'
        self.EntriesPrefsFinanceTop = 'prefs_finance_top.xml'
        self.EntriesPrefsFinanceAcctInfo = 'prefs_finance_acctinfo.xml'
        self.EntriesPrefsFinanceAcctPlan = 'prefs_finance_acctplan.xml'
                
        
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

   
     #singleFinanceAccountInfo
        
        self.loadEntries(self.EntriesPrefsFinanceAcctInfo)
        self.singleFinanceAccountInfo.setEntries(self.getDataEntries(self.EntriesPrefsFinanceAcctInfo) )
        self.singleFinanceAccountInfo.setGladeXml(self.xml)
        self.singleFinanceAccountInfo.setTreeFields( ['account_number', 'designation'] )
        self.singleFinanceAccountInfo.setStore( gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING,  gobject.TYPE_UINT) ) 
        self.singleFinanceAccountInfo.setTreeOrder('account_plan_number, account_number')
        self.singleFinanceAccountInfo.setListHeader([_('Account-Number'), _('Designation')])

        #self.singleFinanceAccountInfo.sWhere  ='where articles_number = ' + `self.singlePrefsFinance.ID`
        self.singleFinanceAccountInfo.setTree(self.xml.get_widget('tree1') )
  

        #singleFinanceAccountPlan
        
        self.loadEntries(self.EntriesPrefsFinanceAcctPlan)
        self.singleFinanceAccountPlan.setEntries(self.getDataEntries(self.EntriesPrefsFinanceAcctPlan) )
        self.singleFinanceAccountPlan.setGladeXml(self.xml)
        self.singleFinanceAccountPlan.setTreeFields( ['name', 'designation'] )
        self.singleFinanceAccountPlan.setStore( gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING,  gobject.TYPE_UINT) ) 
        self.singleFinanceAccountPlan.setTreeOrder('name')
        self.singleFinanceAccountPlan.setListHeader([_('Name'), _('Designation')])

        #self.singleFinanceAccountPlan.sWhere  ='where articles_number = ' + `self.singlePrefsFinance.ID`
        self.singleFinanceAccountPlan.setTree(self.xml.get_widget('tree1') )
       

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
        self.addEnabledMenuItems('editAcct','AcctNew1')
        self.addEnabledMenuItems('editAcct','AcctClear1')
        self.addEnabledMenuItems('editAcct','AcctEdit1')

       # enabledMenues for Account Plan
        self.addEnabledMenuItems('editPlan','AcctPlanNew1')
        self.addEnabledMenuItems('editPlan','AcctPlanClear1')
        self.addEnabledMenuItems('editPlan','AcctPlanEdit1')


        # tabs from notebook
        self.tabVat = 0
        self.tabTop = 1
        self.tabAcctInfo = 2
        self.tabAcctPlan = 3
        
        
        print self.tabVat
        
        # start
        self.tabOption == preparedTab
        self.tabChanged()

  

    #Menu File
              
    def on_quit1_activate(self, event):
        print "exit tops v2"
        self.closeWindow()




  #Menu Vat
        
   
    def on_VatSave1_activate(self, event):
        print "save VAT  v2"
        self.singlePrefsFinanceVat.save()
        self.setEntriesEditable(self.EntriesPrefsFinanceVat, False)

        self.tabChanged()
        
    def on_VatNew1_activate(self, event):
        print "new VAT  v2"
        self.singlePrefsFinanceVat.newRecord()
        self.setEntriesEditable(self.EntriesPrefsFinanceVat, True)

    def on_VatEdit1_activate(self, event):
        self.setEntriesEditable(self.EntriesPrefsFinanceVat, True)

    def on_VatClear1_activate(self, event):
        print "delete VAT  v2"
        self.singlePrefsFinanceVat.deleteRecord()

     
        
    def on_chooseTaxVat_activate(self, event):
        # choose TaxVat from other Modul
        self.setChooseValue(self.singlePrefsFinanceVat.ID)
        #print 'Group-ID = ' + `self.singleGroup.ID`
        self.closeWindow()
  #Menu Terms of Payment
        
        
   
    def on_TopSave1_activate(self, event):
        print "save TOP  v2"
        self.singlePrefsFinanceTop.save()
        self.setEntriesEditable(self.EntriesPrefsFinanceTop, False)

        self.tabChanged()
        
    def on_TopNew1_activate(self, event):
        print "new TOP  v2"
        self.singlePrefsFinanceTop.newRecord()
        self.setEntriesEditable(self.EntriesPrefsFinanceTop, True)

    def on_TopEdit1_activate(self, event):
        self.setEntriesEditable(self.EntriesPrefsFinanceTop, True)

    def on_TopClear1_activate(self, event):
        print "delete TOP  v2"
        self.singlePrefsFinanceTop.deleteRecord()


    def on_chooseTop_activate(self, event):
        # choose Top from other Modul
        self.setChooseValue(self.singlePrefsFinanceTop.ID)
        #print 'Group-ID = ' + `self.singleGroup.ID`
        self.closeWindow()    
        
    #Menu Acct Info
        
   
    def on_AcctInfoSave1_activate(self, event):
        print "save Info  v2"
        self.singleFinanceAccountInfo.save()
        self.setEntriesEditable(self.EntriesPrefsFinanceAcctInfo, False)

        self.tabChanged()
        
    def on_AcctInfoNew1_activate(self, event):
        print "new Info  v2"
        self.singleFinanceAccountInfo.newRecord()
        self.setEntriesEditable(self.EntriesPrefsFinanceAcctInfo, True)

    def on_AcctInfoEdit1_activate(self, event):
        self.setEntriesEditable(self.EntriesPrefsFinanceAcctInfo, True)

    def on_AcctInfoClear1_activate(self, event):
        print "delete Info  v2"
        self.singleFinanceAccountInfo.deleteRecord()



    #Menu Acct Plan
        
   
    def on_AcctPlanSave1_activate(self, event):
        print "save Plan  v2"
        self.singleFinanceAccountPlan.save()
        self.setEntriesEditable(self.EntriesPrefsFinanceAcctPlan, False)

        self.tabChanged()
        
    def on_AcctPlanNew1_activate(self, event):
        print "new Plan  v2"
        self.singleFinanceAccountPlan.newRecord()
        self.setEntriesEditable(self.EntriesPrefsFinanceAcctPlan, True)

    def on_AcctPlanEdit1_activate(self, event):
        self.setEntriesEditable(self.EntriesPrefsFinanceAcctPlan, True)

    def on_AcctPlanClear1_activate(self, event):
        print "delete Plan  v2"
        self.singleFinanceAccountPlan.deleteRecord()

    
    #def on_tree1_row_activated
    def on_tree1_row_activated(self, event, data1, data2):
        print 'DoubleClick tree1 Tab = ', self.tabOption
        if self.tabOption == self.tabVat:
            self.activateClick('chooseTaxVat', event)
        elif self.tabOption == self.tabTop:
            self.activateClick('chooseTOP', event)
               
    # import account-infos from xml-file

    def on_bImportAcct_clicked(self, event):
        self.importAcct()
    # signals from entry eAddressNumber
    
    def on_eAddressNumber_changed(self, event):
        print 'eAdrnbr changed'
        eAdrField = self.getWidget('eAddressField1')
        liAdr = self.singleAddress.getAddress(long(self.getWidget( 'eAddressNumber').get_text()))
        eAdrField.set_text(liAdr[0] + ', ' + liAdr[4])

    def on_eAcctAcctPlan_changed(self, entry):
        print entry
        s = entry.get_text()
        if s:
            des = self.rpc.callRP('Finances.get_AccountPlanNumber', s, self.oUser.getSqlDicUser())
            if des:
                self.getWidget('eAcctPlanText').set_text(des)
        else:
            self.getWidget('eAcctPlanText').set_text('')

    # search button
    def on_bSearch_clicked(self, event):
        self.out( 'Searching ....', self.ERROR)
        sName = self.getWidget('eFindName').get_text()
        sDesignation = self.getWidget('eFindDescription').get_text()
        #self.out('Name and City = ' + `sName` + ', ' + sDesignation, self.ERROR)
        self.Search = True
        self.tabChanged()
        
                     

    def refreshTree(self):
        self.singlePrefsFinanceVat.disconnectTree()
        self.singlePrefsFinanceTop.disconnectTree()
        self.singleFinanceAccountInfo.disconnectTree()
        self.singleFinanceAccountPlan.disconnectTree()
        
        if self.tabOption == self.tabVat:
            
            self.singlePrefsFinanceVat.connectTree()
            self.singlePrefsFinanceVat.refreshTree()


        elif self.tabOption == self.tabTop:
            #self.singlePrefsFinanceTop.sWhere  ='where articles_number = ' + `int(self.singlePrefsFinance.ID)`
            self.singlePrefsFinanceTop.connectTree()
            self.singlePrefsFinanceTop.refreshTree()


        elif self.tabOption == self.tabAcctInfo:
            self.singleFinanceAccountInfo.connectTree()
            self.singleFinanceAccountInfo.refreshTree()
 
        elif self.tabOption == self.tabAcctPlan:
            self.singleFinanceAccountPlan.connectTree()
            self.singleFinanceAccountPlan.refreshTree()
 
 
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
                        plan_number = self.getAttributValue(rn[0],'plan_number')
                        for an in acctNodes:
                            #print '-----------------------------'
                            #print an.toxml()
                            dicAcct = {}
                            dicAcct['account_plan_number'] = [plan_number,'string']

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
                                self.rpc.callRP('Finances.updateAccountInfo',dicAcct, self.dicSqlUser)
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
            
        elif self.tabOption == self.tabAcctInfo:
            self.disableMenuItem('tabs')
            self.enableMenuItem('info')
            self.editAction = 'editInfo'
            # SEARCH FOR iNFO
            if self.Search:
                self.singleFinanceAccountInfo.sWhere = 'where account_number ~* \'.*' + self.searchName + '.*\' and designation ~* \'.*' + self.searchDesignation + '.*\''
                #self.out(self.singlePrefsFinance.sWhere, self.ERROR)
        
            print 'Seite 2'
        elif self.tabOption == self.tabAcctPlan:
            self.disableMenuItem('tabs')
            self.enableMenuItem('plan')
            self.editAction = 'editPlan'
            # fill box_entry
            
            print 'Seite 3'
            
        # refresh the Tree
        self.refreshTree()
        self.enableMenuItem(self.editAction)
        self.editEntries = False
        self.Search = False
        
