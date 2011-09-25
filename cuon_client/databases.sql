
 
CREATE OR REPLACE FUNCTION fct_checkColumn( tablename text, columnname text, typename text, first_size int, second_size int ) returns bool AS '
    -- check and alter table and column
     
    DECLARE
    ok bool;
    sSql text ;
    
    
    BEGIN
        ok = false ;
        
        sSql := ''SELECT a.attname as a_column, pg_catalog.format_type(a.atttypid, a.atttypmod) as p_datatype FROM  pg_catalog.pg_attribute a '' ;
        sSql := sSql || '' WHERE  a.attnum > 0  AND NOT a.attisdropped AND a.attrelid = ( SELECT c.oid FROM pg_catalog.pg_class c LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace  WHERE c.relname = '' || quote_literal(tablename )  ;
        sSql := sSql || '' AND pg_catalog.pg_table_is_visible(c.oid)  ) '' ;

        raise notice '' sSql = %'',sSql ;
        
        
        return ok ;
    END ;
    
     ' LANGUAGE 'plpgsql'; 
   

   

   
CREATE OR REPLACE FUNCTION fct_duplicate_table( tablename text, tablename2 text ) returns bool AS '
    -- insert whole table1 in table2
     
    DECLARE
    ok bool;
    sSql text ;
    sExe text ;
    sExe2 text ;
    sSql2 text ;
    ri record ;
    oldrecord record ;
    len int ;
    
    
    BEGIN
        ok = true ;
    
        sExe := '' insert into '' || tablename2 || '' ( '' ;
        sExe2 := '' select  '' ;
        sSql := '' SELECT ordinal_position, column_name, data_type  FROM information_schema.columns   WHERE    table_schema = '' || quote_literal(''public'') || ''  AND table_name = '' || quote_literal(tablename) || '' ORDER BY ordinal_position '' ;
        
        sSql2 := ''select id from '' || tablename ;
        raise notice '' sSql= %'', sSql ;
        raise notice '' sSql2= %'', sSql2 ;
        FOR oldrecord in execute(sSql2) LOOP
            raise notice ''start loop1 '' ;
            FOR ri in execute(sSql) LOOP
        
        
           
                sExe := sExe || ri.column_name || '', '' ;
                sExe2 := sExe2 || ri.column_name || '', '' ;
                      
                        
            END LOOP;
            raise notice ''end loop2 '' ;
            len := length(sExe);    
            sExe := substring(sExe from 1 for (len-2) ) ;
            sExe := sExe || '' ) '' ;
            
            len := length(sExe2);    
            sExe2 := substring(sExe2 from 1 for (len-2) ) ;
            
            
            
            sExe := sExe || sExe2 || '' from '' || quote_ident(tablename) || '' where id = '' || oldrecord.id ;
            raise notice '' sExe = %'', sExe ;
            -- execute sExe ;
        
         END LOOP;
      return ok ;
    END ;
    
     ' LANGUAGE 'plpgsql'; 
   
   
  
CREATE OR REPLACE FUNCTION fct_duplicate_table_entry( tablename text, tablename2 text, oldid int, id_sequence text ) returns int AS '
    -- insert whole table1 in table2
     
    DECLARE
    ok bool;
    sSql text ;
    sExe text ;
    sExe2 text ;
    sSql2 text ;
    ri record ;
    oldrecord record ;
    len int ;
    newid int ;
    sSql3 text ;
    BEGIN
        ok = true ;
        sSql3 = ''select nextval('' || quote_literal(id_sequence) || '') '' ;
        execute(sSql3) into newid ;
        
        sExe := '' insert into '' || tablename2 || '' ( '' ;
        sExe2 := '' ( select  '' ;
        sSql := '' SELECT ordinal_position, column_name, data_type  FROM information_schema.columns   WHERE    table_schema = '' || quote_literal(''public'') || ''  AND table_name = '' || quote_literal(tablename) || '' ORDER BY ordinal_position '' ;
        
        sSql2 := ''select id from '' || tablename || '' where id = '' || oldid  ;
        raise notice '' sSql= %'', sSql ;
        raise notice '' sSql2= %'', sSql2 ;
        FOR oldrecord in execute(sSql2) LOOP
            raise notice ''start loop1 '' ;
            FOR ri in execute(sSql) LOOP
        
        
                IF ri.column_name = ''id'' THEN
                    sExe := sExe || ri.column_name || '', '' ;
                    sExe2 := sExe2 || newid || '' , '' ;
                ELSE 
                    sExe := sExe || ri.column_name || '', '' ;
                    sExe2 := sExe2 || ri.column_name || '', '' ;
                END IF ;
                      
                        
            END LOOP;
            raise notice ''end loop2 '' ;
            len := length(sExe);    
            sExe := substring(sExe from 1 for (len-2) ) ;
            sExe := sExe || '' ) '' ;
            
            len := length(sExe2);    
            sExe2 := substring(sExe2 from 1 for (len-2) ) ;
            
            
            
            sExe := sExe || sExe2 || '' from '' || quote_ident(tablename) || '' where id = '' || oldid  || '' ) '' ;
            raise notice '' sExe = %'', sExe ;
            execute sExe ;
        
         END LOOP;
      return newid ;
    END ;
    
     ' LANGUAGE 'plpgsql'; 
   

