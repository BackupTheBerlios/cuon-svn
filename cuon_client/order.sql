 CREATE OR REPLACE FUNCTION fct_changeProposal2Order(iProposalID int ) returns bool AS '
 DECLARE
    
    iClient int ;
 

    BEGIN
        
        update orderbook set process_status = 500 where id =  iProposalID ;
        
        if FOUND then
            return 1 ;
        else 
            return 0 ;
        end if ;
        
    END ;
    
     ' LANGUAGE 'plpgsql'; 
    
CREATE OR REPLACE FUNCTION fct_getOrderTotalSum(  iOrderid int) returns float AS '
    DECLARE
    fSum     float ;
    sClient char ;
    cur1 refcursor ;
    sCursor text ;
    sSql text ; 
    fAmount     float;
    fPrice  float;
    fDiscount   float ;
    count   integer ;
    BEGIN
       -- RAISE NOTICE ''begin total sum for id %'', iOrderid ;
        sCursor := ''SELECT amount, price, discount FROM orderposition WHERE  orderid = ''|| iOrderid || '' '' || fct_getWhere(2,'' '')  ;
        fSum := 0.0 ;
        -- RAISE NOTICE ''sCursor = %'', sCursor ;
        OPEN cur1 FOR EXECUTE sCursor ;
        FETCH cur1 INTO fAmount, fPrice, fDiscount ;

        count := 0;

    WHILE FOUND LOOP
        -- RAISE NOTICE ''total sum for position , amount %, price % , discount %'', fAmount,fPrice,fDiscount ;
        if fDiscount IS NULL then
            fDiscount := 0.0 ;
        end if ;
        
        fSum := fSum + ( fAmount * (fPrice * (100 - fDiscount)/100 ) ) ;
        FETCH cur1 INTO fAmount, fPrice, fDiscount ;
    END LOOP ;
    close cur1 ;
    
    -- now get the whole discount 
    sSql := ''select discount from orderbook where id = '' || iOrderid || '' '' || fct_getWhere(2,'' '');
    execute sSql into fDiscount ;
    if fDiscount IS NULL then
            fDiscount := 0.0 ;
        end if ;
    fSum := fSum * ((100 - fDiscount)/100 )  ;
    
    return fSum ;
    END ;
    ' LANGUAGE 'plpgsql'; 

  
  
CREATE OR REPLACE FUNCTION fct_getOpenInvoice(  iOrderNumber int) returns float AS '
    DECLARE
    fSum float ;
    iOrder integer ;
    sSql text := '''';
 BEGIN
     sSql := ''select  sum(list_of_invoices.total_amount ) -  fct_getOrderTotalSum('' || iOrderNumber || '') as residue from list_of_invoices where list_of_invoices.order_number = '' || iOrderNumber || '' '' ||  fct_getWhere(2,'' '') ;
    -- RAISE NOTICE '' get residue for Invoice sql = %'', sSql ;
    
    execute sSql into  fSum ;
   
    return fSum ;
    END ;
    ' LANGUAGE 'plpgsql'; 
    
    
 
CREATE OR REPLACE FUNCTION fct_getInpayment(  iInvoice int) returns float AS '
    DECLARE
    fSum float ;
    sum_inpayment float ;
    sum_discount float ;
    iOrder integer ;
    sSql text := '''';
    r record ;
    sNumber varchar(20) := ''99999999999'' ;
    BEGIN
        sSql = ''select sum(in_payment.inpayment)   as sum_inpayment from in_payment where   to_number(in_payment.invoice_number,'' || quote_literal(sNumber)  || '') = ''  || iInvoice || '' '' ||  fct_getWhere(2,'' '') ;  
        -- RAISE NOTICE '' get residue for Invoice sql = %'', sSql ;
        execute sSql into  sum_inpayment ;
        

        if sum_inpayment is null then
            sum_inpayment := 0.00 ;
        end if ;
         sSql = ''select sum(in_payment.cash_discount)   as sum_discount from in_payment where   to_number(in_payment.invoice_number,'' || quote_literal(sNumber)  || '') = ''  || iInvoice || '' '' ||  fct_getWhere(2,'' '') ;  
        execute sSql into  sum_discount ;
        
        if sum_discount is null then
            sum_discount := 0.00 ;
        end if ;
        fSum := sum_inpayment + sum_discount ;
        
        return fSum ;
  
    END ;
    ' LANGUAGE 'plpgsql'; 
   
