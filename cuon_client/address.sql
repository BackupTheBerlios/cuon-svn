<sql>
  <postgre_sql>
    <nameOfSqlDatabase>Postgre SQL</nameOfSqlDatabase>
      <function>
     
      <nameOfFunction>  fct_getAddress(  iAddressID int) returns  record</nameOfFunction>
      <language>plpgsql</language>
    <textOfFunction>
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
     </textOfFunction>
    <description>get the caddress of an id </description>

    </function>
  </postgre_sql>
  
</sql>
