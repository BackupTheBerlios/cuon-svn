import os
import pygtk
import gtk
import gtk.glade
import gobject
import ConfigParser


class setup:
    def __init__(self):
        
        self.xml = None
        self.xmlAutoconnect = False
        self.cpParser = ConfigParser.ConfigParser()
        self.sFile = 'cuon_setup.ini'
        try:
            f = open(self.sFile, 'rw')
        except:
            print 'create new ini file'
            f = open(self.sFile,'w')
            s = '[local]\n'
            s += 'Description: Install on local host\n'
            s += 'IP: 127.0.0.1\n'
            s += 'SSH_PORT: 22\n'
            s += 'XMLRPC_PORT: 7080\n'
            s += 'Default: True\n'
            
            f.write(s)
            f.close()
            f = open(self.sFile,'rw')
            
        if f:    
            self.cpParser.readfp(f)
            self.ConfigStatus = True
            f.close()
        else:
            print 'Configuration-Error'
            self.ConfigStatus = False
   
        
    def start(self):
        self.sPrefix = 'root@192.168.17.2:/'
        self.sshPort = '3222' 
    


        self.EXECDIR = "/usr/bin"
        self.INSTALLDIR = "/usr/lib/cuon"
        self.ICONDIR =  "/usr/lib/cuon/icons"
        self.SERVERDIRSHARE =  "/usr/share/cuon"
        self.SERVERCONFIGDIR =  "/etc/cuon"
        self.SERVERLOCALEDIR = "/usr/share/locale/"
##        
##        self.CUWEBSHARE = root@cuweb://usr/share/cuon
##        self.CUWEB = root@cuweb:/
##        self.CUWEBEXECDIR = self.CUWEB)/usr/bin
##        self.CUWEBLOCALEXECDIR = self.CUWEB)/usr/local/bin
##        self.CUWEBCONFIGDIR = self.CUWEB)/etc/cuon
##        self.CUWEBLOCALE = self.CUWEB)/usr/share/locale/de/LC_MESSAGES
##        
##        CYWEBSHARE = root@cyweb://usr/share/cuon
##        CYWEB = root@cyweb:/
##        CYWEBEXECDIR = self.CYWEB)/usr/bin
##        CYWEBLOCALEXECDIR = self.CYWEB)/usr/local/bin
##        CYWEBCONFIGDIR = self.CYWEB)/etc/cuon
##        CYWEBLOCALE = self.CYWEB)/usr/share/locale/de/LC_MESSAGES
##        
##        
##        SERVERDIRCONFIG = /etc/cuon
        self.VERSION_CFG ="./version.cfg"
        
        self.I18LDIR_DE=self.SERVERLOCALEDIR + "de/LC_MESSAGES"
        self.I18LDIR_PT=self.SERVERLOCALEDIR + "pt/LC_MESSAGES"
        self.I18LDIR_PT_BR=self.SERVERLOCALEDIR + "pt_BR/LC_MESSAGES"
        
        self.src_locale_de = "./cuon_de.mo"
        self.src_locale_pt = "./cuon_pt.mo"
        self.src_locale_pt_BR = "./cuon_pt_BR.mo"
        
        self.dest_glade = self.SERVERDIRSHARE + "/glade"
        self.dest_report = self.SERVERDIRSHARE + "/report"
        
        
        self.iClientDir = "/opt/Projekte/cuon/iClient"
        self.iClientDirLocale = self.iClientDir + "/locale/de/LC_MESSAGES"
        
        self.CUON_VAR =  "/var/cuon"
        self.CUON_DOCUMENTS = self.CUON_VAR + "/Documents"
        
        self.CUON_DOCUMENTS_LISTS = self.CUON_DOCUMENTS + "/Lists"
        
        self.CUON_DOCUMENTS_LISTS_ADDRESSES = self.CUON_DOCUMENTS_LISTS+ "/Addresses"
        self.CUON_DOCUMENTS_LISTS_ARTICLES = self.CUON_DOCUMENTS_LISTS + "/Articles"
        self.CUON_DOCUMENTS_LISTS_STOCK = self.CUON_DOCUMENTS_LISTS+ "/Stock"
        
        
        
        self.CUON_DOCUMENTS_HIBERNATION = self.CUON_DOCUMENTS + "/Hibernation"
        self.CUON_DOCUMENTS_HIBERNATION_INCOMING = self.CUON_DOCUMENTS_HIBERNATION + "/Incoming"
        
        
        
