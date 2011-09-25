 CREATE OR REPLACE FUNCTION fct_changeProposal2Order(iProposalID int ) returns bool AS '
 DECLARE
    
    iClient int ;
    iNewOrderID int ; 
    iNewPositionID int ;
    sSql text ;
    sSql2 text ;
    
    r record ;
    BEGIN
        iNewOrderID := 0 ;
        
        sSql := ''select * from fct_duplicate_table_entry('' || quote_literal(''proposal'') || '','' || quote_literal(''orderbook'') || '','' || iProposalID || '', '' || quote_literal(''orderbook_id'') || '')  as newid '' ;
        raise notice '' sSql = %'',sSql ;
        execute(sSql) into iNewOrderID;
        raise notice ''new order id = %'',iNewOrderID ;
        
        IF iNewOrderID > 0 THEN 
            -- copy the proposalpositions 
            
            sSql := '' select id from proposalposition where orderid = '' || iProposalID  || '' '' || fct_getWhere(2,'' '')  ;
            
            FOR r in execute(sSql)  LOOP
                sSql2 := ''select * from fct_duplicate_table_entry('' || quote_literal(''proposalposition'') || '','' || quote_literal(''orderposition'') || '','' || r.id || '', '' || quote_literal(''orderposition_id'') || '')  as newid '' ; 
               
                raise notice '' sSql2 = %'',sSql2 ;
                execute(sSql2) into iNewPositionID;
                update orderposition set orderid = iNewOrderID where id =  iNewPositionID ;
                
            END LOOP ;
            
            
            
            
            update orderbook set process_status = 500 where id =  iNewOrderID ;
        END IF ;
            
       return true ;
        
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
    fTaxVat float ;
    iArticleID integer ;
    bNet  bool ;
    BEGIN
       -- RAISE NOTICE ''begin total sum for id %'', iOrderid ;
        sCursor := ''SELECT amount, price, discount, articleid, tax_vat FROM orderposition WHERE  orderid = ''|| iOrderid || '' '' || fct_getWhere(2,'' '')  ;
        fSum := 0.0 ;
        -- RAISE NOTICE ''sCursor = %'', sCursor ;
        OPEN cur1 FOR EXECUTE sCursor ;
        FETCH cur1 INTO fAmount, fPrice, fDiscount,iArticleID, fTaxVat ;

        count := 0;

    WHILE FOUND LOOP
        RAISE NOTICE ''total sum for position , amount %, price % , discount %'', fAmount,fPrice,fDiscount ;
        if fDiscount IS NULL then
            fDiscount := 0.0 ;
        end if ;
        if fTaxVat IS NULL then 
            fTaxVat:= 0.00;
        END IF;
        if fPrice IS NULL then
            fPrice := 0.0 ;
        end if ;
        fTaxVat := fct_get_taxvat_for_article(iArticleID);
        
        -- now search for brutto/netto
        bNet := fct_get_net_for_article(iArticleID);
        raise notice '' order bNet value is %'',bNet ;
        if fTaxVat > 0 THEN
            if bNet = true then 
            -- raise notice '' order calc as bnet is true'';
                fSum := fSum + ( fAmount * ( fPrice + (fPrice *fTaxVat/100) ) * (100 - fDiscount)/100 ) ;
            else 
                fSum := fSum + ( fAmount * (fPrice * (100 - fDiscount)/100 ) ) ;
            end if ;
            
        ELSE    
            fSum := fSum + ( fAmount * (fPrice * (100 - fDiscount)/100 ) ) ;
            
        END IF ;
        FETCH cur1 INTO fAmount, fPrice, fDiscount ,iArticleID, fTaxVat;
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
     
     
DROP FUNCTION fct_duplicateOrder(integer);

