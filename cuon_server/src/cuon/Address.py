import time
import time
from datetime import datetime
import random
import xmlrpclib
from twisted.web import xmlrpc
from basics import basics
import Database
import hashlib



class Address(xmlrpc.XMLRPC, basics):
    def __init__(self):
        basics.__init__(self)
        self.oDatabase = Database.Database()
    def xmlrpc_getComboBoxEntries(self, dicUser):
        cpServer, f = self.getParser(self.CUON_FS + '/clients.ini')
        liTrade0 = self.getConfigOption('CLIENT_' + `dicUser['client']`,'cbTrade', cpServer)
        liTurnover0 = self.getConfigOption('CLIENT_' + `dicUser['client']`,'cbTurnover', cpServer)
        liLegalform0 = self.getConfigOption('CLIENT_' + `dicUser['client']`,'cbLegalform', cpServer)
        liFashion0 = self.getConfigOption('CLIENT_' + `dicUser['client']`,'cbFashion', cpServer)
        liTrade = ['NONE']
        liTurnover = ['NONE']
        liLegalform = ['NONE']
        liFashion = ['NONE']
        if liTrade0:
            liTrade = liTrade0.split(',')
        if liTurnover0:
            liTurnover = liTurnover0.split(',')
        if liLegalform0:
            liLegalform = liLegalform0.split(',')
        if liFashion0:
            liFashion = liFashion0.split(',')
            
        return liFashion, liTrade,liTurnover,liLegalform
        
        
    def xmlrpc_getAddress(self,id, dicUser ):
    
        sSql = 'select address, lastname, lastname2,firstname, street, zip, city, ' 
        sSql = sSql + ' trim(country) || \'-\' || trim(zip) || \' \' || trim(city) as cityfield, state, country from address '
        sWhere = 'where id = ' + `id`
        sWhere = self.getWhere(sWhere, dicUser)
        sSql = sSql + sWhere
        
        return self.xmlrpc_executeNormalQuery(sSql, dicUser)

##    def xmlrpc_getAllActiveSchedul(self, dicUser):
##        
##        sSql = "select to_char(partner_schedul.schedul_date, \'" + dicUser['SQLDateFormat'] + "\') as date, "
##        sSql = sSql + "to_char(partner_schedul.schedul_time, \'" + dicUser['SQLTimeFormat'] + "\') as time, "
##        sSql = sSql + "address.city, partner_schedul.short_remark, partner_schedul.notes , "
##        sSql = sSql + "partner.lastname as partner_lastname, address.lastname as address_lastname, "
##        sSql = sSql + "address.lastname2 as address_lastname2, partner.firstname as partner_firstname "
##        sSql = sSql + " from partner, address, partner_schedul "
##        sW = " where partner.id = partnerid and address.id = partner.addressid and "
##        sW = sW + " process_status != 999 "
##        sSql = sSql + self.getWhere(sW, dicUser)
##        
##        sSql = sSql + " order by partner_schedul.schedul_date, partner_schedul.schedul_time " 
##        
##        return self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser)
##    
    def xmlrpc_getAllActiveSchedulByNames(self, dicUser, OrderType='Name', SelectStaff='All'):
        self.xmlrpc_getAllActiveSchedul(dicUser)
        
    def xmlrpc_getAllActiveSchedul(self, dicUser, OrderType='Name', SelectStaff='All', sChoice = 'New', sHash = 'NONE'):
        value = None
        rep_salesman = None
        result = 'NONE'
        sw = None
        SQL = True
        try:
                       
            cpServer, f = self.getParser(self.CUON_FS + '/user.cfg')
            #print cpServer
            #print cpServer.sections()
            
            value = self.getConfigOption('SHOW_SCHEDUL',dicUser['Name'], cpServer)
                       
            #print cpServer
            #print cpServer.sections()
            
            rep_salesman = self.getConfigOption('SHOW_REP_SALESMAN',dicUser['Name'], cpServer)
            
        except Exception, params:
            print 'Error by Schedul Read user.cfg'
            print Exception, params
        print dicUser['Name']    
        print 'value = ', value
        print 'rep_salesman = ', rep_salesman
        
            
        if value and value == 'NO':
            pass
        
        elif value:
                
                
            sSql = "select partner_schedul.schedul_date as date, partner_schedul.dschedul_date as date_norm, "
            sSql += "partner_schedul.id as id,  "
            sSql +=  "partner_schedul.schedul_time_begin as time_begin,partner_schedul.schedul_time_end as time_end, "
            sSql += " address.zip as a_zip, "
            sSql +=  "address.city as a_city, partner_schedul.short_remark as s_remark, partner_schedul.notes as s_notes, "
            sSql +=  "partner.lastname as p_lastname, address.lastname as a_lastname, "
        
            #
            sSql += " case  schedul_staff_id "
            sSql += " when 0 then  'NONE' else ( select staff.lastname || ', ' || staff.firstname from staff where staff.id = schedul_staff_id) END as schedul_name,  "
            
    
            sSql += "( select staff.lastname from staff where staff.id = (select rep_id from address where address.id = partner.addressid)) as rep_lastname, " 
            sSql += "( select staff.lastname from staff where staff.id = (select salesman_id from address where address.id = partner.addressid)) as salesman_lastname, " 
            sSql +=  "address.lastname2 as a_lastname2, partner.firstname as p_firstname "
            # from 
            sSql += " from partner, address, partner_schedul "
            
            # where
            if SelectStaff == 'All':
                sW = " where partner.id = partner_schedul.partnerid and address.id = partner.addressid and "
                sW += " process_status != 999 "
                
            else:
                sW = " where partner.id = partner_schedul.partnerid and address.id = partner.addressid and "
                sW +=  " process_status != 999 "
                sW += " and schedul_staff_id = " + SelectStaff + " "
            
            #print 'sChoice = ', sChoice
            if sChoice == 'New':
                sW += " and ( ( date_part('doy', to_date(partner_schedul.schedul_date, '" + dicUser['SQLDateFormat'] +"'))  >=  date_part('doy', now())"
                sW += " and date_part('year', to_date(partner_schedul.schedul_date, '" + self.DIC_USER['SQLDateFormat'] +"'))  >=  date_part('year', now()) ) or (date_part('year', to_date(partner_schedul.schedul_date, '" + self.DIC_USER['SQLDateFormat'] +"'))  >  date_part('year', now()) ))"
            elif sChoice == 'actualWeek':
                sW += " and  date_part('week', to_date(partner_schedul.schedul_date, '" + dicUser['SQLDateFormat'] +"'))  =  date_part('week', now())"
                sW += " and date_part('year', to_date(partner_schedul.schedul_date, '" + self.DIC_USER['SQLDateFormat'] +"'))  >=  date_part('year', now())"
            elif sChoice == 'Cancel':
                sW += ' and partner_schedul.process_status between 801 and 998 '
            elif sChoice == 'All':
                pass
