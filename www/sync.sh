#!/bin/sh


rsync  -avz --numeric-ids -e 'ssh -p 22'  *.html root@cuon.org://var/www




rsync  -avz --numeric-ids -e 'ssh -p 22' Cuon/*.html root@cuon.org://var/www/Cuon 
rsync  -avz --numeric-ids -e 'ssh -p 22'  Cyrus/*.html root@cuon.org://var/www/Cyrus
rsync  -avz --numeric-ids -e 'ssh -p 22'  Downloads/*.html root@cuon.org://var/www/Downloads 
rsync  -avz --numeric-ids -e 'ssh -p 22' Extensions/*.html root@cuon.org://var/www/Extensions 

# Images
rsync -r -avz --numeric-ids -e 'ssh -p 22' images root@cuon.org://var/www


# English
rsync  -avz --numeric-ids -e 'ssh -p 22' en_Cuon/*.html root@cuon.org://var/www/en_Cuon
