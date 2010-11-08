
 -- All this here are for trigger or very basic funtions
 
    
     DROP FUNCTION fct_orderposition_insert() CASCADE ;
     
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
        -- raise notice ''Client id = %'', iClient ;
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
        -- raise notice ''NoWhereClient id = %'', iClient ;
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
    if iNoWhereClient = ''1''
    then
        if iSingle = 1
        then
             sWhere := ''WHERE '' ||  sPrefix  || ''client = '' || iClient || '' and '' || sPrefix  || ''status != ''''delete'''' '' ;
                    

        else 
            if iSingle = 2   then
                sWhere := ''AND '' ||  sPrefix  || ''client = '' || iClient || '' and '' || sPrefix  || ''status != ''''delete'''' '' ;
            END IF ;
        END IF ;
        
    END IF ;

  
    -- RAISE NOTICE '' sWhere  = %'', sWhere ;
    RETURN sWhere ;
    END ;
     ' LANGUAGE 'plpgsql'; 
     
    
    CREATE OR REPLACE FUNCTION fct_new_uuid()   RETURNS char(36) AS '
    DECLARE
    
    this_uuid char(36) ;
    new_md5 char(32) ;
    BEGIN
        SELECT into new_md5 md5(current_database()|| user ||current_timestamp ||random() ) ;
        -- 8 4 4 4 12
        this_uuid = substring(new_md5 from 1 for 8) || ''-'' || substring(new_md5 from 9 for 4) || ''-'' || substring(new_md5 from 13 for 4) || ''-'' || substring(new_md5 from 17 for 4) || ''-'' || substring(new_md5 from 21 for 12) ;
    
        --raise notice ''new uuid '', this_uuid ;
       
        
        RETURN this_uuid ;
        
    END ;
    ' LANGUAGE 'plpgsql'; 

    

 DROP FUNCTION fct_insert() CASCADE ;
 
 CREATE OR REPLACE FUNCTION fct_insert( ) returns OPAQUE AS '
    --  set default values at an insert operation 
     
    BEGIN
        NEW.user_id = current_user   ;
        NEW.insert_time = (select  now()) ;
        NEW.status = ''insert'' ;
        NEW.versions_uuid = fct_new_uuid()   ;
        NEW.versions_number = 1 ;
        --RAISE NOTICE ''Name =  % '', TG_NAME ;
        RETURN NEW; 
    END;
     
    ' LANGUAGE 'plpgsql'; 

    
 DROP FUNCTION fct_update() CASCADE ;
 
 CREATE OR REPLACE FUNCTION fct_update( ) returns OPAQUE AS '
    --  set default values at an update operation 
     
    DECLARE
        history_table   varchar(400) ;
        cName           varchar(300) ;
       sText text ;
         ri RECORD;
         q record ;
    t TEXT;
    sSql text ;
    sSql2 text ;
        sExe text ;
        sExe2 text ;
        len integer ;
        
    BEGIN
        history_table := TG_TABLE_NAME || ''_history'' ;
        
        IF TG_TABLE_NAME = ''partner_schedul'' then
            
        if OLD.versions_uuid is NULL OR char_length(OLD.versions_uuid ) <36 then 
                OLD.versions_uuid := fct_new_uuid()   ;
        end if ;  
        if OLD.versions_number is NULL OR OLD.versions_number  < 1 then 
                OLD.versions_number := 1 ;
        end if ;  
        if not OLD.status = ''delete'' then 
        
            sExe := '' insert into '' || history_table || '' ( '' ;
            sExe2 := '' select  '' ;
            sSql := '' SELECT ordinal_position, column_name, data_type  FROM information_schema.columns   WHERE    table_schema = '' || quote_literal(TG_TABLE_SCHEMA) || ''  AND table_name = '' || quote_literal(TG_TABLE_NAME) || '' ORDER BY ordinal_position '' ;
            
            
            FOR ri in execute(sSql)  
               
                LOOP
                    
                   
                    sExe := sExe || ri.column_name || '', '' ;
                    sExe2 := sExe2 || ri.column_name || '', '' ;
                  
                    
                END LOOP;
            len := length(sExe);    
            sExe := substring(sExe from 1 for (len-2) ) ;
            sExe := sExe || '' ) '' ;
            
            len := length(sExe2);    
            sExe2 := substring(sExe2 from 1 for (len-2) ) ;
            
            
            
            sExe := sExe || sExe2 || '' from '' || quote_ident(TG_TABLE_NAME) || '' where id = '' || OLD.id ;
            -- raise notice '' sExe = %'', sExe ;
            execute sExe ;
            
            NEW.update_user_id := current_user   ;
            NEW.update_time := (select  now()) ;
            NEW.user_id := OLD.user_id;
            
            NEW.insert_time := OLD.insert_time ;
            
            if NEW.status != ''delete'' then
                NEW.status := ''update'' ;
            END IF ;
            
            NEW.versions_number := OLD.versions_number+1 ;
            NEW.versions_uuid :=OLD.versions_uuid ;
      
           
            
            RETURN NEW; 
        else 
            RETURN OLD;
        end if ;
      
    END;
    
  
    ' LANGUAGE 'plpgsql'; 

    
 DROP FUNCTION fct_delete() CASCADE ;
 
CREATE OR REPLACE FUNCTION fct_delete( ) returns OPAQUE AS '
    --  set default values at a delete 
    -- if delete a record, dont realy delete, set status to delete 
     
    DECLARE
    f_upd     varchar(400);
    v_delete varchar(20) ;
    BEGIN
        v_delete   := ''delete'' ;
        f_upd := '' update '' || TG_RELNAME  || '' set status =  ''|| quote_literal(v_delete) || ''  where id = '' || OLD.id   ;
        -- RAISE NOTICE '' table-name =  % '', TG_RELNAME ;
        -- RAISE NOTICE '' sql =  % '',f_upd  ;
        execute f_upd ;
        -- RAISE NOTICE '' Name =  % '', TG_NAME ;
        RETURN NULL ;
    END;
     
     ' LANGUAGE 'plpgsql'; 
 
 
