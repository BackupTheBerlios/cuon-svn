import time
import time
from datetime import datetime
import random
import xmlrpclib
from twisted.web import xmlrpc
import base64
import bz2
from basics import basics
import Database

class Article(xmlrpc.XMLRPC, basics):
    def __init__(self):
        basics.__init__(self)
        self.oDatabase = Database.Database()
        
        

    def getArticlelist1(self, dicSearchlist, dicUser):
        
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
        
        
        sSql = sSql + self.getWhere("",dicUser,2)
        sSql = sSql + ' order by number, designation'
        
        return self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser)

    def getPickleListStandard( self,  dicSearchlist, dicUser,  nRows):
        
        
        
        
        sSql = 'select number, designation,sellingprice1, sellingprice2, sellingprice3, sellingprice4, wrapping, unit,quantumperwrap, manufactor_id, material_group, sep_info_1,id,  associated_with, associated_id  from articles'
        sSql3 = ''
        sSql4 = ''
        sSql5 = ''
        sSql6 = ''
        addSql = ''
        
        if dicSearchlist:
            sSql += ' where '
            if dicSearchlist['eNumberFrom'] and dicSearchlist['eNumberTo'] :
               numberFrom =  dicSearchlist['eNumberFrom'].upper()
               numberTo = dicSearchlist['eNumberTo'].lower() 
                
               sSql+= " number  between  '" +  numberFrom + "' and '" + numberTo +"' and"  
               
        
            if dicSearchlist['eDesignationFrom'] and dicSearchlist['eDesignationTo'] :
               designationFrom =  dicSearchlist['eDesignationFrom'].upper()
               designationTo = dicSearchlist['eDesignationTo'].lower()
                
               
               sSql += " designation  between  '" +  designationFrom + "' and '" + designationTo +"' and"  
              
               
            if dicSearchlist['eMGFrom'] and dicSearchlist['eMGTo'] :
                eMGFrom = dicSearchlist['eMGFrom']
                eMGTo = dicSearchlist['eMGTo']
                sSql += " material_group  between  " +  eMGFrom + " and " + eMGTo + ' and' 
                
       
        
            if dicSearchlist['eNumberContains']:
                sSql += " number ~*'" + dicSearchlist['eNumberContains'] + "' and"
                
            if dicSearchlist['eDesignationContains']:
                sSql += " designation ~*'" + dicSearchlist['eDesignationContains'] + "' and"
              
            if dicSearchlist['eMGContains']:
                print 'Material_group'
                liMG = dicSearchlist['eMGContains'].split(',')
                print 'liMG', liMG
                for mg in liMG:
                    print 'mg = ', mg
                    sSql += " material_group = " + mg + "  or"
                    print sSql 
        
            sSql = sSql[:len(sSql)-3] 


        sSql = sSql + self.getWhere("",dicUser,2)
        sSql = sSql + ' order by number, designation'
        
        result = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser)
        result2 = None
            
        if result and result not in ['NONE', 'ERROR']:
                result2 = []
                z1 = 0
                dicValues2 = {}

                for dicValues in result:
                    # look at associated pictures
                    sAssociatedTable, iDMS = self.getAssociatedTable(dicValues['associated_with'])
                    
                    if sAssociatedTable == 'botany' and iDMS:
                        sSql = 'select botany_name, local_name,  description as botany_description , habitat, tips as botany_tips '
                        sSql += ' from botany where id = ' + `dicValues['associated_id']`
                        result6 = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser)
                        if result6 and result6 not in ['NONE', 'ERROR']:
                            for keyV in result6[0].keys():
                                dicValues[keyV] = result6[0][keyV]
                                self.writeLog(keyV,  dicValues[keyV])
                                
                        sSql = "select document_image, file_suffix from dms where insert_from_module = " + `iDMS` + " and title = 'print001' and sep_info_1 = "
                        sSql += `dicValues['associated_id']`
                        sSql += self.getWhere("",dicUser,2)
                        result7 = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser)
                        if result7 and result7 not in ['NONE', 'ERROR']:
                            aFilename = self.createNewSessionID()
                            sFilename = aFilename['SessionID'] + '.' + result7[0]['file_suffix']
                            
                            try:
                                f = open(self.DocumentPathTmp + '/' + sFilename, 'w')
                                s = base64.decodestring(result7[0]['document_image'])
                                s = bz2.decompress(s)
                                f.write(s)
                                f.close()
                            except:
                                print 'file error'
                                sFilename = 'ERROR'
                            dicValues['dms_print001'] = self.DocumentPathTmp + '/' + sFilename
                        else:
                            dicValues['dms_print001'] = 'NOFILE'
                    if z1 >= nRows:
                        z1 = 0
                        result2.append(dicValues2)
                        dicValues2 = {}

                    for key in dicValues.keys():
                        dicValues2[key + '_' + `z1`] = dicValues[key]
                        
                    z1 += 1
                if z1 != 0:
                    result2.append(dicValues2)

        else:
            result2 = 'NONE'
        print '...................................................................................................................................................................'
        print 'Result2',  result2
        return result2

    
    def xmlrpc_insertGoods(self, stock, article_number, move, dicUser):
        
        article_id = None
        sSql = "select id from articles " 
        sSql = sSql + self.getWhere("where number = '" + article_number + "'" ,dicUser,1)
        result = self.oDatabase.xmlrpc_executeNormalQuery(sSql)
        if result not in ['NONE','ERROR']:
           article_id = result[0]['id']
        
        if not article_id:
           dicValues = {}
           dicValues['number']= [article_number,'string']
           result = self.oDatabase.xmlrpc_saveRecord('articles',-1,dicValues, dicUser)
           article_id = result[0]['last_value']
        
        dicValues = {}
        dicValues['stock_id'] = [stock,'int']
        dicValues['article_id'] = [article_id,'int']
        if move > 0:
           dicValues['to_embed'] = [move,'float']
        else:
           dicValues['roll_out'] = [move,'float']
        
        result = self.oDatabase.xmlrpc_saveRecord('stock_goods',-1,dicValues, dicUser)
        if result == None:
            result = 'NONE'
            
        return result
        
    def xmlrpc_insertWebshopArticle(self, dicArticle, dicUser):
        self.writeLog('start py_insertWebshopArticle')
        categorie = None
        result = None
        
        if len(dicArticle) > 4:
            if dicArticle['products_model'][0][0:3] == '004':
                categorie = 36
            elif dicArticle['products_model'][0][0:3] == '401':
                categorie = 33
            elif dicArticle['products_model'][0][0:3] == '402':
                categorie = 33
            elif dicArticle['products_model'][0][0:3] == '403':
                categorie = 34
            elif dicArticle['products_model'][0][0:3] == '011':
                categorie = 35
            elif dicArticle['products_model'][0][0:3] == '029':
                categorie = 37
            elif dicArticle['products_model'][0][0:3] == '006':
                categorie = 38
            elif dicArticle['products_model'][0][0:3] == '014':
                categorie = 39
            elif dicArticle['products_model'][0][0:3] == '022':
                categorie = 40
            elif dicArticle['products_model'][0][0:3] == '015':
                categorie = 42
            elif dicArticle['products_model'][0][0:3] == '027':
                categorie = 23
            elif dicArticle['products_model'][0][0:3] == '050':
                categorie = 43
            elif dicArticle['products_model'][0][0:3] == '052':
                categorie = 44
            elif dicArticle['products_model'][0][0:3] == '030':
                categorie = 27
            elif dicArticle['products_model'][0][0:3] == '031':
                categorie = 27
            elif dicArticle['products_model'][0][0:3] == '101':
                categorie = 45
            elif dicArticle['products_model'][0][0:3] == '102':
                categorie = 46
            elif dicArticle['products_model'][0][0:3] == '404':
                categorie = 29
            elif dicArticle['products_model'][0][0:3] == '911':
                categorie = 48
            elif dicArticle['products_model'][0][0:3] == '913':
                categorie = 49
            elif dicArticle['products_model'][0][0:3] == '024':
                categorie = 50
            elif dicArticle['products_model'][0][0:3] == '911':
                categorie = 51
            elif dicArticle['products_model'][0][0:3] == '214':
                categorie = 52
            elif dicArticle['products_model'][0][0:3] == '213':
                categorie = 53
            elif dicArticle['products_model'][0][0:3] == '214':
                categorie = 55
            elif dicArticle['products_model'][0][0:3] == '913':
                categorie = 56
            elif dicArticle['products_model'][0][0:3] == '311':
                categorie = 57
            elif dicArticle['products_model'][0][0:3] == '301':
                categorie = 58
            elif dicArticle['products_model'][0][0:3] == '302':
                categorie = 58
            elif dicArticle['products_model'][0][0:3] == '303':
                categorie = 58
        
        
        if categorie:
            article_id = None
            dicUser['Database'] = 'osCommerce'
            dicArticle['products_model'][0] = dicArticle['products_model'][0].encode('latin-1')
            dicArticle['remark_w'][0] = dicArticle['remark_w'][0].encode('latin-1')
            dicArticle['s9'][0] = dicArticle['s9'][0].encode('latin-1')
        
            self.writeLog('py_insertWebshopArticle 0 key' + `dicArticle['products_model']`)
            sSql = "select products_id as id from products where products_model = '" + dicArticle['products_model'][0] + "' "
        
            self.writeLog('py_insertWebshopArticle 1 sql' + `sSql`)
            result = self.oDatabase.xmlrpc_executeNormalQuery(sSql)
            self.writeLog('py_insertWebshopArticle 2 result' + `result`)
            if result not in ['NONE','ERROR']:
               article_id = result[0]['id']
            else:
               article_id = -1
            dicValues = {}
        
        
            dicValues['products_model']= dicArticle['products_model']
            dicValues['products_price']= dicArticle['products_price']
            dicValues['products_status']= [1,'int']
            self.writeLog('py_insertWebshopArticle 3 dicValues =' + `dicValues`)
        
        
            result = self.oDatabase.saveWebshopRecord('products',article_id,'products_id', dicValues, dicUser)
            if article_id == -1:
               article_id = result[0]['last_value']
        
        
            sSql = "select products_id as id from products_to_categorie where products_id = " + `article_id`
            result = context.sql.py_executeNormalQuery(sSql)
            if result:
               cat_id = result[0]['id']
            else:
               cat_id = -1
        
            #if cat_id == -1:
            #   cat_id = dicArticle['categorie']
            
            context.logging.writeLog('py_insertWebshopArticle 6 categorie = ' + `categorie`) 
            dicValues = {}
            dicValues['products_id']= [article_id,'int']
            dicValues['categories_id']= [categorie,'int']
        
            context.logging.writeLog('py_insertWebshopArticle 7 dicValues =' + `dicValues`)
            result = context.sql.py_saveWebshopRecord('products_to_categories',cat_id,'products_id',dicValues, dicUser)
        
            sRemark = ''
            sRemarkName = 'No Name'
        
            if dicArticle['remark_w'][0] == None:
               sRemarkName = 'Kein Name'
            else:
               sRemark = dicArticle['remark_w'][0]
               sRemarkName = dicArticle['remark_w'][0]
        
            # Please check later
            sRemarkName = sRemark
        
            dicValues = {}
            dicValues['products_id']= [article_id,'int']
            dicValues['language_id']= [2,'int']
            dicValues['products_description']= [sRemark,'string']
            dicValues['products_name']= [sRemarkName,'string']
            result = context.sql.py_saveWebshopRecord('products_description',-1,'products_id',dicValues, dicUser)
        
        return result

    def xmlrpc_getMaterialGroups(self, dicUser):
        sSql = 'select name, id  from material_group order by name'
        dicResult = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser)
        return dicResult
        
        
    def xmlrpc_getArticlesOfMaterialGroup(self, dicUser, mid):
        cNumber = 'a'
        cSellingprice = 'b'
        cDesignation = 'c'
        try:
                       
            cpServer, f = self.getParser(self.CUON_FS + '/clients.ini')
            #print cpServer
            #print cpServer.sections()
            
            cNumber = self.getConfigOption('CLIENT_' + `dicUser['client']`,'articles_sort1_number', cpServer)
            cSellingprice = self.getConfigOption('CLIENT_' + `dicUser['client']`,'articles_sort1_sellingprice', cpServer)
            cDesignation = self.getConfigOption('CLIENT_' + `dicUser['client']`,'articles_sort1_designation', cpServer)
        
        except:
            pass
            
        sSort = 'number as ' + cNumber +',sellingprice1 as ' + cSellingprice +', designation as ' + cDesignation 
        sSql = 'select ' + sSort +' , id from articles where material_group = ' + `mid`
        sSql += self.getWhere('',dicUser,2) 
        sSql += ' order by number, designation '
        dicResult = self.oDatabase.xmlrpc_executeNormalQuery(sSql, dicUser)

        return dicResult
        
    def xmlrpc_getArticlePrice(self, id, dicUser):
        price = '0.00'
        sSql = "select sellingprice1 from articles where id = " + `id`
        liResult = self.oDatabase.xmlrpc_executeNormalQuery(sSql,dicUser)
        print 'price', liResult
        if liResult and liResult not in ['NONE','ERROR']:
            price = liResult[0]['sellingprice1']
            print 'price2', price
            price = ("%." + `self.CURRENCY_ROUND` + "f") % round(price,self.CURRENCY_ROUND)
            print 'price2', price
            
        return price
            
        
    
        
    def xmlrpc_getStatsMisc(self, dicUser):
        
        return ['NONE']
        
        
