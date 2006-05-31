import time
from datetime import datetime
import random
import xmlrpclib
from twisted.web import xmlrpc
 
from basics import basics
import Database

class Article(xmlrpc.XMLRPC, basics):
    def __init__(self):
        basics.__init__(self)
        self.oDatabase = Database.Database()
        
        

    def xmlrpc_getArticlelist1(self, dicSearchlist, dicUser):
        
        import string 
        
        sSql = 'select number, designation, sep_info_1,id from articles'
        sSql3 = ''
        sSql4 = ''
        sSql5 = ''
        sSql6 = ''
        
        if dicSearchlist:
            sSql2 = sSql + ' where '
            if dicSearchlist['eNumberFrom'] and dicSearchlist['eNumberTo'] :
               numberFrom =  string.upper(dicSearchlist['eNumberFrom']) 
               numberTo = string.lower(dicSearchlist['eNumberTo']) 
                
               sSql3 = sSql2 + " number  between  '" +  numberFrom + "' and '" + numberTo +"'"  
               sSql = sSql3
        
            if dicSearchlist['eDesignationFrom'] and dicSearchlist['eDesignationTo'] :
               designationFrom =  string.upper(dicSearchlist['eDesignationFrom']) 
               designationTo = string.lower(dicSearchlist['eDesignationTo']) 
                
               
               sSql4 = " designation  between  '" +  designationFrom + "' and '" + designationTo +"'"  
               if sSql3:
                   sSql4 = sSql3 + ' and ' + sSql4
               else:
                   sSql4 = sSql2 + sSql4
        
               sSql = sSql4
        
        
        ##    if dicSearchlist['eCityFrom'] and dicSearchlist['eCityTo'] :
        ##       cityFrom =  string.upper(dicSearchlist['eCityFrom']) 
        ##       cityTo = string.lower(dicSearchlist['eCityTo']) 
                
               
        ##       sSql5 = " city  between  '" +  cityFrom + "' and '" + cityTo +"'"  
        ##       if sSql3 and not sSql4:
        ##           sSql5 = sSql3 + ' and ' + sSql5
        ##       elif sSql3 and sSql4:
        ##           sSql5 = sSql4 + ' and ' + sSql5
        ##       else:
        ##           sSql5 = sSql2 + sSql5
        
        ##       sSql = sSql5
        
        
        ##    if dicSearchlist['eCountryFrom'] and dicSearchlist['eCountryTo'] :
        ##       countryFrom =  string.upper(dicSearchlist['eCountryFrom']) 
        ##       countryTo = string.lower(dicSearchlist['eCountryTo']) 
                
               
        ##       sSql6 = " country  between  '" +  countryFrom + "' and '" + countryTo +"'"  
        ##       if sSql3 and not sSql4 and not sSql5:
        ##           sSql6 = sSql3 + ' and ' + sSql6
        ##       elif sSql4 and not sSql5:
        ##           sSql6 = sSql4 + ' and ' + sSql6
        ##       elif sSql5:
        ##           sSql6 = sSql5 + ' and ' + sSql6
        ##       else:
        ##           sSql6 = sSql2 + sSql6
        
        ##       sSql = sSql6
        
        
        sSql = sSql + self.getWhere("",dicUser,1)
        sSql = sSql + ' order by number, designation'
        
        return self.xmlrpc_executeNormalQuery(sSql, dicUser)
