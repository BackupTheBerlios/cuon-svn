#!/usr/bin/python 
import os, sys
import pygtk
import gtk
import gtk.glade
import gobject
import ConfigParser
import commands

class setup:
    def __init__(self):

        self.IP = None
        self.sPrefix = None
        self.sshPort = None
        self.XmlrpcPort = None
        self.Locale = None
        self.Protocol = None
        self.CuonAdmin = None
        self.store = []
        self.liLocale = ['de','pt','pt_BR', 'nl', 'it', 'lv']
        self.LocalDirs = [ "PrefsFinance" , "E_Mail" , "Calendar" ,  "Analysis" , "Login" , "Garden" , "Leasing" , "WebShop" , "Finances" , "XmlValues" , "Logging" , "Editor" , "Biblio" , "Graves" , "Order" , "Bank" , "TypeDefs" , "Proposal" , "AI" , "Web2" , "Stock" , "Preferences" ,"ReportBuilder",  "Staff" , "Windows" , "Misc" , "User" , "Project" , "Addresses" , "Stats" , "Clients" , "OpenOffice" , "Skeleton" , "DMS" , "locale" , "XMLRPC" , "XML" , "Think" , "starter" , "Articles" , "VTK" , "Help" , "Zip" , "Databases" , "Druids",  "SupportTicket", "Charts" ]

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
            s += 'Locale: de\n'
            s += 'Protocol: http\n'
            
            
            
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
   
        
    def setVars(self):
        ''' Set default Values '''
        
        ##        self.sPrefix = 'root@192.168.17.2:/'
        ##        self.sshPort = '3222' 
        
        self.src_ini = "./cuon_ini1.xml"
        
        self.destClient = './Client'
        self.src_main = "./cuon/*.py cuon.sh Cuon.py CuonConfigWizard.py"
        self.dest_main = self.destClient + "/CUON"
        self.dest_cuon = self.dest_main + "/cuon"
        self.ClientDirLocale = self.destClient + "/locale"
        self.ClientDirUsr = self.destClient + '/usr'
        self.ClientDirUsrShare = self.ClientDirUsr + '/share'
        self.ClientDirUsrShareCuon = self.ClientDirUsrShare + '/cuon'
        self.ClientDirIcon =  self.ClientDirUsrShareCuon
        self.DocDir =  "/usr/share/doc"
        self.CuonDocDir = self.DocDir + "/cuon"
        self.CuonDocDir_DE = self.CuonDocDir + "/DE"
        self.CuonDocDir_EN = self.CuonDocDir + "/EN"
        
        self.src_server = "./cuon_server.py ./cuon_client.py"
        self.dest_server =self.dest_main
         

        self.EXECDIR = "/usr/bin"
        self.INSTALLDIR = "/usr/lib/cuon"
        self.SERVERDIRSHARE =  "/usr/share/cuon"
        self.SERVERCONFIGDIR =  "/etc/cuon"
        self.SERVERLOCALEDIR = "/usr/share/locale/"
        
        self.VERSION_CFG ="./version.cfg"
        
        
        
        self.dest_glade = self.ClientDirUsrShareCuon + "/glade"
        self.dest_report = self.SERVERDIRSHARE + "/report"
        
        
        self.iClientDir = "/opt/Projekte/cuon/iClient"
        
        self.CUON_VAR =  "/var/cuon"
        self.CUON_VAR_WWW =  "/var/cuon_www"
        self.CUON_VAR_WWW_ICAL =  "/var/cuon_www/iCal"
        
        self.CUON_VAR_WWW_AI = self.CUON_VAR_WWW + '/AI'
        self.CUON_VAR_WWW_GLADE = self.CUON_VAR_WWW + '/Glade'
        
        self.CUON_VAR_WWW_ST = self.CUON_VAR_WWW + '/SupportTicket'
        self.CUON_VAR_LB = self.CUON_VAR + '/LoadBalancer'
         
        self.CUON_DOCUMENTS = self.CUON_VAR + "/Documents"
        self.CUON_TMP = self.CUON_VAR + "/tmp"
        self.CUON_DOCUMENTS_LISTS = self.CUON_DOCUMENTS + "/Lists"
        
        self.CUON_DOCUMENTS_LISTS_ADDRESSES = self.CUON_DOCUMENTS_LISTS+ "/Addresses"
        self.CUON_DOCUMENTS_LISTS_ARTICLES = self.CUON_DOCUMENTS_LISTS + "/Articles"
        self.CUON_DOCUMENTS_LISTS_STOCK = self.CUON_DOCUMENTS_LISTS+ "/Stock"
        
        self.CUON_DOCUMENTS_ORDER = self.CUON_DOCUMENTS + "/Order"
        self.CUON_DOCUMENTS_ORDER_INVOICE = self.CUON_DOCUMENTS_ORDER + "/Invoice"
        self.CUON_DOCUMENTS_ORDER_PROPOSAL = self.CUON_DOCUMENTS_ORDER + "/Proposal"
        
        
        self.CUON_DOCUMENTS_HIBERNATION = self.CUON_DOCUMENTS + "/Hibernation"
        self.CUON_DOCUMENTS_HIBERNATION_INCOMING = self.CUON_DOCUMENTS_HIBERNATION + "/Incoming"
        self.CUON_DOCUMENTS_HIBERNATION_PICKUP = self.CUON_DOCUMENTS_HIBERNATION + "/Pickup"
        self.CUON_DOCUMENTS_HIBERNATION_INVOICE = self.CUON_DOCUMENTS_HIBERNATION + "/Invoice"
        self.CUON_DOCUMENTS_GRAVES = self.CUON_DOCUMENTS + "/Graves"
        
        self.CUON_DOCUMENTS_GRAVES_INVOICE = self.CUON_DOCUMENTS_GRAVES + "/Invoice"
        self.CUON_DOCUMENTS_GRAVES_PLANT = self.CUON_DOCUMENTS_GRAVES + "/Plants"

        
        
