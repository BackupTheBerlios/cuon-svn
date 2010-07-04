#!/bin/sh


rsync  -avz --numeric-ids -e 'ssh -p 22'  *.html root@cuon.org://var/www

rsync  -avz --numeric-ids -e 'ssh -p 22'  *.js root@cuon.org://var/www

rsync  -avz --numeric-ids -e 'ssh -p 22'  *.css root@cuon.org://var/www





rsync  -avz --numeric-ids -e 'ssh -p 22' Cuon/*.html root@cuon.org://var/www/Cuon 
rsync  -avz --numeric-ids -e 'ssh -p 22'  Cyrus/*.html root@cuon.org://var/www/Cyrus
rsync  -avz --numeric-ids -e 'ssh -p 22'  Downloads/*.html root@cuon.org://var/www/Downloads 
rsync  -avz --numeric-ids -e 'ssh -p 22' Extensions/*.html root@cuon.org://var/www/Extensions 
rsync  -avz --numeric-ids -e 'ssh -p 22' Screenshots/*.html root@cuon.org://var/www/Screenshots
rsync  -avz --numeric-ids -e 'ssh -p 22' CuonDia/*.html root@cuon.org://var/www/CuonDia

# Images
rsync -r -avz --numeric-ids -e 'ssh -p 22' images root@cuon.org://var/www


# English
rsync  -avz --numeric-ids -e 'ssh -p 22' en_Cuon/*.html root@cuon.org://var/www/en_Cuon
