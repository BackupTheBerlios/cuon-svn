
#!/bin/sh

# tested on Debian, Ubuntu
# suitable for local install


CUONADMIN="cuonadmin"
CUONADMINPWD="password"
CUONSC=$HOME/cuon/bin/sc
CUONPROJDIR=$HOME/projekte
CUONCLIENTHTTP=http://85.214.52.49/downloads/
CUONCLIENT=CuonClient-0.41-4.tar.bz2            # should be CounClient-latest.tar.bz2
CUONSERVER=localhost
CUONSERVERSSHPORT=22



# create $HOME/projekte
echo '.'
echo 'create '$CUONPROJDIR
echo '.'
mkdir $CUONPROJDIR
cd $CUONPROJDIR

# generate ssh keys
echo '.'
echo 'generate ssh keys - just hit enter'
echo '.'
mkdir $HOME/.ssh
cd $HOME/.ssh
ssh-keygen -t rsa

scp -P$CUONSERVERSSHPORT id_rsa.pub root@$CUONSERVER://root
ssh -p $CUONSERVERSSHPORT root@$CUONSERVER "cat /root/id_rsa.pub >> /root/.ssh/authorized_keys"


cd $CUONPROJDIR

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


# continue now with graphical installer
echo '.'
echo 'now continue with the graphical installer'
echo '.'
cd $CUONPROJDIR/cuon/cuon_client
python setup.py


