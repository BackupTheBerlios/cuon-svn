#!/bin/sh

EXEC=/usr/bin/python
MyServer=http://localhost:7080
#MyServer=http://server2:9673
case $2 in

n) Server=$MyServer/Cuon 
;;
ssl) Server=https://localhost:7580/Cuon
;;
qemu) Server=http://192.168.17.2:4080/Cuon
;;
qemussl) Server=https://192.168.17.2:4580/Cuon
;;

die) Server=http://dietzel-normteile.dyndns.org:7080/Cuon
;;
diessl) Server=https://dietzel-normteile.dyndns.org:8443/Cuon
;;

cuweb) Server=http://84.244.7.139:7080
;;
cuwebssl) Server=https://84.244.7.139:8443
;;

cyweb) Server=http://84.244.4.80:7080/Cuon
;;

cywebssl) Server=https://84.244.4.80:8443/Cuon
;;

*) Server=$MyServer/Cuon
;;

esac

case $1 in  
ai)
make all
sudo make ai
cp ../cuon_server/src/ai_main.py cuon/AI
cd cuon/AI
$EXEC tki1.py
;;
mini)
make all
sudo make ai
cd cuon/AI
$EXEC miniClient.py
;;
gtkmini)
make all
sudo make ai

rm -R gtkMiniClient
make gtkMiniClient
cd gtkMiniClient
$EXEC gtkMiniClient.py
;;

server)
sudo make install_server
cd CUON/

#make iClient
sudo cp ../cuon_server.py . 
$EXEC cuon_server.py $Server server $3
;;

client)
echo " Server = $Server"
#sudo make install_server
cd Client
cp -R CUON/* ~/cuon/bin
cp -R locale ~/cuon
cd ~/cuon/bin

$EXEC  Cuon.py $Server client NO ~/cuon/locale
;;

profile)
sudo make install_server
cd CUON/
$EXEC -m profile -o cuonprofile Cuon.py $Server client $3
;;

esac



cd ../


