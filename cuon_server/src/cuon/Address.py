import time
from datetime import datetime
import random
import xmlrpclib
from twisted.web import xmlrpc
 
from basics import basics
import Database

class Address(xmlrpc.XMLRPC, basics):
    def __init__(self):
        basics.__init__(self)
        self.oDatabase = Database.Database()
        
    def xmlrpc_getAddress(self,id, dicUser ):
    
        sSql = 'select address, lastname, lastname2,firstname, street, zip, city, ' 
        sSql = sSql + ' trim(country) || \'-\' || trim(zip) || \' \' || trim(city) as cityfield, state, country from address '
        sWhere = 'where id = ' + `id`
        sWhere = self.getWhere(sWhere, dicUser)
        sSql = sSql + sWhere
        
        return self.xmlrpc_executeNormalQuery(sSql, dicUser)

    def xmlrpc_getAllActiveSchedul(self, dicUser):
        
        sSql = "select to_char(partner_schedul.schedul_date, \'" + dicUser['SQLDateFormat'] + "\') as date, "
        sSql = sSql + "to_char(partner_schedul.schedul_time, \'" + dicUser['SQLTimeFormat'] + "\') as time, "
        sSql = sSql + "address.city, partner_schedul.short_remark, partner_schedul.notes , "
        sSql = sSql + "partner.lastname as partner_lastname, address.lastname as address_lastname, "
        sSql = sSql + "address.lastname2 as address_lastname2, partner.firstname as partner_firstname "
        sSql = sSql + " from partner, address, partner_schedul "
        sW = " where partner.id = partnerid and address.id = partner.addressid and "
        sW = sW + " process_status != 999 "
        sSql = sSql + self.getWhere(sW, dicUser)
        
        sSql = sSql + " order by partner_schedul.schedul_date, partner_schedul.schedul_time " 
        
        return self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser)
    

    def xmlrpc_getAllActiveSchedulByNames(self, dicUser):
        
                
        sSql = "select partner_schedul.schedul_date as date, "
        sSql +=  "partner_schedul.schedul_time_begin as time_begin, "
        sSql +=  "address.city, partner_schedul.short_remark, partner_schedul.notes , "
        sSql +=  "partner.lastname as partner_lastname, address.lastname as address_lastname, "
        sSql += "( select staff.lastname from staff where staff.id = (select rep_id from address where address.id = partner.addressid)) as rep_lastname, " 
        sSql += "( select staff.lastname from staff where staff.id = (select salesman_id from address where address.id = partner.addressid)) as salesman_lastname, " 
        sSql +=  "address.lastname2 as address_lastname2, partner.firstname as partner_firstname "
        sSql += " from partner, address, partner_schedul "
        sW = " where partner.id = partnerid and address.id = partner.addressid and "
        sW = sW + " process_status != 999 "
        sSql = sSql + self.getWhere(sW, dicUser,Prefix='partner_schedul.')
        
        sSql = sSql + " order by partner_schedul.schedul_date, partner_schedul.schedul_time_begin " 
        
        return self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser)
        
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
        sW +=  " process_status != 1 and contacter_id = " + self.getStaffID(dicUser) + " "  
        
        sSql = sSql + self.getWhere(sW, dicUser, Prefix='contact.')
        
        sSql = sSql + " order by contact.schedul_date, contact.schedul_time_begin " 
        
        liResult = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser)
        liResult2 = []
        if liResult != 'NONE':
            for dicResult in liResult:
                try:
                    print 'Len1 = ', len(liResult)
                    Hour,Minute = divmod(dicResult['time'],4)
                    Minute = Minute * 15
                    sDate = dicResult['date'] + ' ' + `Hour` + ':' + `Minute` +':00'
                    print 'Date =',  sDate
                    if sDate.find('.') > 0:
                        sFormat = '%d.%m.%Y %H:%M:%S'
                    else:
                        sFormat = '%Y/%m/%d %H:%M:%S'
                    wakeDate = time.strptime(sDate,sFormat)
                    print wakeDate

                    nD1 = datetime(wakeDate[0], wakeDate[1],wakeDate[2],wakeDate[3],wakeDate[4], wakeDate[5])
                    print 'nD1', nD1
                    currentDate = time.localtime()
                    print currentDate
                    nD2 = datetime(currentDate[0], currentDate[1],currentDate[2],currentDate[3],currentDate[4], currentDate[5])
                    print nD2
                    nD3 = nD1 -nD2
                    print nD3
                    print '---------------------------------------------------'
                    print 'Differenz', nD3.days
                    print 'Differenz', nD3.seconds
                    print 'DB-alarm','Differenz', 'Datum', 'Current'
                   
                    print dicResult['alarm_hours'] * 3600 + dicResult['alarm_minutes'] * 60, nD3.seconds, nD1, nD2 

                    ok = False
                    if dicResult['alarm_days'] > 0:
                        if dicResult['alarm_days'] <= nD3.days : 
                            ok = True
                    elif (dicResult['alarm_hours'] * 3600 + dicResult['alarm_minutes'] * 60) > nD3.seconds :
                       ok = True
                    if  ok:
                        print 'copy entry to  list'
                        liResult2.append(dicResult)
                        print 'Len2 = ', len(liResult2)
                        
                    
                except Exception, params:
                    print Exception, params
        
        
        print liResult2
        print 'Len3 = ', len(liResult2)

        return liResult2
        
        
        
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
            sSql2 = sSqlWhere + ' and where '
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
        
        sSql = sSql + self.getWhere(sSqlWhere,dicUser,0,'partner.')
        sSql = sSql + ' order by address.lastname, address.lastname2, address.firstname, address.city, partner.lastname, partner.lastname2, partner.firstname, partner.city'
        print sSql
        return self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser)
        
        
