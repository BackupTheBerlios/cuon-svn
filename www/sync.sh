#!/bin/sh

cd en_Cuon

docbook2html en_cuon.docbook && docbook2tex en_cuon.docbook && pdfjadetex en_cuon.tex

cd ..

cd Cuon

cp cuon.docbook de_cuon.docbook
recode -d utf-8..h4 de_cuon.docbook
docbook2html de_cuon.docbook && docbook2tex de_cuon.docbook && pdfjadetex de_cuon.tex

cd ..

rsync  -avz --numeric-ids -e 'ssh -p 22'  *.html root@cuon.org://var/www/cuon_web

rsync  -avz --numeric-ids -e 'ssh -p 22'  *.js root@cuon.org://var/www/cuon_web

rsync  -avz --numeric-ids -e 'ssh -p 22'  *.css root@cuon.org://var/www/cuon_web

rsync  -avz --numeric-ids -e 'ssh -p 22'  *.gif root@cuon.org://var/www/cuon_web

rsync  -r -avz --numeric-ids -e 'ssh -p 22'  FAQ root@cuon.org://var/www/cuon_web



rsync  -avz --numeric-ids -e 'ssh -p 22' Cuon/*.html root@cuon.org://var/www/cuon_web/Cuon 
rsync  -avz --numeric-ids -e 'ssh -p 22' Cuon/*.css root@cuon.org://var/www/cuon_web/Cuon 

rsync  -avz --numeric-ids -e 'ssh -p 22' Cuon/*.pdf root@cuon.org://var/www/cuon_web/Cuon 
rsync  -avz --numeric-ids -e 'ssh -p 22' Cuon/images/screenshots/*.png root@cuon.org://var/www/cuon_web/Cuon/images/screenshots
# rsync  -avz --numeric-ids -e 'ssh -p 22'  Cyrus/*.html root@cuon.org://var/www/cuon_web/Cyrus
rsync  -avz --numeric-ids -e 'ssh -p 22'  Downloads/*.html root@cuon.org://var/www/cuon_web/Downloads 
rsync  -avz --numeric-ids -e 'ssh -p 22' Extensions/*.html root@cuon.org://var/www/cuon_web/Extensions 
rsync  -avz --numeric-ids -e 'ssh -p 22' Screenshots/*.html root@cuon.org://var/www/cuon_web/Screenshots
rsync  -avz --numeric-ids -e 'ssh -p 22' CuonDia/*.html root@cuon.org://var/www/cuon_web/CuonDia

# Images
rsync -r -avz --numeric-ids -e 'ssh -p 22' images root@cuon.org://var/www/cuon_web

# Api

#client api
rsync  -avz --numeric-ids ../api/html/* api
rsync  -avz --numeric-ids  ../api/pdf/*.pdf  api
# server api
rsync  -avz --numeric-ids ../api/cuonserver api

rsync -r -avz --numeric-ids -e 'ssh -p 22' api root@cuon.org://var/www/cuon_web

# public
rsync -r -avz --numeric-ids -e 'ssh -p 22' public_html root@cuon.org://var/www/cuon_web

# English
rsync  -avz --numeric-ids -e 'ssh -p 22' en_Cuon/*.html root@cuon.org://var/www/cuon_web/en_Cuon
rsync  -avz --numeric-ids -e 'ssh -p 22' en_Cuon/*.css root@cuon.org://var/www/cuon_web/en_Cuon
rsync  -avz --numeric-ids -e 'ssh -p 22' en_Cuon/*.pdf root@cuon.org://var/www/cuon_web/en_Cuon
rsync -r -avz --numeric-ids -e 'ssh -p 22' en_Cuon/images root@cuon.org://var/www/cuon_web/en_Cuon/


# now set the rights
ssh root@cuon.org "cd /var/www/ ; chown -R www-data:www-data *"

