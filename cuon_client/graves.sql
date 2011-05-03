
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

DROP FUNCTION IF EXISTS fct_getGravePlantListSQL(  int, text,  text, text, text,  text, text, text, text, int ) CASCADE ;
DROP FUNCTION IF EXISTS fct_getGravePlantListSQL(  int, text,  text, text, text,  text, text, text, text, int,text,text ) CASCADE ;
CREATE OR REPLACE FUNCTION fct_getGravePlantListSQL(graveyard_id int, grave_lastname_from text, grave_lastname_to text, eSequentialNumberFrom text, eSequentialNumberTo text, dContractBeginFrom text, dContractBeginTo text, dContractEndsFrom text, dContractEndsTo text, contract int, service int, plantation int,price int, iRows int ,additionalRows text, additionalTables text, additionalWhere text) returns text AS '   
 DECLARE
        iClient int ;
       
        searchsql text := '''';
   
        iIndex integer ;
        iIndex2 integer  ;
        sSub1 text ;
        sSub2 text ;
        
    BEGIN
    -- graveyard.lastname 
        -- grab laufnummer
        
        
        searchsql := ''select graveyard.id as graveyard_id, grave.id as grave_id, graveyard.shortname , graveyard.designation , grave.firstname , grave.lastname, grave.pos_number, grave. contract_begins_at , grave.contract_ends_at , grave.detachment , grave.grave_number '' ;
         searchsql :=  searchsql  || additionalRows ;
        
        searchsql :=  searchsql  || ''from  graveyard, grave, address ''  || additionalTables || '' where ''  ;
        
        searchsql :=  searchsql  ||  '' grave.addressid = address.id and grave.graveyardid = graveyard.id and graveyard.id = '' || graveyard_id || '' ''  ;
        searchsql := searchsql || '' and grave.status != ''''delete'''' '' ;
        searchsql :=  searchsql  || additionalWhere || '' '' ;
        
        IF graveyard_id > 0 THEN
        
            searchsql := searchsql  || '' and graveyard.id = '' || graveyard_id || '' '' ;
        END IF ;
            
        IF char_length(grave_lastname_from) > 0 AND char_length(grave_lastname_to) > 0 THEN 
            
            searchsql := searchsql  || '' and grave.lastname between '' || quote_literal(grave_lastname_from) || '' and '' || quote_literal(grave_lastname_to)   || '' '' ;
        
        END IF ;
         IF char_length(grave_lastname_from) > 0 AND char_length(grave_lastname_to) = 0 THEN 
            iIndex := position(''#!#'' in grave_lastname_from) ;
            
            if iIndex > -1 then
                grave_lastname_from := overlay(grave_lastname_from placing '''' from iIndex for 3) ;
                
            end if ;
            sSub1 := substring(grave_lastname_from from 0 for iIndex) ;
            
            iIndex2 := position(''#!#'' in grave_lastname_from) ;
            
            if iIndex2 > -1 then
                grave_lastname_from := overlay(grave_lastname_from placing '''' from iIndex2 for 3) ;
                
            end if ;
            sSub2 := substring(grave_lastname_from from iIndex ) ;
            grave_lastname_from := sSub1 || quote_literal(sSub2) ;
            searchsql := searchsql  || '' and grave.lastname '' || grave_lastname_from || '' '' ;
        END IF ;
        
        IF char_length(eSequentialNumberFrom) > 0 AND char_length(eSequentialNumberTo) > 0 THEN 
           
            searchsql := searchsql  || '' and pos_number between '' || eSequentialNumberFrom || '' and '' || eSequentialNumberTo || '' '' ;
        END IF ;
        if price > -1 then 
            searchsql := searchsql  || '' and type_of_paid = price '' ;
        end if ;
        
        IF char_length(dContractBeginFrom) > 0 AND char_length(dContractBeginTo) > 0 THEN 
            searchsql := searchsql  || '' and contract_begins_at between fct_to_date('' || quote_literal(dContractBeginFrom) || '') and fct_to_date('' || quote_literal(dContractBeginTo) ||'') '' ;
        END IF ;
        
        IF char_length(dContractEndsFrom) > 0 AND char_length(dContractEndsTo) > 0 THEN 
            searchsql := searchsql  || '' and contract_ends_at between fct_to_date('' || quote_literal(dContractEndsFrom) || '') and fct_to_date('' || quote_literal(dContractEndsTo) ||'') '' ;
        END IF ;
        

        IF contract = 1 THEN
            -- show only current running contracts
            
            searchsql := searchsql  || '' and (contract_ends_at  is  NULL or contract_ends_at > now() or contract_ends_at = '' || quote_literal(''1900-01-01'')  || '') '' ;
        END IF ;
        

        raise notice '' sql = %'', searchsql ;
        
        
        return searchsql ;
         
    END ;
    

    
     ' LANGUAGE 'plpgsql'; 
 
 
     
DROP FUNCTION IF EXISTS fct_getGravePlantListValues(IN dicSearchfields text [], IN iRows int ) CASCADE ;
DROP FUNCTION IF EXISTS fct_getGravePlantListValues(  int, text,  text, text, text,  text, text, text, text, int ) CASCADE ;
DROP FUNCTION IF EXISTS fct_getGravePlantListValues(  int, text,  text, text, text,  text, text, text, text, int, int ) CASCADE ;

CREATE OR REPLACE FUNCTION fct_getGravePlantListValues(graveyard_id int, grave_lastname_from text, grave_lastname_to text, eSequentialNumberFrom text, eSequentialNumberTo text, dContractBeginFrom text, dContractBeginTo text, dContractEndsFrom text, dContractEndsTo text, contract int,service int, plantation int, price int, iRows int , iOrderSort int ) returns setof record AS '
    DECLARE
        iClient int ;
        r record;
        searchsql text := '''';
        additionalTables text := '' '' ;
        additionalWhere text  := '' '' ;
         additionalRows text  := '' '' ;
    
    
    BEGIN
        searchsql := fct_getGravePlantListSQL(graveyard_id , grave_lastname_from , grave_lastname_to , eSequentialNumberFrom , eSequentialNumberTo , dContractBeginFrom , dContractBeginTo , dContractEndsFrom , dContractEndsTo ,contract,service, plantation, price, iRows,additionalRows,  additionalTables, additionalWhere) ;
        searchsql := searchsql  ||  fct_getWhere(2,''graveyard.'') || '' order by  graveyard.shortname, grave.pos_number, grave.lastname, grave.firstname '';
         FOR r in execute(searchsql)  LOOP
         
        
            return next r ;

        END LOOP ;
        
    END ;
    

    
     ' LANGUAGE 'plpgsql'; 

   
DROP FUNCTION IF EXISTS fct_getGravePlantListArticles(  int, text,  text, text, text,  text, text, text, text, int ) CASCADE ;
DROP FUNCTION IF EXISTS fct_getGravePlantListArticles(  int, text,  text, text, text,  text, text, text, text, int, int ) CASCADE ;

CREATE OR REPLACE FUNCTION fct_getGravePlantListArticles(graveyard_id int, grave_lastname_from text, grave_lastname_to text, eSequentialNumberFrom text, eSequentialNumberTo text, dContractBeginFrom text, dContractBeginTo text, dContractEndsFrom text, dContractEndsTo text, contract int, service int, plantation int, price int,  iRows int, iOrderSort int ) returns setof record AS '
    DECLARE
        iClient int ;
        r record;
        searchsql text := '''';
         additionalTables text := '' '' ;
        additionalWhere text  := '' '' ;
        additionalRows text  := '' '' ;
    
    
    BEGIN
        additionalTables  :='',grave_work_maintenance as gm, articles as ar  '' ;
        additionalWhere  := '' and gm.grave_id = grave.id and  gm.article_id = ar.id '' ;
        IF service > -1 THEN
            -- show the service graves
            
            additionalWhere := additionalWhere  || '' and gm.grave_service_id = '' || service || '' and gm.status != ''''delete'''' ''   ;
        END IF ;
        additionalRows  := '', gm.article_id as service_article_id , ar.number as article_number, ar.designation as article_designation,gm.service_price as service_price, gm.service_count as service_count '' ;
        
        searchsql := fct_getGravePlantListSQL(graveyard_id , grave_lastname_from , grave_lastname_to , eSequentialNumberFrom , eSequentialNumberTo , dContractBeginFrom , dContractBeginTo , dContractEndsFrom , dContractEndsTo ,contract,service, plantation, price,  iRows,additionalRows, additionalTables, additionalWhere) ;
        -- searchsql := searchsql || '' '' ;
        
        
       
        searchsql := searchsql  ||  fct_getWhere(2,''graveyard.'') || '' order by graveyard.id, grave.pos_number'';
        raise notice ''SQL = %'',searchsql ;
        
        for r in execute(searchsql)  LOOP 
            raise notice ''Article_number = %'',r.article_designation ;
            return  next r; 
        END LOOP ;
        
        
    END ;
    

    
     ' LANGUAGE 'plpgsql'; 

     
     
 
CREATE OR REPLACE FUNCTION fct_saveGraveServiceNote(iGraveID int, iGraveServiceID int,  sNote text ) returns int AS '
 DECLARE
  
    iRecordID int ;
    
    BEGIN
       select into iRecordID id from grave_service_notes where  grave_id = iGraveID and service_id = iGraveServiceID ;
        if iRecordID is null then 
            insert into grave_service_notes (id, grave_id, service_id, service_note) values (nextval(''grave_service_notes_id''),iGraveID,iGraveServiceID,sNote) ;
            iRecordID = 0;
        ELSE
            update grave_service_notes set service_note = sNote where grave_id = iGraveID and service_id = iGraveServiceID ;
        END IF ;
        
        return iRecordID ;
        
    END ;
    

    
     ' LANGUAGE 'plpgsql'; 
   
CREATE OR REPLACE FUNCTION fct_loadGraveServiceNote(iGraveID int, iGraveServiceID int ) returns text AS '
 DECLARE
  
    sNote text ;
    
    BEGIN
       select into sNote service_note from grave_service_notes where  grave_id = iGraveID and service_id = iGraveServiceID ;
        if sNote is null then 
            sNote = '' '' ;
        
        END IF ;
        
        return sNote;
        
    END ;
    

    
     ' LANGUAGE 'plpgsql'; 
