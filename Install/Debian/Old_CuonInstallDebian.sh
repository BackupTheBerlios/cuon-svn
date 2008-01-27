
#!/bin/sh

# tested on Debian Etch (clean Netinstall)
# suitable for local install
# DON'T execute it as as root !!!
# make sure you are in the sudoers list
# execute it

CUONADMIN="cuonadmin"
CUONADMINPWD="password"
CUONSC=$HOME/cuon/bin/sc
CUONPROJDIR=$HOME/projekte
CUONCLIENTHTTP=http://85.214.52.49/downloads/
CUONCLIENT=CuonClient-0.41-4.tar.bz2            # should be CounClient-latest.tar.bz2

sudo apt-get install python-glade2 \
python-gnome2 \
python-gnome2-extras \
python-gtk2 \
python-imaging \
python-imaging-sane \
python-twisted-web \
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

# create $HOME/projekte
echo '.'
echo 'create '$CUONPROJDIR
echo '.'
mkdir $CUONPROJDIR
cd $CUONPROJDIR

# download and install missing icalendar package
echo '.'
echo 'download and install missing icalendar package'
echo '.'
rm -f python-icalendar_0.11-etch1_i386.deb
wget http://opensync.gforge.punktart.de/repo/opensync-0.21/pool/main/p/python-icalendar/python-icalendar_0.11-etch1_i386.deb
sudo dpkg -i python-icalendar_0.11-etch1_i386.deb

# postgres
echo '.'
echo 'create database'
echo '.'
sudo su postgres -c 'createdb -E utf-8 cuon'
echo '.'
echo 'create user cuonadmin - Superuser'
echo '.'
sudo su postgres -c 'createuser -s '$CUONADMIN
#psql -U$CUONADMIN cuon -c "ALTER USER "$CUONADMIN" WITH PASSWORD '"$CUONADMINPWD"'"
echo '.'
echo 'create user zope - no rights'
echo '.'
sudo su postgres -c 'createuser -S -D -R zope'
echo '.'
echo 'create plpgsql'
echo '.'
sudo su postgres -c '/usr/lib/postgresql/8.1/bin/createlang -d cuon plpgsql'

# generate ssh keys
echo '.'
echo 'generate ssh keys - just hit enter'
echo '.'
mkdir $HOME/.ssh
cd $HOME/.ssh
ssh-keygen -t rsa
sudo mkdir /root/.ssh
sudo su root -c 'cat id_rsa.pub >> /root/.ssh/authorized_keys'
cd $CUONPROJDIR/cuon/cuon_client/

# get latest version
echo '.'
echo 'get latest cuon version'
echo '.'
svn checkout http://svn.berlios.de/svnroot/repos/cuon
echo $CUONADMIN': '$CUONADMINPWD >> $CUONPROJDIR/cuon/cuon_server/examples/user.cfg
echo $CUONADMIN': cuon_all' >> $CUONPROJDIR/cuon/cuon_server/examples/UserGroups.cfg

# downlad cuon client
echo '.'
echo 'installing cuon client'
echo '.'
cd $HOME
wget $CUONCLIENTHTTP$CUONCLIENT
tar xf $CUONCLIENT
rm -f $CUONCLIENT

# create client startup script
echo '.'
echo 'create client startup script'
echo '.'
rm -f $CUONSC
echo '#!/bin/sh' > $CUONSC
echo 'CUONHOME='$HOME'/cuon' >> $CUONSC
echo 'SERVER=localhost' >> $CUONSC
echo 'PORT=7080' >> $CUONSC
echo 'if [ "$1" != "" ]; then' >> $CUONSC
echo '   if [ $1 = "-ssl" ] || [ "$1" = "-SSL" ] ; then' >> $CUONSC
echo '      PROTOCOL=https' >> $CUONSC
echo '      PORT=7580' >> $CUONSC
echo '   fi' >> $CUONSC
echo 'fi' >> $CUONSC
echo 'cd $CUONHOME/bin' >> $CUONSC
echo 'python Cuon.py PROTOCOL://$SERVER:$PORT client NO $CUONHOME/locale $CUONHOME' >> $CUONSC
chmod +x $CUONSC
cd $CUONPROJDIR/cuon/cuon_client

# generate ssl keys
echo '.'
echo 'generate ssl keys'
echo '.'
sudo mkdir /etc/cuon
sudo openssl genrsa -out /etc/cuon/serverkey.pem 2048
sudo openssl req -new -x509 -key /etc/cuon/serverkey.pem -out /etc/cuon/servercert.pem -days 1095

# continue now with graphical installer
echo '.'
echo 'now continue with the graphical installer'
echo 'BUT dont forget:'
echo '.. to edit pg_hba.conf and restart postgresql!!!'
echo '.. to edit the config files within setup.py.'
echo '.'


