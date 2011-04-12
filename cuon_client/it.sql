CREATE OR REPLACE FUNCTION fct_create_index(sName text,sTable text, sColumn text ,sUnique text) returns bool AS '
 DECLARE
    bRet bool := False ;
    sSql text ;
    
    BEGIN
    
      begin
        sSql := ''DROP  INDEX '' || sName  ;
        execute sSql ;
        exception when others then
          raise notice ''error Index Drop'';
          raise notice ''SQL = %'', sSql ;
      end;
      
      begin
      sSql := ''CREATE '' || sUnique ||'' INDEX '' || sName || '' ON '' || sTable || '' ('' || sColumn|| '')'' ;
      execute sSql ;
      exception when others then
          raise notice ''error Index Create'';
          raise notice ''SQL = %'', sSql ;
      end;
    

    return bRet ;     
    END ;
        
     ' LANGUAGE 'plpgsql';     
     
     
CREATE OR REPLACE FUNCTION fct_create_trigger(sName text, sTable text , sAction text, sCursor text, sText text) returns bool AS '
 DECLARE
    bRet bool := False ;
    sSql text ;
    BEGIN
      begin
        sSql := ''DROP TRIGGER '' || sName || '' ON '' || sTable ;
        execute sSql ;
        exception when others then
          raise notice ''error 1'';
          raise notice ''SQL = %'', sSql ;
      end;
      
      begin
        sSql := ''CREATE TRIGGER '' || sName ||'' '' || sAction ||'' ON '' || sTable || '' '' ||sCursor || '' '' || sText ;
        execute sSql ;
        exception when others then
          raise notice ''error 2'';
          raise notice ''SQL = %'', sSql ;
      end;
         
    return bRet ;
    END ;
   
    ' LANGUAGE 'plpgsql';     
    
       
CREATE OR REPLACE FUNCTION fct_create_allindex()    returns bool AS '
  DECLARE
    bRet bool := True ;
    
    BEGIN 
    
        -- cuon_user 
        perform fct_create_index(''cuon_user_idx_name'', ''cuon_user'', ''username'', '' '' );

        -- address 
        perform fct_create_index(''address_idx_lastname'', ''address'', ''lastname'', '' '' );
        perform fct_create_index(''address_idx_firstname'', ''address'', ''firstname'', '' '' );
        perform fct_create_index(''address_idx_phone'', ''address'', ''phone'', '' '' );
        perform fct_create_index(''address_idx_caller_id'', ''address'', ''caller_id'', '' '' );
        perform fct_create_index(''address_idx_rep_id'', ''address'', ''rep_id'', '' '' );
        perform fct_create_index(''address_idx_salesman_id'', ''address'', ''salesman_id'', '' '' );
        perform fct_create_index(''address_idx_status_info'', ''address'', ''status_info'', '' '' );
        perform fct_create_index(''address_idx_status_client'', ''address'', ''status,client'', '' '' );
        perform fct_create_index(''address_idx_newsletter'', ''address'', ''newsletter'', '' '' );
        
        -- partner
        perform fct_create_index(''partner_idx_addressid'', ''partner'', ''addressid'', '' '' );
        perform fct_create_index(''partner_idx_status_client'', ''partner'', ''status,client'', '' '' );

        -- partner_schedul
        perform fct_create_index(''partner_schedul_idx_partnerid'', ''partner_schedul'', ''partnerid'', '' '' );
        perform fct_create_index(''partner_schedul_idx_process_status'', ''partner_schedul'', ''process_status'', '' '' );
        perform fct_create_index(''partner_schedul_idx_status_client'', ''partner_schedul'', ''status,client'', '' '' );
        perform fct_create_index(''partner_schedul_idx_user_id'', ''partner_schedul'', ''user_id'', '' '' );
        perform fct_create_index(''partner_schedul_idx_schedul_staff_id'', ''partner_schedul'', ''schedul_staff_id'', '' '' );

        -- address_notes
        perform fct_create_index(''address_notes_idx_address_id'', ''address_notes'', ''address_id'', '' '' );
        perform fct_create_index(''address_notes_idx_status_client'', ''address_notes'', ''status,client'', '' '' );

        
        return bRet ;
    END ;
   
    ' LANGUAGE 'plpgsql'; 
  
  
CREATE OR REPLACE FUNCTION fct_create_alltrigger()    returns bool AS '
  DECLARE
    bRet bool := True ;
    vList text[]  ;
    array_size integer ;
    sSql text ;
    BEGIN
    
        vList[1] := ''address'' ;
        vList[2] := ''partner'' ;
        vList[3] := ''address_notes'' ;
        
        vList[4] := ''list_of_deliveries'' ;
      
        array_size := 4;
      
        for ct in 1..array_size loop
            -- raise notice '' ct = %, array = % '', ct,vList[ct] ;
            sSql := ''select * from fct_create_Trigger(''''trg_insert'' || vList[ct] || '''''','' || quote_literal(vList[ct]) ||'', ''''before insert'''', ''''FOR EACH ROW'''',''''EXECUTE PROCEDURE fct_insert()'''' )'' ;  -- EXECUTE PROCEDURE fct_insert()
            -- raise notice ''alltrigger sSql = %'', sSql ;
            execute sSql ;
            sSql := ''select * from fct_create_Trigger(''''trg_delete'' || vList[ct] || '''''','' || quote_literal(vList[ct]) ||'', ''''before delete'''', ''''FOR EACH ROW'''',''''EXECUTE PROCEDURE fct_delete()'''' )'' ;  -- EXECUTE PROCEDURE fct_insert()
            -- raise notice ''alltrigger sSql = %'', sSql ;
            execute sSql ;
         
            sSql := ''select * from fct_create_Trigger(''''trg_update'' || vList[ct] || '''''','' || quote_literal(vList[ct]) ||'', ''''before update'''', ''''FOR EACH ROW'''',''''EXECUTE PROCEDURE fct_update()'''' )'' ;  -- EXECUTE PROCEDURE fct_insert()
         -- raise notice ''alltrigger sSql = %'', sSql ;
            execute sSql ;    
         
         
        
        
        end loop;  
    

        return bRet ;
    END ;
   
    ' LANGUAGE 'plpgsql';     
    

  
CREATE OR REPLACE FUNCTION fct_test_array()    returns bool AS '
  DECLARE
    bRet bool := True ;
    vList integer[]  ;
    array_size integer ;
    ct integer ;
    BEGIN   
    vList[1] := 1 ;
    vList[2] := 7 ;
    vList[3] := 9 ;
    vList[4] := 11 ;
    
    array_size := 4;
    for ct in 1..array_size loop
      raise notice '' ct = %, array = % '', ct,vList[ct] ;
    end loop;  
    return bRet ;
    END ;
   
    ' LANGUAGE 'plpgsql';  
