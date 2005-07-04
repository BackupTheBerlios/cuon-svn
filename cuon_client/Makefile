EXECDIR = /usr/bin
INSTALLDIR = /usr/lib/cuon
ICONDIR = /usr/lib/cuon/icons
SERVERDIRSHARE = /usr/share/cuon
SERVERDIRCONFIG = /etc/cuon
I18LDIR_DE=/usr/share/locale/de/LC_MESSAGES
dest_glade = $(SERVERDIRSHARE)/glade
dest_report = $(SERVERDIRSHARE)/report

# Please set here your values
zope_extension =  root@server2://var/lib/zope/instance/default/Extensions
zope_import =  root@server2://var/lib/zope/instance/default/import


src_ini=./cuon_ini1.xml


src_main = ./cuon/*.py cuon.sh Cuon.py
dest_main = ./CUON
dest_cuon = $(dest_main)/cuon


src_server = ./cuon_server.py
dest_server =$(dest_cuon)
 

src_typedefs = ./cuon/TypeDefs/*.py
dest_typedefs = $(dest_cuon)/TypeDefs


src_login = ./cuon/Login/*.py
dest_login = $(dest_cuon)/Login

src_misc = ./cuon/Misc/*.py
dest_misc = $(dest_cuon)/Misc

src_addresses = ./cuon/Addresses/*.py
dest_addresses = $(dest_cuon)/Addresses


src_articles = ./cuon/Articles/*.py
dest_articles = $(dest_cuon)/Articles

src_order = ./cuon/Order/*.py
dest_order = $(dest_cuon)/Order


src_databases = ./cuon/Databases/*.py
dest_databases = $(dest_cuon)/Databases



src_xml = ./cuon/XML/*.py
dest_xml = $(dest_cuon)/XML

src_xmlrpc = ./cuon/XMLRPC/*.py
dest_xmlrpc = $(dest_cuon)/XMLRPC


src_windows = ./cuon/Windows/*.py
dest_windows = $(dest_cuon)/Windows


src_log = ./cuon/Logging/*.py
dest_log = $(dest_cuon)/Logging


src_oo = ./cuon/OpenOffice/*.py
dest_oo = $(dest_cuon)/OpenOffice

src_pdf = ./cuon/PDF/*.py 
dest_pdf = $(dest_cuon)/PDF

src_pdf_xml = ./cuon/PDF/XML/*.py
dest_pdf_xml = $(dest_cuon)/PDF/XML



src_preferences = ./cuon/Preferences/*.py 
dest_preferences = $(dest_cuon)/Preferences

src_preferences_xml = ./cuon/Preferences/XML/*.py
dest_preferences_xml = $(dest_cuon)/Preferences/XML


src_repgen = ./cuon/ReportGenerator/*.py
dest_repgen = $(dest_cuon)/ReportGenerator

src_stock = ./cuon/Stock/*.py
dest_stock = $(dest_cuon)/Stock

src_email = ./cuon/E_Mail/*.py
dest_email = $(dest_cuon)/E_Mail


src_dms = ./cuon/DMS/*.py
dest_dms = $(dest_cuon)/DMS


src_vtk = ./cuon/VTK/*.py
dest_vtk = $(dest_cuon)/VTK

src_prefs_finance = ./cuon/PrefsFinance/*.py 
dest_prefs_finance = $(dest_cuon)/PrefsFinance

src_webshop = ./cuon/WebShop/*.py
dest_webshop = $(dest_cuon)/WebShop


src_finances_misc =  ./cuon/Finances/*.py
src_finances_cab = ./cuon/Finances/CashAccountBook/*.py 
src_finances_ib =  ./cuon/Finances/InvoiceBook/*.py

dest_finances = $(dest_cuon)/Finances




#src_cuon =  $(dest_cuon)/*
#dest_primus_cuon = ~/Projekte/Primus/Py/cuon


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
	if [ ! -d $(dest_pdf_xml) ] ; then mkdir $(dest_pdf_xml) ; fi ; cp $(src_pdf_xml) $(dest_pdf_xml) 
	if [ ! -d $(dest_preferences_xml) ] ; then mkdir $(dest_preferences_xml) ; fi ; cp $(src_preferences_xml) $(dest_preferences_xml) 
	if [ ! -d $(dest_repgen) ] ; then mkdir $(dest_repgen) ; fi ; cp $(src_repgen) $(dest_repgen) 
	if [ ! -d $(dest_stock) ] ; then mkdir $(dest_stock) ; fi ; cp $(src_stock) $(dest_stock) 
	if [ ! -d $(dest_email) ] ; then mkdir $(dest_email) ; fi ; cp $(src_email) $(dest_email) 
	if [ ! -d $(dest_dms) ] ; then mkdir $(dest_dms) ; fi ; cp $(src_dms) $(dest_dms) 
	if [ ! -d $(dest_vtk) ] ; then mkdir $(dest_vtk) ; fi ; cp $(src_vtk) $(dest_vtk) 
	if [ ! -d $(dest_prefs_finance) ] ; then mkdir $(dest_prefs_finance) ; fi ; cp $(src_prefs_finance) $(dest_prefs_finance) 
	if [ ! -d $(dest_webshop) ] ; then mkdir $(dest_webshop) ; fi ; cp $(src_webshop) $(dest_webshop) 
	if [ ! -d $(dest_finances) ] ; then mkdir $(dest_finances) ; fi  
	cp $(src_finances_misc) $(dest_finances)
	cp $(src_finances_cab) $(dest_finances)
	cp $(src_finances_ib) $(dest_finances) 

	if [ ! -e $(dest_cuon)/__init__.py ] ; then touch $(dest_cuon)/__init__.py ; fi
	if [ ! -e $(dest_cuon)/__init__.py ] ; then touch $(dest_cuon)/__init__.py ; fi






install:
	make  all
	if  [ ! -d $(INSTALLDIR) ] ; then mkdir $(INSTALLDIR) ; fi 
	cp -R $(dest_main)/* $(INSTALLDIR)
	if [ -f $(EXECDIR)/cuon ] ; then rm $(EXECDIR)/cuon ; fi
	cp $(INSTALLDIR)/cuon.sh $(EXECDIR)/cuon
	if [ -f de.mo ] ; then rm de.mo ; fi 
	msgfmt -o de.mo de.po
	if [ ! -d $(I18LDIR_DE) ] ; then mkdir $(I18LDIR_DE) ; fi ; 
	cp $(src_locale_de) $(I18LDIR_DE)/cuon.mo 
	cp ./createUserDirs.sh $(INSTALLDIR)
	chmod a+x $(INSTALLDIR)/createUserDirs.sh
	if  [ ! -d $(INSTALLDIR)/icons ] ; then mkdir $(INSTALLDIR)/icons ; fi 

	if  [ ! -d $(ICONDIR)/ ] ; then mkdir $(ICONDIR) ; fi 	

	find ./GUI/pixmaps  -name "*.xpm" -exec cp {} $(ICONDIR) \; 

install_server:

	make install
	if  [ ! -d $(SERVERDIRCONFIG) ] ; then mkdir $(SERVERDIRCONFIG) ; fi 	
	cp $(src_ini) $(SERVERDIRCONFIG)
	if  [ ! -d $(SERVERDIRSHARE) ] ; then mkdir $(SERVERDIRSHARE) ; fi 	
	if  [ ! -d $(ICONDIR) ] ; then mkdir $(ICONDIR) ; fi 	
	if  [ ! -d $(dest_glade) ] ; then mkdir $(dest_glade) ; fi 	
	if  [ ! -d $(dest_report) ] ; then mkdir $(dest_report) ; fi 	

	cp $(src_xmlDefaults) $(SERVERDIRSHARE)
	cp ./GUI/*.glade2 $(dest_glade) 
	find ./cuon  -name "*.glade2" -exec cp {} $(dest_glade) \; 
	find ./cuon  -name "entry_*" -exec cp {}  $(SERVERDIRSHARE) \; 
	find ./cuon/PDF/XML -name "*.xml" -exec cp {} $(dest_report) \; 
	find ./GUI/pixmaps  -name "*.xpm" -exec cp {} $(ICONDIR) \; 

install_zope:

	scp ../cuon_server//src/cuon_zope.py $(zope_extension)
	scp ../cuon_server//zope/*.zexp $(zope_import)

