
PGCONF=/var/lib/pgsql/data/pg_hba.conf
PGCONFSED=/var/lib/pgsql/data/pg_hba.conf_sed
echo $PGCONF
echo $PGCONFSED

cp $PGCONF $PGCONF.bak
sed -e s/local.*all.*all.*ident.*sameuser/local\ \ \ \ all\ \ \ \ all\ \ \ \ trust/1  \
-e s/host.*all.*all.*127.0.0.1.32.*ident.*sameuser/host\ \ \ \ all\ \ \ \ all\ \ \ \127.0.0.1\\/32\ \ \ \ trust/g  \
-e s/host.*all.*all.*\\:\\:1\\/128.*ident.*sameuser/host\ \ \ \ all\ \ \ \ all\ \ \ \ \\:\\:1\\/128\ \ \ \ trust/g  \
-e w$PGCONFSED  $PGCONF
cp $PGCONFSED $PGCONF
chown postgres:postgres $PGCONF