#            if OrderType == 'rep_salesman':
#                if rep_salesman == 'ALL':
#                    #print 'dicUser = ',  dicUser['Name']
#                    sW += " and address.rep_id = (select id from staff where cuon_username = '" + dicUser['Name'] + "') "
#                    sW += ' and address.salesman_id > 0'
                
            if value != 'ALL':
                liValue = value.split(',')
                sW += ' and ( '
                for sOptValue in liValue:
                    sW += ' schedul_staff_id = ' + sOptValue + ' or '
                
                sW = sW[:len(sW)-4]
                sW += ')'
            sW += " and char_length(partner_schedul.schedul_date) = 10 "
            sSql = sSql + self.getWhere(sW, dicUser,Prefix='partner_schedul.')
                
                
            if OrderType == 'Name' or OrderType == 'rep_salesman':
                sSql = sSql + " order by schedul_name DESC, to_date(partner_schedul.schedul_date, '" + dicUser['SQLDateFormat'] +"') DESC , partner_schedul.schedul_time_begin DESC" 
            elif OrderType == 'Schedul' :
                sSql = sSql + " order by to_date(partner_schedul.schedul_date , '" + dicUser['SQLDateFormat'] +"') DESC  , schedul_name DESC,  partner_schedul.schedul_time_begin DESC " 
            #print sSql    
            if OrderType == 'rep_salesman':
                if not rep_salesman or rep_salesman == 'NO':
                    SQL = False
            if SQL:
                result = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser)
                
        elif value == None:
            pass
        if OrderType == 'rep_salesman':
                if not rep_salesman or rep_salesman == 'NO':
                    result = 'NONE'
                    
        m = hashlib.md5()
        m.update(`result`)
        sNewHash =  m.hexdigest()
        print sHash
        print sNewHash
        if sNewHash == sHash:
            result = ['NO_NEW_DATA']
            
         
        return result,  sNewHash
        
        
    def xmlrpc_getAllActiveContacts(self, dicUser):
        #caller_id = self.getConfigOption('caller_id',dicUser['name'],self.getParser(self.CUON_FS +'/user.cfg'))
        #print caller_id
        sSql = "select contact.schedul_date as date, contact.id as id, "
        
        sSql +=  "contact.schedul_time_begin as time, "
        sSql += "alarm_days, alarm_hours, alarm_minutes, "
        sSql +=  "address.city, contact.partnerid as partner_id, contact.address_id as address_id, "
        sSql +=  " (select lastname as partner_lastname from partner where contact.partnerid = id), address.lastname as address_lastname, "
        sSql +=  "address.lastname2 as address_lastname2 "
        sSql +=  " from  address, contact "
        sW = " where address.id = contact.address_id and "
        sW +=  " process_status = 0 and contacter_id = " + self.getStaffID(dicUser) + " "  
        sW += " and char_length(contact.schedul_date) = 10 "
        sSql = sSql + self.getWhere(sW, dicUser, Prefix='contact.')
        
        sSql = sSql + " order by contact.schedul_date, contact.schedul_time_begin " 
        
        liResult = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser)
        liResult2 = []
        if liResult not in ['NONE','ERROR']:
            for dicResult in liResult:
                try:
                    #print 'Len1 = ', len(liResult)
                    Hour, Minute = self.getTime(dicResult['time'])
                    
                    sDate = dicResult['date'] + ' ' + `Hour` + ':' + `Minute` +':00'
                    #print 'Date =',  sDate
                    if sDate.find('.') > 0:
                        sFormat = '%d.%m.%Y %H:%M:%S'
                    else:
                        sFormat = '%Y/%m/%d %H:%M:%S'
                    wakeDate = time.strptime(sDate,sFormat)
                    #print wakeDate

                    nD1 = datetime(wakeDate[0], wakeDate[1],wakeDate[2],wakeDate[3],wakeDate[4], wakeDate[5])
                    #print 'nD1', nD1
                    currentDate = time.localtime()
                    #print currentDate
                    nD2 = datetime(currentDate[0], currentDate[1],currentDate[2],currentDate[3],currentDate[4], currentDate[5])
                    #print nD2
                    nD3 = nD1 -nD2
                    #print nD3
                    #print '---------------------------------------------------'
                    #print 'Name = ', dicResult['address_lastname']
                    #print 'Differenz Tage', nD3.days
                    #print 'Differenz Sekunden', nD3.seconds
                    #print 'DB-alarm','Differenz', 'Datum', 'Current'
                   
                    #print dicResult['alarm_hours'] * 3600 + dicResult['alarm_minutes'] * 60, nD3.seconds, nD1, nD2 

                    ok = False
                    
                    if nD3.days < 0:
                        ok = True
                    
                    elif nD3.days >= 0:
                    
                        warningDays = nD3.days - dicResult['alarm_days'] 
                        
                        if warningDays < 0 : 
                            ok = True
                        elif warningDays > 0 : 
                            ok = False
                        elif warningDays == 0 :
                            AlarmSeconds = dicResult['alarm_hours'] * 3600 + dicResult['alarm_minutes'] * 60
                            #print 'AlarmSeconds = ', AlarmSeconds
                            #print 'nD3-seconds', nD3.seconds
                            #print 'Differenz' , nD3.seconds - AlarmSeconds
                            if nD3.seconds - AlarmSeconds < 0 :
                               ok = True
                    if  ok:
                        #print 'copy entry to  list'
                        liResult2.append(dicResult)
                        #print 'Len2 = ', len(liResult2)
                        
                    
                except Exception, params:
                    print 'xmlrpc_getAllActiveContacts'
                    print Exception, params
        
        
        #print liResult2
        #print 'Len3 = ', len(liResult2)

        return liResult2
        
        
    def xmlrpc_getNotes(self, addressid, dicUser):
        dicReturn = 'NONE'
        sSql = 'select * from address_notes where address_id = ' +  `addressid`
        liResult = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser)
        if liResult not in ['NONE','ERROR']:
            dicReturn = liResult[0]
            #print dicReturn
            for key in dicReturn.keys():
                #print "key = ",  key
                #rint key[0:5]
                if key[0:6] == 'notes_':
                   #print 'found notes'
                    #or i in range(len(dicReturn[key])):
                    #  print ord(dicReturn[key][i])
                    dicReturn[key] = dicReturn[key].replace(chr(10), '</text:p><text:p text:style-name="Standard">')
                    #print dicReturn[key]
        return dicReturn
        
    def xmlrpc_getMisc(self, addressid, dicUser):
        dicReturn = 'NONE'
        sSql = 'select * from addresses_misc where address_id = ' +  `addressid`
        liResult = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser)
        if liResult not in ['NONE','ERROR']:
            dicReturn = liResult[0]
            liFashion, liTrade,liTurnover,liLegalform = self.xmlrpc_getComboBoxEntries(dicUser)
            try:
                dicReturn['cb_fashion'] = liFashion[dicReturn['cb_fashion']]
                dicReturn['turnover'] = liTurnover[dicReturn['turnover']]
                dicReturn['trade'] = liTrade[dicReturn['trade']]
                dicReturn['legal_form'] = liLegalform[dicReturn['legal_form']]
            except:
                pass
                    
        return dicReturn
            
    def sentChangesPerMail(self, sModul, addressID, dicUser):
        if sModul == 'address_notes':
            
            value = None
            try:
                           
                cpServer, f = self.getParser(self.CUON_FS + '/user.cfg')
                #print cpServer
                #print cpServer.sections()
                
                value = self.getConfigOption('SENT_MAIL','representant', cpServer)
                
            except Exception, params:
                print 'Error by Schedul Read user.cfg'
                print Exception, params
            if value and addressID:
                dicRecord = self.xmlrpc_getNotes(addressID, dicUser)
                if dicRecord not in ['NONE','ERROR']:
                    pass
                
                
            
            
    def xmlrpc_getPartnerAddress(self, id, dicUser):
        sSql = 'select address, lastname, lastname2,firstname, street, zip, city, state, country, phone from partner where id = ' + `id`
        
        return self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser)
     
    def xmlrpc_getPartnerToAddress(self, id, dicUser):
        sSql = 'select * from partner where addressid = ' + `id`
        return self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser)


    def getPhonelist1(self, dicSearchlist, dicUser):
        import string 
        
        sSql = 'select lastname, lastname2, firstname, street, zip, city, phone, id from address'
        sSql3 = ''
        sSql4 = ''
        sSql5 = ''
        sSql6 = ''
        sSql7 = ''
        sSql8 = ''
        
        if dicSearchlist:
            sSql2 = sSql + ' where '
            if dicSearchlist['eLastnameFrom'] and dicSearchlist['eLastnameTo'] :
               lastnameFrom =  string.upper(dicSearchlist['eLastnameFrom']) 
               lastnameTo = string.lower(dicSearchlist['eLastnameTo']) 
                
               sSql3 = sSql2 + " lastname  between  '" +  lastnameFrom + "' and '" + lastnameTo +"'"  
               sSql = sSql3
        
            if dicSearchlist['eFirstnameFrom'] and dicSearchlist['eFirstnameTo'] :
               firstnameFrom =  string.upper(dicSearchlist['eFirstnameFrom']) 
               firstnameTo = string.lower(dicSearchlist['eFirstnameTo']) 
                
               
               sSql4 = " firstname  between  '" +  firstnameFrom + "' and '" + firstnameTo +"'"  
               if sSql3:
                   sSql4 = sSql3 + ' and ' + sSql4
               else:
                   sSql4 = sSql2 + sSql4
        
               sSql = sSql4
        
        
            if dicSearchlist['eCityFrom'] and dicSearchlist['eCityTo'] :
               cityFrom =  string.upper(dicSearchlist['eCityFrom']) 
               cityTo = string.lower(dicSearchlist['eCityTo']) 
                
               
               sSql5 = " city  between  '" +  cityFrom + "' and '" + cityTo +"'"  
               if sSql3 and not sSql4:
                   sSql5 = sSql3 + ' and ' + sSql5
               elif sSql3 and sSql4:
                   sSql5 = sSql4 + ' and ' + sSql5
               else:
                   sSql5 = sSql2 + sSql5
        
               sSql = sSql5
        
        
            if dicSearchlist['eCountryFrom'] and dicSearchlist['eCountryTo'] :
               countryFrom =  string.upper(dicSearchlist['eCountryFrom']) 
               countryTo = string.lower(dicSearchlist['eCountryTo']) 
                
           
                
               sSql6 = " country  between  '" +  countryFrom + "' and '" + countryTo +"'"  
               if sSql3 and not sSql4 and not sSql5:
                   sSql6 = sSql3 + ' and ' + sSql6
               elif sSql4 and not sSql5:
                   sSql6 = sSql4 + ' and ' + sSql6
               elif sSql5:
                   sSql6 = sSql5 + ' and ' + sSql6
               else:
                   sSql6 = sSql2 + sSql6
        
               sSql = sSql6
            if dicSearchlist['eInfoContains'] :
                sSql7 = " info ~*'" + dicSearchlist['eInfoContains'] +"' " 
                if sSql3 or sSql4 or sSql5 or sSql6:
                    sSql = sSql + " and " + sSql7
                else:
                    sSql = sSql2 + sSql7
                    
            if dicSearchlist['eNewsletterContains'] :
                sSql8 = " newsletter ~*'" + dicSearchlist['eNewsletterContains'] +"' " 
                if sSql3 or sSql4 or sSql5 or sSql6 or sSql7:
                    sSql = sSql + " and " + sSql8
                else:
                    sSql = sSql2 + sSql8
                    
        if dicSearchlist:
            sSql = sSql + self.getWhere("",dicUser,2)
        else:
            sSql = sSql + self.getWhere("",dicUser,1)
            
        
        
        sSql = sSql + ' order by lastname, lastname2, firstname, city'
        
        return self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser)
        
    def getPhonelist11(self, dicSearchlist, dicUser):
        import string 
        
        sSql = 'select address.id as address_id, address.lastname as address_lastname, address.lastname2 as ddress_lastname2, address.firstname as address_firstname, address.street as address_street, address.zip as ddress_zip, address.city as address_city, address.phone as address_phone, '
        sSql = sSql + ' partner.lastname as partner_lastname, partner.lastname2 as partner_lastname2, partner.firstname as partner_firstname, partner.street as partner_street, partner.zip as partner_zip, partner.city as partner_city, partner.phone as partner_phone '
        sSql = sSql + ' from address, partner '
        sSqlWhere = 'where partner.addressid = address.id  '
        sSql3 = ''
        sSql4 = ''
        sSql5 = ''
        sSql6 = ''
        
        if dicSearchlist:
            sSql2 = sSql + sSqlWhere + ' and '
            if dicSearchlist['eLastnameFrom'] and dicSearchlist['eLastnameTo'] :
               lastnameFrom =  string.upper(dicSearchlist['eLastnameFrom']) 
               lastnameTo = string.lower(dicSearchlist['eLastnameTo']) 
                
               sSql3 = sSql2 + " address.lastname  between  '" +  lastnameFrom + "' and '" + lastnameTo +"'"  
               sSql = sSql3
        
            if dicSearchlist['eFirstnameFrom'] and dicSearchlist['eFirstnameTo'] :
               firstnameFrom =  string.upper(dicSearchlist['eFirstnameFrom']) 
               firstnameTo = string.lower(dicSearchlist['eFirstnameTo']) 
                
               
               sSql4 = " address.firstname  between  '" +  firstnameFrom + "' and '" + firstnameTo +"'"  
               if sSql3:
                   sSql4 = sSql3 + ' and ' + sSql4
               else:
                   sSql4 = sSql2 + sSql4
        
               sSql = sSql4
        
        
            if dicSearchlist['eCityFrom'] and dicSearchlist['eCityTo'] :
               cityFrom =  string.upper(dicSearchlist['eCityFrom']) 
               cityTo = string.lower(dicSearchlist['eCityTo']) 
                
               
               sSql5 = " address.city  between  '" +  cityFrom + "' and '" + cityTo +"'"  
               if sSql3 and not sSql4:
                   sSql5 = sSql3 + ' and ' + sSql5
               elif sSql3 and sSql4:
                   sSql5 = sSql4 + ' and ' + sSql5
               else:
                   sSql5 = sSql2 + sSql5
        
               sSql = sSql5
        
        
            if dicSearchlist['eCountryFrom'] and dicSearchlist['eCountryTo'] :
               countryFrom =  string.upper(dicSearchlist['eCountryFrom']) 
               countryTo = string.lower(dicSearchlist['eCountryTo']) 
                
               
               sSql6 = " address.country  between  '" +  countryFrom + "' and '" + countryTo +"'"  
               if sSql3 and not sSql4 and not sSql5:
                   sSql6 = sSql3 + ' and ' + sSql6
               elif sSql4 and not sSql5:
                   sSql6 = sSql4 + ' and ' + sSql6
               elif sSql5:
                   sSql6 = sSql5 + ' and ' + sSql6
               else:
                   sSql6 = sSql2 + sSql6
        
               sSql = sSql6
        if dicSearchlist:
            sSql = sSql + self.getWhere("",dicUser,2,'partner.')
        else:
            sSql = sSql + self.getWhere("",dicUser,1,'partner.')
            
        #sSql = sSql + self.getWhere(sSqlWhere,dicUser,0,'partner.')
        sSql = sSql + ' order by address.lastname, address.lastname2, address.firstname, address.city, partner.lastname, partner.lastname2, partner.firstname, partner.city'
        print sSql
        return self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser)
    def xmlrpc_sendEmail2Address(self, dicEmail, liAttach, dicUser):
        print 'read Email-config'
        
    def xmlrpc_getNewsletterAddresses(self, NewsletterShortcut, dicUser):
        print NewsletterShortcut
        result = []
        sSql = "select address,lastname,lastname2,firstname,street,country,zip,city,letter_address from address where newsletter ~'.*" + NewsletterShortcut +".*'"
        sSql += self.getWhere("",dicUser,2)
        #print sSql
        result = self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
        if result in [ 'NONE','ERROR']:
            result = []
        #print 'result 1 ', result
        sSql = "select partner.address as address,partner.lastname as lastname, partner.lastname2 as lastname2, partner.firstname as firstname, partner.street as street, partner.country as country, partner.zip as zip , partner.city as city, partner.letter_address as letter_address, "
        sSql += " address.id as address_id, address.address as address_address, address.lastname as address_lastname, address.lastname2 as address_lastname2, address.firstname as address_firstname, address.zip as address_zip, address.city as address_city,address.street as address_street,address.country as address_country,address.letter_address as address_letter_address"
       
        sSql += " from partner, address where addressid = address.id and " 
        sSql += " partner.newsletter ~'.*" + NewsletterShortcut +".*' "
        sSql += self.getWhere("",dicUser,2,'partner.')
        #print sSql
        result2 = self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
        #print 'result2 = ', result2
        if result2 not in ['NONE','ERROR']:
            for res in result2:
                result.append(res)
        #print 'result3', result
        result4 = []
        for record in result:
            result4.append(self.addDateTime(record))
          
        return result4  
        
        
    def xmlrpc_getStatCaller(self, dicUser):
        result = {}
        CALLER_ID = None
        WITHOUT_ID = None
        MIN_SCHEDUL_YEAR = '2005'
        SCHEDUL_PROCESS_STATUS = None
        liCaller = None
        liSchedulProcessStatus = None
        iCentury = 2
        iDecade = 5
        iYear = 3
        iQuarter = 6
        iMonth = 14
        iWeek = 5
        
        try:
                       
            cpServer, f = self.getParser(self.CUON_FS + '/user.cfg')
            #print cpServer
            #print cpServer.sections()
            
            CALLER_ID = self.getConfigOption('STATS','CALLER_ID', cpServer)
            WITHOUT_ID = self.getConfigOption('STATS','WITHOUT_ID', cpServer)
        
        except:
            pass
        try:
                       
            cpServer, f = self.getParser(self.CUON_FS + '/clients.ini')
            #print cpServer
            #print cpServer.sections()
            
            SCHEDUL_PROCESS_STATUS = self.getConfigOption('CLIENT_' + `dicUser['client']`,'SchedulProcessStatus', cpServer)
            iValue = self.getConfigOption('CLIENT_' + `dicUser['client']`,'StatsCallerCentury', cpServer)
            if iValue:
                iCentury = int(iValue)
            
            iValue = self.getConfigOption('CLIENT_' + `dicUser['client']`,'StatsCallerDecade', cpServer)
            if iValue:
                iDecade = int(iValue)
            
            iValue = self.getConfigOption('CLIENT_' + `dicUser['client']`,'StatsCallerYear', cpServer)
            if iValue:
                iYear = int(iValue)
            
            iValue = self.getConfigOption('CLIENT_' + `dicUser['client']`,'StatsCallerQuarter', cpServer)
            if iValue:
                iQuarter = int(iValue)
            
            iValue = self.getConfigOption('CLIENT_' + `dicUser['client']`,'StatsCallerMonth', cpServer)
            if iValue:
                iMonth = int(iValue)
                
            iValue = self.getConfigOption('CLIENT_' + `dicUser['client']`,'StatsCallerWeek', cpServer)
            if iValue:
                iWeek = int(iValue)
                
                    
                
        except:
            pass    
        print "SCHEDUL_PROCESS_STATUS",   SCHEDUL_PROCESS_STATUS
        
        if SCHEDUL_PROCESS_STATUS:
            liSPS = SCHEDUL_PROCESS_STATUS.split(',')
            print "liSPS",  liSPS
            liSchedulProcessStatus = []
            for st in liSPS:
                print st
                liSchedulProcessStatus.append(int(st.strip()))
            
       
            
        if CALLER_ID:
            liCaller = CALLER_ID.split(',')
            liSql = []
            liSql.append({'id':'day','sql':'doy','logic':'='})
            liSql.append({'id':'week','sql':'week','logic':'='})
            liSql.append({'id':'month','sql':'month','logic':'='})
            liSql.append({'id':'quarter','sql':'quarter','logic':'='})
            liSql.append({'id':'year','sql':'year','logic':'='})
            liSql.append({'id':'decade','sql':'decade','logic':'='})
            liSql.append({'id':'century','sql':'century','logic':'='})
        
            for caller in liCaller:
                caller_name = None
                sSql = 'select cuon_username from staff where staff.id = ' + caller 
                res1 = self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
                print 'dicUser' , dicUser
                if res1 and res1 not in ['NONE','ERROR']:
                    caller_name = res1[0]['cuon_username']
                if caller_name:    
                    sSql = "select '" + caller_name + "' as caller_name_" + caller + " ,"
                    for vSql in liSql:
                        for z1 in range(0,30):
                            if vSql['id'] == 'decade' and z1 > iDecade:
                                pass
                            elif vSql['id'] == 'century' and z1 > iCentury:
                                pass 
                            elif vSql['id'] == 'year' and z1 > iYear:
                                pass 
                            elif vSql['id'] == 'quarter' and z1 > iQuarter:
                                pass 
                            elif vSql['id'] == 'month' and z1 > iMonth:
                                pass     
                            elif vSql['id'] == 'week' and z1 > iWeek:
                                pass     
                            elif vSql['id'] == 'day' and z1 > 10:
                                pass   
                            else:
                                sSql += "(select  count(ps.id)  from partner_schedul as ps, address as a, partner as p where a.id = p.addressid and ps.user_id = '" + caller_name + "' and ps.partnerid = p.id and  ps.process_status != 999 "
                                #sSql +=  " and  date_part('" + vSql['sql'] +"', ps.insert_time) " + vSql['logic']+"  date_part('" + vSql['sql'] + "', now()) - " + `z1`
                                sSql +=  " and  date_part('" + vSql['sql'] +"', ps.insert_time) " + vSql['logic']+" " + self.getNow(vSql, z1)[0]
                                                                
                                sSql += " and date_part('year', ps.insert_time) =  " + `self.getBeforeYears(vSql['id'],z1)`
                                if WITHOUT_ID:
                                    liWithoutId = WITHOUT_ID.split(',')
                                    for no_id in liWithoutId:
                                        sSql += ' and a.id != ' + no_id
                                sSql += " and date_part('year',to_date(ps.schedul_date , '" + dicUser['SQLDateFormat'] +"')) >= " + MIN_SCHEDUL_YEAR
                                sSql += self.getWhere('',dicUser,2,'ps.')
                                sSql += ") as " + 'caller_' + caller +'_'+ vSql['id'] + '_count_' + `z1` + " , "
                                
                                #sSql += " group by a.caller_id "
                                if liSchedulProcessStatus:
                                    for sps in liSchedulProcessStatus:
                                        sSql += "(select  count(process_status)  from partner_schedul as ps, address as a, partner as p where a.id = p.addressid and ps.user_id = '" + caller_name + "' and ps.partnerid = p.id and  ps.process_status != 999 "
                                        sSql +=  " and  date_part('" + vSql['sql'] +"', ps.insert_time) " + vSql['logic'] + " " + self.getNow(vSql,  z1)[0]
                                        sSql += " and date_part('year', ps.insert_time) = "  + `self.getBeforeYears(vSql['id'],z1)`
                                        if WITHOUT_ID:
                                            liWithoutId = WITHOUT_ID.split(',')
                                            for no_id in liWithoutId:
                                                sSql += ' and a.id != ' + no_id
                                        sSql += " and date_part('year',to_date(ps.schedul_date , '" + dicUser['SQLDateFormat'] +"')) >= " + MIN_SCHEDUL_YEAR
                                        sSql += "and process_status = " + `sps` + " " 
                                        sSql += self.getWhere('',dicUser,2,'ps.')
                                        sSql += ") as " + 'caller_' + caller +'_'+ vSql['id'] + '_count_' + `z1` + "_status_" + `sps` +", "   

                    sSql = sSql[0:len(sSql)-2]
                    self.writeLog(sSql)
                    tmpResult = self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
                    if tmpResult and tmpResult not in ['NONE','ERROR']:
                        oneResult = tmpResult[0]
                        for key in oneResult.keys():
                            if oneResult[key]:
                                result[key] = oneResult[key]
                            else:
                                result[key] =0
                            #result[key] = oneResult[key]
                                      
                 