CREATE OR REPLACE FUNCTION fct_getResidueForInvoice(  iInvoice int) returns float AS '
    DECLARE
    fSum float ;
    iOrder integer ;
    sSql text := '''';
 BEGIN
     sSql := ''select  list_of_invoices.total_amount  -  fct_getInpayment(list_of_invoices.invoice_number ) as residue from list_of_invoices where list_of_invoices.id = '' || iInvoice || '' '' ||  fct_getWhere(2,'' '') ;
    -- RAISE NOTICE '' get residue for Invoice sql = %'', sSql ;
    
    execute sSql into  fSum ;
   
    return fSum ;
    END ;
    ' LANGUAGE 'plpgsql'; 
    
CREATE OR REPLACE FUNCTION fct_getResidue( ) returns setof  record AS '
 DECLARE
     iClient int ;
    searchsql text := '''';
    r  record;
    r2 record ;
    sSql text := '''' ;
    BEGIN
       
        searchsql := ''select  list_of_invoices.order_number, fct_getResidueForInvoice(list_of_invoices.id) as residue, id  from list_of_invoices   ''  || fct_getWhere(1,'' '') || '' order by list_of_invoices.id'' ;
        
        -- RAISE NOTICE '' get residue sql = %'', searchsql ;

        FOR r in execute(searchsql)  LOOP
        
        IF r.residue > 0.01  THEN
        
            
          
                sSql := ''select  list_of_invoices.total_amount as total_amount, address.lastname as lastname, address.city as city, orderbook.id as order_id, list_of_invoices.maturity as maturity, fct_getResidueForInvoice(list_of_invoices.id) as residue ,  list_of_invoices.order_number as order_number,  list_of_invoices.invoice_number as invoice_number, list_of_invoices.date_of_invoice as date_of_invoice, current_date  from list_of_invoices , orderbook, address  where list_of_invoices.id = '' ||  r.id  || '' and list_of_invoices.order_number = orderbook.id and address.id = orderbook.addressnumber order by list_of_invoices.maturity'';
            FOR r2 in execute(sSql)  LOOP
                return NEXT r2 ;
            END LOOP ;
        
        END IF ;

        
        END LOOP ;
        
    END ;
    

    
     ' LANGUAGE 'plpgsql'; 

     
        
CREATE OR REPLACE FUNCTION fct_getReminder( iDays integer) returns setof  record AS '
 DECLARE
     iClient int ;
    sSql text := '''';
    r  record;
    r2 record ;
    
    BEGIN
       sSql := '' select total_amount,lastname, city, order_id, maturity,  residue , order_number, invoice_number,date_of_invoice, this_date from fct_getResidue() as (total_amount float, lastname varchar(150),  city varchar(150),  order_id integer,  maturity date,residue float,  order_number integer, invoice_number integer, date_of_invoice date, this_date date )  ''  ;
       
        FOR r in execute(sSql)  LOOP
        
        IF r.this_date - r.maturity > iDays   THEN
            return next r;
        END IF ;
        
        END LOOP ;
        
    END ;
    

    
     ' LANGUAGE 'plpgsql'; 
       
