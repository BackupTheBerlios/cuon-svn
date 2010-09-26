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

