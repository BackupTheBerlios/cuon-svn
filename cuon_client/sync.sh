
REMOTEDIR=www.cyrus-computer.de:"/home/cyrus-computer.de/www/cuon/src"
LOCALDIR=~/Projekte/cuon/*
USER=cyrus-computer.de
echo "Sync gestartet"

scp2 -r $LOCALDIR  $USER@$REMOTEDIR