##        # Please set here your values
##        zope_extension =  root@cyweb://var/lib/zope2.8/instance/default/Extensions
##        zope_import =  root@cyweb://var/lib/zope2.8/instance/default/import
##        
##        zope_extension2 =  root@cuweb://var/lib/zope2.8/instance/default/Extensions
##        zope_import2 =  root@cuweb://var/lib/zope2.8/instance/default/import
        
        self.src_ini="./cuon_ini1.xml"
        
        
        self.src_main = "./cuon/*.py cuon.sh Cuon.py"
        self.dest_main = "./CUON"
        self.dest_cuon = self.dest_main + "/cuon"
        
        
        self.src_server = "./cuon_server.py"
        self.dest_server =self.dest_cuon
         
        
        self.src_typedefs = "./cuon/TypeDefs/*.py"
        self.dest_typedefs = self.dest_cuon + "/TypeDefs"
        
        
        self.src_login = "./cuon/Login/*.py"
        self.dest_login = self.dest_cuon + "/Login"
        
        self.src_user = "./cuon/User/*.py"
        self.dest_user = self.dest_cuon + "/User"
        
        
        self.src_misc = "./cuon/Misc/*.py"
        self.dest_misc = self.dest_cuon + "/Misc"
        
        self.src_addresses = "./cuon/Addresses/*.py"
        self.dest_addresses = self.dest_cuon + "/Addresses"
        
        
        self.src_articles = "./cuon/Articles/*.py"
        self.dest_articles = self.dest_cuon + "/Articles"
        
        
        self.src_clients = "./cuon/Clients/*.py"
        self.dest_clients = self.dest_cuon + "/Clients"
        
        self.src_order = "./cuon/Order/*.py"
        self.dest_order = self.dest_cuon + "/Order"
        
        
        self.src_databases = "./cuon/Databases/*.py"
        self.dest_databases = self.dest_cuon + "/Databases"
        
        
        
        self.src_xml = "./cuon/XML/*.py"
        self.dest_xml = self.dest_cuon + "/XML"
        
        self.src_xmlrpc = "./cuon/XMLRPC/*.py"
        self.dest_xmlrpc = self.dest_cuon + "/XMLRPC"
        
        
        self.src_windows = "./cuon/Windows/*.py"
        self.dest_windows = self.dest_cuon + "/Windows"
        
        
        self.src_log = "./cuon/Logging/*.py"
        self.dest_log = self.dest_cuon + "/Logging"
        
        self.src_help = "./cuon/Help/*.py"
        self.dest_help = self.dest_cuon + "/Help"
        
        
        
        self.src_oo = "./cuon/OpenOffice/*.py"
        self.dest_oo = self.dest_cuon + "/OpenOffice"
        
        
        
        
        self.src_preferences = "./cuon/Preferences/*.py" 
        self.dest_preferences = self.dest_cuon + "/Preferences"
        
        self.src_preferences_xml = "./cuon/Preferences/XML/*.py"
        self.dest_preferences_xml = self.dest_cuon + "/Preferences/XML"
        
        
        
        self.src_stock = "./cuon/Stock/*.py"
        self.dest_stock = self.dest_cuon + "/Stock"
        
        self.src_email = "./cuon/E_Mail/*.py"
        self.dest_email = self.dest_cuon + "/E_Mail"
        
        
        self.src_dms = "./cuon/DMS/*.py"
        self.dest_dms = self.dest_cuon + "/DMS"
        
        self.src_staff = "./cuon/Staff/*.py"
        self.dest_staff = self.dest_cuon + "/Staff"
        
        
        self.src_vtk = "./cuon/VTK/*.py"
        self.dest_vtk = self.dest_cuon + "/VTK"
        
        self.src_prefs_finance = "./cuon/PrefsFinance/*.py" 
        self.dest_prefs_finance = self.dest_cuon + "/PrefsFinance"
        
        self.src_webshop = "./cuon/WebShop/*.py"
        self.dest_webshop = self.dest_cuon + "/WebShop"
        
        
        self.src_finances_misc = "./cuon/Finances/*.py"
        self.src_finances_cab = "./cuon/Finances/CashAccountBook/*.py" 
        self.src_finances_ib =  "./cuon/Finances/InvoiceBook/*.py"
        
        self.dest_finances = self.dest_cuon + "/Finances"
        
        self.src_biblio = "./cuon/Biblio/*.py"
        self.dest_biblio = self.dest_cuon + "/Biblio"
        
        
        self.src_ai = "./cuon/AI/*.py"
        self.dest_ai = self.dest_cuon + "/AI"
        self.src_aiml = "./cuon/AI/AIML"
        self.dest_aiml = self.SERVERDIRSHARE + "/AI/AIML"
        self.src_ai_clients = "./cuon/AI"
        self.dest_ai_gtkMiniClient = "./gtkMiniClient"
        
        self.src_project = "./cuon/Project/*.py"
        self.dest_project = self.dest_cuon + "/Project"
        
        
        # Ext. modules with GPL
        self.src_garden = "./cuon/Garden/*.py"
        self.dest_garden = self.dest_cuon + "/Garden"
        
        
        
        #src_cuon =  self.dest_cuon)/*
        #dest_primus_cuon = ~/Projekte/Primus/Py/cuon
        
        
        self.src_xmlDefaults = "./*.xml"
        
    
    def install_all(self):
        
        self.copyFiles()
        
    def install_server(self):
        self.executeSSH('mkdir ' + self.SERVERCONFIGDIR)
        self.install_all()
        scp1 = " -P " + self.sshPort + " "
        scp2 = self.sPrefix 
        self.executeSSH(" mkdir " + self.INSTALLDIR)
        self.executeString("scp -r " + scp1 + ' ' + self.dest_main + "/* " + scp2 + self.INSTALLDIR)
        self.executeString("scp " + scp1 + ' ' + "./cuon.sh " + scp2 + self.EXECDIR )
        self.executeString("if [ -f cuon_de.mo ] ; then rm -f cuon_de.mo ; fi ")
        self.executeString("msgfmt -o cuon_de.mo de.po")  
        self.executeString("if [ -f cuon_pt.mo ] ; then rm -f cuon_pt.mo ; fi ")
        self.executeString("msgfmt -o cuon_pt.mo pt.po")
        self.executeString("if [ -f cuon_pt_BR.mo ] ; then rm -f cuon_pt_BR.mo ; fi ")
        self.executeString("msgfmt -o cuon_pt_BR.mo pt_BR.po")
        
        self.executeSSH("if [ ! -d  " + self.I18LDIR_DE + " ; then mkdir " +  self.I18LDIR_DE + " ; fi ")
        self.executeSCP(self.src_locale_de, self.I18LDIR_DE )
        self.executeSSH("mv " + self.I18LDIR_DE + "/cuon_de.mo "+  self.I18LDIR_DE +"/cuon.mo")
        
        self.executeSSH("if [ ! -d  " + self.I18LDIR_PT + " ; then mkdir " +  self.I18LDIR_PT + " ; fi ")
        self.executeSCP(self.src_locale_pt, self.I18LDIR_PT )
        self.executeSSH("mv " + self.I18LDIR_PT + "/cuon_pt.mo "+  self.I18LDIR_PT +"/cuon.mo")
        
        self.executeSSH("if [ ! -d  " + self.I18LDIR_PT_BR + " ; then mkdir " +  self.I18LDIR_PT_BR + " ; fi ")
        self.executeSCP(self.src_locale_pt, self.I18LDIR_PT_BR )
        self.executeSSH("mv " + self.I18LDIR_PT_BR + "/cuon_pt_BR.mo "+  self.I18LDIR_PT_BR +"/cuon.mo")
  
        self.executeSSH('mkdir ' + self.SERVERDIRSHARE)
        self.executeSSH('mkdir ' + self.SERVERDIRSHARE + '/cuon_server')
        self.executeSSH('mkdir ' + self.SERVERDIRSHARE + '/cuon_server/src')
        self.executeSSH('mkdir ' + self.SERVERDIRSHARE + '/cuon_server/src/cuon')
        self.executeSSH('mkdir ' + self.SERVERDIRSHARE + '/cuon_server/src/cuon/Reports')
        self.executeSSH('mkdir ' + self.SERVERDIRSHARE + '/cuon_server/src/cuon/Reports/XML')
        
        self.executeSCP(" ../cuon_server/src/*.py", self.SERVERDIRSHARE + "/cuon_server/src")
        self.executeSCP(" ../cuon_server/src/cuon/*.py", self.SERVERDIRSHARE + "/cuon_server/src/cuon")
        self.executeSCP(" ../cuon_server/src/cuon/Reports/*",  self.SERVERDIRSHARE + "/cuon_server/src/cuon/Reports")
        self.executeSCP(" ../cuon_server/src/cuon/Reports/XML/*", self.SERVERDIRSHARE + "/cuon_server/src/cuon/Reports/XML")
        self.executeSSH(" if  [ ! -d " + self.ICONDIR + " ] ; then mkdir " + self.ICONDIR + " ; fi ")	
        self.executeSSH(" if  [ ! -d " + self.dest_glade + " ] ; then mkdir " + self.dest_glade + " ; fi ")	

        self.executeSSH(" if  [ ! -d " + self.CUON_VAR + " ] ; then mkdir " + self.CUON_VAR + " ; fi ")	
        self.executeSSH(" if  [ ! -d " + self.CUON_DOCUMENTS + " ] ; then mkdir " + self.CUON_DOCUMENTS + " ; fi ")	
        self.executeSSH(" if  [ ! -d " + self.CUON_DOCUMENTS_LISTS  + " ] ; then mkdir " + self.CUON_DOCUMENTS_LISTS + " ; fi ")	
        self.executeSSH(" if  [ ! -d " + self.CUON_DOCUMENTS_LISTS_ADDRESSES  + " ] ; then mkdir " + self.CUON_DOCUMENTS_LISTS_ADDRESSES + " ; fi ")	
        self.executeSSH(" if  [ ! -d " + self.CUON_DOCUMENTS_LISTS_ARTICLES  + " ] ; then mkdir " + self.CUON_DOCUMENTS_LISTS_ARTICLES + " ; fi ")	
        self.executeSSH(" if  [ ! -d " + self.CUON_DOCUMENTS_LISTS_STOCK  + " ] ; then mkdir " + self.CUON_DOCUMENTS_LISTS_STOCK + " ; fi ")	

        self.executeSSH(" if  [ ! -d " + self.CUON_DOCUMENTS_HIBERNATION + " ] ; then mkdir " + self.CUON_DOCUMENTS_HIBERNATION + " ; fi ")	
        self.executeSSH(" if  [ ! -d " + self.CUON_DOCUMENTS_HIBERNATION_INCOMING + " ] ; then mkdir " + self.CUON_DOCUMENTS_HIBERNATION_INCOMING + " ; fi ")	

        self.executeSCP(self.src_xmlDefaults, self.SERVERDIRSHARE)
        self.executeSCP('.GUI/*.glade2', self.dest_glade)
        self.executeString('find ./cuon  -name "*.glade2" -exec scp ' + scp1 + ' {} ' +scp2 + self.dest_glade + ' \;' )
        self.executeString('find ./cuon  -name "entry_*" -exec scp ' + scp1 + ' {} ' +scp2 + self.SERVERDIRSHARE + ' \;' )
        self.executeString('find ./GUI/pixmaps  -name "*.xpm" -exec scp ' + scp1 + ' {} ' +scp2 + self.ICONDIR + ' \;' )


