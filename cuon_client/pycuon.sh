EXEC=/usr/bin/python

sudo make install_server

cd Py/

case $1 in 

server)
cp ../cuon_server.py . 
$EXEC cuon_server.py $2
;;

client)
$EXEC Cuon.py $2 
;;

esac



cd ../