##        # Please set here your values
##        zope_extension =  root@cyweb://var/lib/zope2.8/instance/default/Extensions
##        zope_import =  root@cyweb://var/lib/zope2.8/instance/default/import
##        
##        zope_extension2 =  root@cuweb://var/lib/zope2.8/instance/default/Extensions
##        zope_import2 =  root@cuweb://var/lib/zope2.8/instance/default/import
        
        
        
        self.liLocaldirs = []
        for sDir in  self.LocalDirs:
            print 'sDir = ',  sDir
            self.liLocaldirs.append(["./cuon/" + sDir + "/*.py",self.dest_cuon + "/" + sDir])
        

        
##        
##        self.src_finances_misc = "./cuon/Finances/*.py"
        self.liLocaldirs.append(["./cuon/Finances/CashAccountBook/*.py", self.dest_cuon + "/Finances"])
        self.liLocaldirs.append(["./cuon/Finances/InvoiceBook/*.py", self.dest_cuon + "/Finances"])
        self.liLocaldirs.append(["./cuon/Finances/Bookkeeping/*.py", self.dest_cuon + "/Finances"])
        self.liLocaldirs.append(["./*.py",self.dest_main + "/"])
        self.liLocaldirs.append(["./Plugins/Dia/*.py", self.dest_cuon + "/Plugins"])
        
##        self.src_finances_ib =  "./cuon/Finances/InvoiceBook/*.py"
##        
##        self.dest_finances = self.dest_cuon + "/Finances"
##        
##        self.src_biblio = "./cuon/Biblio/*.py"
##        self.dest_biblio = self.dest_cuon + "/Biblio"
##        
##        
##        self.src_ai = "./cuon/AI/*.py"
##        self.dest_ai = self.dest_cuon + "/AI"
        
    #    self.src_ai_clients = "./cuon/AI"
    #    self.dest_ai_gtkMiniClient = "./gtkMiniClient"
