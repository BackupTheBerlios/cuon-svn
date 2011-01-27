
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

DROP FUNCTION fct_getGravePlantListValues(IN dicSearchfields text [], IN iRows int ) CASCADE ;
CREATE OR REPLACE FUNCTION fct_getGravePlantListValues(graveyard_id int, grave_lastname_from text, grave_lastname_to text, eSequentialNumberFrom text, eSequentialNumberTo text,  iRows int ) returns setof record AS '
 DECLARE
     iClient int ;
    r record;
    searchsql text := '''';
   
    
    
    BEGIN
        -- graveyard.lastname 
        -- grab laufnummer
        
        -- raise notice '' sql = %'', searchsql ;
        searchsql := ''select graveyard.shortname , graveyard.designation , grave.firstname , grave.lastname  from  graveyard, grave, address where grave.addressid = address.id and grave.graveyardid = graveyard.id ''  ;
        
        IF graveyard_id > 0 THEN
        
            searchsql := searchsql  || '' and graveyard.id = '' || graveyard_id || '' '' ;
        END IF ;
            
        IF char_length(grave_lastname_from) > 0 AND char_length(grave_lastname_to) > 0 THEN 
            
            searchsql := searchsql  || '' and grave.lastname between '' || quote_literal(grave_lastname_from) || '' and '' || quote_literal(grave_lastname_to)   || '' '' ;
        
        END IF ;
        
        IF char_length(eSequentialNumberFrom) > 0 AND char_length(eSequentialNumberTo) > 0 THEN 
           
            searchsql := searchsql  || '' and pos_number between '' || eSequentialNumberFrom || '' and '' || eSequentialNumberTo || '' '' ;
        END IF ;
        
        
        
        
        searchsql := searchsql  ||  fct_getWhere(2,''graveyard.'') || '' order by graveyard.shortname, grave.pos_number, grave.lastname, grave.firstname '';


        raise notice '' sql = %'', searchsql ;
        
         FOR r in execute(searchsql)  LOOP
         
        
            return next r ;

        END LOOP ;
        
    END ;
    

    
     ' LANGUAGE 'plpgsql'; 

   
