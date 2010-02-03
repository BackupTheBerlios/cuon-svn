CREATE OR REPLACE FUNCTION fct_selectTable(s_table varchar, s_list varchar, s_where varchar, s_limit int ) returns setof RECORD AS '  
    DECLARE
    e1  varchar(5) ;
    v_fila   RECORD ;

    BEGIN
        
        FOR v_fila in 
        Execute ''SELECT '' || s_list || '' from address ''  LOOP
        RETURN NEXT v_fila ;
    END LOOP ;

    RETURN ;

    END ;
       ' LANGUAGE 'plpgsql'; 


CREATE OR REPLACE FUNCTION fct_getWhere_old(iSingle int, dicUser char[] , sPrefix char ) returns text AS '  
    DECLARE
    sWhere  text ;
    iClient char ;
    iNoWhereClient char ;

    BEGIN
    iClient := dicUser[2];
    iNoWhereClient := dicUser[3];
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

CREATE OR REPLACE FUNCTION old_fct_changeProposal2Order(iProposalID int ) returns bool AS '  
    DECLARE
    
    iClient char ;
 

    BEGIN
    
        
        update orderbook set process_status = 500 where id = iProposalID ;
        if FOUND then
            return 1 ;
        else 
            return 0 ;
        end if ;
        
    END ;
       ' LANGUAGE 'plpgsql'; 
       
       
CREATE OR REPLACE FUNCTION old_fct_setUserData( dicUser char  [] ) returns bool AS '  
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
    
    CREATE OR REPLACE FUNCTION old_fct_getUserDataClient(  ) returns int AS '  
    DECLARE
    iClient    int ;
    sClient char ;
    BEGIN
    
        select into iClient current_client from cuon_user where username = CURRENT_USER ;
        -- raise notice ''Client id = %'', iClient ;
        return iClient ;
    END ;
       ' LANGUAGE 'plpgsql'; 
    
    
        CREATE OR REPLACE FUNCTION old_fct_getAddress(  iAddressID int) returns  record  AS '  
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
    
    CREATE OR REPLACE FUNCTION fct_getChar(sValue varchar ) returns  varchar  AS '  
    DECLARE
    BEGIN
        if sValue is null then
            return  '''' ;
        END IF ;
        return sValue ;
        
    END ;
       ' LANGUAGE 'plpgsql'; 
    
    
        CREATE OR REPLACE FUNCTION  old_fct_getOrderTotalSum(  iOrderid int) returns float AS '  
    DECLARE
    fSum     float ;
    sClient char ;
    cur1 CURSOR FOR SELECT amount, price, discount FROM orderposition WHERE  orderid = iOrderid;
    fAmount     float;
    fPrice  float;
    fDiscount   float ;
    count   integer ;
    BEGIN
        fSum := 0.0 ;
        open cur1 ;
        FETCH cur1 INTO fAmount, fPrice, fDiscount ;

        count := 0;

    WHILE FOUND LOOP
        RAISE NOTICE ''total sum for position , amount %, price % , discount %'', fAmount,fPrice,fDiscount ;
        if fDiscount IS NULL then
            fDiscount := 0.0 ;
        end if ;
        
        fSum := fSum + ( fAmount * (fPrice * (100 - fDiscount)/100 ) ) ;
        FETCH cur1 INTO fAmount, fPrice, fDiscount ;
    END LOOP ;
    close cur1 ;
    
    /* now get the whole discount */
    select into fDiscount discount from orderbook where id = iOrderid ;
    if fDiscount IS NULL then
            fDiscount := 0.0 ;
        end if ;
    fSum := fSum * ((100 - fDiscount)/100 )  ;
    
    return fSum ;
    END ;
       ' LANGUAGE 'plpgsql'; 
       
       
