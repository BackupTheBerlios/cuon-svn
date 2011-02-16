 CREATE OR REPLACE FUNCTION fct_getAddress(  iAddressID int) returns  record AS '
 
     DECLARE
    sSql    text ;
    recAddress  record;
    
    
    
    BEGIN
    sSql := ''select address, lastname, lastname2,firstname, street, zip, city,city as cityfield,  
        state, country from address 
        where id = '' || iAddressID  || '' '' || fct_getWhere(2,'' '') ;
    for recAddress in execute sSql 
    LOOP 
        raise notice ''addresslastnmae = %'',recAddress.lastname ;
        raise notice ''address = %'',recAddress.address ;
        --raise notice ''cityfield = %'',recAddress.cityfield ;
       
        if recAddress.country is NULL then
            recAddress.cityfield := recAddress.zip || '' '' || recAddress.city ;
        else 
            recAddress.cityfield := recAddress.country || ''-'' || recAddress.zip || '' '' || recAddress.city ;
        END IF ;
        --recAddress.country := fct_getChar(recAddress.country) ;
        raise notice ''country = %'',recAddress.country ;
       raise notice ''cityfield = %'',recAddress.cityfield ;
       
    END LOOP ;
    return recAddress  ;
       END ;
    ' LANGUAGE 'plpgsql'; 
 
            # first set new li scheduls

CREATE OR REPLACE FUNCTION fct_getSchedulTime(  iTimeBegin int, iTimeEnd int , aTimes char[] ,recId int) returns  varchar AS '
 
     DECLARE
    sSql    text ;
    sTime varchar;
    BEGIN 
        sTime := aTimes[iTimeBegin] || '' - '' ||  aTimes[iTimeEnd]  ;
        
    return sTime ;
       END ;
    ' LANGUAGE 'plpgsql'; 



 
