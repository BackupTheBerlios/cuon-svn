
 CREATE OR REPLACE FUNCTION fct_getGravesForAddressID(iAddressID int ) returns setof record AS '
 DECLARE
     iClient int ;
    r record;
    searchsql text := '';

    BEGIN
       
         searchsql := 'select graveyard.shortname || grave.lastname || grave.firstname || ''###'' || to_char(grave.id,''99999999999999999'') as gravevalue from graveyard, grave  where grave.addressid = '|| iAddressID ||' and graveyard.id = grave.graveyardid '|| fct_getWhere(2,' ')  ;


        FOR r in execute(searchsql)  LOOP
         
        
         return next r;

        END LOOP ;
        
    END ;
    

    
     ' LANGUAGE 'plpgsql'; 
