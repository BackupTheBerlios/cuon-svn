  
     CREATE OR REPLACE FUNCTION fct_orderposition_insert( ) returns OPAQUE AS '
    --  set default values to orderposition 
     
    
    BEGIN
               IF NEW.tax_vat is NULL THEN
                    NEW.tax_vat = 0.00 ;
               end if ;
               IF NEW.discount is NULL THEN
                    NEW.discount = 0.00 ;
               end if ;
               RETURN NEW; 
    END;
  
     ' LANGUAGE 'plpgsql'; 
     
  
  
  
  
  CREATE OR REPLACE FUNCTION fct_setUserData( dicUser char  [] ) returns bool AS '
    -- set the userdata for the current work
     
    DECLARE
    sName char(50) ;    
    sClient char ;
    sNoWhereClient char ;
    iNextID     int ;

    BEGIN
    
        sName := dicUser[1];
        sClient := dicUser[2];
        sNoWhereClient := dicUser[3];
        
        execute ''delete from cuon_user where username = '' || quote_literal(sName )  ;
        select into iNextID nextval from  nextval(''cuon_user_id''); 

        execute ''insert into  cuon_user (id,username, current_client, no_where_client ) VALUES (
        '' || iNextID || '', '' || quote_literal(sName) || '','' || sClient  ||'','' || sNoWhereClient || '' )'' ;
        
        return 1 ;
    END ;
    
     ' LANGUAGE 'plpgsql'; 
     
     
     
   CREATE OR REPLACE FUNCTION  fct_getUserDataClient(  ) returns int AS '
   -- get the client id
    DECLARE
    iClient    int ;
    sClient char ;
    BEGIN
    
        select into iClient current_client from cuon_user where username = CURRENT_USER ;
        raise notice ''Client id = %'', iClient ;
        return iClient ;
    END ;
    
     ' LANGUAGE 'plpgsql'; 
     
     
     
   CREATE OR REPLACE FUNCTION  fct_getUserDataNoWhereClient(  ) returns int  AS '
       -- get the nowhereclient id
     DECLARE
    iClient    int ;
    sClient char ;
    BEGIN
    
        select into iClient no_where_client from cuon_user where username = CURRENT_USER ;
        raise notice ''NoWhereClient id = %'', iClient ;
        return iClient ;
    END ;
    
     ' LANGUAGE 'plpgsql'; 
     
     
   CREATE OR REPLACE FUNCTION  fct_getWhere(iSingle int,  sPrefix char ) returns text  AS '
    -- retuns the sWhere value
     DECLARE
    sWhere  text ;
    iClient int ;
    iNoWhereClient int ;

    BEGIN
        iClient := fct_getUserDataClient();
        iNoWhereClient := fct_getUserDataNoWhereClient();
        
    sWhere := '' '' ;
    if iNoWhereClient = ''0''
    then
        if iSingle = 1
        then
             sWhere := ''WHERE '' ||  sPrefix  || ''client = '' || iClient || '' and '' || sPrefix  || ''status != ''''delete'''' '' ;
                    

        else 
            if iSingle = 2
            then
                sWhere := ''AND '' ||  sPrefix  || ''client = '' || iClient || '' and '' || sPrefix  || ''status != ''''delete'''' '' ;
            END IF ;
        END IF ;
        
    END IF ;

    RETURN sWhere ;
    END ;
     ' LANGUAGE 'plpgsql'; 
    
      
