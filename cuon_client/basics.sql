<sql>
  <postgre_sql>
    <nameOfSqlDatabase>Postgre SQL</nameOfSqlDatabase>
    
    
    
    <function>
     
      <nameOfFunction>    fct_setUserData( dicUser char  [] ) returns bool </nameOfFunction>
      <language>plpgsql</language>
    <textOfFunction>
    DECLARE
    sName char(50) ;    
    sClient char ;
    sNoWhereClient char ;
    iNextID     int ;

    BEGIN
    
        sName := dicUser[1];
        sClient := dicUser[2];
        sNoWhereClient := dicUser[3];
        
        execute ''delete from cuon_user where username = '' || quote_literal(sName )  ;
        select into iNextID nextval from  nextval(''cuon_user_id''); 

        execute ''insert into  cuon_user (id,username, current_client, no_where_client ) VALUES (
        '' || iNextID || '', '' || quote_literal(sName) || '','' || sClient  ||'','' || sNoWhereClient || '' )'' ;
        
        return 1 ;
    END ;
     </textOfFunction>
    <description>set the userdata for the current work</description>

    </function>
     <function>
     
      <nameOfFunction>    fct_getUserDataClient(  ) returns int </nameOfFunction>
      <language>plpgsql</language>
    <textOfFunction> DECLARE
    iClient    int ;
    sClient char ;
    BEGIN
    
        select into iClient current_client from cuon_user where username = CURRENT_USER ;
        raise notice ''Client id = %'', iClient ;
        return iClient ;
    END ;
     </textOfFunction>
    <description>get the client id </description>

    </function>
    
    <function>
    
      <nameOfFunction>    fct_getUserDataNoWhereClient(  ) returns int </nameOfFunction>
      <language>plpgsql</language>
    <textOfFunction> DECLARE
    iClient    int ;
    sClient char ;
    BEGIN
    
        select into iClient no_where_client from cuon_user where username = CURRENT_USER ;
        raise notice ''NoWhereClient id = %'', iClient ;
        return iClient ;
    END ;
     </textOfFunction>
    <description>get the nowhereclient id </description>

    </function>
    
    
    
  <function>
     
      <nameOfFunction>fct_getWhere(iSingle int,  sPrefix char ) returns text</nameOfFunction>
      <language>plpgsql</language>
    <textOfFunction>
     DECLARE
    sWhere  text ;
    iClient int ;
    iNoWhereClient int ;

    BEGIN
        iClient := fct_getUserDataClient();
        iNoWhereClient := fct_getUserDataNoWhereClient();
        
    sWhere := '' '' ;
    if iNoWhereClient = ''0''
    then
        if iSingle = 1
        then
             sWhere := ''WHERE '' ||  sPrefix  || ''client = '' || iClient || '' and '' || sPrefix  || ''status != ''''delete'''' '' ;
                    

        else 
            if iSingle = 2
            then
                sWhere := ''AND '' ||  sPrefix  || ''client = '' || iClient || '' and '' || sPrefix  || ''status != ''''delete'''' '' ;
            END IF ;
        END IF ;
        
    END IF ;

    RETURN sWhere ;
    END ;
      </textOfFunction>
    <description>retuns the sWhere value</description>

    </function>

  </postgre_sql>
  
</sql>
