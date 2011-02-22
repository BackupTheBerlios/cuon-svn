 

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

    
    
    
    
