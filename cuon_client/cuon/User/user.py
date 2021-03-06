 # -*- coding: utf-8 -*-

##Copyright (C) [2003-2005]  [Juergen Hamel, D-32584 Loehne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 
import os.path
import cuon.TypeDefs
#from cuon.Windows.windows import windows
from cuon.Databases.dumps import dumps
#from gtk import True, False
from cuon.TypeDefs.defaultValues import defaultValues
class User(defaultValues):
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
        defaultValues.__init__(self)
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
        self.userShowNews = True
        self.Encode = True
        self.userPdfEncoding = 'latin-1'
        self.userType = 'cuon'        
        self.userDateFormatString = "%d.%m.%Y"
        self.userDateTimeFormatString = "%d.%m.%Y %H:%M"
        self.userDateTimeFormatEncoding = "%Y.%m.%d %H:%M:%S"
        self.userTimeFormatString = "%H:%M"
        self.sDebug = 'NO'
        self.XMLRPC_TRY = 0
        
        
        self.serverAddress = None
        self.userSQLDateFormat = 'DD.MM.YYYY'
        self.userSQLTimeFormat = 'HH24:MI'
        self.userSQLDateTimeFormat = 'DD.MM.YYYY HH24:MI'
        self.userTimeOffset = '+0'
        self.prefPath = {}
        self.prefApps = {}
        self.prefLocale = {}
        self.Twitter = {}
        
        self.serverSqlDateFormat = '%Y-%m-%d'
        self.client = 0
        self.contact_id = 0
        
        self.prefPath['tmp'] =  os.path.normpath(self.td.cuon_path) + '/'  
        self.prefPath['pwd'] =  os.path.normpath(self.td.cuon_path) + '/work' 
        self.prefPath['templates'] =  os.path.normpath(self.td.cuon_path) + '/work/templates'
        self.prefPath['StandardInvoice1'] =  os.path.normpath(self.td.cuon_path + '/' +  'Invoice' )
        self.prefPath['StandardSupply1'] =  os.path.normpath(self.td.cuon_path + '/' +  'Delivery' )
        self.prefPath['StandardPickup1'] =  os.path.normpath(self.td.cuon_path + '/' +  'Pickup' )
        self.prefPath['AddressLists'] =  os.path.normpath(self.td.cuon_path + '/' +  'address' )
        self.prefPath['ArticleLists'] =  os.path.normpath(self.td.cuon_path + '/' +  'article' )
        self.prefPath['StandardCAB1'] =  os.path.normpath(self.td.cuon_path + '/' +  'address' )

        self.prefPath['ReportStandardInvoice1'] =  os.path.normpath(self.td.cuon_path + '/' +  'Reports' )
        self.prefPath['ReportStandardSupply1'] =  os.path.normpath(self.td.cuon_path + '/' +  'Reports' )
        self.prefPath['ReportStandardPickup1'] =  os.path.normpath(self.td.cuon_path + '/' +  'Reports' )
        
        self.prefPath['ReportAddressLists'] =  os.path.normpath(self.td.cuon_path + '/' +  'Reports' )
        self.prefPath['ReportArticleLists'] =  os.path.normpath(self.td.cuon_path + '/' +  'Reports' )
        self.prefPath['ReportStockGoodsLists'] =  os.path.normpath(self.td.cuon_path + '/' +  'Reports' )
        self.prefPath['ReportStandardFinancesCAB'] =  os.path.normpath(self.td.cuon_path + '/' +  'Reports' )
        
        
        self.prefColor = {'FG':'#000000', 'BG':'#FFFFFF', 'DUTY_FG':'#af0000','DUTY_BG':'#5feeec'}

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
        self.prefDMS['exe']['googleearth'] = 'googleearth'
        self.prefDMS['exe']['internet'] = '/usr/bin/firefox'
        self.prefDMS['exe']['html'] = '/usr/bin/bluefish'
        self.prefDMS['exe']['python'] = '/usr/bin/gedit'
        self.prefDMS['exe']['mindmap'] = '/usr/bin/vym'
        self.prefDMS['exe']['CAD'] = '/usr/bin/qcad'

        self.prefApps['PDF']=self.prefDMS['exe']['pdf']
        self.prefApps['printPickup'] = 'lpr'
        self.prefApps['printSupply'] = 'lpr'
        self.prefApps['printInvoice'] = 'lpr'
        self.prefApps['printNewsletter'] = 'lpr'
        self.prefApps['SIP'] = 'ekiga'
        self.prefApps['SIP_PARAMS'] = '-c'
        
        # Email 
        
        self.prefDMS['fileformat'] = {}
        self.setFileFormats()
        self.Email = {}
       
        
        self.Email['sendInvoice'] = False
        self.Email['sendSupply'] = False
        self.Email['sendGet'] = False
        self.Email['SSL']=False
        self.Email['From']='MyAddress@mail_anywhere.com'
        self.Email['Host']='mail_anywhere.com'
        self.Email['Port']='25'
        self.Email['LoginUser']='login'
        self.Email['Password']='secret'
        self.Email['Signatur']='NONE'
        self.Email['extPrg'] = 'thunderbird'
        self.Email['check_imap'] = False

        self.Email['ImapSSL']=False
        self.Email['ImapHost']='mail_anywhere.com'
        self.Email['ImapPort']='25'
        self.Email['ImapLoginUser']='login'
        self.Email['ImapPassword']='secret'
        self.Email['ImapCrypt']=0
        self.Email['Crypt']=0
        
        #Twitter
        self.Twitter = {}
        self.Twitter['TwitterName'] = 'cuonOne'
        self.Twitter['TwitterPassword'] = 'barner'
        
        self.Communications = {}
        self.Communications['textChat'] = '/usr/bin/slitechat'
        self.Communications['3DChat'] = '/usr/bin/phoenix'
        self.Communications['emailPrg'] = '/usr/bin/thunderbird'
        
        
        self.prefFinances = {}
        self.prefFinances['cash1'] = '16000'
        self.prefFinances['cash2'] = '16100'
        self.prefFinances['bank1'] = '18100'
        self.prefFinances['bank2'] = '18200'
        self.prefFinances['bank3'] = '18300'
        self.prefFinances['directDebit1'] = '18100'
        self.prefFinances['directDebit2'] = '18200'
        self.prefFinances['directDebit3'] = '18300'
        self.prefFinances['creditCard1'] = '18100'

        self.prefFinances['debits1'] = '12210'
        self.prefFinances['payable1'] = '33000'
        
        self.prefWindow = {}
        self.prefWindow ['MainMaximize'] = True
        
        self.prefLocale['TimeOffset'] = '+0'


        
        

        
        
        self.dicUser = {}
        self.sqlDicUser = {}
        
        self.dicUserKeys = {}
        
        
        
        # setting for files and path
        self.pathAddressPhoneListing1 = os.path.abspath('.')
        print  self.pathAddressPhoneListing1
        
        # setting keys for eachWindow
        #normal
        self.setDicUserKeys('edit','e')
        self.setDicUserKeys('delete','d')
        self.setDicUserKeys('new','n')
        self.setDicUserKeys('print','p')
        self.setDicUserKeys('save','s')
        
        
        #Address
        self.setDicUserKeys('address_edit','e')
        self.setDicUserKeys('address_delete','d')
        self.setDicUserKeys('address_new','n')
        self.setDicUserKeys('address_save','s')
        self.setDicUserKeys('address_print','p')

       
        self.setDicUserKeys('address_partner_edit','e')
        self.setDicUserKeys('address_partner_delete','d')
        self.setDicUserKeys('address_partner_new','n')
        self.setDicUserKeys('address_partner_print','p')
        self.setDicUserKeys('address_partner_save','s')
        
        
    
        
        
        # articles
        
        self.setDicUserKeys('articles_edit','e')
        self.setDicUserKeys('articles_delete','d')
        self.setDicUserKeys('articles_new','n')
        self.setDicUserKeys('articles_print','p')
        self.setDicUserKeys('articles_save','s')

        self.setDicUserKeys('articles_purchase_edit','e')
        self.setDicUserKeys('articles_purchase_delete','d')
        self.setDicUserKeys('articles_purchase_new','n')
        self.setDicUserKeys('articles_purchase_print','p')
        self.setDicUserKeys('articles_purchase_save','s')

        # Leasing
        self.setDicUserKeys('leasing_edit','e')
        self.setDicUserKeys('leasing_delete','d')
        self.setDicUserKeys('leasing_new','n')
        self.setDicUserKeys('leasing_print','p')
        self.setDicUserKeys('leasing_save','s')

        # staff
        self.setDicUserKeys('staff_edit','e')
        self.setDicUserKeys('staff_delete','d')
        self.setDicUserKeys('staff_new','n')
        self.setDicUserKeys('staff_print','p')
        self.setDicUserKeys('staff_save','s')

        self.setDicUserKeys('staff_fee_edit','e')
        self.setDicUserKeys('staff_fee_delete','d')
        self.setDicUserKeys('staff_fee_new','n')
        self.setDicUserKeys('staff_fee_print','p')
        self.setDicUserKeys('staff_fee_save','s')

 
        self.setDicUserKeys('staff_misc_edit','e')
        self.setDicUserKeys('staff_misc_delete','d')
        self.setDicUserKeys('staff_misc_new','n')
        self.setDicUserKeys('staff_misc_print','p')
        self.setDicUserKeys('staff_misc_save','s')

        self.setDicUserKeys('staff_vacation_edit','e')
        self.setDicUserKeys('staff_vacation_delete','d')
        self.setDicUserKeys('staff_vacation_new','n')
        self.setDicUserKeys('staff_vacation_print','p')
        self.setDicUserKeys('staff_vacation_save','s')

        self.setDicUserKeys('staff_disease_edit','e')
        self.setDicUserKeys('staff_disease_delete','d')
        self.setDicUserKeys('staff_disease_new','n')
        self.setDicUserKeys('staff_disease_print','p')
        self.setDicUserKeys('staff_disease_save','s')

        # project
        self.setDicUserKeys('project_edit','e')
        self.setDicUserKeys('project_delete','d')
        self.setDicUserKeys('project_new','n')
        self.setDicUserKeys('project_print','p')
        self.setDicUserKeys('project_save','s')


        # botany
        
        self.setDicUserKeys('botany_edit','e')
        self.setDicUserKeys('botany_delete','d')
        self.setDicUserKeys('botany_new','n')
        self.setDicUserKeys('botany_print','p')
        self.setDicUserKeys('botany_save','s')
        
        
        # hibernation
        
        self.setDicUserKeys('hibernation_edit','e')
        self.setDicUserKeys('hibernation_delete','d')
        self.setDicUserKeys('hibernation_new','n')
        self.setDicUserKeys('hibernation_save','s')
        self.setDicUserKeys('hibernation_print','p')
        
        # hibernation_plant
        
        self.setDicUserKeys('hibernation_plant_edit','f')
        self.setDicUserKeys('hibernation_plant_delete','g')
        self.setDicUserKeys('hibernation_plant_new','h')
        self.setDicUserKeys('hibernation_plant_save','a')
        self.setDicUserKeys('hibernation_plant_print','t')
        
         # grave
        
        self.setDicUserKeys('grave_edit','e')
        self.setDicUserKeys('grave_delete','d')
        self.setDicUserKeys('grave_new','n')
        self.setDicUserKeys('grave_save','s')
        self.setDicUserKeys('grave_print','p')
         # grave Spring
        
        self.setDicUserKeys('graveSpring_edit','e')
        self.setDicUserKeys('graveSpring_delete','d')
        self.setDicUserKeys('graveSpring_new','n')
        self.setDicUserKeys('graveSpring_save','s')
        self.setDicUserKeys('graveSpring_print','p')
        
        # grave Summer
        
        self.setDicUserKeys('graveSummer_edit','e')
        self.setDicUserKeys('graveSummer_delete','d')
        self.setDicUserKeys('graveSummer_new','n')
        self.setDicUserKeys('graveSummer_save','s')
        self.setDicUserKeys('graveSummer_print','p')
        
         # grave Autumn
        
        self.setDicUserKeys('graveAutumn_edit','e')
        self.setDicUserKeys('graveAutumn_delete','d')
        self.setDicUserKeys('graveAutumn_new','n')
        self.setDicUserKeys('graveAutumn_save','s')
        self.setDicUserKeys('graveAutumn_print','p')
        
         # grave Winter
        
        self.setDicUserKeys('graveWinter_edit','e')
        self.setDicUserKeys('graveWinter_delete','d')
        self.setDicUserKeys('graveWinter_new','n')
        self.setDicUserKeys('graveWinter_save','s')
        self.setDicUserKeys('graveWinter_print','p')
        
        
         # grave Holidays
        
        self.setDicUserKeys('graveHolidays_edit','e')
        self.setDicUserKeys('graveHolidays_delete','d')
        self.setDicUserKeys('graveHolidays_new','n')
        self.setDicUserKeys('graveHolidays_save','s')
        self.setDicUserKeys('graveHolidays_print','p')
        
         # grave Annual
        
        self.setDicUserKeys('graveAnnual_edit','e')
        self.setDicUserKeys('graveAnnual_delete','d')
        self.setDicUserKeys('graveAnnual_new','n')
        self.setDicUserKeys('graveAnnual_save','s')
        self.setDicUserKeys('graveAnnual_print','p')
         # grave Unique
        
        self.setDicUserKeys('graveUnique_edit','e')
        self.setDicUserKeys('graveUnique_delete','d')
        self.setDicUserKeys('graveUnique_new','n')
        self.setDicUserKeys('graveUnique_save','s')
        self.setDicUserKeys('graveUnique_print','p')
        
        
        self.refreshDicUser()

    def setFileFormats(self):
          
       

        # File-format
        self.prefDMS['fileformat'] = {}
        self.prefDMS['fileformat']['scanImage'] = {'format':'Image Scanner', 'suffix':['NONE'], 'executable': 'INTERN'}
        self.prefDMS['fileformat']['LINK'] =  {'format':'LINK', 'suffix':['NONE'], 'executables': 'INTERN'}
        self.prefDMS['fileformat']['oow'] =  {'format':'Open Office Writer',  'suffix':['sxw', 'sdw','odt','ott','doc','rtf'], 'executable': self.prefDMS['exe']['writer'] }
        self.prefDMS['fileformat']['ooc'] =  {'format':'Open Office Calc',  'suffix':['sxc','sdc','ods','ots','xls'], 'executable': self.prefDMS['exe']['calc']}
        self.prefDMS['fileformat']['ood'] =  {'format':'Open Office Draw',  'suffix':['sxd','odg','otg'], 'executable': self.prefDMS['exe']['draw']}
        self.prefDMS['fileformat']['ooi'] =  {'format':'Open Office Impress', 'suffix':['sti','sxi','odp','otp'], 'executable': self.prefDMS['exe']['impress']}
        self.prefDMS['fileformat']['gimp'] =  {'format':'Gimp',  'suffix':['xcf','jpg','gif','png'], 'executable': self.prefDMS['exe']['image']}
        self.prefDMS['fileformat']['mp3'] =  {'format':'MP3',  'suffix':['mp3'], 'executable': self.prefDMS['exe']['music']}
        self.prefDMS['fileformat']['ogg'] =  {'format':'OGG',  'suffix':['ogg'], 'executable': self.prefDMS['exe']['ogg']}
        self.prefDMS['fileformat']['wav'] =  {'format':'WAV',  'suffix':['wav'], 'executable': self.prefDMS['exe']['wav']}
        self.prefDMS['fileformat']['txt'] =  {'format':'Text',  'suffix':['txt'], 'executable': self.prefDMS['exe']['txt']}
        self.prefDMS['fileformat']['tex'] =  {'format':'TEX',  'suffix':['tex',], 'executable': self.prefDMS['exe']['tex']}
        self.prefDMS['fileformat']['latex'] =  {'format':'LATEX',  'suffix':['ltx',], 'executable': self.prefDMS['exe']['ltx']}
        self.prefDMS['fileformat']['pdf'] =  {'format':'Adobe PDF',  'suffix':['pdf',], 'executable': self.prefDMS['exe']['pdf']}
        
        self.prefDMS['fileformat']['dia'] =  {'format':'DIA', 'suffix':['dia'], 'executable': self.prefDMS['exe']['flowchart']}
        self.prefDMS['fileformat']['googleearth'] =  {'format':'KMZ', 'suffix':['kmz','kml','eta'], 'executable': self.prefDMS['exe']['googleearth']}
        self.prefDMS['fileformat']['html'] =  {'format':'HTML', 'suffix':['html','htm'], 'executable': self.prefDMS['exe']['html']}
        self.prefDMS['fileformat']['python'] =  {'format':'PYTHON', 'suffix':['py'], 'executable': self.prefDMS['exe']['python']}
        self.prefDMS['fileformat']['mindmap'] =  {'format':'MINDMAP', 'suffix':['vym', 'mm', 'mmp', 'emm', 'nmind', 'TWD'], 'executable': self.prefDMS['exe']['mindmap']}
        self.prefDMS['fileformat']['cad'] =  {'format':'CAD', 'suffix':['dwb', 'stp', 'step', 'dwg', 'dxf', 'igs', 'iges'], 'executable': self.prefDMS['exe']['CAD']}
        
        self.prefDMS['fileformat']['bin'] =  {'format':'BINARY', 'suffix':['bin'], 'executable': self.prefDMS['exe']['txt']}
        
        
        
    def refreshDicUser(self):
        '''
        set self.dicuser to actual values
        '''
        self.dicUser['Locales'] = self.userLocales
        self.dicUser['showNews'] = self.userShowNews
        self.dicUser['Database'] = self.Database
        self.dicUser['Encoding'] = self.userEncoding
        self.dicUser['Encode'] = self.Encode
        self.dicUser['DateTimeformatString'] = self.userDateTimeFormatString
        self.dicUser['DateformatString'] = self.userDateFormatString
        self.dicUser['DateTimeformatEncoding'] = self.userDateTimeFormatEncoding
        self.dicUser['TimeformatString'] = self.userTimeFormatString
        self.dicUser['TimeOffset'] = self.userTimeOffset

       
        
        
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
        self.dicUser['prefApps'] = self.prefApps
        
        self.dicUser['client'] = self.client
        self.dicUser['Email'] = self.Email
        self.dicUser['Twitter'] = self.Twitter
        self.dicUser['prefFinances'] = self.prefFinances
        self.dicUser['prefLocale'] = self.prefLocale
        self.dicUser['Communications'] = self.Communications
        self.dicUser['prefWindow'] = self.prefWindow
        
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
        self.sqlDicUser['Twitter'] = self.Twitter
        self.sqlDicUser['DateTimeformatEncoding'] = self.userDateTimeFormatEncoding
        self.sqlDicUser['SQLDateFormat'] = self.userSQLDateFormat
        self.sqlDicUser['SQLTimeFormat'] = self.userSQLTimeFormat
        self.sqlDicUser['SQLDateTimeFormat'] = self.userSQLDateTimeFormat

    def getUser(self, result):
        try:
            
            
            self.userLocales =  result['locales']
            if result['user_show_news'] == 'f' :
                self.userShowNews = False
            else:
                self.userShowNews = True
            
            if result['user_win_max'] == 'f':
                self.prefWindow['MainMaximize'] = False
            else:
                self.prefWindow['MainMaximize'] = True
                
            
            self.prefPath['StandardInvoice1'] =  result['path_to_docs_invoices']
            self.prefPath['StandardSupply1'] =  result['path_to_docs_supply']
            self.prefPath['StandardPickup1'] =  result['path_to_docs_pickup']
            self.prefPath['AddressLists'] =   result['path_to_docs_address_lists']
    
            self.prefPath['ReportStandardInvoice1'] =   result['path_to_report_invoices']
            self.prefPath['ReportStandardSupply1'] =  result['path_to_report_supply']
            self.prefPath['ReportStandardPickup1'] =  result['path_to_report_pickup']
    
            self.prefPath['ReportAddressLists'] =  result['path_to_report_address_lists']
    
            self.prefDMS['scan_device'] = result['scanner_device']
            self.prefDMS['scan_r'] = {'x':result['scanner_brx'], 'y':result['scanner_bry']}
            self.prefDMS['scan_mode'] = result['scanner_mode']
            self.prefDMS['scan_contrast'] = result['scanner_contrast']
            self.prefDMS['scan_brightness'] = result['scanner_brightness']
            self.prefDMS['scan_white_level'] = result['scanner_white_level']
            self.prefDMS['scan_depth'] = result['scanner_depth']
            self.prefDMS['scan_resolution'] = result['scanner_resolution']
            # Executables
            
            self.prefDMS['exe']['writer'] = result['exe_oowriter']
            self.prefDMS['exe']['calc'] = result['exe_oocalc']
            self.prefDMS['exe']['draw'] = result['exe_oodraw']
            self.prefDMS['exe']['impress'] = result['exe_ooimpress']
            self.prefDMS['exe']['image'] = result['exe_image']
            self.prefDMS['exe']['music'] = result['exe_music']
            self.prefDMS['exe']['ogg'] = result['exe_ogg']
            self.prefDMS['exe']['wav'] = result['exe_wav']
            self.prefDMS['exe']['pdf'] = result['exe_pdf']
            self.prefDMS['exe']['tex'] = result['exe_tex']
            self.prefDMS['exe']['ltx'] = result['exe_ltx']
            self.prefDMS['exe']['txt'] = result['exe_txt']
            self.prefDMS['exe']['flowchart'] = result['exe_flowchart']
            self.prefDMS['exe']['googleearth'] = result['exe_googleearth']
            self.prefDMS['exe']['internet'] = result['exe_internet']
            self.prefDMS['exe']['html'] = result['exe_html']
            self.prefDMS['exe']['python'] = result['exe_python']
            self.prefDMS['exe']['mindmap'] = result['exe_mindmap']
            self.prefDMS['exe']['CAD'] = result['exe_cad']
           
            self.prefColor['BG'] = result['color_bg']
            self.prefColor['FG'] = result['color_fg']
            self.prefColor['DUTY_BG'] = result['color_duty_bg']
            self.prefColor['DUTY_FG'] = result['color_duty_fg']
            
            self.prefLocale['TimeOffset'] = result['time_offset']
            
            