CREATE OR REPLACE FUNCTION fct_duplicateOrder( iOrderID integer, OrderType integer) returns int AS '
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
        partPrefix text ;
    BEGIN
    partPrefix = '''' ;
    
    select nextval(''orderbook_id'') into newOrderID ;
    
       select into rData user_id , status ,  insert_time , update_time, update_user_id  ,  client ,  sep_info_1 ,  sep_info_2 ,  sep_info_3 ,  number ,  designation ,         orderedat , deliveredat , packing_cost , postage_cost , misc_cost ,build_retry , type_retry  , supply_retry, gets_retry , invoice_retry , custom_retry_days , modul_number  ,                modul_order_number, discount  , ready_for_invoice , process_status   , proposal_number , customers_ordernumber , customers_partner_id , project_id , versions_number ,  versions_uuid   , staff_id , addressnumber from orderbook where id =  iOrderID    ;
    
        
        RAISE NOTICE ''status by rdata = %'', rData.status;
        
        
    insert into orderbook (id, user_id , status ,  insert_time , update_time, update_user_id  ,  client ,  sep_info_1 ,  sep_info_2 ,  sep_info_3 ,  number ,  designation ,         orderedat , deliveredat , packing_cost , postage_cost , misc_cost ,build_retry , type_retry  , supply_retry, gets_retry , invoice_retry , custom_retry_days , modul_number  ,                modul_order_number, discount  , ready_for_invoice , process_status   , proposal_number , customers_ordernumber , customers_partner_id , project_id , versions_number  ,versions_uuid   , staff_id , addressnumber) values ( newOrderID, rData.user_id , rData.status ,  rData.insert_time , rData.update_time, rData.update_user_id  ,  rData.client ,  rData.sep_info_1 ,  rData.sep_info_2 ,  rData.sep_info_3 ,  ''NEW-'' || rData.number || partPrefix ,  rData.designation ,         rData.orderedat , rData.deliveredat , rData.packing_cost , rData.postage_cost , rData.misc_cost ,rData.build_retry , rData.type_retry  , rData.supply_retry, rData.gets_retry , rData.invoice_retry , rData.custom_retry_days , rData.modul_number  , rData.modul_order_number, rData.discount  , rData.ready_for_invoice , rData.process_status   , rData.proposal_number , rData.customers_ordernumber , rData.customers_partner_id , rData.project_id , 0,   fct_new_uuid()  , rData.staff_id, rData.addressnumber) ;
            
       
     
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

     
DROP function fct_getUnreckonedOrder() ;
DROP function fct_getUnreckonedOrder(integer) ;
CREATE OR REPLACE FUNCTION fct_getUnreckonedOrder(OrderID integer) returns bool AS '
        DECLARE
        iClient int ;
    sSql text := '''';
    t1  text := ''  -1 '' ;
    r record ;
    r2 record ;
    bInsert bool ;
    
    BEGIN
       
            bInsert = True ;
            sSql := ''select id from list_of_invoices where order_number =  '' || OrderID ||  '' '' ||  fct_getWhere(2,'' '') ;
            raise notice ''sql  = %'',sSql ;
            FOR r2 in execute(sSql)  LOOP
                raise notice ''id = %'',r2.id ;
                if r2.id > 0 then
                    bInsert = False;
                end if ;
            END LOOP ;
            
        return bInsert ;
    END ;
    

    
     ' LANGUAGE 'plpgsql'; 

     
drop function fct_getGet_number(int) ;
CREATE OR REPLACE FUNCTION fct_getGet_number(OrderID integer) returns  int AS '
 DECLARE
    iData int ;
    sSql text ;
    r2 record ;
    
    BEGIN
       iData := 0 ;
       sSql := ''select number as get_number from orderget where orderid = '' || OrderID || '' '' ||  fct_getWhere(2,'' '') ;
       
       FOR r2 in execute(sSql)  LOOP
            
            if r2.get_number is not null then 
                iData := r2.get_number ;
            else
                iData := 0 ;
            END IF ;
            
             
        END LOOP ;
     
            
     return iData ; 
       
    END ;
    

    
     ' LANGUAGE 'plpgsql'; 
     
drop function fct_getSupply_number(int) ;
CREATE OR REPLACE FUNCTION fct_getSupply_number(OrderID integer) returns  int AS '
 DECLARE
    iData int ;
    sSql text ;
    r2 record ;
    
    BEGIN
       iData := 0 ;
       
       
       sSql := ''select delivery_number as supply_number from list_of_deliveries where order_number = '' || OrderID || '' '' ||  fct_getWhere(2,'' '') ;
       raise notice '' SQL at fct_getSupply_number = % '', sSql ;
       FOR r2 in execute(sSql)  LOOP
           
            if r2.supply_number is not null then 
                iData := r2.supply_number ;
            else
                iData := 0 ;
            END IF ;
            raise notice ''iData = %'',iData ;
             
        END LOOP ;
     
            
     return iData ; 
       
    END ;
    

    
     ' LANGUAGE 'plpgsql';      

     
