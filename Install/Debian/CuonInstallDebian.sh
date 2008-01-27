#!/bin/sh

# tested on Debian, ubuntu
# suitable for local install
# execute it as as root !!!
# execute it

CUONADMIN="cuonadmin"
CUONADMINPWD="password"
CUONDOWNLOAD=http://85.214.52.49/downloads


apt-get install python-twisted-web \
python-pygresql \
python-pyopenssl \
python-reportlab \
python-xml \
postgresql-8.1 \
postgresql-client-8.1 \
subversion \
openssl \
bzip2 \
ssh \

# download and install missing icalendar package
echo '.'
echo 'download and install missing icalendar package'
echo '.'
rm -f python-icalendar_0.11-etch1_i386.deb
wget http://opensync.gforge.punktart.de/repo/opensync-0.21/pool/main/p/python-icalendar/python-icalendar_0.11-etch1_i386.deb
dpkg -i python-icalendar_0.11-etch1_i386.deb




# postgres
echo '.'
echo 'restart database'
echo '.'
/etc/init.d/postgresql-8.1 restart
echo '.'
echo 'create database'
echo '.'
su postgres -c 'createdb -E utf-8 cuon'
echo '.'
echo 'create user cuonadmin - Superuser'
echo '.'
su postgres -c 'createuser -s '$CUONADMIN
echo '.'
echo 'create user zope - no rights'
echo '.'
su postgres -c 'createuser -S -D -R zope'
echo '.'
echo 'create plpgsql'
echo '.'
su postgres -c '/usr/bin/createlang -d cuon plpgsql'

#pg_hba change to trust
# 
# 
#

PGCONF=/etc/postgresql/8.1/main/pg_hba.conf
PGCONFSED=/etc/postgresql/8.1/main/pg_hba.conf_sed
echo $PGCONF
echo $PGCONFSED

cp $PGCONF $PGCONF.bak
sed -e s/local.*all.*all.*ident.*sameuser/local\ \ \ \ all\ \ \ \ all\ \ \ \ trust/1  \
-e s/host.*all.*all.*127.0.0.1.32.*md5/host\ \ \ \ all\ \ \ \ all\ \ \ \127.0.0.1\\/32\ \ \ \ trust/g  \
-e s/host.*all.*all.*\\:\\:1\\/128.*md5/host\ \ \ \ all\ \ \ \ all\ \ \ \ \\:\\:1\\/128\ \ \ \ trust/g  \
-e w$PGCONFSED  $PGCONF
cp $PGCONFSED $PGCONF
chown postgres:postgres $PGCONF

echo '.'
echo 'restart database'
echo '.'

/etc/init.d/postgresql-8.1 restart


# generate ssl keys
echo '.'
echo 'generate ssl keys'
echo '.'
mkdir /etc/cuon
openssl genrsa -out /etc/cuon/serverkey.pem 2048
openssl req -new -x509 -key /etc/cuon/serverkey.pem -out /etc/cuon/servercert.pem -days 1095

#
#
# sudo mkdir /root/.ssh