##            self.Email['From']='MyAddress@mail_anywhere.com'
##        self.Email['Host']='mail_anywhere.com'
##        self.Email['Port']='25'
##        self.Email['LoginUser']='login'
##        self.Email['Password']='secret'
##        self.Email['Signatur']='NONE'
            print 'User set email values: ',  result['user_mail_supply']  
            if result['user_mail_pickup'] in ['t', True, 'T', 'true']:
                self.Email['sendGet'] = True
            else:
                self.Email['sendGet'] = False
                
            if result['user_mail_supply'] in ['t', True, 'T', 'true']:
                 
                self.Email['sendSupply'] = True
                print 'Set sendSupply totrue,  ', self.Email['sendSupply']
            else:
                self.Email['sendSupply'] = False
                
            if result['user_mail_invoice'] in ['t', True, 'T', 'true']:
                self.Email['sendInvoice'] = True
            else:
                self.Email['sendInvoice'] = False
                    
           
            
            self.Email['From'] = result['email_user_address']
            self.Email['Host'] = result['email_user_host']
            self.Email['Port'] = result['email_user_port']
            self.Email['LoginUser'] = result['email_user_loginname']
            self.Email['Password'] = result['email_user_password']
            
            
            self.Email['ImapHost'] = result['email_user_imap_host']
            self.Email['ImapPort'] = result['email_user_imap_port']
            self.Email['ImapLoginUser'] = result['email_user_imap_loginname']
            self.Email['ImapPassword'] = result['email_user_imap_password']
            
            self.Email['Crypt'] = result['email_user_crypt']
            self.Email['ImapCrypt'] = result['email_user_imap_crypt']
            if result['user_imap_email_ssl'] =='t':
                self.Email['ImapSSL'] = True
            else:
                self.Email['ImapSSL'] = False
            if result['user_email_ssl'] =='t':
                self.Email['SSL'] = True
            else:
                self.Email['SSL'] = False
                
                
            self.Email['Signatur'] = result['email_user_signatur']
            self.Email['extPrg'] = result['email_ext_prg']
            if result['user_check_imap'] =='t':
                self.Email['check_imap'] = True
            else:
                self.Email['check_imap'] = False
            
            
            
            
            self.prefApps['PDF'] = self.prefDMS['exe']['pdf']
            print "prefApps['PDF'] 0=",  self.prefDMS['exe']['pdf']
            print "prefApps['PDF'] 1= ",  self.prefApps['PDF']
            
            self.prefApps['printPickup'] = result['exe_print_pickup']
            self.prefApps['printSupply'] = result['exe_print_supply']
            self.prefApps['printInvoice'] = result['exe_print_invoice']
            self.prefApps['printNewsletter'] = result['exe_print_newsletter']
            
        except Exception, param:
            print 'user.py,  getuser'
            print Exception
            print param
        self.setFileFormats()
        self.refreshDicUser()
        
        
        return self

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

    def getInternetUser(self):
        sqlDicUser2 = {}
        sqlDicUser2['Name'] = self.userName
        sqlDicUser2['SessionID'] = self.getSessionID()
        sqlDicUser2['userType'] = self.userType
        sqlDicUser2['Database'] = self.Database
        sqlDicUser2['client'] = self.client
        
        
        return sqlDicUser2
        
        
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
            return True
        else:
            return False
        
          