##                                tmpResult = self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
##                                if tmpResult and tmpResult not in ['NONE','ERROR']:
##                                    oneResult = tmpResult[0]
##                                    for key in oneResult.keys():
##                                      result['caller_' + caller +'_'+ vSql['id'] + '_' + key + '_' + `z1` ] = oneResult[key]
##                                      
                    
                
                
            
        if not result:
            result = 'NONE'


        #self.writeLog('Caller-Result = ' + `result`)
        
        return result
        
    def xmlrpc_getStatRep(self, dicUser):
        result = {}
        REP_ID = None
        WITHOUT_ID = None
        MIN_SCHEDUL_YEAR = '2003'
        iCentury = 2
        iDecade = 5
        iYear = 3
        iQuarter = 6
        iMonth = 14
        iWeek = 5
        
        try:
                       
            cpServer, f = self.getParser(self.CUON_FS + '/user.cfg')
            #print cpServer
            #print cpServer.sections()
            
            REP_ID = self.getConfigOption('STATS','REP_ID', cpServer)
            WITHOUT_ID = self.getConfigOption('STATS','WITHOUT_ID', cpServer)
        
        except:
            pass
        try:
                       
            cpServer, f = self.getParser(self.CUON_FS + '/clients.ini')
            #print cpServer
            #print cpServer.sections()
            
            SCHEDUL_PROCESS_STATUS = self.getConfigOption('CLIENT_' + `dicUser['client']`,'SchedulProcessStatus', cpServer)
            iValue = self.getConfigOption('CLIENT_' + `dicUser['client']`,'StatsCallerCentury', cpServer)
            if iValue:
                iCentury = int(iValue)
            
            iValue = self.getConfigOption('CLIENT_' + `dicUser['client']`,'StatsCallerDecade', cpServer)
            if iValue:
                iDecade = int(iValue)
            
            iValue = self.getConfigOption('CLIENT_' + `dicUser['client']`,'StatsCallerYear', cpServer)
            if iValue:
                iYear = int(iValue)
            
            iValue = self.getConfigOption('CLIENT_' + `dicUser['client']`,'StatsCallerQuarter', cpServer)
            if iValue:
                iQuarter = int(iValue)
            
            iValue = self.getConfigOption('CLIENT_' + `dicUser['client']`,'StatsCallerMonth', cpServer)
            if iValue:
                iMonth = int(iValue)
                
            iValue = self.getConfigOption('CLIENT_' + `dicUser['client']`,'StatsCallerWeek', cpServer)
            if iValue:
                iWeek = int(iValue)
                
                    
                
        except:
            pass    
        print "SCHEDUL_PROCESS_STATUS",   SCHEDUL_PROCESS_STATUS
        
        if SCHEDUL_PROCESS_STATUS:
            liSPS = SCHEDUL_PROCESS_STATUS.split(',')
            print "liSPS",  liSPS
            liSchedulProcessStatus = []
            for st in liSPS:
                print st
                liSchedulProcessStatus.append(int(st.strip()))
            

        if REP_ID:
            lirep = REP_ID.split(',')
            liSql = []
            liSql.append({'id':'day','sql':'doy','logic':'='})
            liSql.append({'id':'week','sql':'week','logic':'='})
            liSql.append({'id':'month','sql':'month','logic':'='})
            liSql.append({'id':'quarter','sql':'quarter','logic':'='})
            liSql.append({'id':'year','sql':'year','logic':'='})
            liSql.append({'id':'decade','sql':'decade','logic':'='})
            liSql.append({'id':'century','sql':'century','logic':'='})

            for rep in lirep:
                rep_name = None
                sSql = 'select cuon_username from staff where staff.id = ' + rep 
                res1 = self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
                if res1 and res1 not in ['NONE','ERROR']:
                    rep_name = res1[0]['cuon_username']
                if rep_name:    
                    sSql = "select '" + rep_name + "' as rep_name_" + rep + " ,"
                    for vSql in liSql:
                        for z1 in range(-5,20):
                            if vSql['id'] == 'decade' and z1 > iDecade:
                                pass
                            elif vSql['id'] == 'century' and z1 > iCentury:
                                pass 
                            elif vSql['id'] == 'year' and z1 > iYear:
                                pass 
                            elif vSql['id'] == 'quarter' and z1 > iQuarter:
                                pass 
                            elif vSql['id'] == 'month' and z1 > iMonth:
                                pass     
                            elif vSql['id'] == 'week' and z1 > iWeek:
                                pass     
                            
                            else:
                                sSql += "(select  count(ps.id) from partner_schedul as ps, address as a, partner as p where a.id = p.addressid and ps.schedul_staff_id = '" + rep + "' and ps.partnerid = p.id and  ps.process_status != 999 "
                                sSql +=  " and  date_part('" + vSql['sql'] +"',to_date(ps.schedul_date , '" + dicUser['SQLDateFormat'] +"') ) " + vSql['logic'] +" " + self.getNow(vSql, z1)[0]
                                sSql += " and date_part('year', to_date(ps.schedul_date , '" + dicUser['SQLDateFormat'] +"') ) = "  + `self.getBeforeYears(vSql['id'],z1)`
                                if WITHOUT_ID:
                                    liWithoutId = WITHOUT_ID.split(',')
                                    for no_id in liWithoutId:
                                        sSql += ' and a.id != ' + no_id
                                sSql += " and date_part('year',to_date(ps.schedul_date , '" + dicUser['SQLDateFormat'] +"')) >= " + MIN_SCHEDUL_YEAR
                                sSql += self.getWhere('',dicUser,2,'ps.')
                                sSql += ") as " + 'rep_' + rep +'_'+ vSql['id'] + '_count_' + `z1`.replace('-','M') + " , "
                                if liSchedulProcessStatus:
                                    for sps in liSchedulProcessStatus:
                                        sSql += "(select  count(ps.id) from partner_schedul as ps, address as a, partner as p where a.id = p.addressid and ps.schedul_staff_id = '" + rep + "' and ps.partnerid = p.id and  ps.process_status != 999 "
                                        sSql +=  " and  date_part('" + vSql['sql'] +"',to_date(ps.schedul_date , '" + dicUser['SQLDateFormat'] +"') ) " + vSql['logic'] +" " + self.getNow(vSql, z1)[0]
                                        sSql += " and date_part('year', to_date(ps.schedul_date , '" + dicUser['SQLDateFormat'] +"') ) = "  + `self.getBeforeYears(vSql['id'],z1)`
                                         
                                        if WITHOUT_ID:
                                            liWithoutId = WITHOUT_ID.split(',')
                                            for no_id in liWithoutId:
                                                sSql += ' and a.id != ' + no_id
                                        sSql += " and date_part('year',to_date(ps.schedul_date , '" + dicUser['SQLDateFormat'] +"')) >= " + MIN_SCHEDUL_YEAR
                                        sSql += "and process_status = " + `sps` + " " 
                                        sSql += self.getWhere('',dicUser,2,'ps.')
                                        sSql += ") as " + 'rep_' + rep +'_'+ vSql['id'] + '_count_' + `z1`.replace('-','M') + "_status_" + `sps` + " , "       
                                                
                                        
                                        
                                #sSql += " group by a.rep_id "


                    sSql = sSql[0:len(sSql)-2]
                    self.writeLog(sSql)
                    tmpResult = self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
                    if tmpResult and tmpResult not in ['NONE','ERROR']:
                        oneResult = tmpResult[0]
                        for key in oneResult.keys():
                            if oneResult[key]:
                                result[key] = oneResult[key]
                            else:
                                result[key] =0
                                
                                      
                 

