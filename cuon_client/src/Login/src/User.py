# -*- coding: utf-8 -*-

##Copyright (C) [2003]  [Jürgen Hamel, D-32584 Löhne]

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
        
        self.sessionID = 0
        #self.openDB()
        #self.td = self.loadObject('td')
        #self.closeDB()
        # setting for locales
        self.userLocales ='de'
        self.userEncoding = 'utf-8'
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

        self.prefPath['tmp'] =  os.path.normpath(os.environ['CUON_HOME']) + '/'  

        self.prefPath['StandardInvoice1'] =  os.path.normpath(os.environ['CUON_HOME'] + '/' +  'Invoice' )
        self.prefPath['StandardSupply1'] =  os.path.normpath(os.environ['CUON_HOME'] + '/' +  'Delivery' )
        self.prefPath['StandardPickup1'] =  os.path.normpath(os.environ['CUON_HOME'] + '/' +  'Pickup' )
        self.prefPath['AddressLists'] =  os.path.normpath(os.environ['CUON_HOME'] + '/' +  'address' )

        self.prefPath['ReportStandardInvoice1'] =  os.path.normpath(os.environ['CUON_HOME'] + '/' +  'Reports' )
        self.prefPath['ReportStandardSupply1'] =  os.path.normpath(os.environ['CUON_HOME'] + '/' +  'Reports' )
        self.prefPath['ReportStandardPickup1'] =  os.path.normpath(os.environ['CUON_HOME'] + '/' +  'Reports' )
        
        self.prefPath['ReportAddressLists'] =  os.path.normpath(os.environ['CUON_HOME'] + '/' +  'Reports' )
        
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
        # File-format
        self.prefDMS['fileformat'] = {}
        self.prefDMS['fileformat']['scanImage'] = {'format':'Image Scanner', 'suffix':['NONE'], 'executable': 'INTERN'}
        self.prefDMS['fileformat']['oow'] =  {'format':'Open Office Writer',  'suffix':['sxw', 'sdw'], 'executable': '/usr/bin/oowriter'}
        self.prefDMS['fileformat']['ooc'] =  {'format':'Open Office Calc',  'suffix':['sxc','sdc'], 'executable': '/usr/bin/oocalc'}
        self.prefDMS['fileformat']['ood'] =  {'format':'Open Office Draw',  'suffix':['sxd'], 'executable': '/usr/bin/oodraw'}
        self.prefDMS['fileformat']['ooi'] =  {'format':'Open Office Impress', 'suffix':['sxi'], 'executable': '/usr/bin/ooimpress'}
        self.prefDMS['fileformat']['gimp'] =  {'format':'Gimp',  'suffix':['xcf'], 'executable': '/usr/bin/gimp'}
        self.prefDMS['fileformat']['mp3'] =  {'format':'MP3',  'suffix':['mp3'], 'executable': '/usr/bin/xmms'}
        self.prefDMS['fileformat']['ogg'] =  {'format':'OGG',  'suffix':['ogg'], 'executable': '/usr/bin/xmms'}
        self.prefDMS['fileformat']['txt'] =  {'format':'Text',  'suffix':['txt'], 'executable': '/usr/bin/gedit'}
        self.prefDMS['fileformat']['tex'] =  {'format':'TEX',  'suffix':['tex',], 'executable': '/usr/bin/xemacs'}
        self.prefDMS['fileformat']['latex'] =  {'format':'LATEX',  'suffix':['ltx',], 'executable': '/usr/bin/xemacs'}
        self.prefDMS['fileformat']['pdf'] =  {'format':'Adobe PDF',  'suffix':['pdf',], 'executable': '/usr/bin/gpdf'}

        self.prefDMS['fileformat']['dia'] =  {'format':'DIA ', 'suffix':['dia'], 'executables': '/usr/bin/dia'}
        
        
        
        
 

        
        self.dicUser = {}
        
        
        
        # setting for files and path
        self.pathAddressPhoneListing1 = os.path.abspath('.')
        print  self.pathAddressPhoneListing1
        

        
    def refreshDicUser(self):
        '''
        set self.dicuser to actual values
        '''
        self.dicUser['Locales'] = self.userLocales
        self.dicUser['Encoding'] = self.userEncoding
        self.dicUser['DateTimeformatString'] = self.userDateTimeFormatString
        self.dicUser['DateTimeformatEncoding'] = self.userDateTimeFormatEncoding
        #self.dicUser['serverAddress'] = self.serverAddress
        self.dicUser['SQLDateFormat'] = self.userSQLDateFormat
        self.dicUser['SQLTimeFormat'] = self.userSQLTimeFormat
        self.dicUser['SQLDateTimeFormat'] = self.userSQLDateTimeFormat
        self.dicUser['Name'] = self.userName
        #self.dicUser['Password'] = self.userPassword
        self.dicUser['Debug'] = self.sDebug
        self.dicUser['prefPath'] = self.prefPath
        self.dicUser['SessionID'] = self.getSessionID()
        self.dicUser['userType'] = self.userType
        self.dicUser['prefColor'] = self.prefColor
        self.dicUser['prefDMS'] = self.prefDMS
        
		
    def getDicUser(self):
        '''
        @return: Dictionary with user-infos
        '''
  
        return self.dicUser



 
        
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
        