##        
##        self.src_project = "./cuon/Project/*.py"
##        self.dest_project = self.dest_cuon + "/Project"
##        
##        
##        # Ext. modules with GPL
##        self.src_garden = "./cuon/Garden/*.py"
##        self.dest_garden = self.dest_cuon + "/Garden"
##        
        
        
        #src_cuon =  self.dest_cuon)/*
        #dest_primus_cuon = ~/Projekte/Primus/Py/cuon
        
        
        self.src_xmlDefaults = "./*.xml"
        
    
    def install_local(self):
        
        self.copyFiles()
        
        for sLocale in self.liLocale:
            # create Locale client

            self.executeString("if [ -f cuon_" + sLocale + ".mo ] ; then rm -f cuon_" + sLocale + ".mo ; fi ")
            self.executeString("msgfmt -o cuon_"+ sLocale + ".mo " + sLocale + ".po")  

            #create Locale server 
            
            self.executeString('msgfmt -o ../cuon_server/src/' + sLocale + '.mo ../cuon_server/src/' + sLocale + '.po')
        
        for sLocale in self.liLocale:
            dir = self.ClientDirLocale +"/" + sLocale
            self.executeString("if [ ! -d  " + dir + " ] ; then mkdir " +  dir + "  ; fi ")
            dir2 = dir + "/LC_MESSAGES"
            self.executeString("if [ ! -d  " + dir2 + " ] ; then mkdir " +  dir2 + "  ; fi ")
            
            self.executeString("cp cuon_" + sLocale + ".mo " + dir2 + '/cuon.mo')
        
            self.executeString('cp ../cuon_server/src/'+ sLocale + '.mo ' + dir2 + '/cuon_server.mo')
        
        self.testDir(self.ClientDirUsr)
        self.testDir(self.ClientDirUsrShare)
        self.testDir(self.ClientDirUsrShareCuon)
        
        self.copyLocalValues(self.src_xmlDefaults, self.ClientDirUsrShareCuon)
        self.copyLocalValues(self.src_ini, self.ClientDirUsrShareCuon)
        
        self.copyLocalValues('./GUI/*.glade2', self.dest_glade)
        
        self.copyLocalValues('./GUI/maemo/*.glade2', self.dest_glade)
        self.copyLocalValues('./GUI/800/*.glade2', self.dest_glade)
        self.copyLocalValues('./GUI/alternate*/*.glade2', self.dest_glade)
        self.copyLocalValues('./GUI/web/web_*.glade', self.dest_glade)
        
        self.executeString('find ./cuon  -name "*.glade2" -exec cp  {} ' +  self.dest_glade + ' \;' )
        self.executeString('find ./cuon  -name "web_*.glade" -exec cp  {} ' +  self.dest_glade + ' \;' )
        self.executeString('find ./cuon  -name "entry_*" -exec cp {} ' + self.ClientDirUsrShareCuon + ' \;' )
        self.executeString('find ./GUI/pixmaps  -name "*.svg" -exec cp {} '  + self.ClientDirIcon + ' \;' )

    def install_server(self):
        
        self.install_local()
        scp1 = " -P " + self.sshPort + " "
        scp2 = self.sPrefix 
        self.executeSSH(" mkdir " + self.INSTALLDIR)
        self.executeString("scp -r " + scp1 + ' ' + self.dest_main + "/* " + scp2 + self.INSTALLDIR)
        self.executeString("scp " + scp1 + ' ' + "./cuon.sh " + scp2 + self.EXECDIR )
        
        
        # create tmp dir
        self.executeSSH("if  [ ! -d "  + "/tmp"  + " ] ; then mkdir " + "/tmp" + " ; fi ")
         
        # create server dirs in share
        self.executeSSH('mkdir ' + self.SERVERDIRSHARE)
        self.executeSSH('mkdir ' + self.SERVERDIRSHARE + '/cuon_server')
        self.executeSSH('mkdir ' + self.SERVERDIRSHARE + '/cuon_server/bin')      
        self.executeSSH('mkdir ' + self.SERVERDIRSHARE + '/cuon_server/src')
        self.executeSSH('mkdir ' + self.SERVERDIRSHARE + '/cuon_server/src/cuon')
        self.executeSSH('mkdir ' + self.SERVERDIRSHARE + '/cuon_server/src/cuon/Reports')
        self.executeSSH('mkdir ' + self.SERVERDIRSHARE + '/cuon_server/src/cuon/Reports/XML')
        self.executeSSH('mkdir ' + self.SERVERDIRSHARE + '/cuon_server/AI')
        self.executeSSH('mkdir ' + self.SERVERDIRSHARE + '/cuon_server/AI/AIML')
        
        # create Doc dirs
        self.executeSSH("if  [ ! -d "  + self.DocDir  + " ] ; then mkdir " + self.DocDir + " ; fi ")
        self.executeSSH("if  [ ! -d "  + self.CuonDocDir  + " ] ; then mkdir " + self.CuonDocDir + " ; fi " )
        
        self.executeSSH("if  [ ! -d "  + self.CuonDocDir_DE  + " ] ; then mkdir " + self.CuonDocDir_DE + " ; fi ")
        self.executeSSH("if  [ ! -d "  + self.CuonDocDir_EN  + " ] ; then mkdir " + self.CuonDocDir_EN + " ; fi " )
         
        # copy version.cfg
        self.executeSCP(" " + self.VERSION_CFG , self.SERVERDIRSHARE + "/cuon_server/")
        # copy other
        self.executeSCP(" ../cuon_server/src/*.py", self.SERVERDIRSHARE + "/cuon_server/src")
        self.executeSCP(" ../cuon_server/bin/*", self.SERVERDIRSHARE + "/cuon_server/bin")
        self.executeSSH("chmod u+x " + self.SERVERDIRSHARE + "/cuon_server/bin/*" )
        self.executeSCP(" ../cuon_server/src/cuon/*.py", self.SERVERDIRSHARE + "/cuon_server/src/cuon")
        self.executeSCP(" ../cuon_server/src/cuon/Reports/*",  self.SERVERDIRSHARE + "/cuon_server/src/cuon/Reports")
        self.executeSCP(" ../cuon_server/src/cuon/Reports/XML/*", self.SERVERDIRSHARE + "/cuon_server/src/cuon/Reports/XML")
        
        # cp Docs
        self.executeSCP(" ../www/Cuon/cuon.docbook", self.CuonDocDir_DE)
        self.executeSCP(" -r ../www/Cuon/images",  self.CuonDocDir_DE)
        
        
        self.executeSCP(" ../www/en_Cuon/en_cuon.docbook", self.CuonDocDir_EN)
        self.executeSCP(" -r ../www/en_Cuon/images",  self.CuonDocDir_EN)
        
        
        #create the documents from dockbook docbook
        self.executeSSH(" cd " + self.CuonDocDir_DE + " ;  recode -d utf-8..h4  cuon.docbook ; docbook2html cuon.docbook && docbook2pdf cuon.docbook ;")

        self.executeSSH(" cd " + self.CuonDocDir_EN + " ;   docbook2html en_cuon.docbook && docbook2pdf en_cuon.docbook ;")

        # cp cuon.docbook de_cuon.docbook ; recode -d utf-8..h4 de_cuon.docbook ; docbook2html de_cuon.docbook && docbook2pdf de_cuon.docbook

        # AI 
        ai_module = ['main.sgml','cuon.sgml','cuon_article.sgml','cuon_address.sgml','cuon_misc.sgml']
        self.executeSCP(" cuon/AI/AIML/*.sgml", self.SERVERDIRSHARE + "/cuon_server/AI/AIML")
        self.executeSCP(" cuon/AI/AIML/" + self.Locale + "_startup.aiml", self.SERVERDIRSHARE + "/cuon_server/AI/AIML/startup.aiml")
        self.executeSCP(" cuon/AI/AIML/" + self.Locale + "_startup.ini", self.SERVERDIRSHARE + "/cuon_server/AI/AIML/startup.ini")
        for aim in ai_module:
            self.executeSCP(" cuon/AI/AIML/" + self.Locale + '_' + aim, self.SERVERDIRSHARE + "/cuon_server/AI/AIML/" + aim)
        # create web and iCal
        self.executeSSH(" if  [ ! -d " + self.CUON_VAR_WWW + " ] ; then mkdir " + self.CUON_VAR_WWW + " ; fi ") 
        self.executeSSH(" if  [ ! -d " + self.CUON_VAR_WWW_ICAL + " ] ; then mkdir " + self.CUON_VAR_WWW_ICAL + " ; fi ")   
        self.executeSSH(" if  [ ! -d " + self.CUON_VAR_WWW_AI + " ] ; then mkdir " + self.CUON_VAR_WWW_AI + " ; fi ")   
        self.executeSSH(" if  [ ! -d " + self.CUON_VAR_WWW_ST + " ] ; then mkdir " + self.CUON_VAR_WWW_ST + " ; fi ")   
        self.executeSSH(" if  [ ! -d " + self.CUON_VAR_LB + " ] ; then mkdir " + self.CUON_VAR_LB + " ; fi ")   
        self.executeSSH(" if  [ ! -d " + self.CUON_VAR_WWW_GLADE + " ] ; then mkdir " + self.CUON_VAR_WWW_GLADE + " ; fi ")   
        self.executeSCP(" -r ../cuon_server/WEB/html/*",  self.CUON_VAR_WWW  )
        self.executeSCP(" -r " +self.dest_glade + "/*",  self.CUON_VAR_WWW_GLADE  )
        self.executeSCP(" -r ../cuon_server/AI/*",  self.CUON_VAR_WWW_AI  )
        self.executeSCP(" -r ../cuon_server/SupportTicket/*",  self.CUON_VAR_WWW_ST )
        self.executeSCP(" -r ../cuon_server/LoadBalancer/*",  self.CUON_VAR_LB )
        
        
        # create and copy reports and doc
        self.executeSSH(" if  [ ! -d " + self.CUON_VAR + " ] ; then mkdir " + self.CUON_VAR + " ; fi ") 
        self.executeSSH(" if  [ ! -d " + self.CUON_TMP + " ] ; then mkdir " + self.CUON_TMP + " ; fi ") 
        
        self.executeSSH(" if  [ ! -d " + self.CUON_DOCUMENTS + " ] ; then mkdir " + self.CUON_DOCUMENTS + " ; fi ") 
        self.executeSSH(" if  [ ! -d " + self.CUON_DOCUMENTS_LISTS  + " ] ; then mkdir " + self.CUON_DOCUMENTS_LISTS + " ; fi ")    
        self.executeSSH(" if  [ ! -d " + self.CUON_DOCUMENTS_LISTS_ADDRESSES  + " ] ; then mkdir " + self.CUON_DOCUMENTS_LISTS_ADDRESSES + " ; fi ")    
        self.executeSSH(" if  [ ! -d " + self.CUON_DOCUMENTS_LISTS_ARTICLES  + " ] ; then mkdir " + self.CUON_DOCUMENTS_LISTS_ARTICLES + " ; fi ")  
        self.executeSSH(" if  [ ! -d " + self.CUON_DOCUMENTS_LISTS_STOCK  + " ] ; then mkdir " + self.CUON_DOCUMENTS_LISTS_STOCK + " ; fi ")    


        self.executeSSH(" if  [ ! -d " + self.CUON_DOCUMENTS_ORDER + " ] ; then mkdir " + self.CUON_DOCUMENTS_ORDER + " ; fi ") 
        self.executeSSH(" if  [ ! -d " + self.CUON_DOCUMENTS_ORDER_INVOICE + " ] ; then mkdir " + self.CUON_DOCUMENTS_ORDER_INVOICE + " ; fi ") 
        self.executeSSH(" if  [ ! -d " + self.CUON_DOCUMENTS_ORDER_PROPOSAL + " ] ; then mkdir " + self.CUON_DOCUMENTS_ORDER_PROPOSAL + " ; fi ") 


        self.executeSSH(" if  [ ! -d " + self.CUON_DOCUMENTS_HIBERNATION + " ] ; then mkdir " + self.CUON_DOCUMENTS_HIBERNATION + " ; fi ") 
        self.executeSSH(" if  [ ! -d " + self.CUON_DOCUMENTS_HIBERNATION_INCOMING + " ] ; then mkdir " + self.CUON_DOCUMENTS_HIBERNATION_INCOMING + " ; fi ")   
        self.executeSSH(" if  [ ! -d " + self.CUON_DOCUMENTS_HIBERNATION_PICKUP + " ] ; then mkdir " + self.CUON_DOCUMENTS_HIBERNATION_PICKUP + " ; fi ")   
        self.executeSSH(" if  [ ! -d " + self.CUON_DOCUMENTS_HIBERNATION_INVOICE + " ] ; then mkdir " + self.CUON_DOCUMENTS_HIBERNATION_INVOICE + " ; fi ") 

        
        self.executeSSH(" if  [ ! -d " + self.CUON_DOCUMENTS_GRAVES+ " ] ; then mkdir " + self.CUON_DOCUMENTS_GRAVES + " ; fi ") 
        self.executeSSH(" if  [ ! -d " + self.CUON_DOCUMENTS_GRAVES_INVOICE+ " ] ; then mkdir " + self.CUON_DOCUMENTS_GRAVES_INVOICE + " ; fi ")  
        self.executeSSH(" if  [ ! -d " + self.CUON_DOCUMENTS_GRAVES_PLANT+ " ] ; then mkdir " + self.CUON_DOCUMENTS_GRAVES_PLANT + " ; fi ")  
        
        # copy config-files to configdir or configdir/examples
        self.executeSSH("if  [ ! -d " + self.SERVERCONFIGDIR + " ] ; then mkdir " + self.SERVERCONFIGDIR + " ; fi ")
        self.executeSSH("if  [ ! -d " + self.SERVERCONFIGDIR + "/examples ] ; then mkdir " + self.SERVERCONFIGDIR + "/examples ; fi ")
        self.executeSSH("if  [ ! -d " + self.SERVERCONFIGDIR + "/sql ] ; then mkdir " + self.SERVERCONFIGDIR + "/sql ; fi ")
        
        # copy all files to example
        self.executeSCP('../cuon_server/examples/*', self.SERVERCONFIGDIR + "/examples ")
        self.executeSCP('../cuon_server/src/cuon*', self.SERVERCONFIGDIR + "/examples ")
       
       
        # startscripts in /etc/init.d
        
        
        self.executeSCP(" scp ../cuon_server/src/cuond.sh ","/usr/bin/")
        self.executeSCP(" scp ../cuon_server/src/cuond ","/etc/init.d")
        