##                                tmpResult = self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
##                                if tmpResult and tmpResult not in ['NONE','ERROR']:
##                                    oneResult = tmpResult[0]
##                                    for key in oneResult.keys():
##                                      result['rep_' + rep +'_'+ vSql['id'] + '_' + key + '_' + `z1` ] = oneResult[key]
##                                      
                    
                
                
            
        if not result:
            result = 'NONE'


        self.writeLog('rep-Result = ' + `result`)
        
        return result

    def xmlrpc_getStatSalesman(self, dicUser):
        result = {}
        SALESMAN_ID = None
        WITHOUT_ID = None
        MIN_SCHEDUL_YEAR = '2005'
        try:
                       
            cpServer, f = self.getParser(self.CUON_FS + '/user.cfg')
            #print cpServer
            #print cpServer.sections()
            
            SALESMAN_ID = self.getConfigOption('STATS','SALESMAN_ID', cpServer)
            WITHOUT_ID = self.getConfigOption('STATS','WITHOUT_ID', cpServer)
        
        except:
            pass
            

        if SALESMAN_ID:
            lisalesman = SALESMAN_ID.split(',')
            liSql = []
            liSql.append({'id':'day','sql':'doy','logic':'='})
            liSql.append({'id':'week','sql':'week','logic':'='})
            liSql.append({'id':'month','sql':'month','logic':'='})
            liSql.append({'id':'quarter','sql':'quarter','logic':'='})
            liSql.append({'id':'year','sql':'year','logic':'='})
            liSql.append({'id':'decade','sql':'decade','logic':'='})
            liSql.append({'id':'century','sql':'century','logic':'='})

            for salesman in lisalesman:
                salesman_name = None
                sSql = 'select cuon_username from staff where staff.id = ' + salesman 
                res1 = self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
                if res1 and res1 not in ['NONE','ERROR']:
                    salesman_name = res1[0]['cuon_username']
                if salesman_name:    
                    sSql = "select '" + salesman_name + "' as salesman_name_" + salesman + " ,"
                    for vSql in liSql:
                        for z1 in range(-5,20):
                            if vSql['id'] == 'decade' and z1 > 4:
                                pass
                            elif vSql['id'] == 'century' and z1 > 1:
                                pass 
                            elif vSql['id'] == 'year' and z1 > 5:
                                pass 
                            elif vSql['id'] == 'quarter' and z1 > 9:
                                pass 
                            elif vSql['id'] == 'month' and z1 > 14:
                                pass     
                            elif vSql['id'] == 'week' and z1 > 9:
                                pass     
                            
                            else:
                                sSql += "(select  count(ps.id) from partner_schedul as ps, address as a, partner as p where a.id = p.addressid and ps.schedul_staff_id = '" + salesman + "' and ps.partnerid = p.id and  ps.process_status != 999 "
                                sSql +=  " and  date_part('" + vSql['sql'] +"',to_date(ps.schedul_date , '" + dicUser['SQLDateFormat'] +"') ) " + vSql['logic']+"  date_part('" + vSql['sql'] + "', now()) - " + `z1`
                                if WITHOUT_ID:
                                    liWithoutId = WITHOUT_ID.split(',')
                                    for no_id in liWithoutId:
                                        sSql += ' and a.id != ' + no_id
                                sSql += " and date_part('year',to_date(ps.schedul_date , '" + dicUser['SQLDateFormat'] +"')) >= " + MIN_SCHEDUL_YEAR
                                sSql += self.getWhere('',dicUser,2,'ps.')
                                sSql += ") as " + 'salesman_' + salesman +'_'+ vSql['id'] + '_count_' + `z1`.replace('-','M') + " , "
                                
                                #sSql += " group by a.salesman_id "


                    sSql = sSql[0:len(sSql)-2]
                    self.writeLog(sSql)
                    tmpResult = self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
                    if tmpResult and tmpResult not in ['NONE','ERROR']:
                        oneResult = tmpResult[0]
                        for key in oneResult.keys():
                            result[key] = oneResult[key]
                                      
                 

