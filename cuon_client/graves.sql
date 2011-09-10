
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
     
     
CREATE OR REPLACE FUNCTION fct_calc_all_prices() returns boolean AS '
 DECLARE
 ok boolean ;
 BEGIN
        ok := true ;
        ok := fct_calc_all_prices_for_db(''grave_work_maintenance'') ;
        ok := fct_calc_all_prices_for_db(''grave_work_spring'') ;
        ok := fct_calc_all_prices_for_db(''grave_work_summer'') ;
        ok := fct_calc_all_prices_for_db(''grave_work_autumn'') ;
        ok := fct_calc_all_prices_for_db(''grave_work_winter'') ;
        ok := fct_calc_all_prices_for_db(''grave_work_holiday'') ;
        ok := fct_calc_all_prices_for_db(''grave_work_year'') ;
         ok := fct_calc_all_prices_for_db(''grave_work_single'') ;
        return ok ;
      END ;
    
     ' LANGUAGE 'plpgsql';   
     
CREATE OR REPLACE FUNCTION fct_calc_all_prices_for_db(sDB text ) returns boolean AS '
 DECLARE
    sSql text   ;
    sSql2 text ;
    r0 record ;
    newPrice float ;
    ok boolean ;
    BEGIN
        sSql := ''select id, grave_id, article_id, automatic_price from '' || sDB || ''  '' || fct_getWhere(1,'''') || '' order by id '' ;
        
        FOR r0 in execute(sSql) LOOP 
            if r0.automatic_price is NULL then
                r0.automatic_price := 0 ;
            end if ;
            if r0.automatic_price = 1 then 
            
                newPrice = fct_get_price_for_pricegroup(''grave'',r0.grave_id , r0.article_id )  ;
                -- raise notice '' new price for article % , grave % = %'', r0.article_id, r0.grave_id, newPrice ;
                if newPrice > 0 then 
                
                    sSql2 := ''update '' || sDB || '' set service_price = '' || newPrice || '' where id = '' || r0.id  ;
                    execute(sSql2) ;
                end if ;
            end if ;
        END LOOP ;
        ok = true ;
        return ok ;
      END ;
    
     ' LANGUAGE 'plpgsql';   
     
     
     
CREATE OR REPLACE FUNCTION fct_createNewInvoice(sService text , iGraveID int ) returns setof int AS '
 DECLARE
    sSql text   ;
    iNewOrderID int ;
     r0 record ;
    counter int ; 
     iDiscount float ;   
    
     
    BEGIN
      
        counter := 1 ;
       
            
         if counter = 1 then 
            sSql := '' select grave.id , grave.addressid,inv.address_id as partner_id ,inv.part, sum(inv.part) as sum_part from grave left join grave_invoice_info inv on  grave.id =  inv.grave_id where grave.id = '' || iGraveID || '' group by grave.id, grave.addressid, inv.address_id, inv.part ''  ;
            FOR r0 in execute(sSql)  LOOP
                    if r0.sum_part IS NULL then
                        iDiscount := 0 ;
                    else 
                        iDiscount :=  r0.sum_part ;
                    END IF ;
                    
                    iNewOrderID := fct_createSingleNewInvoice(sService , iGraveID  , r0.addressid, iDiscount ) ;
                    counter := 2 ;
                    return next iNewOrderID ;
                    
            END LOOP ;
        END IF ;
        
            
            if counter = 2  then 
            sSql := '' select grave.id , grave.addressid,inv.address_id as partner_id ,inv.part, sum(inv.part) as sum_part from grave left join grave_invoice_info inv on  grave.id =  inv.grave_id where grave.id = '' || iGraveID || '' group by grave.id, grave.addressid, inv.address_id, inv.part ''  ;
            FOR r0 in execute(sSql)  LOOP
                if r0.partner_id IS NOT NULL THEN
                    if r0.part IS NULL then 
                        iDiscount := 0 ;
                    else 
                        iDiscount :=  100 - r0.part ;
                    END IF ;
                    
                    iNewOrderID := fct_createSingleNewInvoice(sService , iGraveID  , r0.partner_id, iDiscount ) ;
                    
                    return next iNewOrderID ;
            
                END IF ;
            END LOOP ;
            
        END IF ;
           
    
      END ;
    
     ' LANGUAGE 'plpgsql'; 
    
CREATE OR REPLACE FUNCTION fct_createSingleNewInvoice(sService text , iGraveID int , iAddressID int, iDiscount float) returns  int AS '
 DECLARE
    
    iClient int ;
    sSql text   ;
    iNewOrderID int ;
   
    r1 record ;
    r2 record ;
   last_position int ;
    grave_headline int ;
    grave_headline_designation text ;
    allInvoices int [] ;
    grave_part int ;
    
    BEGIN
        iNewOrderID := -1 ;
        iClient = fct_getUserDataClient(  ) ;
        raise notice '' Client Number = %'',iClient ;
        grave_headline = fct_get_config_option(iClient,''clients.ini'', ''CLIENT_'' || iClient, ''order_main_headline_articles_id'') ;
        
        
        select into iNewOrderID nextval(''orderbook_id'' ) ;
    
        raise notice '' new OrderNumber = %'', iNewOrderID ;
        
        sSql := '' select grave.*, graveyard.shortname as graveyard_shortname from grave, graveyard '' ;
        
        IF sService = ''Service'' THEN
            sSql = sSql || '', grave_work_maintenance as gm '' ;

        ELSEIF sService = ''Spring'' THEN
            sSql = sSql || '', grave_work_spring as gm '' ;
            
         ELSEIF sService = ''Summer'' THEN
            sSql = sSql || '', grave_work_summer as gm '' ;
            
         ELSEIF sService = ''Autumn'' THEN
            sSql = sSql || '', grave_work_autumn as gm '' ;
            
        ELSEIF sService = ''Winter'' THEN
            sSql = sSql || '', grave_work_winter as gm '' ;   
            
         ELSEIF sService = ''Holliday'' THEN
            sSql = sSql || '', grave_work_holiday as gm '' ;
            
         ELSEIF sService = ''Unique'' THEN
            sSql = sSql || '', grave_work_single as gm '' ;
            
         ELSEIF sService = ''Yearly'' THEN
            sSql = sSql || '', grave_work_year as gm '' ;    
            
        END IF ;
        
        sSql := sSql || '' where graveyard.id = grave.graveyardid and grave.id = gm.grave_id and grave.id = '' || iGraveID || '' ''  || fct_getWhere(2,''grave.'') ;
        execute(sSql) into r1 ;
        
        if r1.id is null then 
            
            return  iNewOrderID;
        else 
            raise notice ''r1 = % '', r1.id ;
    
            sSql := '' insert into orderbook (id,addressnumber,ready_for_invoice,pricegroup1,pricegroup2,pricegroup3,pricegroup4,pricegroup_none, orderedat, from_modul, from_modul_id,deliveredat, discount) values ('' ;
            sSql := sSql || iNewOrderID || '', '' || iAddressID || '', true, '' || r1.pricegroup1 || '', '' || r1.pricegroup2 || '', '' || r1.pricegroup3 || '', '' || r1.pricegroup4 || '', '' || r1.pricegroup_none  ;
            sSql := sSql || '', '' ||  quote_literal(current_date ) || '' , 40000, '' || r1.id || '', ''  ||  quote_literal(current_date)  || '', '' || iDiscount  || '' ) ''  ;
            
            
            raise notice '' new sSql insert = % '', sSql ;
            
            
            execute (sSql) ;    
            
            select into last_position max(position) from orderposition where orderid = iNewOrderID ;
            if last_position IS NULL then 
                last_position = 0 ;
            end if ;
            
            
            
            if iDiscount > 0 THEN 
                 grave_part = fct_get_config_option(iClient,''clients.ini'', ''CLIENT_'' || iClient , ''order_part_id'') ;
                  last_position := last_position + 1 ;
                   sSql := ''insert into orderposition ( id, orderid , articleid , designation, amount  ,  position, price)  values (  (select nextval(''''orderposition_id'''') ) , '' ;
            sSql := sSql ||  iNewOrderID || '', '' || grave_part ||  '', '' || quote_literal(iDiscount || ''%'') || '', '' || 1   || '', '' || last_position  || '', 0 ) '' ;
            raise notice ''SQL for Discount %'' , sSql ;
              execute (sSql) ; 
            END IF ;
                 
            grave_headline_designation := r1.lastname || '', Nr: '' || r1.detachment || '' / '' || r1.grave_number || '',  '' || r1.graveyard_shortname ;
             last_position := last_position + 1 ;
             
             
            sSql := ''insert into orderposition ( id, orderid , articleid , designation, amount  ,  position, price)  values (  (select nextval(''''orderposition_id'''') ) , '' ;
            sSql := sSql ||  iNewOrderID || '', '' || grave_headline ||  '', '' || quote_literal(grave_headline_designation) || '', '' || 1   || '', '' || last_position  || '', 0 ) '' ;
            raise notice ''SQL for headline %'' , sSql ;
              execute (sSql) ;  
             
           
            
            return  iNewOrderID;
        end if ;
        
    END ;
    

    
     ' LANGUAGE 'plpgsql'; 

     
      
  
 
CREATE OR REPLACE FUNCTION fct_addPositionToInvoice(sService text , iNewOrderID int, iLastOrder int ) returns boolean AS '
 DECLARE
  
    iClient int ;
    sSql text   ;
    sSql2 text ;
    sSql3 text ;
    sSql4 text ;
    sSql5 text ;
    sSql_date text ;
    r1 record ;
    r2 record ;
    ok boolean ;
    igrave_id int ;
    last_position int ;
    article_headline int ;
    article_headline_designation text ;
    fTaxVat float ;
    existID int ;
    article_designation text ;
    BEGIN
    sSql_date := '' '' ;
        ok := true ;
        existID := -1 ;
         iClient = fct_getUserDataClient(  ) ;
         raise notice '' Client Number = %'',iClient ;
         
         
        sSql := ''select  from_modul_id from orderbook where id = '' || iNewOrderID  ;
        raise notice '' fetch grave id sSql = % '', sSql ;
        
        execute(sSql) into igrave_id ;
          
        raise notice ''execute (sSql) ; grave id = % '', igrave_id ;
        
        sSql := '' select gm.* from '' ;
          
        if sService = ''Service'' then
           article_headline = fct_get_config_option(iClient,''clients.ini'', ''CLIENT_'' || iClient, ''order_service_headline_articles_id'') ;
            -- raise notice '' article headline = %'', article_headline ;
            
           IF article_headline IS NOT NULL THEN 
               sSql4 := ''select designation from articles where id = '' || article_headline ;
               
               execute(sSql4) into article_headline_designation ;
               
            END IF ;
            
            sSql := sSql || ''grave_work_maintenance as gm '' ;
            sSql2 := '' update grave_work_maintenance set created_order = 1 where id = ''  ;
            
        ELSEIF sService = ''Spring'' THEN
           article_headline = fct_get_config_option(iClient,''clients.ini'', ''CLIENT_'' || iClient, ''order_spring_headline_articles_id'') ;
            -- raise notice '' article headline = %'', article_headline ;
            
           IF article_headline IS NOT NULL THEN 
               sSql4 := ''select designation from articles where id = '' || article_headline ;
               
               execute(sSql4) into article_headline_designation ;
               
            END IF ;
            
            sSql := sSql || ''grave_work_spring as gm '' ;
            sSql2 := '' update grave_work_spring set created_order = 1 where id = ''  ;     
            
        
         
            
            ELSEIF sService = ''Summer'' THEN
            article_headline = fct_get_config_option(iClient,''clients.ini'', ''CLIENT_'' || iClient, ''order_summer_headline_articles_id'') ;
            -- raise notice '' article headline = %'', article_headline ;
            
            IF article_headline IS NOT NULL THEN 
               sSql4 := ''select designation from articles where id = '' || article_headline ;
               
               execute(sSql4) into article_headline_designation ;
               
            END IF ;
            
            sSql := sSql || ''grave_work_summer as gm '' ;
            sSql2 := '' update grave_work_summer set created_order = 1 where id = ''  ;     
                
          ELSEIF sService = ''Autumn'' THEN
           article_headline = fct_get_config_option(iClient,''clients.ini'', ''CLIENT_'' || iClient, ''order_autumn_headline_articles_id'') ;
            -- raise notice '' article headline = %'', article_headline ;
            
           IF article_headline IS NOT NULL THEN 
               sSql4 := ''select designation from articles where id = '' || article_headline ;
               
               execute(sSql4) into article_headline_designation ;
               
            END IF ;
            
            sSql := sSql || ''grave_work_autumn as gm '' ;
            sSql2 := '' update grave_work_autumn set created_order = 1 where id = ''  ;     
            
          ELSEIF sService = ''Winter'' THEN
           article_headline = fct_get_config_option(iClient,''clients.ini'', ''CLIENT_'' || iClient, ''order_winter_headline_articles_id'') ;
            -- raise notice '' article headline = %'', article_headline ;
            
           IF article_headline IS NOT NULL THEN 
               sSql4 := ''select designation from articles where id = '' || article_headline ;
               
               execute(sSql4) into article_headline_designation ;
               
            END IF ;
            
            sSql := sSql || ''grave_work_winter as gm '' ;
            sSql2 := '' update grave_work_winter set created_order = 1 where id = ''  ;     
         
           ELSEIF sService = ''Holliday'' THEN
           article_headline = fct_get_config_option(iClient,''clients.ini'', ''CLIENT_'' || iClient, ''order_holliday_headline_articles_id'') ;
            -- raise notice '' article headline = %'', article_headline ;
            
           IF article_headline IS NOT NULL THEN 
               sSql4 := ''select designation from articles where id = '' || article_headline ;
               
               execute(sSql4) into article_headline_designation ;
               
            END IF ;
            
            sSql := sSql || ''grave_work_holiday as gm '' ;
            sSql2 := '' update grave_work_holiday set created_order = 1 where id = ''  ;     
            
            
          ELSEIF sService = ''Unique'' THEN
           article_headline = fct_get_config_option(iClient,''clients.ini'', ''CLIENT_'' || iClient, ''order_Unique_headline_articles_id'') ;
            -- raise notice '' article headline = %'', article_headline ;
            
           IF article_headline IS NOT NULL THEN 
               sSql4 := ''select designation from articles where id = '' || article_headline ;
               
               execute(sSql4) into article_headline_designation ;
               
            END IF ;
            
            sSql := sSql || ''grave_work_single as gm '' ;
            sSql2 := '' update grave_work_single set created_order = 1 where id = ''  ;     
            sSql_date := '' and gm.unique_date < now() '' ;
            
          ELSEIF sService = ''Yearly'' THEN
           article_headline = fct_get_config_option(iClient,''clients.ini'', ''CLIENT_'' || iClient, ''order_Yearly_headline_articles_id'') ;
            -- raise notice '' article headline = %'', article_headline ;
            
           IF article_headline IS NOT NULL THEN 
               sSql4 := ''select designation from articles where id = '' || article_headline ;
               
               execute(sSql4) into article_headline_designation ;
              
            END IF ;
            
            sSql := sSql || ''grave_work_year as gm '' ;
            sSql2 := '' update grave_work_year set created_order = 1 where id = ''  ;     
            sSql_date := '' and to_date(gm.annual_day || ''''-'''' || gm.annual_month || ''''-'''' ||  EXTRACT(YEAR FROM  now()) ,''''DD-MM-YYYY'''' ) < now() '' ;    
        end if ;
        
        
       
        sSql := sSql || '' where grave_id = '' || igrave_id ;
        sSql := sSql || sSql_date ;
        sSql := sSql || '' ''  || fct_getWhere(2,'''') ;
        
        raise notice '' fetch positions  sSql = % '', sSql ;
        FOR r1 in execute(sSql)  LOOP
            existID := existID + r1.id ;
        END LOOP ;
          
        if existID > -1 then
            select into last_position max(position) from orderposition where orderid = iNewOrderID ;
            
            if last_position IS NULL then 
                last_position = 0 ;
            end if ;
             last_position := last_position + 1 ;
             
               sSql5 := ''insert into orderposition ( id, orderid , articleid , designation, amount  ,  position, price)  values (  (select nextval(''''orderposition_id'''') ) , '' ;
                sSql5 := sSql5 ||  iNewOrderID || '', '' || article_headline ||  '', '' ||  quote_literal('''') || '', '' || 1   || '', '' || last_position  || '' ,0 ) '' ;
              execute (sSql5) ;  
              
              
            raise notice '' look at r1 for position   sSql = % '', sSql ;
            FOR r1 in execute(sSql)  LOOP
                if r1.created_order is null then
                    r1.created_order = 0 ;
                end if ;
                if r1.created_order = 0 then
                    IF r1.service_price IS NULL THEN
                        r1.service_price = 0 ;
                    END IF ;
                    IF r1.service_price = 0  THEN
                        r1.service_price := fct_get_price_for_pricegroup(  ''orderposition'', iNewOrderID, r1.article_id)  ;
                    END IF;
                    if r1.service_designation is null then 
                        article_designation := '''' ;
                    else 
                        article_designation := r1.service_designation ;
                    end if ;
                    
                    -- select into article_designation designation from articles where id = r1.article_id ;
                    IF sService = ''Unique'' THEN
                        article_designation := article_designation || '' / '' || to_char(r1.unique_date,''DD.MM.YYYY'' ) ;
                    end if ;
                      IF sService = ''Yearly'' THEN
                        article_designation := article_designation || '' / '' || r1.annual_day ||''.'' ||  r1.annual_month ;
                    end if ;
                    if article_designation is null then 
                        article_designation := '''' ;
                    end if ;
                    
                    last_position := last_position + 1 ;
                    fTaxVat := fct_get_new_tax_vat_for_article_1(r1.article_id);
                    
                    sSql4 := ''insert into orderposition ( id, orderid , articleid , designation, amount  ,  position , price, tax_vat ) values (  (select nextval(''''orderposition_id'''') ) , '' ;
                    sSql4 := sSql4 ||  iNewOrderID || '', '' || r1.article_id ||  '', '''''' || article_designation || '''''', '' || r1.service_count   || '', '' || last_position ;
                    sSql4 := sSql4 || '', '' || r1.service_price || '', '' || fTaxVat || '' ) '' ;
                    raise notice '' insert position sSql4 = % '', sSql4 ;
                    execute (sSql4) ;
                    
                    if iLastOrder = 1 then 
                        sSql3 := sSql2 || r1.id ;
                        raise notice '' update = % '', sSql3 ;
                        execute(sSql3);
                    end if ;
                    
                    
                end if ;
            END LOOP ;
            
        end if ;
        return ok;
        
    END ;
    

    
     ' LANGUAGE 'plpgsql'; 
     
     
         
CREATE OR REPLACE FUNCTION fct_createAllNewInvoices(cash_id int)returns setof int AS '
 DECLARE
 
        igrave_id int ;
        sSql text ;
        r1 record ;
        
    BEGIN
    
        sSql := ''select id, type_of_paid from grave where (created_order is NULL or created_order = 0) and (contract_ends_at IS NULL or contract_ends_at > now()) '';
        FOR r1 in execute(sSql)  LOOP
            if r1.type_of_paid is null then 
                r1.type_of_paid = -1 ;
            end if ;
            
            if cash_id < 0 then 
                return next r1.id ;
            else 
                if r1.type_of_paid = cash_id then 
                    return next r1.id ;
                end if ;
            end if ;
            
        END LOOP ;
        
        
 
    END ;
     ' LANGUAGE 'plpgsql'; 
     
     
