# -*- coding: utf-8 -*-
##Copyright (C) [2003-2005]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 

import sys
sys.path.append('/usr/lib/python/')
sys.path.append('/usr/lib/python/site-packages/PIL')

from types import *
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import gobject
import string
import commands
import logging
from cuon.Windows.windows  import windows

import cuon.Misc.misc
import cuon.Misc.cuon_dialog

import os

try:
    import Image
except:
    print "no package Image found"
    print ""
    



class statswindow(windows):

    
    def __init__(self, allTables, module = 0, sep_info = None, dicVars={}, dicExtInfo={}):
        
        windows.__init__(self)

        self.ModulNumber = self.MN['Stats']
        self.dicVars = dicVars
        self.dicExtInfo = dicExtInfo
        
            
        self.allTables = allTables
        
        self.openDB()
        self.oUser = self.loadObject('User')
        self.closeDB()
        #print self.oUser
        #print '-.............................'
        self.loadGlade('stats.xml', 'StatsMainwindow')
        #self.win1 = self.getWidget('DMSMainwindow')


    def on_quit1_activate(self,event):
        self.closeWindow() 

    def on_adr_caller1_activate(self, event):
        
        dicExtInfo = {'sep_info':{'1':0},'Modul':self.MN['Address_stat_caller']}
        dicCaller = self.rpc.callRP('Address.getStatCaller',self.oUser.getSqlDicUser())
        Dms = cuon.DMS.dms.dmswindow(self.allTables, self.MN['Address_stat_caller'], {'1':-103}, dicCaller, dicExtInfo)
        
    def on_adr_rep1_activate(self, event):
        
        dicExtInfo = {'sep_info':{'1':0},'Modul':self.MN['Address_stat_rep']}
        dicRep = self.rpc.callRP('Address.getStatRep',self.oUser.getSqlDicUser())
        Dms = cuon.DMS.dms.dmswindow(self.allTables, self.MN['Address_stat_rep'], {'1':-104}, dicRep, dicExtInfo)
        
    def on_adr_salesman1_activate(self, event):
        
        dicExtInfo = {'sep_info':{'1':0},'Modul':self.MN['Address_stat_salesman']}
        dicSales = self.rpc.callRP('Address.getStatSalesman',self.oUser.getSqlDicUser())
        Dms = cuon.DMS.dms.dmswindow(self.allTables, self.MN['Address_stat_salesman'], {'1':-105}, dicSales, dicExtInfo)
        
    def on_order_misc1_activate(self, event):
        
        dicExtInfo = {'sep_info':{'1':0},'Modul':self.MN['Order_stat_misc1']}
        dicOrder = self.rpc.callRP('Order.getStatsMisc',self.oUser.getSqlDicUser())
        Dms = cuon.DMS.dms.dmswindow(self.allTables, self.MN['Order_stat_misc1'], {'1':-111}, dicOrder, dicExtInfo)
               
               
    def on_project_misc1_activate(self, event):
        
        dicExtInfo = {'sep_info':{'1':0},'Modul':self.MN['Project_stat_misc1']}
        dicProject = self.rpc.callRP('Projects.getStatsMisc',self.oUser.getSqlDicUser())
        Dms = cuon.DMS.dms.dmswindow(self.allTables, self.MN['Project_stat_misc1'], {'1':-121}, dicProject, dicExtInfo)
        
         
    def on_articles_misc1_activate(self, event):
        
        dicExtInfo = {'sep_info':{'1':0},'Modul':self.MN['Articles_stat_misc1']}
        dicArticle = self.rpc.callRP('Article.getStatsMisc',self.oUser.getSqlDicUser())
        Dms = cuon.DMS.dms.dmswindow(self.allTables, self.MN['Articles_stat_misc1'], {'1':-131}, dicArticle, dicExtInfo)
            
                       
        
        
                        