##	cp $(src_xmlDefaults) $(SERVERDIRSHARE)
##	cp ./GUI/*.glade2 $(dest_glade) 
##	find ./cuon  -name "*.glade2" -exec cp {} $(dest_glade) \; 
##	find ./cuon  -name "entry_*" -exec cp {}  $(SERVERDIRSHARE) \; 
##	find ./GUI/pixmaps  -name "*.xpm" -exec cp {} $(ICONDIR) \; 
##	cp -R ../cuon_server/src  $(SERVERDIRSHARE)/cuon_server/
##	cp -R ../cuon_server/src/cuonai /etc/init.d
##	cp -R ../cuon_server/src/cuonweb /etc/init.d
##	cp -R ../cuon_server/src/cuonxmlrpc /etc/init.d
##	cp -R ../cuon_server/src/cuonreport /etc/init.d
##
##	 
##	msgfmt -o ../cuon_server/src/de.mo ../cuon_server/src/de.po
##	if [ ! -d $(I18LDIR_DE) ] ; then mkdir $(I18LDIR_DE) ; fi ; 
##	cp ../cuon_server/src/de.mo $(I18LDIR_DE)/cuon_server.mo 

        
    def install_client(self):
        print 'client'
##        cp ./createUserDirs.sh self.INSTALLDIR)
##        
##        chmod a+x self.INSTALLDIR + "/createUserDirs.sh
##        if  [ ! -d self.INSTALLDIR + "/icons ] ; then mkdir self.INSTALLDIR + "/icons ; fi 
##    
##        if  [ ! -d self.ICONDIR + "/ ] ; then mkdir self.ICONDIR) ; fi 	
##    
##        find ./GUI/pixmaps  -name "*.xpm" -exec cp {} self.ICONDIR) \; 


    def executeSSH(self, s):
        ssh = " -p" + self.sshPort + " " + self.sPrefix[0:len(self.sPrefix)-2] 
        print ssh
        self.executeString("ssh " +  ssh +' ' + s )
        
    def executeSCP(self, src, dest):
        scp1 = " -P " + self.sshPort + " "
        scp2 = self.sPrefix 
        
        self.executeString("scp " +scp1 + src + ' ' + scp2 +  dest )
    
  
    def copyFiles(self):
        
        ssh = "-p -P " + self.sshPort + self.sPrefix 
        
        print "first copy files to /etc/init.d"
        
        self.executeString("scp ../cuon_server/src/cuonxmlrpc " + ssh +  "/etc/init.d")
        self.executeString("scp ../cuon_server/src/cuonai " + ssh +  "/etc/init.d")
        self.executeString("scp ../cuon_server/src/cuonreport " + ssh +  "/etc/init.d")
        self.executeString("scp ../cuon_server/src/cuonweb " + ssh +  "/etc/init.d")
        
        print "now create local dirs"
        self.copyLocalValues(self.src_main, self.dest_main)
        self.copyLocalValues(self.VERSION_CFG, self.dest_main)
        self.removePrefix(self.src_main, self.dest_cuon)
        self.testDir()
        self.touchFile(self.dest_cuon, '__init__.py')
        self.copyLocalValues(self.src_server, self.dest_server)
        self.copyLocalValues(self.src_user,self.dest_user)
        self.copyLocalValues(self.src_addresses,self.dest_addresses)
        self.copyLocalValues(self.src_articles,self.dest_articles)
        self.copyLocalValues(self.src_login,self.dest_login)
        self.copyLocalValues(self.src_clients,self.dest_clients)
        self.copyLocalValues(self.src_order,self.dest_order)
        self.copyLocalValues(self.src_databases,self.dest_databases)
        self.copyLocalValues(self.src_xml,self.dest_xml)
        self.copyLocalValues(self.src_xmlrpc,self.dest_xmlrpc)
        self.copyLocalValues(self.src_typedefs,self.dest_typedefs)
        self.copyLocalValues(self.src_windows,self.dest_windows)
        self.copyLocalValues(self.src_log,self.dest_log)
        self.copyLocalValues(self.src_oo,self.dest_oo)
        self.copyLocalValues(self.src_misc,self.dest_misc)
        self.copyLocalValues(self.src_preferences,self.dest_preferences)
        self.copyLocalValues(self.src_preferences_xml,self.dest_preferences_xml)
        self.copyLocalValues(self.src_stock,self.dest_stock)
        self.copyLocalValues(self.src_email,self.dest_email)
        self.copyLocalValues(self.src_dms,self.dest_dms)
        self.copyLocalValues(self.src_help,self.dest_help)
        self.copyLocalValues(self.src_staff,self.dest_staff)
        self.copyLocalValues(self.src_vtk,self.dest_vtk)
        self.copyLocalValues(self.src_prefs_finance,self.dest_prefs_finance)
        self.copyLocalValues(self.src_finances_cab,self.dest_finances)
        self.copyLocalValues(self.src_finances_ib,self.dest_finances)
        self.copyLocalValues(self.src_finances_misc,self.dest_finances)
        self.copyLocalValues(self.src_biblio,self.dest_biblio)
        self.copyLocalValues(self.src_ai,self.dest_ai)
        self.copyLocalValues(self.src_project,self.dest_project)
        #self.copyLocalValues(self.src_,self.dest_)
        
        
        # ext. Modules with GPL
        self.copyLocalValues(self.src_garden,self.dest_garden)
        


    def executeString(self, s):
        print s
        liResult = os.system(s)
        self.setTv1(`liResult`)
        
        
    def testDir(self):
        s = "if [ ! -d " +  self.dest  + " ] ; then mkdir " +  self.dest  + " ; fi "
        self.executeString(s)
    def removePrefix(self, src,dest):
        self.dest = dest.replace(self.sPrefix,'')
        self.src = src.replace(self.sPrefix,'')
  
    def copyLocalValues(self, src, dest):
        self.removePrefix(src, dest)
        
        self.testDir()
        
        
        s = " cp " + self.src + " " + self.dest
        self.executeString(s)
        
    def touchFile(self, dest, sFile):
        dest = dest.replace(self.sPrefix,'')
        self.executeString("if [ ! -e " + dest + "/__init__.py ] ; then touch "+ dest + "/__init__.py ; fi")
    
    def getConfigOption(self, section, option):
        value = None
        if self.cpParser.has_option(section,option):
            value = self.cpParser.get(section, option)
            print 'getConfigOption', section + ', ' + option + ' = ' + value
        return value   
     
    def setDefaultServer(self):
        existDefaultSection = None
        firstSection = None
        cbe = -1
        z = -1
        liName = []
        store = gtk.ListStore(gobject.TYPE_STRING)
        if self.ConfigStatus:
            for sect in self.cpParser.sections():
                print sect
                z += 1  
                if z == -1:
                    firstSection = sect
                    
                store.append([sect])
                if self.getConfigOption(sect, 'default') == 'True':
                    existDefaultSection =  sect
                    cbe = z
        
        if existDefaultSection:
            sSect = existDefaultSection
        else:
            sSect = firstSection
            

        self.getWidget('cbeName').set_model(store)
        print 'cbe', cbe
        
        #s += 'Description: Install on local host\n'
        #    s += 'IP: 127.0.0.1\n'
        #    s += 'SSH_PORT: 22\n'
        #    s += 'XMLRPC_PORT: 7080\n'
        #    s += 'Default: True\n'
            
        self.getWidget('cbeName').set_text_column(cbe)
        self.setData2Widget(sSect)
    
    
    def setData2Widget(self, sSect):
        
        self.getWidget('eHostIP').set_text(self.getConfigOption(sSect,'IP'))
        self.getWidget('ePortSSH').set_text(self.getConfigOption(sSect,'SSH_PORT'))
        self.getWidget('ePortXmlrpc').set_text(self.getConfigOption(sSect,'XMLRPC_PORT'))
        self.getWidget('eDescription').set_text(self.getConfigOption(sSect,'Description'))
        if self.getConfigOption(sSect,'Default') == 'True':
            self.getWidget('rbTrue').set_active(True)
        else:
            self.getWidget('rbFalse').set_active(True)
            


    def on_bOK_clicked(self, event):
        # save ini
        print 'bOK', event
        existSect = False
        nSect = self.getWidget('cbeName').get_text_column()
        sSect = self.getWidget('cbeName').get_model()[nSect][0]
        for sect in self.cpParser.sections():
            if sSect == sect:
                print 'Data found in Config-file'
                existSect = True
                
        
        if not existSect:
            self.cpParser.add_section(sSect)
        
        self.cpParser.set(sSect,'IP', self.getWidget('eHostIP').get_text())
        self.cpParser.set(sSect,'SSH_PORT', self.getWidget('ePortSSH').get_text())
        self.cpParser.set(sSect,'XMLRPC_PORT', self.getWidget('ePortXmlrpc').get_text())
        self.cpParser.set(sSect,'Description', self.getWidget('eDescription').get_text())
        if self.getWidget('rbTrue').get_active():
            self.cpParser.set(sSect,'Default','True')
        else:
            self.cpParser.set(sSect,'Default','False')
        print 'Save File'
        
        f = open(self.sFile,'w')
        self.cpParser.write(f)
        f.close()
        
        # start install
        
        
        
        
    def on_cbeName_editing_done(self, event):
        print event
        print 'line = ', event.get_model()[nSect][0]
        
    
    def on_cbeName_changed(self, event):
        print event
        nSect = self.getWidget('cbeName').get_text_column()
        print 'nSect = ', nSect
        print event.get_model()
        for sL in event.get_model():
            print sL[0]
            
            
        for sect in self.cpParser.sections():
            if event.get_model()[nSect][0] == sect:
                print 'Data found', sect
                self.setData2Widget(sect)
        
    
        
    def setXmlAutoconnect(self):
        if self.xmlAutoconnect:
            pass
        else:
            nameFuncMap = {}
            for key in dir(self.__class__):
                nameFuncMap[key] = getattr(self, key)
                
            if  nameFuncMap:
                               
                self.xml.signal_autoconnect(nameFuncMap)

            self.xmlAutoconnect = True
    def getWidget(self, sName):
        return self.xml.get_widget(sName )

    def setTv1(self, sText):
        tv1 = self.getWidget('tv1')
        buffer = self.tv1.get_buffer()
        a1 = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), 1)
        
        a1.insert(a1.get_end_iter(),sText , len(sText) ) 
        
        self.a1.set_buffer(buffer)
        buffer = a1.get_buffer()
        a1.scroll_to_iter(buffer.get_end_iter(),0.0,False,0.0,0.0)
        
    def main(self, args):
        self.xml = gtk.glade.XML('GUI/setup.glade2')
        self.setXmlAutoconnect()
        self.setDefaultServer()
        gtk.main()
stu = setup()
stu.main(None)
#stu.start()
#stu.install_server()
