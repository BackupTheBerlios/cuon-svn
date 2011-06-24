
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
        newGravename text ;
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
         
            newGravename := grave_lastname_from ;
            iIndex := position(''#!#'' in newGravename) ;
            
            if iIndex > -1 then
                newGravename := overlay(newGravename placing '''' from iIndex for 3) ;
                
            end if ;
            sSub1 := substring(newGravename from 0 for iIndex) ;
            
            iIndex2 := position(''#!#'' in newGravename) ;
            
            if iIndex2 > -1 then
                newGravename := overlay(newGravename placing '''' from iIndex2 for 3) ;
                
            end if ;
            sSub2 := substring(newGravename from iIndex ) ;
            newGravename := sSub1 || quote_literal(sSub2) ;
            searchsql := searchsql  || '' and grave.lastname '' || newGravename || '' '' ;
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

CREATE OR REPLACE FUNCTION fct_getGravePlantListValues(graveyard_id int, grave_lastname_from text, grave_lastname_to text, eSequentialNumberFrom text, eSequentialNumberTo text, dContractBeginFrom text, dContractBeginTo text, dContractEndsFrom text, dContractEndsTo text, contract int,service int, plantation int, price int, timetab int, iRows int , iOrderSort int ) returns setof record AS '
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

CREATE OR REPLACE FUNCTION fct_getGravePlantListArticles(graveyard_id int, grave_lastname_from text, grave_lastname_to text, eSequentialNumberFrom text, eSequentialNumberTo text, dContractBeginFrom text, dContractBeginTo text, dContractEndsFrom text, dContractEndsTo text, contract int, service int, plantation int, price int, timetab int,  iRows int, iOrderSort int ) returns setof record AS '
    DECLARE
        iClient int ;
        r record;
        searchsql text := '''';
         additionalTables text := '' '' ;
        additionalWhere text  := '' '' ;
        additionalRows text  := '' '' ;
        GraveServiceNotesService int  := 40100  ;
        GraveServiceNotesSpring int  := 40101 ;
        GraveServiceNotesSummer int  := 40102 ;
        GraveServiceNotesAutumn int  := 40103 ;
        GraveServiceNotesWinter int  := 40104 ;
        GraveServiceNotesAnnual int  := 40105 ;
        GraveServiceNotesUnique int  := 40106 ;
        GraveServiceNotesHolliday int  := 40107 ;
         iGraveServiceID  int := 0 ;
         iRecordID int ;
        
    BEGIN
        IF timetab = 0 then 
            additionalTables  :='',grave_work_maintenance as gm, articles as ar  '' ;
             iGraveServiceID := GraveServiceNotesService ;
        ELSEIF timetab = 1 then 
            additionalTables  :='',grave_work_spring as gm, articles as ar  '' ;
              iGraveServiceID := GraveServiceNotesSpring ;
        ELSEIF timetab = 2 then 
            additionalTables  :='',grave_work_summer as gm, articles as ar  '' ;
              iGraveServiceID := GraveServiceNotesSummer ;
        ELSEIF timetab = 3 then 
            additionalTables  :='',grave_work_autumn as gm, articles as ar  '' ;
              iGraveServiceID := GraveServiceNotesAutumn ;
        ELSEIF timetab = 4 then 
            additionalTables  :='',grave_work_holiday as gm, articles as ar  '' ;
              iGraveServiceID := GraveServiceNotesHolliday ;
                       
        ELSEIF timetab = 5 then 
            additionalTables  :='',grave_work_winter as gm, articles as ar  '' ;
              iGraveServiceID := GraveServiceNotesWinter ;
        ELSEIF timetab = 6 then 
            additionalTables  :='',grave_work_year as gm, articles as ar  '' ;
             iGraveServiceID := GraveServiceNotesAnnual;       
        ELSEIF timetab = 7 then 
            additionalTables  :='',grave_work_single as gm, articles as ar  '' ;
              iGraveServiceID := GraveServiceNotesUnique ;
               
        END IF ;    
         
               
     
            
        additionalWhere  := '' and gm.grave_id = grave.id and  gm.article_id = ar.id '' || '' and gm.status != ''''delete'''' ''    ;
        
        IF service > -1 THEN
            -- show the service graves
                IF timetab = 0 then 
                        additionalWhere := additionalWhere  || '' and gm.grave_service_id = '' || service ;
                ELSE 
                        additionalWhere := additionalWhere  || '' and gm.period_id = '' || service ; 
                END IF ;
        END IF ;
        
        additionalRows  := '', gm.article_id as service_article_id , ar.number as article_number, ar.designation as article_designation,gm.service_price as service_price, gm.service_count as service_count, gm.service_notes as article_notes,  (select fct_loadGraveServiceNote(gm.grave_id, ''  ||  iGraveServiceID  || '' ) as service_notes ) , grave.common_notes as grave_notes '' ;
        
        searchsql := fct_getGravePlantListSQL(graveyard_id , grave_lastname_from , grave_lastname_to , eSequentialNumberFrom , eSequentialNumberTo , dContractBeginFrom , dContractBeginTo , dContractEndsFrom , dContractEndsTo ,contract,service, plantation, price,  iRows,additionalRows, additionalTables, additionalWhere)  
        ;
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
        ELSEIF ascii(sNote) = 32 then 
            sNote = '' '' ;
            
        END IF ;
        
        return sNote;
        
    END ;
    

    
     ' LANGUAGE 'plpgsql'; 

     
   
CREATE OR REPLACE FUNCTION fct_createNewInvoice(sService text , iServiceID int ) returns int AS '
 DECLARE
    
    iClient int ;
    sSql text   ;
    iNewOrderID int ;
    r1 record ;
    r2 record ;
   last_position int ;
    grave_headline int ;
    grave_headline_designation text ;
    BEGIN
    
        iClient = fct_getUserDataClient(  ) ;
        grave_headline = fct_get_config_option(iClient,''clients.ini'', ''CLIENT_'' || iClient, ''order_main_headline_articles_id'') ;
        select into iNewOrderID nextval(''orderbook_id'' ) ;
    
        raise notice '' new OrderNumber = %'', iNewOrderID ;
        
        sSql := '' select grave.*, graveyard.shortname as graveyard_shortname from grave, '' ;
        
        if sService = ''Service'' then
         
            sSql = sSql || ''grave_work_maintenance as gm '' ;
        end if ;
        
        sSql := sSql || '' where graveyard.id = grave.graveyardid and grave.id = gm.grave_id and gm.id = '' || iServiceID || '' ''  || fct_getWhere(2,''grave.'') ;
        execute(sSql) into r1 ;
        raise notice ''r1 = % '', r1.id ;

        sSql := '' insert into orderbook (id,addressnumber,ready_for_invoice,pricegroup1,pricegroup2,pricegroup3,pricegroup4,pricegroup_none, orderedat, from_modul, from_modul_id) values ('' ;
        sSql := sSql || iNewOrderID || '', '' || r1.addressid || '', true, '' || r1.pricegroup1 || '', '' || r1.pricegroup2 || '', '' || r1.pricegroup3 || '', '' || r1.pricegroup4 || '', '' || r1.pricegroup_none  ;
        sSql := sSql || '', '''''' ||  current_date  || '''''' , 40000, '' || r1.id || '' ) '' ;
        
        
        raise notice '' new sSql insert = % '', sSql ;
        
        
        execute (sSql) ;    
        
        select into last_position max(position) from orderposition where orderid = iNewOrderID ;
        if last_position IS NULL then 
            last_position = 0 ;
        end if ;
        
        grave_headline_designation := r1.lastname || '', '' || r1.detachment || '',  '' || r1.graveyard_shortname ;
         last_position := last_position + 1 ;
         
         
           sSql := ''insert into orderposition ( id, orderid , articleid , designation, amount  ,  position)  values (  (select nextval(''''orderposition_id'''') ) , '' ;
            sSql := sSql ||  iNewOrderID || '', '' || grave_headline ||  '', '''''' || grave_headline_designation || '''''', '' || 1   || '', '' || last_position  || '' ) '' ;
          execute (sSql) ;  
        
        return iNewOrderID;
        
    END ;
    

    
     ' LANGUAGE 'plpgsql'; 

     
      
   
CREATE OR REPLACE FUNCTION fct_addPositionToInvoice(sService text , iNewOrderID int ) returns boolean AS '
 DECLARE
  
    iClient int ;
    sSql text   ;
    sSql2 text ;
    sSql3 text ;
    sSql4 text ;
    r1 record ;
    r2 record ;
    ok boolean ;
    igrave_id int ;
    last_position int ;
    article_headline int ;
    article_headline_designation text ;
     
    BEGIN
        ok := true ;
        
        sSql := ''select  from_modul_id from orderbook where id = '' || iNewOrderID  ;
        raise notice '' fetch grave id sSql = % '', sSql ;
        
        execute(sSql) into igrave_id ;
          
        raise notice ''execute (sSql) ; grave id = % '', igrave_id ;
        
        sSql := '' select gm.* from '' ;
          
        if sService = ''Service'' then
           article_headline = fct_get_config_option(iClient,''clients.ini'', ''CLIENT_'' || iClient, ''order_service_headline_articles_id'') ;
           IF article_headline IS NOT NULL THEN 
               sSql4 := ''select designation from articles where id = '' || article_headline ;
               execute(sSql4) into article_headline_designation ;
            END IF ;
            
            sSql := sSql || ''grave_work_maintenance as gm '' ;
            sSql2 := '' update grave_work_maintenance set created_order = 1 where id = ''  ;
        end if ;
        
        
       
        sSql := sSql || '' where grave_id = '' || igrave_id ;
        sSql := sSql || '' ''  || fct_getWhere(2,'''') ;
        
        raise notice '' fetch positions  sSql = % '', sSql ;
        
        select into last_position max(position) from orderposition where orderid = iNewOrderID ;
        if last_position IS NULL then 
            last_position = 0 ;
        end if ;
         last_position := last_position + 1 ;
           sSql := ''insert into orderposition ( id, orderid , articleid , designation, amount  ,  position)  values (  (select nextval(''''orderposition_id'''') ) , '' ;
            sSql := sSql ||  iNewOrderID || '', '' || article_headline ||  '', '''''' || article_headline_designation || '''''', '' || 1   || '', '' || last_position  || '' ) '' ;
          execute (sSql) ;  
        FOR r1 in execute(sSql)  LOOP
            if r1.created_order is null then
                r1.created_order = 0 ;
            end if ;
            if r1.created_order = 0 then
                last_position := last_position + 1 ;
                sSql := ''insert into orderposition ( id, orderid , articleid , designation, amount  ,  position , price ) values (  (select nextval(''''orderposition_id'''') ) , '' ;
                sSql := sSql ||  iNewOrderID || '', '' || r1.article_id ||  '', '''''' || r1.service_designation || '''''', '' || r1.service_count   || '', '' || last_position ;
                sSql := sSql || '', '' || r1.service_price || '' ) '' ;
                raise notice '' insert position sSql = % '', sSql ;
                execute (sSql) ;
                sSql3 := sSql2 || r1.id ;
                raise notice '' update = % '', sSql3 ;
                execute(sSql3);
                
            end if ;
        END LOOP ;
            
        
        return ok;
        
    END ;
    

    
     ' LANGUAGE 'plpgsql'; 
