EXECDIR = /usr/bin
INSTALLDIR = /usr/lib/cuon
ICONDIR = /usr/lib/cuon/icons
SERVERDIRSHARE = /usr/share/cuon


CUWEBSHARE = root@cuweb://usr/share/cuon
CUWEB = root@cuweb:/
CUWEBEXECDIR = $(CUWEB)/usr/bin
CUWEBLOCALEXECDIR = $(CUWEB)/usr/local/bin
CUWEBCONFIGDIR = $(CUWEB)/etc/cuon
CUWEBLOCALE = $(CUWEB)/usr/share/locale/de/LC_MESSAGES

CYWEBSHARE = root@cyweb://usr/share/cuon
CYWEB = root@cyweb:/
CYWEBEXECDIR = $(CYWEB)/usr/bin
CYWEBLOCALEXECDIR = $(CYWEB)/usr/local/bin
CYWEBCONFIGDIR = $(CYWEB)/etc/cuon
CYWEBLOCALE = $(CYWEB)/usr/share/locale/de/LC_MESSAGES


SERVERDIRCONFIG = /etc/cuon
VERSION_CFG = ./version.cfg

I18LDIR_DE=/usr/share/locale/de/LC_MESSAGES
I18LDIR_PT=/usr/share/locale/pt/LC_MESSAGES
I18LDIR_PT_BR=/usr/share/locale/pt_BR/LC_MESSAGES

src_locale_de = ./de.mo
src_locale_pt = ./pt.mo
src_locale_pt_BR = ./pt_BR.mo

dest_glade = $(SERVERDIRSHARE)/glade
dest_report = $(SERVERDIRSHARE)/report
iClientDir = /opt/Projekte/cuon/iClient
iClientDirLocale = $(iClientDir)/locale/de/LC_MESSAGES

CUON_VAR = /var/cuon
CUON_DOCUMENTS = $(CUON_VAR)/Documents

CUON_DOCUMENTS_LISTS = $(CUON_DOCUMENTS)/Lists

CUON_DOCUMENTS_LISTS_ADDRESSES = $(CUON_DOCUMENTS_LISTS)/Addresses
CUON_DOCUMENTS_LISTS_ARTICLES = $(CUON_DOCUMENTS_LISTS)/Articles
CUON_DOCUMENTS_LISTS_STOCK = $(CUON_DOCUMENTS_LISTS)/Stock



CUON_DOCUMENTS_HIBERNATION = $(CUON_DOCUMENTS)/Hibernation
CUON_DOCUMENTS_HIBERNATION_INCOMING = $(CUON_DOCUMENTS_HIBERNATION)/Incoming



# Please set here your values
zope_extension =  root@cyweb://var/lib/zope2.8/instance/default/Extensions
zope_import =  root@cyweb://var/lib/zope2.8/instance/default/import

zope_extension2 =  root@cuweb://var/lib/zope2.8/instance/default/Extensions
zope_import2 =  root@cuweb://var/lib/zope2.8/instance/default/import

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

