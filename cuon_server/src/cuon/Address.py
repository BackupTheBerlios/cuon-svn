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
        
    def xmlrpc_getPartnerAddress(self, id, dicUser):
        sSql = 'select address, lastname, lastname2,firstname, street, zip, city, state, country, phone from partner where id = ' + `id`
        
        return self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser)
     
    def xmlrpc_getPartnerToAddress(self, id, dicUser):
        sSql = 'select * from partner where addressid = ' + `id`
        return self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser)


    def xmlrpc_getPhonelist1(self, dicSearchlist, dicUser):
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
        
    def xmlrpc_getPhonelist11(self, dicSearchlist, dicUser):
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
        
        
