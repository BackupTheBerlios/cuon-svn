##Copyright (C) [2003]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 
import os.path

from cuon.Windows.windows import windows

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
        
        self.userName = 'EMPTY'
        self.userPassword = 'EMPTY'
        #self.openDB()
        #self.td = self.loadObject('td')
        #self.closeDB()
        # setting for locales
        self.userLocales ='de'
        self.userEncoding = 'utf-8'
        self.userPdfEncoding = 'latin-1'
        
        self.userDateTimeFormatString = "%d.%m.%Y"
        self.userTimeFormatString = "%H:%M"
        
        self.serverAddress = None
        self.userSQLDateFormat = 'DD.MM.YYYY'
        self.userSQLTimeFormat = 'HH24:MI'
        self.prefPath = {}

        self.prefPath['StandardInvoice1'] =  os.path.normpath(os.environ['CUON_HOME'] + '/' +  'Invoice' )
        self.prefPath['StandardSupply1'] =  os.path.normpath(os.environ['CUON_HOME'] + '/' +  'Delivery' )
        self.prefPath['StandardPickup1'] =  os.path.normpath(os.environ['CUON_HOME'] + '/' +  'Pickup' )
        self.prefPath['AddressLists'] =  os.path.normpath(os.environ['CUON_HOME'] + '/' +  'address' )

        self.prefPath['ReportStandardInvoice1'] =  os.path.normpath(os.environ['CUON_HOME'] + '/' +  'Reports' )
        self.prefPath['ReportStandardSupply1'] =  os.path.normpath(os.environ['CUON_HOME'] + '/' +  'Reports' )
        self.prefPath['ReportStandardPickup1'] =  os.path.normpath(os.environ['CUON_HOME'] + '/' +  'Reports' )
        
        self.prefPath['ReportAddressLists'] =  os.path.normpath(os.environ['CUON_HOME'] + '/' +  'Reports' )

        
        self.dicUser = {}
        
        
        
        # setting for files and path
        self.pathAddressPhoneListing1 = os.path.abspath('.')
        print  self.pathAddressPhoneListing1
        

        
    def refreshDicUser(self):
        self.dicUser['Locales'] = self.userLocales
        self.dicUser['Encoding'] = self.userEncoding
        self.dicUser['DateTimeformatString'] = self.userDateTimeFormatString
        #self.dicUser['serverAddress'] = self.serverAddress
        self.dicUser['SQLDateFormat'] = self.userSQLDateFormat
        self.dicUser['SQLTimeFormat'] = self.userSQLTimeFormat
        self.dicUser['Name'] = self.userName
        #self.dicUser['Password'] = self.userPassword
        self.dicUser['Password'] = self.getUserPassword()
        self.dicUser['prefPath'] = self.prefPath

    def getDicUser(self):
        return self.dicUser


 
        
    def setUserName(self, s):
        """@param s: Name of the User """
        self.userName = s
        self.refreshDicUser()

    def getUserName(self):
        """@return: Name of the user"""
        return self.userName

    
    def setUserPassword(self, s):
        """@param s: Password of the User """
        self.userPassword = s
        self.refreshDicUser()
  
    def getUserPassword(self):
        return self.userPassword

    
        