src_user = ./cuon/User/*.py
dest_user = $(dest_cuon)/User


src_misc = ./cuon/Misc/*.py
dest_misc = $(dest_cuon)/Misc

src_addresses = ./cuon/Addresses/*.py
dest_addresses = $(dest_cuon)/Addresses


src_articles = ./cuon/Articles/*.py
dest_articles = $(dest_cuon)/Articles


src_clients = ./cuon/Clients/*.py
dest_clients = $(dest_cuon)/Clients

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

src_help = ./cuon/Help/*.py
dest_help = $(dest_cuon)/Help



src_oo = ./cuon/OpenOffice/*.py
dest_oo = $(dest_cuon)/OpenOffice




src_preferences = ./cuon/Preferences/*.py 
dest_preferences = $(dest_cuon)/Preferences

src_preferences_xml = ./cuon/Preferences/XML/*.py
dest_preferences_xml = $(dest_cuon)/Preferences/XML



src_stock = ./cuon/Stock/*.py
dest_stock = $(dest_cuon)/Stock

src_email = ./cuon/E_Mail/*.py
dest_email = $(dest_cuon)/E_Mail


src_dms = ./cuon/DMS/*.py
dest_dms = $(dest_cuon)/DMS

src_staff = ./cuon/Staff/*.py
dest_staff = $(dest_cuon)/Staff


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

src_biblio = ./cuon/Biblio/*.py
dest_biblio = $(dest_cuon)/Biblio


src_ai = ./cuon/AI/*.py
dest_ai = $(dest_cuon)/AI
src_aiml = ./cuon/AI/AIML
dest_aiml = $(SERVERDIRSHARE)/AI/AIML
dest_aiml_cuweb = $(CUWEBSHARE)/AI/AIML
src_ai_clients = ./cuon/AI
dest_ai_gtkMiniClient = ./gtkMiniClient

src_project = ./cuon/Project/*.py
dest_project = $(dest_cuon)/Project


# Ext. modules with GPL
src_garden = ./cuon/Garden/*.py
dest_garden = $(dest_cuon)/Garden



#src_cuon =  $(dest_cuon)/*
#dest_primus_cuon = ~/Projekte/Primus/Py/cuon


src_xmlDefaults = ./*.xml


 

all :
	if [ ! -d $(dest_main) ] ; then mkdir $(dest_main) ; fi ; cp $(src_main) $(dest_main) 
	cp $(VERSION_CFG) $(dest_main) 
	if [ ! -d $(dest_cuon) ] ; then mkdir $(dest_cuon) ; fi  

	if [ ! -d $(dest_server) ] ; then mkdir $(dest_server) ; fi ; cp $(src_server) $(dest_server) 
	if [ ! -d $(dest_login) ] ; then mkdir $(dest_login) ; fi ; cp $(src_login) $(dest_login) 
	if [ ! -d $(dest_user) ] ; then mkdir $(dest_user) ; fi ; cp $(src_user) $(dest_user) 
	if [ ! -d $(dest_addresses) ] ; then mkdir $(dest_addresses) ; fi ; cp $(src_addresses) $(dest_addresses) 
	if [ ! -d $(dest_articles) ] ; then mkdir $(dest_articles) ; fi ; cp $(src_articles) $(dest_articles) 
	if [ ! -d $(dest_clients) ] ; then mkdir $(dest_clients) ; fi ; cp $(src_clients) $(dest_clients) 
	if [ ! -d $(dest_order) ] ; then mkdir $(dest_order) ; fi ; cp $(src_order) $(dest_order) 
	if [ ! -d $(dest_databases) ] ; then mkdir $(dest_databases) ; fi ; cp $(src_databases) $(dest_databases) 
	if [ ! -d $(dest_xml) ] ; then mkdir $(dest_xml) ; fi ; cp $(src_xml) $(dest_xml) 
	if [ ! -d $(dest_xmlrpc) ] ; then mkdir $(dest_xmlrpc) ; fi ; cp $(src_xmlrpc) $(dest_xmlrpc) 
	if [ ! -d $(dest_typedefs) ] ; then mkdir $(dest_typedefs) ; fi ; cp $(src_typedefs) $(dest_typedefs) 
	if [ ! -d $(dest_windows) ] ; then mkdir $(dest_windows) ; fi ; cp $(src_windows) $(dest_windows) 
	if [ ! -d $(dest_log) ] ; then mkdir $(dest_log) ; fi ; cp $(src_log) $(dest_log) 
	if [ ! -d $(dest_oo) ] ; then mkdir $(dest_oo) ; fi ; cp $(src_oo) $(dest_oo) 
	if [ ! -d $(dest_misc) ] ; then mkdir $(dest_misc) ; fi ; cp $(src_misc) $(dest_misc) 
	if [ ! -d $(dest_preferences) ] ; then mkdir $(dest_preferences) ; fi ; cp $(src_preferences) $(dest_preferences) 
	if [ ! -d $(dest_preferences_xml) ] ; then mkdir $(dest_preferences_xml) ; fi ; cp $(src_preferences_xml) $(dest_preferences_xml) 
	if [ ! -d $(dest_stock) ] ; then mkdir $(dest_stock) ; fi ; cp $(src_stock) $(dest_stock) 
	if [ ! -d $(dest_email) ] ; then mkdir $(dest_email) ; fi ; cp $(src_email) $(dest_email) 
	if [ ! -d $(dest_dms) ] ; then mkdir $(dest_dms) ; fi ; cp $(src_dms) $(dest_dms) 
	if [ ! -d $(dest_help) ] ; then mkdir $(dest_help) ; fi ; cp $(src_help) $(dest_help) 
	if [ ! -d $(dest_staff) ] ; then mkdir $(dest_staff) ; fi ; cp $(src_staff) $(dest_staff) 
	if [ ! -d $(dest_vtk) ] ; then mkdir $(dest_vtk) ; fi ; cp $(src_vtk) $(dest_vtk) 
	if [ ! -d $(dest_prefs_finance) ] ; then mkdir $(dest_prefs_finance) ; fi ; cp $(src_prefs_finance) $(dest_prefs_finance) 
	if [ ! -d $(dest_webshop) ] ; then mkdir $(dest_webshop) ; fi ; cp $(src_webshop) $(dest_webshop) 
	if [ ! -d $(dest_finances) ] ; then mkdir $(dest_finances) ; fi  
	cp $(src_finances_misc) $(dest_finances)
	cp $(src_finances_cab) $(dest_finances)
	cp $(src_finances_ib) $(dest_finances) 
	if [ ! -d $(dest_biblio) ] ; then mkdir $(dest_biblio) ; fi ; cp $(src_biblio) $(dest_biblio) 
	if [ ! -d $(dest_ai) ] ; then mkdir $(dest_ai) ; fi ; cp $(src_ai) $(dest_ai) 
	if [ ! -e $(dest_cuon)/__init__.py ] ; then touch $(dest_cuon)/__init__.py ; fi
	if [ ! -e $(dest_cuon)/__init__.py ] ; then touch $(dest_cuon)/__init__.py ; fi
	if [ ! -d $(dest_project) ] ; then mkdir $(dest_project) ; fi ; cp $(src_project) $(dest_project)

	# ext. Modules with GPL
	if [ ! -d $(dest_garden) ] ; then mkdir $(dest_garden) ; fi ; cp $(src_garden) $(dest_garden) 

iClient:
	cp /usr/share/locale/de/LC_MESSAGES/cuon.mo $(iClientDirLocale)
	cp ~/cuon/*.xml $(iClientDir)/cuon
	cp ~/cuon/Reports/* $(iClientDir)/cuon/Reports
	cp ~/cuon/*.jpg $(iClientDir)/cuon
	cp ~/cuon/cuonObjects $(iClientDir)/cuon

install:
	make  all
	if  [ ! -d $(INSTALLDIR) ] ; then mkdir $(INSTALLDIR) ; fi 
	cp -R $(dest_main)/* $(INSTALLDIR)
	if [ -f $(EXECDIR)/cuon ] ; then rm $(EXECDIR)/cuon ; fi
	cp $(INSTALLDIR)/cuon.sh $(EXECDIR)/cuon
	if [ -f de.mo ] ; then rm de.mo ; fi 
	msgfmt -o de.mo de.po
	if [ -f pt.mo ] ; then rm pt.mo ; fi 
	msgfmt -o pt.mo pt.po
	if [ -f pt_BR.mo ] ; then rm pt_BR.mo ; fi 
	msgfmt -o pt_BR.mo pt_BR.po

	if [ ! -d $(I18LDIR_DE) ] ; then mkdir $(I18LDIR_DE) ; fi ; 
	cp $(src_locale_de) $(I18LDIR_DE)/cuon.mo 
	if [ ! -d $(I18LDIR_PT) ] ; then mkdir $(I18LDIR_PT) ; fi ; 
	cp $(src_locale_pt) $(I18LDIR_PT)/cuon.mo 
	if [ ! -d $(I18LDIR_PT_BR) ] ; then mkdir $(I18LDIR_PT_BR) ; fi ; 
	cp $(src_locale_pt_BR) $(I18LDIR_PT_BR)/cuon.mo 
	cp ./createUserDirs.sh $(INSTALLDIR)
    
	chmod a+x $(INSTALLDIR)/createUserDirs.sh
	if  [ ! -d $(INSTALLDIR)/icons ] ; then mkdir $(INSTALLDIR)/icons ; fi 

	if  [ ! -d $(ICONDIR)/ ] ; then mkdir $(ICONDIR) ; fi 	

	find ./GUI/pixmaps  -name "*.xpm" -exec cp {} $(ICONDIR) \; 

ai:

	if  [ ! -d $(SERVERDIRSHARE)/AI ] ; then mkdir $(SERVERDIRSHARE)/AI ; fi 
	if  [ ! -d $(dest_aiml) ] ; then mkdir $(dest_aiml) ; fi 
	cp $(src_aiml)/de_startup.ini $(dest_aiml)/startup.ini
	cp $(src_aiml)/de_main.sgml $(dest_aiml)/main.sgml
	cp $(src_aiml)/cuon.sgml $(dest_aiml)/cuon.sgml
	cp $(src_aiml)/de_cuon*.sgml $(dest_aiml)/


	chmod a+r $(dest_aiml)/*
	cp ../cuon_server/src/ai_subs.ini $(SERVERDIRCONFIG)/
	cp ../cuon_server/src/ai_aiml.ini $(SERVERDIRCONFIG)/

gtkMiniClient:
	sudo make ai
	if [ ! -d $(dest_ai_gtkMiniClient) ] ; then mkdir $(dest_ai_gtkMiniClient) ; fi ; cp $(src_ai_clients)/gtkMiniClient.py $(dest_ai_gtkMiniClient)/ 
	cp $(src_ai_clients)/GUI/ai.glade2 $(dest_ai_gtkMiniClient)/gtkMiniClient.glade


aicuweb_aiml:
	scp $(src_aiml)/de_startup.ini $(dest_aiml_cuweb)/startup.ini
	scp $(src_aiml)/de_cuon*.sgml $(dest_aiml_cuweb)/
	scp ../cuon_server/src/ai_subs.ini $(CUWEBCONFIGDIR)/	
	scp ../cuon_server/src/ai_aiml.ini $(CUWEBCONFIGDIR)/	
	scp $(src_aiml)/cuon.sgml $(dest_aiml_cuweb)/cuon.sgml

aicuweb:
	make aicuweb_aiml
	scp $(src_aiml)/de_main.sgml $(dest_aiml_cuweb)/main.sgml

install_server:

	make install
	make ai
	if  [ ! -d $(SERVERDIRCONFIG) ] ; then mkdir $(SERVERDIRCONFIG) ; fi 	
	cp $(src_ini) $(SERVERDIRCONFIG)
	if  [ ! -d $(SERVERDIRSHARE) ] ; then mkdir $(SERVERDIRSHARE) ; fi 	
	if  [ ! -d $(ICONDIR) ] ; then mkdir $(ICONDIR) ; fi 	
	if  [ ! -d $(dest_glade) ] ; then mkdir $(dest_glade) ; fi 	
	if  [ ! -d $(dest_report) ] ; then mkdir $(dest_report) ; fi 	
	if  [ ! -d $(SERVERDIRSHARE)/cuon_server ] ; then mkdir $(SERVERDIRSHARE)/cuon_server ; fi 	

	if  [ ! -d $(CUON_VAR) ] ; then mkdir $(CUON_VAR) ; fi 
	if  [ ! -d $(CUON_DOCUMENTS) ] ; then mkdir $(CUON_DOCUMENTS) ; fi 

	if  [ ! -d $(CUON_DOCUMENTS_LISTS) ] ; then mkdir $(CUON_DOCUMENTS_LISTS) ; fi 
	if  [ ! -d $(CUON_DOCUMENTS_LISTS_ADDRESSES) ] ; then mkdir $(CUON_DOCUMENTS_LISTS_ADDRESSES) ; fi 
	if  [ ! -d $(CUON_DOCUMENTS_LISTS_ARTICLES) ] ; then mkdir $(CUON_DOCUMENTS_LISTS_ARTICLES) ; fi 
	if  [ ! -d $(CUON_DOCUMENTS_LISTS_STOCK) ] ; then mkdir $(CUON_DOCUMENTS_LISTS_STOCK) ; fi 

    
    
	if  [ ! -d $(CUON_DOCUMENTS_HIBERNATION) ] ; then mkdir $(CUON_DOCUMENTS_HIBERNATION) ; fi 
	if  [ ! -d $(CUON_DOCUMENTS_HIBERNATION_INCOMING) ] ; then mkdir $(CUON_DOCUMENTS_HIBERNATION_INCOMING) ; fi 


	cp $(src_xmlDefaults) $(SERVERDIRSHARE)
	cp ./GUI/*.glade2 $(dest_glade) 
	find ./cuon  -name "*.glade2" -exec cp {} $(dest_glade) \; 
	find ./cuon  -name "entry_*" -exec cp {}  $(SERVERDIRSHARE) \; 
	find ./GUI/pixmaps  -name "*.xpm" -exec cp {} $(ICONDIR) \; 
	cp -R ../cuon_server/src  $(SERVERDIRSHARE)/cuon_server/
	cp -R ../cuon_server/src/cuonai /etc/init.d
	cp -R ../cuon_server/src/cuonweb /etc/init.d
	cp -R ../cuon_server/src/cuonxmlrpc /etc/init.d
	cp -R ../cuon_server/src/cuonreport /etc/init.d

	 
	msgfmt -o ../cuon_server/src/de.mo ../cuon_server/src/de.po
	if [ ! -d $(I18LDIR_DE) ] ; then mkdir $(I18LDIR_DE) ; fi ; 
	cp ../cuon_server/src/de.mo $(I18LDIR_DE)/cuon_server.mo 

install_zope_cy:
	scp ../cuon_server/src/cuon_zope.py $(zope_extension)
	scp ../cuon_server/src/iCal.py $(zope_extension)

	scp ../cuon_server/zope/*.zexp $(zope_import)

install_zope_cu:

	scp ../cuon_server/src/cuon_zope.py $(zope_extension2)
	scp ../cuon_server/src/iCal.py $(zope_extension2)
    
	scp ../cuon_server/zope/*.zexp $(zope_import2)

install_server_cu:
	sudo make install

	scp  ../cuon_server/src/cuonxmlrpc $(CUWEB)/etc/init.d
	scp  ../cuon_server/src/cuonai $(CUWEB)/etc/init.d
	scp  ../cuon_server/src/cuonweb $(CUWEB)/etc/init.d
	scp  ../cuon_server/src/cuonreport $(CUWEB)/etc/init.d

	#scp -r $(CUON_DOCUMENTS) $(CUWEB)$(CUON_DOCUMENTS)
	scp /etc/cuon/server.ini $(CUWEB)/etc/cuon
	scp ../cuon_server/src/de.mo $(CUWEBLOCALE)/cuon_server.mo
    
	rsync -v -e ssh ../cuon_server/src/*.py $(CUWEBSHARE)/cuon_server/src
	rsync -v -e ssh ../cuon_server/src/cuon/*.py $(CUWEBSHARE)/cuon_server/src/cuon
	rsync -v -e ssh ../cuon_server/src/cuon/Reports/* $(CUWEBSHARE)/cuon_server/src/cuon/Reports
	rsync -v -e ssh ../cuon_server/src/cuon/Reports/XML/* $(CUWEBSHARE)/cuon_server/src/cuon/Reports/XML

install_server_cy:
	sudo make install

	scp  ../cuon_server/src/cuonxmlrpc $(CYWEB)/etc/init.d
	scp  ../cuon_server/src/cuonai $(CYWEB)/etc/init.d
	scp  ../cuon_server/src/cuonweb $(CYWEB)/etc/init.d
	scp  ../cuon_server/src/cuonreport $(CYWEB)/etc/init.d

	#scp -r $(CUON_DOCUMENTS) $(CUWEB)$(CUON_DOCUMENTS)
	scp /etc/cuon/server.ini $(CYWEB)/etc/cuon
	scp ../cuon_server/src/de.mo $(CYWEBLOCALE)/cuon_server.mo
    
	rsync -v -e ssh ../cuon_server/src/*.py $(CYWEBSHARE)/cuon_server/src
	rsync -v -e ssh ../cuon_server/src/cuon/*.py $(CYWEBSHARE)/cuon_server/src/cuon
	rsync -v -e ssh ../cuon_server/src/cuon/Reports/* $(CYWEBSHARE)/cuon_server/src/cuon/Reports
	rsync -v -e ssh ../cuon_server/src/cuon/Reports/XML/* $(CYWEBSHARE)/cuon_server/src/cuon/Reports/XML




