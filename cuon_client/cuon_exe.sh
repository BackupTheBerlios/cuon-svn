#!/bin/sh

EXEC=/usr/bin/python
Server=http://192.168.17.2:7080
#MyServer=http://server2:9673


echo " Server = $Server"
#sudo make install_server
cd Client
cp -R CUON/* ~/cuon/bin
cp -R locale ~/cuon
cd ~/cuon/bin

$EXEC  Cuon.py $Server client NO ~/cuon/locale
