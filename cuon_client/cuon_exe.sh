#!/bin/sh

EXEC=/usr/bin/python
# PARAMETER=client NO /home/jhamel/cuon/locale /home/jhamel/cuon
CLIENT=client
DEBUG=NO
CUON_LOCALE=/home/jhamel/cuon/locale
CUON_PATH=/home/jhamel/cuon
Typ=LINUX-Standard
echo $1 $2 $3 $4
if [ $1 ] ; then
    case $1 in
        qemu) Server=http://192.168.17.2:4080
        ;;
        bgu) Server=http://slox.homelinux.net:7080
        ;;
        cuon) Server=http://84.244.7.139:7080
        ;;
        heino) Server=https://n3.blumen-schwarz.net:7580
        ;;
        vm) Server=http://192.168.17.7:7080
        ;;
        dietzel) Server=http://dietzel-normteile.dyndns.org:7080
        ;;
        maemo) Server=http://192.168.17.2:7080 
        Typ=Maemo
        ;;
        alternate1) Server=http://192.168.17.2:7080 
                Typ=alternate1
        ;;
        alternate4) Server=http://192.168.17.2:7080 
                Typ=alternate4
        ;;
		
		p0) Server=https://192.168.17.2:7580
                ;;

        p1) Server=http://192.168.17.2:7100
                ;;

        *)
            Server=$1 
        ;;

    esac
    

else
    Server=https://192.168.17.2:7580 ;
fi

echo " Server = $Server"
#sudo make install_server
cd Client
rm CUON/cuonObjects
cp -R CUON/* ~/cuon/bin
cp -R locale ~/cuon
cp ../Plugins/Dia/*.py ~/.dia/python


cp usr/share/cuon/*.svg ~/cuon
cd ~/cuon/bin
echo "Cuon.py $Server $CLIENT $DEBUG $CUON_LOCALE $CUON_PATH $Typ"


$EXEC  Cuon.py $Server $CLIENT $DEBUG $CUON_LOCALE $CUON_PATH $Typ $2 $3 $4
