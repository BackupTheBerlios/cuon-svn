#!/bin/sh

EXEC=/usr/bin/python

case $2 in

n) Server=http://server2:9673/Cuon 
;;
ssl) Server=http://server2:8443/Cuon
;;
inn) Server=http://innovatec.dyndns.org:9673/Cuon
;;
innssl) Server=http://innovatec.dyndns.org:8443/Cuon
;;
*) Server=http://server2:9673/Cuon
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