##        self.executeSCP(" scp ../cuon_server/src/cuonxmlrpc ","/etc/init.d")
##        self.executeSCP(" scp ../cuon_server/src/cuonai " , "/etc/init.d")
##        self.executeSCP(" scp ../cuon_server/src/cuonreport " , "/etc/init.d")
##        self.executeSCP(" scp ../cuon_server/src/cuonweb " , "/etc/init.d")
##        self.executeSCP(" scp ../cuon_server/src/cuonweb2 " , "/etc/init.d")
##        
        self.executeSSH("if  [ ! -f /etc/init.d/cuonxmlrpc ] ; then cp " 
            + self.SERVERCONFIGDIR + "/examples/cuonxmlrpc /etc/init.d  ; fi ")
        
    
        self.executeSSH("if  [ ! -f /etc/init.d/cuonai ] ; then cp " 
            + self.SERVERCONFIGDIR + "/examples/cuonai /etc/init.d  ; fi ")
        
        self.executeSSH("if  [ ! -f /etc/init.d/cuonreport ] ; then cp " 
            + self.SERVERCONFIGDIR + "/examples/cuonreport /etc/init.d  ; fi ")
        
        self.executeSSH("if  [ ! -f /etc/init.d/cuonweb ] ; then cp " 
            + self.SERVERCONFIGDIR + "/examples/cuonweb /etc/init.d  ; fi ")
        
        self.executeSSH("if  [ ! -f /etc/init.d/cuonweb2 ] ; then cp " 
            + self.SERVERCONFIGDIR + "/examples/cuonweb2 /etc/init.d  ; fi ")
            
        self.executeSSH("if  [ ! -f /etc/init.d/cuonweb3 ] ; then cp " 
            + self.SERVERCONFIGDIR + "/examples/cuonweb3 /etc/init.d  ; fi ")
            
        self.executeSSH("if  [ ! -f /etc/init.d/cuonjabber ] ; then cp " 
            + self.SERVERCONFIGDIR + "/examples/cuonjabber /etc/init.d  ; fi ")
        
        # make executable
        self.executeSSH(" chmod a+x " + self.SERVERDIRSHARE + "/cuon_server/src/server_*")
        
        self.executeSSH(" chmod u+x /etc/init.d/cuon*")
        self.executeSSH(" chmod u+x /usr/bin/cuond*")
        
        # aktivierung setzen
        #self.executeSSH(" update-rc.d cuond defaults")
        #self.executeSSH(" update-rc.d cuonxmlrpc defaults")
        #self.executeSSH(" update-rc.d cuonweb defaults")
        #self.executeSSH(" update-rc.d cuonreport defaults")
        #self.executeSSH(" update-rc.d cuonai defaults")
        #self.executeSSH(" update-rc.d cuonweb2 defaults")
        #self.executeSSH(" update-rc.d cuonweb3 defaults")
        #self.executeSSH(" update-rc.d cuonjabber defaults")
       
        
        # Then check the files 
        #server.ini
        self.executeSSH("if  [ ! -f " + self.SERVERCONFIGDIR + "/server.ini ] ; then cp " 
            + self.SERVERCONFIGDIR + "/examples/server.ini " + self.SERVERCONFIGDIR + " ; fi ")
        #sql.ini
        self.executeSSH("if  [ ! -f " + self.SERVERCONFIGDIR + "/sql.ini ] ; then cp " 
            + self.SERVERCONFIGDIR + "/examples/sql.ini " + self.SERVERCONFIGDIR + " ; fi ")
        #clients.ini
        self.executeSSH("if  [ ! -f " + self.SERVERCONFIGDIR + "/clients.ini ] ; then cp " 
            + self.SERVERCONFIGDIR + "/examples/clients.ini " + self.SERVERCONFIGDIR + " ; fi ")
        
        #menus.cfg
        self.executeSSH("if  [ ! -f " + self.SERVERCONFIGDIR + "/menus.cfg ] ; then cp " 
            + self.SERVERCONFIGDIR + "/examples/menus.cfg " + self.SERVERCONFIGDIR + " ; fi ")
        
        #grants.xml 
        
        
        #cfg files for sql
        
        # all right to user cuon_all
        self.executeSCP('GroupRightsCuon.cfg', self.SERVERCONFIGDIR + "/sql")
        self.executeSSH("if  [ ! -f " + self.SERVERCONFIGDIR + "/sql/GroupRightsOther.cfg ] ; then cp " 
            + self.SERVERCONFIGDIR + "/examples/GroupRightsOther.cfg " + self.SERVERCONFIGDIR + "/sql ;  fi ")
            
        self.executeSSH("if  [ ! -f " + self.SERVERCONFIGDIR + "/sql/UserGroups.cfg ] ; then cp " 
            + self.SERVERCONFIGDIR + "/examples/UserGroups.cfg " + self.SERVERCONFIGDIR + "/sql ;  fi ")
        # sql.xml
        # copy trigger to etc/cuon/sql
        liFunctions = ['sql.xml',  'basics.sql', 'order.sql', 'address.sql', 'garden.sql', 'graves.sql', 'articles.sql', 'it.sql', 'invoice.sql', 'databases.sql']
        for oneFile in liFunctions:
            self.executeSCP(oneFile, self.SERVERCONFIGDIR + "/sql")
        
        
        # user.cfg
        self.executeSSH("if  [ ! -f " + self.SERVERCONFIGDIR + "/user.cfg ] ; then cp " 
            + self.SERVERCONFIGDIR + "/examples/user.cfg " + self.SERVERCONFIGDIR + " ; fi ")
        
        
        #self.src_aiml = "./cuon/AI/AIML"
        #self.dest_aiml = self.SERVERDIRSHARE + "/AI/AIML"
        
        
        
        self.restartServer()
        
    def QuestionMsg(self, sText):
        # gtk
        ok = False
        print 'QuestionMsg'
        dialog = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_QUESTION,gtk.BUTTONS_YES_NO, sText);
        response = dialog.run ();
        dialog.destroy ();
        print 'Response', response
        if response == gtk.RESPONSE_YES:
            ok = True
        return ok    
    def restartServer(self):
        # restart the server
        
        if self.QuestionMsg('Restart the Load Balancing System ( cuond ) ?' ):
            self.executeSSH(" nohup /etc/init.d/cuond restart &")
        else:
            
            if self.QuestionMsg('Restart the normal Cuon Server ?' ):
                self.executeSSH(" nohup /etc/init.d/cuonxmlrpc restart &")
                self.executeSSH(" nohup /etc/init.d/cuonreport restart &")
                self.executeSSH(" nohup /etc/init.d/cuonweb restart &")
                self.executeSSH(" nohup /etc/init.d/cuonweb2 restart &")
                self.executeSSH(" nohup /etc/init.d/cuonweb3 restart &")
                self.executeSSH(" nohup /etc/init.d/cuonai restart &")
                self.executeSSH(" nohup /etc/init.d/cuonjabber restart &")
                
        
        
        # start some sql-things
