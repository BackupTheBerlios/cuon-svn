#! /bin/sh

echo "cuondsh $1"
cd /usr/share/cuon/cuon_server/src
python cuond.py $1
