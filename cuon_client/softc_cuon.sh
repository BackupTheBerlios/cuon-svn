EXEC=/usr/bin/python

make -f Makefile.pyth all
sudo make -f Makefile.pyth install

cd Py/

case $1 in 

server)
cp ../cuon_server.py . 
export CUON_SERVER=softc.dyndns.org:9673/Cuon; export CUON_HOME=/home/jhamel/softc_cuon; $EXEC cuon_server.py
;;

client)
export CUON_SERVER=softc.dyndns.org:9673/Cuon; export CUON_HOME=/home/jhamel/softc_cuon; $EXEC Cuon.py 
;;

esac



cd ../


