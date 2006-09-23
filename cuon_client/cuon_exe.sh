#!/bin/sh

EXEC=/usr/bin/python
if [ $1 ] ; then
Server=$1 ;
else
Server=http://192.168.17.2:7080 ;
fi


echo " Server = $Server"
#sudo make install_server
cd Client
rm CUON/cuonObjects
cp -R CUON/* ~/cuon/bin
cp -R locale ~/cuon
cd ~/cuon/bin

$EXEC  Cuon.py $Server client NO ~/cuon/locale
