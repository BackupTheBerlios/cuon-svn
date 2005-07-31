#!/bin/sh

EXEC=/usr/bin/python
MyServer=http://localhost:8080
case $2 in

n) Server=$MyServer/Cuon 
;;
ssl) Server=https://server2:9443/Cuon
;;
inn) Server=http://innovatec.dyndns.org:9673/Cuon
;;
innssl) Server=https://innovatec.dyndns.org:8443/Cuon
;;

die) Server=http://dietzel-normteile.dyndns.org:9673/Cuon
;;
diessl) Server=https://dietzel-normteile.dyndns.org:8443/Cuon
;;

*) Server=$MyServer/Cuon
;;
esac

sudo make install_server

cd CUON/

case $1 in 

server)
cp ../cuon_server.py . 
$EXEC cuon_server.py $Server server $3
;;

client)
$EXEC Cuon.py $Server client $3
;;

esac



cd ../


