EXECDIR = /usr/bin
INSTALLDIR = /usr/lib/cuon
SERVERDIRSHARE = /usr/share/cuon
SERVERDIRCONFIG = /etc/cuon
I18LDIR_DE=/usr/share/locale/de/LC_MESSAGES
dest_glade = $(SERVERDIRSHARE)/glade
dest_report = $(SERVERDIRSHARE)/report

# Please set here your values
zope_extension =  root@server2://var/lib/zope/instance/default/Extensions
zope_import =  root@server2://var/lib/zope/instance/default/import


src_ini=./cuon_ini1.xml


src_main = ./src/*.py cuon.sh
dest_main = ./Py
dest_cuon = $(dest_main)/cuon


src_server = ./cuon_server.py
dest_server =$(dest_cuon)
 

src_typedefs = ./src/TypeDefs/src/*.py
dest_typedefs = $(dest_cuon)/TypeDefs


src_login = ./src/Login/src/*.py
dest_login = $(dest_cuon)/Login

src_misc = ./src/Misc/src/*.py
dest_misc = $(dest_cuon)/Misc

src_addresses = ./src/Addresses/src/*.py
dest_addresses = $(dest_cuon)/Addresses


src_articles = ./src/Articles/src/*.py
dest_articles = $(dest_cuon)/Articles

src_order = ./src/Order/src/*.py
dest_order = $(dest_cuon)/Order


src_databases = ./src/Databases/src/*.py
dest_databases = $(dest_cuon)/Databases



src_xml = ./src/XML/src/*.py
dest_xml = $(dest_cuon)/XML

src_xmlrpc = ./src/XMLRPC/src/*.py
dest_xmlrpc = $(dest_cuon)/XMLRPC


src_windows = ./src/Windows/src/*.py
dest_windows = $(dest_cuon)/Windows


src_log = ./src/Logging/src/*.py
dest_log = $(dest_cuon)/Logging


src_oo = ./src/OpenOffice/src/*.py
dest_oo = $(dest_cuon)/OpenOffice

src_pdf = ./src/PDF/src/*.py ./src/PDF/XML/*.py
dest_pdf = $(dest_cuon)/PDF



src_preferences = ./src/Preferences/src/*.py ./src/Preferences/XML/*.py
dest_preferences = $(dest_cuon)/Preferences

src_repgen = ./src/ReportGenerator/src/*.py
dest_repgen = $(dest_cuon)/ReportGenerator


src_report = 


src_cuon =  $(dest_cuon)/*
dest_primus_cuon = ~/Projekte/Primus/Py/cuon


src_xmlDefaults = ./*.xml

src_locale_de = ./de.mo

 

all :
	if [ ! -d $(dest_main) ] ; then mkdir $(dest_main) ; fi ; cp $(src_main) $(dest_main) 
	if [ ! -d $(dest_cuon) ] ; then mkdir $(dest_cuon) ; fi  

	if [ ! -d $(dest_server) ] ; then mkdir $(dest_server) ; fi ; cp $(src_server) $(dest_server) 
	if [ ! -d $(dest_login) ] ; then mkdir $(dest_login) ; fi ; cp $(src_login) $(dest_login) 
	if [ ! -d $(dest_addresses) ] ; then mkdir $(dest_addresses) ; fi ; cp $(src_addresses) $(dest_addresses) 
	if [ ! -d $(dest_articles) ] ; then mkdir $(dest_articles) ; fi ; cp $(src_articles) $(dest_articles) 
	if [ ! -d $(dest_order) ] ; then mkdir $(dest_order) ; fi ; cp $(src_order) $(dest_order) 
	if [ ! -d $(dest_databases) ] ; then mkdir $(dest_databases) ; fi ; cp $(src_databases) $(dest_databases) 
	if [ ! -d $(dest_xml) ] ; then mkdir $(dest_xml) ; fi ; cp $(src_xml) $(dest_xml) 
	if [ ! -d $(dest_xmlrpc) ] ; then mkdir $(dest_xmlrpc) ; fi ; cp $(src_xmlrpc) $(dest_xmlrpc) 
	if [ ! -d $(dest_typedefs) ] ; then mkdir $(dest_typedefs) ; fi ; cp $(src_typedefs) $(dest_typedefs) 
	if [ ! -d $(dest_windows) ] ; then mkdir $(dest_windows) ; fi ; cp $(src_windows) $(dest_windows) 
	if [ ! -d $(dest_log) ] ; then mkdir $(dest_log) ; fi ; cp $(src_log) $(dest_log) 
	if [ ! -d $(dest_oo) ] ; then mkdir $(dest_oo) ; fi ; cp $(src_oo) $(dest_oo) 
	if [ ! -d $(dest_misc) ] ; then mkdir $(dest_misc) ; fi ; cp $(src_misc) $(dest_misc) 
	if [ ! -d $(dest_pdf) ] ; then mkdir $(dest_pdf) ; fi ; cp $(src_pdf) $(dest_pdf) 
	if [ ! -d $(dest_preferences) ] ; then mkdir $(dest_preferences) ; fi ; cp $(src_preferences) $(dest_preferences) 
	if [ ! -d $(dest_repgen) ] ; then mkdir $(dest_repgen) ; fi ; cp $(src_repgen) $(dest_repgen) 

	if [ ! -e $(dest_cuon)/__init__.py ] ; then touch $(dest_cuon)/__init__.py ; fi
	if [ ! -e $(dest_cuon)/__init__.py ] ; then touch $(dest_cuon)/__init__.py ; fi






install:
	make  all
	if  [ ! -d $(INSTALLDIR) ] ; then mkdir $(INSTALLDIR) ; fi 
	cp -R Py/* $(INSTALLDIR)
	if [ -f $(EXECDIR)/cuon ] ; then rm $(EXECDIR)/cuon ; fi
	cp $(INSTALLDIR)/cuon.sh $(EXECDIR)/cuon
	if [ -f de.mo ] ; then rm de.mo ; fi 
	msgfmt -o de.mo de.po
	if [ ! -d $(I18LDIR_DE) ] ; then mkdir $(I18LDIR_DE) ; fi ; 
	cp $(src_locale_de) $(I18LDIR_DE)/cuon.mo 
	cp ./createUserDirs.sh $(INSTALLDIR)
	chmod a+x $(INSTALLDIR)/createUserDirs.sh


install_server:

	make install
	if  [ ! -d $(SERVERDIRCONFIG) ] ; then mkdir $(SERVERDIRCONFIG) ; fi 	
	cp $(src_ini) $(SERVERDIRCONFIG)
	if  [ ! -d $(SERVERDIRSHARE) ] ; then mkdir $(SERVERDIRSHARE) ; fi 	
	if  [ ! -d $(dest_glade) ] ; then mkdir $(dest_glade) ; fi 	
	if  [ ! -d $(dest_report) ] ; then mkdir $(dest_report) ; fi 	

	cp $(src_xmlDefaults) $(SERVERDIRSHARE)
	find ./ -name "*.glade2" -exec cp {} $(dest_glade) \; 
	find ./ -name "entry_*" -exec cp {}  $(SERVERDIRSHARE) \; 
	find ./src/PDF/XML -name "*.xml" -exec cp {} $(dest_report) \; 

install_zope:

	scp ../cuon_server//src/cuon_zope.py $(zope_extension)
	scp ../cuon_server//zope/*.zexp $(zope_import)