#        try:
#            fsql = open('./sql_orders.sql', 'w')
#            
#            s =  "update orderbook set process_status = 500 where process_status is null  ; \n"
#            
#            fsql.write(s)
#            fsql.close()
#            
#        except:
#            print 'error in sql orders'
#           
#        self.executeSCP("./sql_orders.sql", "/root")
#        self.executeSSH('psql -U' + self.CuonAdmin + ' cuon < /root/sql_orders.sql ')
        
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
        s1 = "ssh " +  ssh + ' "'+  s +'"'
        print s1
        self.setTv1(s1)
        return self.executeString( s1  )
        
    def executeSCP(self, src, dest):
        scp1 = " -P " + self.sshPort + " "
        scp2 = self.sPrefix 
        s1 = "scp " +scp1 + src + ' ' + scp2 +  dest
        print s1
        self.setTv1(s1)

        return self.executeString(s1 )
    
  
    def copyFiles(self):
        
        ssh = "-p -P " + self.sshPort + self.sPrefix 
        
       
        self.removePrefix(self.src_main, self.dest_cuon)
        
        print "now create local dirs"
        self.testDir(self.destClient)
        self.testDir(self.dest_main)
        
        self.testDir(self.ClientDirLocale)
        self.testDir(self.dest_cuon)
        
        for key in self.liLocaldirs:
            print 'Key = ',  key
            self.copyLocalValues(key[0], key[1])
        
        self.copyLocalValues(self.VERSION_CFG, self.dest_main)
        
        self.touchFile(self.dest_cuon, '__init__.py')
        self.copyLocalValues('cuonObjects',self.dest_main)
        
