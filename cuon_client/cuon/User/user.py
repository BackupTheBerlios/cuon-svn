 # -*- coding: utf-8 -*-

##Copyright (C) [2003-2005]  [Juergen Hamel, D-32584 Loehne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 
import os.path
import cuon.TypeDefs
#from cuon.Windows.windows import windows
from cuon.Databases.dumps import dumps
from gtk import TRUE, FALSE

class User:
    """
    @author: Jürgen Hamel
    @organization: Cyrus-Computer GmbH, D-32584 Löhne
    @copyright: by Jürgen Hamel
    @license: GPL ( GNU GENERAL PUBLIC LICENSE )
    @contact: jh@cyrus.de
    """
    def __init__(self):
        """
        Variables:
            1. self.userName: Name of the User
        """
#        self.openDB()
#        self.td = self.loadObject('td')
#        self.closeDB()
#        self.rpc = cuon.XMLRPC.xmlrpc.myXmlRpc()

        self.userName = 'EMPTY'
        self.dicTest = {}
        
        self.sessionID = 0
        #self.openDB()
        #self.td = self.loadObject('td')
        #self.closeDB()
        self.Database = 'cuon'
        # setting for locales
        self.userLocales ='de'
        self.userEncoding = 'utf-8'
        self.Encode = True
        self.userPdfEncoding = 'latin-1'
        self.userType = 'cuon'        
        self.userDateFormatString = "%d.%m.%Y"
        self.userDateTimeFormatString = "%d.%m.%Y %H:%M"
        self.userDateTimeFormatEncoding = "%Y.%m.%d %H:%M:%S"
        self.userTimeFormatString = "%H:%M"
        self.sDebug = 'NO'
        
        self.serverAddress = None
        self.userSQLDateFormat = 'DD.MM.YYYY'
        self.userSQLTimeFormat = 'HH24:MI'
        self.userSQLDateTimeFormat = 'DD.MM.YYYY HH24:MI'
        self.prefPath = {}
        self.prefApps = {}
        self.serverSqlDateFormat = '%Y-%m-%d'
        self.client = 0
        
        
        self.prefPath['tmp'] =  os.path.normpath(os.environ['CUON_HOME']) + '/'  

        self.prefPath['StandardInvoice1'] =  os.path.normpath(os.environ['CUON_HOME'] + '/' +  'Invoice' )
        self.prefPath['StandardSupply1'] =  os.path.normpath(os.environ['CUON_HOME'] + '/' +  'Delivery' )
        self.prefPath['StandardPickup1'] =  os.path.normpath(os.environ['CUON_HOME'] + '/' +  'Pickup' )
        self.prefPath['AddressLists'] =  os.path.normpath(os.environ['CUON_HOME'] + '/' +  'address' )
        self.prefPath['ArticleLists'] =  os.path.normpath(os.environ['CUON_HOME'] + '/' +  'article' )
        self.prefPath['StandardCAB1'] =  os.path.normpath(os.environ['CUON_HOME'] + '/' +  'address' )

        self.prefPath['ReportStandardInvoice1'] =  os.path.normpath(os.environ['CUON_HOME'] + '/' +  'Reports' )
        self.prefPath['ReportStandardSupply1'] =  os.path.normpath(os.environ['CUON_HOME'] + '/' +  'Reports' )
        self.prefPath['ReportStandardPickup1'] =  os.path.normpath(os.environ['CUON_HOME'] + '/' +  'Reports' )
        
        self.prefPath['ReportAddressLists'] =  os.path.normpath(os.environ['CUON_HOME'] + '/' +  'Reports' )
        self.prefPath['ReportArticleLists'] =  os.path.normpath(os.environ['CUON_HOME'] + '/' +  'Reports' )
        self.prefPath['ReportStockGoodsLists'] =  os.path.normpath(os.environ['CUON_HOME'] + '/' +  'Reports' )
        self.prefPath['ReportStandardFinancesCAB'] =  os.path.normpath(os.environ['CUON_HOME'] + '/' +  'Reports' )
        self.prefApps['PDF']='/usr/bin/gpdf'
        
        
        self.prefColor = {'FG':0, 'BG':0}

        self.prefDMS = {}
        #Scanner prefs
        self.prefDMS['scan_device'] = 'plustek:libusb:002:002'
        self.prefDMS['scan_r'] = {'x':1024.0, 'y':768.0}
        self.prefDMS['scan_mode'] = 'color'
        self.prefDMS['scan_contrast'] = 0.0
        self.prefDMS['scan_brightness'] = 0.0
        self.prefDMS['scan_white_level'] = 0.0
        self.prefDMS['scan_depth'] = 24
        self.prefDMS['scan_resolution'] = 300
        
        # Executables
        self.prefDMS['exe'] = {}
        self.prefDMS['exe']['writer'] = '/usr/bin/oowriter'
        self.prefDMS['exe']['calc'] = '/usr/bin/oocalc'
        self.prefDMS['exe']['draw'] = '/usr/bin/oodraw'
        self.prefDMS['exe']['impress'] = '/usr/bin/ooimpress'
        self.prefDMS['exe']['image'] = '/usr/bin/gimp'
        self.prefDMS['exe']['music'] = '/usr/bin/xmms'
        self.prefDMS['exe']['ogg'] = '/usr/bin/xmms'
        self.prefDMS['exe']['wav'] = '/usr/bin/xmms'
        self.prefDMS['exe']['pdf'] = '/usr/bin/evince'
        self.prefDMS['exe']['tex'] = '/usr/bin/xemacs'
        self.prefDMS['exe']['ltx'] = '/usr/bin/xemacs'
        self.prefDMS['exe']['txt'] = '/usr/bin/gedit'
        self.prefDMS['exe']['flowchart'] = '/usr/bin/dia'



        # File-format
        self.prefDMS['fileformat'] = {}
        self.prefDMS['fileformat']['scanImage'] = {'format':'Image Scanner', 'suffix':['NONE'], 'executable': 'INTERN'}
        self.prefDMS['fileformat']['oow'] =  {'format':'Open Office Writer',  'suffix':['sxw', 'sdw'], 'executable': self.prefDMS['exe']['writer'] }
        self.prefDMS['fileformat']['ooc'] =  {'format':'Open Office Calc',  'suffix':['sxc','sdc'], 'executable': self.prefDMS['exe']['calc']}
        self.prefDMS['fileformat']['ood'] =  {'format':'Open Office Draw',  'suffix':['sxd'], 'executable': self.prefDMS['exe']['draw']}
        self.prefDMS['fileformat']['ooi'] =  {'format':'Open Office Impress', 'suffix':['sxi'], 'executable': self.prefDMS['exe']['impress']}
        self.prefDMS['fileformat']['gimp'] =  {'format':'Gimp',  'suffix':['xcf','jpg','gif','png'], 'executable': self.prefDMS['exe']['image']}
        self.prefDMS['fileformat']['mp3'] =  {'format':'MP3',  'suffix':['mp3'], 'executable': self.prefDMS['exe']['music']}
        self.prefDMS['fileformat']['ogg'] =  {'format':'OGG',  'suffix':['ogg'], 'executable': self.prefDMS['exe']['ogg']}
        self.prefDMS['fileformat']['wav'] =  {'format':'WAV',  'suffix':['wav'], 'executable': self.prefDMS['exe']['wav']}
        self.prefDMS['fileformat']['txt'] =  {'format':'Text',  'suffix':['txt'], 'executable': self.prefDMS['exe']['txt']}
        self.prefDMS['fileformat']['tex'] =  {'format':'TEX',  'suffix':['tex',], 'executable': self.prefDMS['exe']['tex']}
        self.prefDMS['fileformat']['latex'] =  {'format':'LATEX',  'suffix':['ltx',], 'executable': self.prefDMS['exe']['ltx']}
        self.prefDMS['fileformat']['pdf'] =  {'format':'Adobe PDF',  'suffix':['pdf',], 'executable': self.prefDMS['exe']['pdf']}

        self.prefDMS['fileformat']['dia'] =  {'format':'DIA ', 'suffix':['dia'], 'executables': self.prefDMS['exe']['flowchart']}
        
        
        
        
 

        
        
        self.dicUser = {}
        self.sqlDicUser = {}
        
        self.dicUserKeys = {}
        
        
        
        # setting for files and path
        self.pathAddressPhoneListing1 = os.path.abspath('.')
        print  self.pathAddressPhoneListing1
        
        # setting keys for eachWindow
        self.setDicUserKeys('address_edit','e')
        self.setDicUserKeys('address_delete','d')
        self.setDicUserKeys('address_new','n')
        self.setDicUserKeys('address_print','p')

       
        self.setDicUserKeys('address_partner_edit','e')
        self.setDicUserKeys('address_partner_delete','d')
        self.setDicUserKeys('address_partner_new','n')
        self.setDicUserKeys('address_partner_print','p')
    
        #address
        
        # articles
        
        self.setDicUserKeys('articles_edit','e')
        self.setDicUserKeys('articles_delete','d')
        self.setDicUserKeys('articles_new','n')
        self.setDicUserKeys('articles_print','p')

        self.setDicUserKeys('articles_purchase_edit','e')
        self.setDicUserKeys('articles_purchase_delete','d')
        self.setDicUserKeys('articles_purchase_new','n')
        self.setDicUserKeys('articles_purchase_print','p')

        # staff
        self.setDicUserKeys('staff_edit','e')
        self.setDicUserKeys('staff_delete','d')
        self.setDicUserKeys('staff_new','n')
        self.setDicUserKeys('staff_print','p')

        self.setDicUserKeys('staff_fee_edit','e')
        self.setDicUserKeys('staff_fee_delete','d')
        self.setDicUserKeys('staff_fee_new','n')
        self.setDicUserKeys('staff_fee_print','p')

        # project
        self.setDicUserKeys('project_edit','e')
        self.setDicUserKeys('project_delete','d')
        self.setDicUserKeys('project_new','n')
        self.setDicUserKeys('project_print','p')


        self.refreshDicUser()

        
        
    def refreshDicUser(self):
        '''
        set self.dicuser to actual values
        '''
        self.dicUser['Locales'] = self.userLocales
        self.dicUser['Database'] = self.Database
        self.dicUser['Encoding'] = self.userEncoding
        self.dicUser['Encode'] = self.Encode
        self.dicUser['DateTimeformatString'] = self.userDateTimeFormatString
        self.dicUser['DateformatString'] = self.userDateFormatString
        self.dicUser['DateTimeformatEncoding'] = self.userDateTimeFormatEncoding
        #self.dicUser['serverAddress'] = self.serverAddress
        self.dicUser['SQLDateFormat'] = self.userSQLDateFormat
        self.dicUser['SQLTimeFormat'] = self.userSQLTimeFormat
        self.dicUser['SQLDateTimeFormat'] = self.userSQLDateTimeFormat
        self.dicUser['Name'] = self.userName
        #self.dicUser['Password'] = self.userPassword
        self.dicUser['Debug'] = self.sDebug
        
        self.dicUser['prefPath'] = self.prefPath
        self.dicUser['prefApps'] = self.prefApps
        
        self.dicUser['SessionID'] = self.getSessionID()
        self.dicUser['userType'] = self.userType
        self.dicUser['prefColor'] = self.prefColor
        self.dicUser['prefDMS'] = self.prefDMS
        
        self.dicUser['client'] = self.client
        
        
        self.refreshSqlDicUser()
        
    def refreshSqlDicUser(self):
        self.sqlDicUser['Name'] = self.userName
        self.sqlDicUser['SessionID'] = self.getSessionID()
        self.sqlDicUser['userType'] = self.userType
        self.sqlDicUser['client'] = self.client
        self.sqlDicUser['Locales'] = self.userLocales
        self.sqlDicUser['Database'] = self.Database
        self.sqlDicUser['Encoding'] = self.userEncoding
        self.sqlDicUser['Encode'] = self.Encode
        self.sqlDicUser['DateTimeformatString'] = self.userDateTimeFormatString
        self.sqlDicUser['DateformatString'] = self.userDateFormatString

        self.sqlDicUser['DateTimeformatEncoding'] = self.userDateTimeFormatEncoding
        #self.sqlDicUser['serverAddress'] = self.serverAddress
        self.sqlDicUser['SQLDateFormat'] = self.userSQLDateFormat
        self.sqlDicUser['SQLTimeFormat'] = self.userSQLTimeFormat
        self.sqlDicUser['SQLDateTimeFormat'] = self.userSQLDateTimeFormat
        
    def getDicUser(self):
        '''
        @return: Dictionary with user-infos
        '''
  
        return self.dicUser


    def getSqlDicUser(self):
        return self.sqlDicUser
        

    def getDicUserKeys(self):
        
        return self.dicUserKeys
        
    def setDicUserKeys(self, dKey, sKey):
        self.dicUserKeys[dKey] = sKey

        
        
    def setUserName(self, s):
        """@param s: Name of the User """
        self.userName = s
        self.refreshDicUser()

    def getUserName(self):
        """@return: Name of the user"""
        return self.userName

   
    
        
    def setSessionID(self, sid):
        ''' 
        set the sessionID 
        @param sid: session-id
        '''
        self.sessionID = sid
        self.refreshDicUser()
        
		
    def getSessionID(self):
        return self.sessionID
		
		
    def setDebug(self, sDebug='NO'):
        self.sDebug = sDebug
        print 'sDebug(User)  = ' + sDebug
        self.refreshDicUser()
        
        
    
    def getDebug(self):
        if self.sDebug == 'YES':
            return TRUE
        else:
            return FALSE
        
