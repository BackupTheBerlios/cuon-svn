cd c:\cuon\bin
echo start cuon
rem testing to see if a file exists
if  exist  newversion  goto  filefound
echo  file does not exist
goto end
:filefound
cd c:\cuon
c:\python24\python untar.py
cd c:\cuon\bin
del newversion

:end
cd c:\cuon\bin

c:\python24\python  Cuon.py http://localhost:7080 client NO ../locale c:\cuon