##        self.copyLocalValues(self.src_server, self.dest_server)
##        self.copyLocalValues(self.src_user,self.dest_user)
##        self.copyLocalValues(self.src_addresses,self.dest_addresses)
##        self.copyLocalValues(self.src_articles,self.dest_articles)
##        self.copyLocalValues(self.src_login,self.dest_login)
##        self.copyLocalValues(self.src_clients,self.dest_clients)
##        self.copyLocalValues(self.src_order,self.dest_order)
##        self.copyLocalValues(self.src_databases,self.dest_databases)
##        self.copyLocalValues(self.src_xml,self.dest_xml)
##        self.copyLocalValues(self.src_xmlrpc,self.dest_xmlrpc)
##        self.copyLocalValues(self.src_typedefs,self.dest_typedefs)
##        self.copyLocalValues(self.src_windows,self.dest_windows)
##        self.copyLocalValues(self.src_log,self.dest_log)
##        self.copyLocalValues(self.src_oo,self.dest_oo)
##        self.copyLocalValues(self.src_misc,self.dest_misc)
##        self.copyLocalValues(self.src_preferences,self.dest_preferences)
##        self.copyLocalValues(self.src_preferences_xml,self.dest_preferences_xml)
##        self.copyLocalValues(self.src_stock,self.dest_stock)
##        self.copyLocalValues(self.src_email,self.dest_email)
##        self.copyLocalValues(self.src_dms,self.dest_dms)
##        self.copyLocalValues(self.src_help,self.dest_help)
##        self.copyLocalValues(self.src_staff,self.dest_staff)
##        self.copyLocalValues(self.src_vtk,self.dest_vtk)
##        self.copyLocalValues(self.src_prefs_finance,self.dest_prefs_finance)
##        self.copyLocalValues(self.src_finances_cab,self.dest_finances)
##        self.copyLocalValues(self.src_finances_ib,self.dest_finances)
##        self.copyLocalValues(self.src_finances_misc,self.dest_finances)
##        self.copyLocalValues(self.src_biblio,self.dest_biblio)
##        self.copyLocalValues(self.src_ai,self.dest_ai)
##        self.copyLocalValues(self.src_project,self.dest_project)
##        #self.copyLocalValues(self.src_,self.dest_)
##        
##        
##        # ext. Modules with GPL
##        self.copyLocalValues(self.src_garden,self.dest_garden)
##        

        
        
    def executeString(self, s):
        print s
        self.setTv1(s)
        #liResult = os.system(s)
        liResult = commands.getstatusoutput(s)
        print 'execute String',  liResult
        self.setTv1(`liResult`)
        return liResult
        
    def testDir(self, destdir):
        s = "if [ ! -d " +  destdir  + " ] ; then mkdir " +  destdir  + " ; fi "
        self.executeString(s)
        
    def removePrefix(self, src,dest):
        self.dest = dest.replace(self.sPrefix,'')
        self.src = src.replace(self.sPrefix,'')
  
    def copyLocalValues(self, src, dest):
        self.removePrefix(src, dest)
        
        self.testDir(dest)
        
        
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
        if not value:
            value = " "
        return value   
     
    def setDefaultServer(self,sNewSect = None):
        existDefaultSection = None
        firstSection = None
        cbe = -1
        z = -1
        liName = []
        self.store = []
        if self.ConfigStatus:
            for sect in self.cpParser.sections():
                
                print 'sect = ', sect
                z += 1  
                if z == -1:
                    firstSection = sect
                    
                self.store.append(sect)
                if self.getConfigOption(sect, 'default') == 'True':
                    existDefaultSection =  sect
                    cbe = z
        
        if existDefaultSection:
            sSect = existDefaultSection
        else:
            sSect = firstSection
        
        print 'store = ', `self.store`
        for i in self.store:
            print 'listentry = ', i
            
        
        for i in range(len(self.store)):
            s = 'radiobutton'+`i+1`
            print 's = ', s
            print 'store = ', self.store[i]
            self.getWidget(s).set_label(self.store[i])
            self.getWidget(s).show()

        
        #s += 'Description: Install on local host\n'
        #    s += 'IP: 127.0.0.1\n'
        #    s += 'SSH_PORT: 22\n'
        #    s += 'XMLRPC_PORT: 7080\n'
        #    s += 'Default: True\n'
            
        #self.getWidget('cbeName').set_text_column(cbe)
        if sNewSect:
                sSect = sNewSect
                
        self.setActiveRadiobutton(sSect)
        self.setOptions2Data(sSect)
        
        #self.setData2Widget(sSect)
    
    def setData2Widget(self, sSect):
        self.getWidget('eName').set_text(sSect)
       
        self.getWidget('eHostIP').set_text(self.getConfigOption(sSect,'IP'))
        self.getWidget('ePortSSH').set_text(self.getConfigOption(sSect,'SSH_PORT'))
        self.getWidget('ePortXmlrpc').set_text(self.getConfigOption(sSect,'XMLRPC_PORT'))
        self.getWidget('eDescription').set_text(self.getConfigOption(sSect,'Description'))
        self.getWidget('eCuonadmin').set_text(self.getConfigOption(sSect,'Cuonadmin'))
        if self.getConfigOption(sSect,'Default') == 'True':
            self.getWidget('rbTrue').set_active(True)
        else:
            self.getWidget('rbFalse').set_active(True)
        try:    
            self.getWidget('eLocale').set_text(self.getConfigOption(sSect,'Locale'))
        except:
            pass
        try:    
            self.getWidget('eProtocol').set_text(self.getConfigOption(sSect,'Protocol'))
        except:
            pass
            
        
            
        self.setOptions2Data(sSect)
        self.on_bCheckVersion_clicked(None)
        
    def setActiveRadiobutton(self, sSect):
        for i in range(len(self.store)):
            s = 'radiobutton'+`i+1`
            if self.getWidget(s).get_label() == sSect:
                self.getWidget(s).set_active(True)
                self.setData2Widget(sSect)
                
    def on_radiobutton_toggled(self, event):
        for i in range(len(self.store)):
            s = 'radiobutton'+`i+1`
            if self.getWidget(s).get_active():
                print 'active = ', s
                s2 = self.getWidget(s).get_label()
                print 's2', s2
                self.setActiveRadiobutton(s2)
            
    
        
    def setOptions2Data(self, sSect):
        self.sPrefix = 'root@' + self.getConfigOption(sSect,'IP') + ':/'
        self.IP = self.getConfigOption(sSect,'IP')
        self.sshPort = self.getConfigOption(sSect,'SSH_PORT')
        self.XmlrpcPort = self.getConfigOption(sSect,'XMLRPC_PORT')
        self.Locale = self.getConfigOption(sSect,'Locale')
        self.Protocol = self.getConfigOption(sSect,'Protocol')
        self.CuonAdmin = self.getConfigOption(sSect,'Cuonadmin')
        print 'install sPrefix = ', self.sPrefix
        print 'install sshPort = ', self.sshPort
        print 'install XmlrpcPort = ', self.XmlrpcPort
        
    def on_bCheckVersion_clicked(self,  event):
        liResult1 = self.executeSSH("grep ^Major " + self.SERVERDIRSHARE + "/cuon_server/version.cfg" )
        liResult2 = self.executeSSH("grep ^Minor " + self.SERVERDIRSHARE + "/cuon_server/version.cfg" )
        liResult3 = self.executeSSH("grep ^Rev " + self.SERVERDIRSHARE + "/cuon_server/version.cfg" )
        sVersion = liResult1[1][7:].strip()  + '.'  + liResult2[1][7:].strip()  + '-' +  liResult3[1][5:].strip() 
        print sVersion
        liResult1 = commands.getstatusoutput("grep ^Major " + self.dest_main + "/version.cfg")
        #print "this Major ",  liResult1
        liResult2 = commands.getstatusoutput("grep ^Minor " + self.dest_main + "/version.cfg")
        liResult3 = commands.getstatusoutput("grep ^Rev " + self.dest_main + "/version.cfg")
        sThisVersion = liResult1[1][7:].strip()  + '.'  + liResult2[1][7:].strip()  + '-' +  liResult3[1][5:].strip() 
        try:
            if not sVersion[0].isdigit():
                sVersion = ' '
            self.getWidget("eThisVersion").set_text(sThisVersion)
            self.getWidget("eServerVersion").set_text(sVersion)
        except Exception,  params:
            print Exception,  params

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
                print key
                nameFuncMap[key] = getattr(self, key)
                
            if  nameFuncMap:
                print  "Funcmap = ",  nameFuncMap              
                self.xml.signal_autoconnect(nameFuncMap)

            self.xmlAutoconnect = True
    def getWidget(self, sName):
        return self.xml.get_widget(sName )

    def clearTv1(self):
        tv1 = self.getWidget('tv1')
        buffer = tv1.get_buffer()
        buffer.set_text('\n')
        tv1.set_buffer(buffer)
        tv1.show()
        while gtk.events_pending():
            gtk.main_iteration(False)
    def setTv1(self, sText):
        sText += '\n'
        
        tv1 = self.getWidget('tv1')
        buffer = tv1.get_buffer()
        #a1 = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), 1)
        
        buffer.insert(buffer.get_end_iter(),sText , len(sText) ) 
        
        tv1.set_buffer(buffer)
        buffer = tv1.get_buffer()
        tv1.scroll_to_iter(buffer.get_end_iter(),0.0,False,0.0,0.0)
        tv1.show()
        while gtk.events_pending():
            gtk.main_iteration(False)
            
    def saveData2File(self):
        print 'save Data to config-File'
        existSect = False
