<sql>
  <postgre_sql>
    <nameOfSqlDatabase>Postgre SQL</nameOfSqlDatabase>
    
    <function>
     
      <nameOfFunction>fct_changeProposal2Order(iProposalID int ) returns bool</nameOfFunction>
      <language>plpgsql</language>
    <textOfFunction>
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
     </textOfFunction>
    <description>change a proposal to an order</description>

    </function>
    
        <function>
     
      <nameOfFunction>fct_getOrderTotalSum(  iOrderid int) returns float </nameOfFunction>
      <language>plpgsql</language>
       <textOfFunction>
    DECLARE
    fSum     float ;
    sClient char ;
    cur1 CURSOR FOR SELECT amount, price, discount FROM orderposition WHERE  orderid = iOrderid || '' '' || fct_getWhere(2,'' '');
    fAmount     float;
    fPrice  float;
    fDiscount   float ;
    count   integer ;
    BEGIN
        fSum := 0.0 ;
        open cur1 ;
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
    select into fDiscount discount from orderbook where id = iOrderid || '' '' || fct_getWhere(2,'' '');
    if fDiscount IS NULL then
            fDiscount := 0.0 ;
        end if ;
    fSum := fSum * ((100 - fDiscount)/100 )  ;
    
    return fSum ;
    END ;
    </textOfFunction>
    <description>get the total sum</description>

    </function>
  </postgre_sql>
  
</sql>
