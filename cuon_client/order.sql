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
        sCursor := ''CURSOR FOR SELECT amount, price, discount FROM orderposition WHERE  orderid = '' || iOrderid || '' '' || fct_getWhere(2,'' '');
        fSum := 0.0 ;
        OPEN cur1 FOR EXECUTE sCursor;;
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
    
    /* now get the whole discount */
    sSql := ''select discount from orderbook where id = '' || iOrderid || '' '' || fct_getWhere(2,'' '');
    execute sSql into fDiscount ;
    if fDiscount IS NULL then
            fDiscount := 0.0 ;
        end if ;
    fSum := fSum * ((100 - fDiscount)/100 )  ;
    
    return fSum ;
    END ;
    ' LANGUAGE 'plpgsql'; 
