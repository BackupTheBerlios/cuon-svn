 

CREATE OR REPLACE FUNCTION fct_get_price_for_pricegroup(  sModul varchar, iModulID integer, iArticleID integer) returns  float AS '
 
    DECLARE
        sSql    text ;
        fPrice float ;
        iAddressID integer ;
        recData record ;
        pricegroupID integer ;
        
    BEGIN 
        fPrice := 0.00 ;
           IF sModul = ''grave'' THEN
                select into recData pricegroup1, pricegroup2,pricegroup3,pricegroup4,pricegroup_none from grave where grave.id = iModulID ;
            ELSEIF sModul = ''orderposition'' THEN
                select into recData pricegroup1, pricegroup2,pricegroup3,pricegroup4,pricegroup_none from orderbook where id = iModulID ;
            END IF ;
           
            if recData.pricegroup1 IS NULL then
                pricegroupID :=5 ;
            ELSEIF recData.pricegroup1 = TRUE THEN 
                pricegroupID :=1 ;
            ELSEIF recData.pricegroup2 = TRUE THEN 
                recData.pricegroupID :=2 ;
            ELSEIF recData.pricegroup3 = TRUE THEN 
                pricegroupID :=3 ;
            ELSEIF recData.pricegroup4 = TRUE THEN 
                pricegroupID :=4 ;
            ELSEIF recData.pricegroup_none = TRUE THEN 
                pricegroupID :=5 ;
            ELSE 
                pricegroupID :=5 ;
            END IF ;
            
            -- raise notice '' pricegroup id = % '',pricegroupID ;
            
            
            
            IF pricegroupID = 5 then
                
            IF sModul = ''grave'' THEN
                select into recData addressid from grave where id = iModulID ;
                -- raise notice '' address id = % '',recData.addressid ;
                iAddressID = recData.addressid ;
            ELSEIF sModul = ''orderposition'' THEN
                select into recData addressnumber from orderbook  where orderbook.id = iModulID ;
                -- raise notice '' address id = % '',recData.addressnumber;
                iAddressID = recData.addressnumber ;
            END IF ;
            
            
                
                
                
                select into recData pricegroup1, pricegroup2,pricegroup3,pricegroup4,pricegroup_none from addresses_misc where address_id = iAddressID ;
                -- raise notice '' pricegroup by address = %, % , %'',recData.pricegroup1, recData.pricegroup2,recData.pricegroup3;
                if recData.pricegroup1 IS NULL then
                    pricegroupID :=1 ;
                ELSEIF recData.pricegroup1 = TRUE THEN 
                    pricegroupID :=1 ;
                ELSEIF recData.pricegroup2 = TRUE THEN 
                    pricegroupID :=2 ;
                ELSEIF recData.pricegroup3 = TRUE THEN 
                    pricegroupID :=3 ;
                ELSEIF recData.pricegroup4 = TRUE THEN 
                    pricegroupID :=4 ;
                ELSEIF recData.pricegroup_none = TRUE THEN 
                    pricegroupID :=5 ;
                ELSE 
                    pricegroupID :=1 ;
                END IF ;
            END IF ;
        
        -- raise notice '' pricegroup id last value = % '',pricegroupID ;
        
        if pricegroupID < 5 then 
            sSql = ''select sellingprice''||pricegroupID||'' as price from articles where id = '' || iArticleID ;
            -- raise notice '' sql  = % '',sSql ;
            
            for recData in execute sSql 
                LOOP 
            END LOOP ;
        
            -- raise notice '' price = % '', recData.price ;
         
            fPrice := recData.price ;
            if fPrice IS NULL THEN 
                fPrice := 0.00 ;
            END IF ;
            -- raise notice '' price = % '',fPrice ;
        END IF ;
         
        return fPrice ;
    END ;
    ' LANGUAGE 'plpgsql'; 

    
    
CREATE OR REPLACE FUNCTION fct_get_taxvat_for_article( iArticleID integer) returns  float AS '
 
    DECLARE
        sSql    text ;
        fTaxVat float ;
        iTaxVatArticle integer ;
        rData  record ;
    BEGIN 
        fTaxVat := 0.00;
    
        select into rData tax_vat_id from articles where id = iArticleID ;
        IF rData.tax_vat_id IS NULL then
            iTaxVatArticle = 0;
        ELSE
            iTaxVatArticle = rData.tax_vat_id ;
        END IF ;
        
        IF iTaxVatArticle= 0 THEN
            select into rData  material_group.tax_vat from articles,material_group where articles.id = iArticleID and articles.material_group = material_group.id ;
            IF rData.tax_vat IS NULL then
                iTaxVatArticle = 0;
            ELSE
                iTaxVatArticle = rData.tax_vat ;
            END IF ;
        END IF ;
        IF iTaxVatArticle>0 then
            select into rData vat_value from tax_vat where id = iTaxVatArticle;
            fTaxVat = rData.vat_value ;
        else
        
            fTaxVat = 0.00 ;
        END IF;

        
        return fTaxVat ;
    END ;
    ' LANGUAGE 'plpgsql'; 

       
    
CREATE OR REPLACE FUNCTION fct_get_net_for_article( iArticleID integer) returns  bool AS '
 
    DECLARE
        sSql    text ;
        bNet bool ;
        net bool ;
        rData  record ;
    BEGIN 
        bNet := true ;
        raise notice '' net value is %'',bNet ;
        select into rData price_type_net from material_group, articles where articles.id = iArticleID and articles.material_group = material_group.id ;
        
        if rData.price_type_net is null then 
            bNet := true ;
        else
            bNet := rData.price_type_net ;
        end if ;
        
        raise notice '' net value is %'',bNet ;
       return bNet ;
    END ;
    ' LANGUAGE 'plpgsql'; 