CREATE OR REPLACE FUNCTION  fct_getArticlePartsListForOrder(OrderID integer) returns setof record AS '
 DECLARE
 
 
    sSql text ;
    r2 record ;
    rPositions record ;
    rArticlesPart record ;
    
    
    BEGIN
       
       sSql := ''select articleid  as article_id from orderposition where orderid = '' || OrderID || '' '' ||  fct_getWhere(2,'' '') ;
       
       FOR r2 in execute(sSql)  LOOP
           
           
      
            
            return next r2 ;
            
        END LOOP ;
     
            
      
       
    END ;
    

    
     ' LANGUAGE 'plpgsql';      

     
     
     CREATE OR REPLACE FUNCTION  fct_getTopIDForOrder(OrderbookID integer) returns  integer AS '
    DECLARE
 
    t1 integer ;
    sSql text ;
    r2 record ;
    
    topID integer ;
    
    BEGIN
    
        topID := 0;
    
        select into r2  order_top from orderinvoice where orderid = OrderbookID ;
        
        IF r2.order_top is not NULL then 
            
            topID :=  r2.order_top ;
            
        END IF ;
        
        
    
        IF topID = 0 THEN 
        
            execute  ''select addresses_misc.top_id as adr_top_id from addresses_misc,orderbook where addresses_misc.address_id = orderbook.addressnumber and orderbook.id = '' || OrderbookID || '' '' ||  fct_getWhere(2,''addresses_misc.'') INTO  t1;
       
       
            
            raise notice ''top id adr = %'', t1 ;
            
            if t1 is  not null then 
            
                if t1 > 0 then 
                    topID :=  t1;
                end if;
            end if ;
  
            
        
            
            
            
        end if ;
        
        return topID ;
        
            
      
       
    END ;
    
     ' LANGUAGE 'plpgsql';      
     

     
