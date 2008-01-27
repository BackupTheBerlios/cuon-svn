CUONSC=$HOME/cuon/bin/sc
CUONPROJDIR=$HOME/projekte
CUONCLIENTHTTP=http://85.214.52.49/downloads/
CUONCLIENT=CuonClient-0.41-4.tar.bz2			# should be CounClient-latest.tar.bz2
CUONSERVER=localhost
CUONSERVERPORT=7080
CUONSERVERPROTOCOL=http


# create client startup script
echo '.'
echo 'create client startup script'
echo '.'
rm -f $CUONSC
echo "#!/bin/sh" > $CUONSC
echo "CUONHOME=$HOME/cuon" >> $CUONSC
echo "SERVER=$CUONSERVER" >> $CUONSC
echo "PORT=$CUONSERVERPORT" >> $CUONSC
echo "PROTOCOL=$CUONSERVERPROTOCOL" >> $CUONSC
echo " " >> $CUONSC
echo 'cd $CUONHOME/bin' >> $CUONSC
echo 'python Cuon.py $PROTOCOL://$SERVER:$PORT client NO $CUONHOME/locale $CUONHOME' >> $CUONSC
chmod +x $CUONSC