CREATE OR REPLACE FUNCTION fct_duplicateOrder( iOrderID integer) returns int AS '
 DECLARE
     
    newOrderID int ;
     new_table   varchar(400) ;
     
      sSql text ;
    sSql2 text ;
        sExe text ;
        sExe2 text ;
        sTable  text;
        rData  record ;
        sCursor text ;
        iPosID int ;
        cur1 refcursor ;
    BEGIN
    select nextval(''orderbook_id'') into newOrderID ;
    
       select into rData user_id , status ,  insert_time , update_time, update_user_id  ,  client ,  sep_info_1 ,  sep_info_2 ,  sep_info_3 ,  number ,  designation ,         orderedat , deliveredat , packing_cost , postage_cost , misc_cost ,build_retry , type_retry  , supply_retry, gets_retry , invoice_retry , custom_retry_days , modul_number  ,                modul_order_number, discount  , ready_for_invoice , process_status   , proposal_number , customers_ordernumber , customers_partner_id , project_id , versions_number ,  versions_uuid   , staff_id  from orderbook where id =  iOrderID    ;
    
        
        RAISE NOTICE ''status by rdata = %'', rData.status;
        
        
    insert into orderbook (id, user_id , status ,  insert_time , update_time, update_user_id  ,  client ,  sep_info_1 ,  sep_info_2 ,  sep_info_3 ,  number ,  designation ,         orderedat , deliveredat , packing_cost , postage_cost , misc_cost ,build_retry , type_retry  , supply_retry, gets_retry , invoice_retry , custom_retry_days , modul_number  ,                modul_order_number, discount  , ready_for_invoice , process_status   , proposal_number , customers_ordernumber , customers_partner_id , project_id , versions_number  ,versions_uuid   , staff_id  ) values ( newOrderID, rData.user_id , rData.status ,  rData.insert_time , rData.update_time, rData.update_user_id  ,  rData.client ,  rData.sep_info_1 ,  rData.sep_info_2 ,  rData.sep_info_3 ,  rData.number ,  rData.designation ,         rData.orderedat , rData.deliveredat , rData.packing_cost , rData.postage_cost , rData.misc_cost ,rData.build_retry , rData.type_retry  , rData.supply_retry, rData.gets_retry , rData.invoice_retry , rData.custom_retry_days , rData.modul_number  , rData.modul_order_number, rData.discount  , rData.ready_for_invoice , rData.process_status   , rData.proposal_number , rData.customers_ordernumber , rData.customers_partner_id , rData.project_id , 0,   fct_new_uuid()  , rData.staff_id) ;
            
       
     
        sCursor := ''SELECT id from orderposition WHERE  orderid = ''|| iOrderID || '' '' || fct_getWhere(2,'' '')  ;
       
        OPEN cur1 FOR EXECUTE sCursor ;
        FETCH cur1 INTO iPosID ;

     

        WHILE FOUND LOOP
        RAISE NOTICE ''iPosID % '', iPosID ;
        select into rData user_id , status ,  insert_time , update_time, update_user_id  ,  client ,  sep_info_1 ,  sep_info_2 ,  sep_info_3 ,orderid,   articleid, designation, amount,  position,   price , tax_vat,  discount,  versions_number  ,versions_uuid  from orderposition where id = iPosID ;
        
        insert into orderposition (id, user_id , status ,  insert_time , update_time, update_user_id  ,  client ,  sep_info_1 ,  sep_info_2 ,  sep_info_3 ,orderid,   articleid, designation, amount,  position,   price , tax_vat,  discount,  versions_number  ,versions_uuid ) values ( nextval(''orderposition_id''), rData.user_id , rData.status ,  rData.insert_time , rData.update_time, rData.update_user_id  ,  rData.client ,  rData.sep_info_1 ,  rData.sep_info_2 ,  rData.sep_info_3 , newOrderID,   rData.articleid, rData.designation, rData.amount,  rData.position,   rData.price , rData.tax_vat,  rData.discount,    0,   fct_new_uuid()  )  ; 
           
        FETCH cur1 INTO iPosID ;
    END LOOP ;
       
    close cur1 ;
    
      
       
       
     --  RAISE NOTICE ''sql = %'', sSql ; 
      --  execute(sSql) ;
    return newOrderID ;    
    END ;
    

    
     ' LANGUAGE 'plpgsql'; 

     
   
        
CREATE OR REPLACE FUNCTION fct_getUnreckonedOrder() returns setof  record AS '
 DECLARE
     iClient int ;
    sSql text := '''';
    r  record;
    r2 record ;
    
    BEGIN
       sSql := '' select id from orderbook '' || '' '' ||  fct_getWhere(2,'' '') ;
       
        FOR r in execute(sSql)  LOOP
        
        IF r.this_date - r.maturity > iDays   THEN
            return next r;
        END IF ;
        
        END LOOP ;
        
    END ;
    

    
     ' LANGUAGE 'plpgsql'; 
     