##        nSect = self.getWidget('cbeName').get_text_column()
##        sSect = self.getWidget('cbeName').get_model()[nSect][0]
##        for sect in self.cpParser.sections():
##            if sSect == sect:
##                print 'Data found in Config-file'
##                existSect = True
##        print 'nSect = ', nSect
##        print 'sSect = ', sSect
##        self.getWidget('cbeName').get_model()[nSect][0]
##        print 'model = ', self.getWidget('cbeName').get_model()
##        for i in self.getWidget('cbeName').get_model():
##            print 'i = ', i 
##        #self.getWidget('cbeName').get_model()[1][0]
        
        sSect = self.getWidget('eName').get_text()
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
        self.cpParser.set(sSect,'Cuonadmin', self.getWidget('eCuonadmin').get_text())
        if self.getWidget('rbTrue').get_active():
            self.cpParser.set(sSect,'Default','True')
        else:
            self.cpParser.set(sSect,'Default','False')
            
        self.cpParser.set(sSect,'Locale', self.getWidget('eLocale').get_text())
        self.cpParser.set(sSect,'Protocol', self.getWidget('eProtocol').get_text())
            
        print 'Save File'
        
        f = open(self.sFile,'w')
        self.cpParser.write(f)
        f.close()
        self.setDefaultServer(sSect)
        
        
    def on_database_tools1_activate(self, event):
        s1 = "cd " + self.dest_main + " ; python  cuon_server.py " + self.Protocol + '://' +  self.IP +':' + self.XmlrpcPort + ' ' + self.sshPort + " " + self.IP + " NO  " + self.dest_main + "/cuon"
        
        print 's1 = ', s1
        os.system(s1)
        print os.system('pwd')
        
    def on_create_client1_activate(self, event):
        print 'create client'
        s1 = "python cuon_client.py " + self.Protocol + '://' +  self.IP +':' + self.XmlrpcPort + ' ' + self.Locale
        
        print 's1 = ', s1
        os.system(s1)
        print os.system('pwd')

    def on_quit1_activate(self, event):
        self.gtk_main_quit()
        
        
        
    # Buttons
    
    # save Data
    def on_bSaveData_clicked(self, event):
        
        self.saveData2File()
        
    def on_bRestart_clicked(self, event):
        # restart cuon server 
        print "restart Server"
        self.restartServer()
    
    # Install 
    def on_bOK_clicked(self, event):
        # save ini
        self.saveData2File()
        
        # start install
        self.clearTv1()
        
        self.install_server()
        
        self.setTv1('###################### END SETUP #################')
        
    def on_bTest_clicked(self,  event):
        print "test"
    
    def on_bCancel_clicked(self, event):  
        sys.exit(0)
        
    def gtk_main_quit(self):
        #os.system('rm users.cfg')
        
        gtk.main_quit()

    def main(self, args):
        self.setVars()
        print "start_glade"
        self.xml = gtk.glade.XML('GUI/setup.glade2')
        self.setXmlAutoconnect()
        print "end_glade"
        self.setDefaultServer()
        gtk.main()

print "starting"
stu = setup()
print "main starting"
stu.main(None)
