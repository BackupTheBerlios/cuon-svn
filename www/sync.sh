#!/bin/sh

cd en_Cuon

docbook2html en_cuon.docbook && docbook2pdf en_cuon.docbook

cd ..

cd Cuon

cp cuon.docbook de_cuon.docbook
recode -d utf-8..h4 de_cuon.docbook
docbook2html de_cuon.docbook && docbook2pdf de_cuon.docbook

cd ..

rsync  -avz --numeric-ids -e 'ssh -p 22'  *.html root@cuon.org://var/www

rsync  -avz --numeric-ids -e 'ssh -p 22'  *.js root@cuon.org://var/www

rsync  -avz --numeric-ids -e 'ssh -p 22'  *.css root@cuon.org://var/www





rsync  -avz --numeric-ids -e 'ssh -p 22' Cuon/*.html root@cuon.org://var/www/Cuon 
rsync  -avz --numeric-ids -e 'ssh -p 22' Cuon/*.pdf root@cuon.org://var/www/Cuon 
rsync  -avz --numeric-ids -e 'ssh -p 22'  Cyrus/*.html root@cuon.org://var/www/Cyrus
rsync  -avz --numeric-ids -e 'ssh -p 22'  Downloads/*.html root@cuon.org://var/www/Downloads 
rsync  -avz --numeric-ids -e 'ssh -p 22' Extensions/*.html root@cuon.org://var/www/Extensions 
rsync  -avz --numeric-ids -e 'ssh -p 22' Screenshots/*.html root@cuon.org://var/www/Screenshots
rsync  -avz --numeric-ids -e 'ssh -p 22' CuonDia/*.html root@cuon.org://var/www/CuonDia

# Images
rsync -r -avz --numeric-ids -e 'ssh -p 22' images root@cuon.org://var/www

# public
rsync -r -avz --numeric-ids -e 'ssh -p 22' public_html root@cuon.org://var/www

# English
rsync  -avz --numeric-ids -e 'ssh -p 22' en_Cuon/*.html root@cuon.org://var/www/en_Cuon
rsync  -avz --numeric-ids -e 'ssh -p 22' en_Cuon/*.pdf root@cuon.org://var/www/en_Cuon
rsync -r -avz --numeric-ids -e 'ssh -p 22' en_Cuon/images root@cuon.org://var/www/en_Cuon/