##                                tmpResult = self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
##                                if tmpResult and tmpResult not in ['NONE','ERROR']:
##                                    oneResult = tmpResult[0]
##                                    for key in oneResult.keys():
##                                      result['salesman_' + salesman +'_'+ vSql['id'] + '_' + key + '_' + `z1` ] = oneResult[key]
##                                      
                    
                
                
            
        if not result:
            result = 'NONE'


        self.writeLog('salesman-Result = ' + `result`)
        
        return result

    def xmlrpc_getAllAddressForThisPartner(self,sWhere,dicUser):
        sAddressWhere = ' where id = 0'
        sSql = 'select addressid from partner ' + sWhere
        sSql += self.getWhere('',dicUser,2)
        result = self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
        if result and result not in ['ERROR','NONE']:
            sAddressWhere = ' where '
            for i in result:
                sAddressWhere += ' id = ' + `i['addressid']` + ' or'
                #print sAddressWhere
            sAddressWhere = sAddressWhere[:len(sAddressWhere)-3]
            
        return sAddressWhere
        
    def xmlrpc_getButtonGrave(self, dicUser):
        print 'button grave'
        cpServer, f = self.getParser(self.CUON_FS + '/menus.cfg')
        setButton = self.getConfigOption(dicUser['Name'],'address_button_grave', cpServer)
        print 'setButton = ',  setButton
        buttonPosition = self.getConfigOption(dicUser['Name'],'address_button_grave_position', cpServer)
        if setButton and buttonPosition:
            return setButton.upper() ,  buttonPosition
        else:
            return 'NO',  '-1'
            
                
