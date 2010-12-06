
 CREATE OR REPLACE FUNCTION fct_getGravesForAddressID(iAddressID int ) returns setof text AS '
 DECLARE
     iClient int ;
    r record;
    searchsql text := '''';

    BEGIN
       
         searchsql := ''select graveyard.shortname as graveyard ,grave.lastname as lastname ,grave.firstname as firstname, grave.id as gravevalue from graveyard, grave  where grave.addressid = '' || iAddressID ||  ''and graveyard.id = grave.graveyardid ''  || fct_getWhere(2,''graveyard.'') ;


        FOR r in execute(searchsql)  LOOP
         
        
         return next r.graveyard || '', '' || r.lastname || '', '' || r.firstname || ''   ###'' || r.gravevalue ;

        END LOOP ;
        
    END ;
    

    
     ' LANGUAGE 'plpgsql'; 


CREATE OR REPLACE FUNCTION fct_getGravePlantListValues(IN dicSearchfields char [] , IN iRows int ) returns setof record AS '
 DECLARE
     iClient int ;
    r record;
    searchsql text := '''';

    BEGIN
       
         searchsql := ''select graveyard.shortname , graveyard.designation , grave.firstname , grave.lastname  from  graveyard, grave, address where grave.addressid = address.id ''  || fct_getWhere(2,''graveyard.'') || '' order by graveyard.id '';


        FOR r in execute(searchsql)  LOOP
         
        
            return next r ;

        END LOOP ;
        
    END ;
    

    
     ' LANGUAGE 'plpgsql'; 

   