CREATE OR REPLACE FUNCTION  fct_getStatTaxVat() returns  setof record AS '
    DECLARE
    r1 record ;
    r2 record ;
    r3 record ;
    
    iMonth int ;
    iYear int ;
    sSql text ;
    sSql2 text ;
    invoice_netto float;
    invoice_taxvat float ;
    
    br1 float ;
    br0 float ;
    BEGIN
    
        br0 = 0.00 ;
        br1 = 0.00 ;
  
        FOR i IN 0 .. 1 LOOP
            
            iMonth := date_part(''month'',current_date) - i ;
            
            iYear := date_part(''year'',current_date) ;
            if iMonth < 1 then
                iMonth = iMonth + 12 ;
                iYear = iYear -1 ;
            end if ;
            
            
            FOR  r1 in select  id, vat_value, vat_name, vat_designation,0.00 as tax_vatSum, 0.00 as sum_price_netto, i as z1 from tax_vat  LOOP
    
                sSql := ''select li.invoice_number as invoice_number,  li.date_of_invoice as li_date, '' || i || '' as z1, li.order_number  as li_orderid from list_of_invoices  as li  where  date_part(''''month'''', li.date_of_invoice) = '' ||  iMonth  || '' and date_part(''''year'''', li.date_of_invoice) = '' || iYear ||  fct_getWhere(2,'' '') || '' order by li.invoice_number '' ; 
               
                FOR r2 in execute(sSql)  LOOP
                 invoice_taxvat := 0.00 ;
                invoice_netto := 0.00 ;
               
                -- raise notice '' Invoice Number % Invoice Date % Order ID % '',r2.invoice_number, r2.li_date, r2.li_orderid ;

                    br0 :=   r1.tax_vatSum   +  r1.sum_price_netto ;
                     
                     
                    sSql2 := ''select ( select tax_vat_for_all_positions from orderinvoice where orderinvoice.orderid  = '' || r2.li_orderid  || '' ) as   tax_vat_for_all_positions ,   
                    orderposition.amount as amount,  orderposition.position as position, orderposition.price as price, 
                    orderposition.discount as discount, orderposition.tax_vat as position_tax_vat, 
                    (select  material_group.tax_vat from material_group,articles where  articles.material_group = material_group.id and articles.id = orderposition.articleid) as m_group_taxvat, 
                    case 
                        ( select material_group.price_type_net from material_group, articles where  articles.material_group = material_group.id and  articles.id = orderposition.articleid)
                        when true then price when false then price / (100 + (select  tax_vat.vat_value from tax_vat,material_group,articles  
                        where  articles.material_group = material_group.id and material_group.tax_vat = tax_vat.id and articles.id = orderposition.articleid)) * 100  when NULL then 0.00
                    end  as end_price_netto,  
                    case 
                        ( select material_group.price_type_net from material_group, articles where  articles.material_group = material_group.id and  
                        articles.id = orderposition.articleid)  when true then price /100 * (100 + (select  tax_vat.vat_value from tax_vat,material_group,articles  
                        where  articles.material_group = material_group.id and material_group.tax_vat = tax_vat.id and articles.id = orderposition.articleid)) 
                        when false then price when NULL then 0.00 
                    end as end_price_gross  
                    from  orderposition, articles, orderbook  
                    where orderbook.id = '' || r2.li_orderid  || '' and orderposition.orderid = orderbook.id and articles.id = orderposition.articleid ''  ||  fct_getWhere(2,''orderposition.'')  ;
                   
                    FOR r3 in execute(sSql2) LOOP
                        IF r3.discount IS NULL THEN 
                            r3.discount := 0.00 ;
                        END IF ;
                        
                        IF r3.position_tax_vat IS NOT NULL and  r3.position_tax_vat > 0.00  and r1.vat_value = r3.position_tax_vat THEN
                             r1.tax_vatSum :=   r1.tax_vatSum +( (r3.end_price_netto -r3.discount)  * r3.amount * r3.position_tax_vat / 100 ) ;
                             r1.sum_price_netto:=   r1.sum_price_netto +( r3.end_price_netto  * r3.amount );
                             raise notice '' position taxvat = % '', r3.position_tax_vat ;
                        ELSEIF r3.tax_vat_for_all_positions IS NOT NULL and r3.tax_vat_for_all_positions > 0 and  r3.tax_vat_for_all_positions =  r1.id  THEN
                             r1.tax_vatSum :=   r1.tax_vatSum +  ( (r3.end_price_netto -r3.discount) * r3.amount * r1.vat_value /100 );
                             r1.sum_price_netto:=   r1.sum_price_netto + ( r3.end_price_netto  * r3.amount );
                             raise notice  ''tax vatforalpositions ''  ;
                      
                        ELSEIF  r3.m_group_taxvat IS NOT NULL and r3.m_group_taxvat > 0 and   r3.m_group_taxvat= r1.id and not (r3.tax_vat_for_all_positions IS NOT NULL and r3.tax_vat_for_all_positions > 0 ) THEN
                             r1.tax_vatSum :=   r1.tax_vatSum +( (r3.end_price_netto-r3.discount)  * r3.amount * r1.vat_value / 100 );
                             r1.sum_price_netto:=   r1.sum_price_netto + (r3.end_price_netto  * r3.amount );
                            raise notice '' materialgroup taxvat '' ;
                              
                       
                        END IF ;
                       
                         -- raise notice '' Orderid % Posion ID % TaxVat %  Menge % Netto % '', r2.li_orderid,r3.position,r1.vat_value,  r3.amount,r3.end_price_netto *  r3.amount ;
                    
                        
                        
                        
                    END LOOP ;
                      br1 :=  r1.tax_vatSum   +  r1.sum_price_netto ;
                      raise notice ''  Invoice Number %           Br1 = % '',r2.invoice_number,  br1 - br0  ;
                     
                END LOOP ;
            RETURN NEXT r1;
        
            END LOOP ;
             -- raise notice '' Discount =   % '',  invoice_netto ;

        END LOOP;
    
     
       
    END ;
    
     ' LANGUAGE 'plpgsql';      

     
     
CREATE OR REPLACE FUNCTION  fct_getInvoiceGross() returns  setof record AS '
    DECLARE
    r1 record ;
    BEGIN 
    
        for i in 4614 .. 4714 LOOP 
            select into r1 list_of_invoices.invoice_number,  list_of_invoices.order_number, sum(amount*price) from orderposition, list_of_invoices where list_of_invoices.invoice_number = i and orderposition.orderid = list_of_invoices.order_number group by list_of_invoices.invoice_number, list_of_invoices.order_number ;
             
            return next r1 ;
        END LOOP ;
        
     
     
          
    END ;
    
     ' LANGUAGE 'plpgsql';      
