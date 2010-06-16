#!/usr/bin/python 
import os, sys
import pygtk
import gtk
import gtk.glade
import gobject
import ConfigParser



class CuonConfigWizard:
    
    def  __init__(self):
        self.xml = None
        self.xmlAutoconnect = False
        self.cpParser = ConfigParser.ConfigParser()
        self.sFile = 'cuon.ini'
        self.Description = None
        self.WorkingDir= None
        self.Host = None
        self.Port = None 
        self.Proto = None
        self.Type = None
        self.Locale = None
        self.Debug = None
        self.AlternateGui = None
        try:
            f = open(self.sFile, 'rw')
        except:
            print 'create new ini file'
            f = open(self.sFile,'w')
            s = '[Client]\n'
            s += 'DESCRIPTION: Cuon Client Configuration\n'
            s += 'WORKINGDIR: /home/user/cuon\n'
            s += 'HOST: localhost\n'
            s += 'PORT: 7080\n'
            s += 'PROTOCOL: http\n'
            s += 'TYPE: client\n'
            s += 'LOCALE: /locale\n'
            s += 'DEBUG: NO\n'
            s += 'ALTERNATEGUI:NO'
            
            
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
   
    def on_save_activate(self, event):
        self.readDataFromGUI()
        self.saveData()
        self.close()
        
    def on_quit1_activate(self, event):
        self.close()    
   
    def getConfigOption(self, section, option):
        value = None
        if self.cpParser.has_option(section,option):
            value = self.cpParser.get(section, option)
            print 'getConfigOption', section + ', ' + option + ' = ' + value
        if not value:
            value = " "
        return value   
        
    def on_bOK_clicked(self, event):
        self.on_save_activate(event)
        
    def on_bCancel_clicked(self, event):
        self.on_quit1_activate(event)
        
    def close(self):
        gtk.main_quit()
        
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
        
        
    def setDataFromFile(self):
       
        sSect = 'Client'
        
        self.Description = self.getConfigOption(sSect,'DESCRIPTION')
        self.WorkingDir = self.getConfigOption(sSect,'WORKINGDIR')
        self.Host =  self.getConfigOption(sSect,'HOST')
        self.Port =  self.getConfigOption(sSect,'PORT')
        self.Proto =  self.getConfigOption(sSect,'PROTOCOL')
        self.Type =  self.getConfigOption(sSect,'TYPE')
        self.Locale =  self.getConfigOption(sSect,'LOCALE')
        self.Debug =  self.getConfigOption(sSect,'DEBUG')
        self.AlternateGui =  self.getConfigOption(sSect,'ALTERNATEGUI')
        
        print 'Des = ',  self.Description
        self.getWidget('eDescription').set_text(self.Description)
        self.getWidget('eDir').set_text(self.WorkingDir)
        self.getWidget('eHost').set_text(self.Host)
        self.getWidget('ePort').set_text(self.Port)
        self.getWidget('eProtocol').set_text(self.Proto)
        self.getWidget('eType').set_text(self.Type)
        self.getWidget('eLocale').set_text(self.Locale)
        self.getWidget('eDebug').set_text(self.Debug)
        self.getWidget('eAlternateGUI').set_text(self.AlternateGui)
        
        
    def readDataFromGUI(self):
        self.Description = self.getWidget('eDescription').get_text()
        self.WorkingDir = self.getWidget('eDir').get_text()
        self.Host =self.getWidget('eHost').get_text()
        self.Port = self.getWidget('ePort').get_text()
        self.Proto = self.getWidget('eProtocol').get_text()
        self.Type = self.getWidget('eType').get_text()
        self.Locale = self.getWidget('eLocale').get_text()
        self.Debug = self.getWidget('eDebug').get_text()
        self.AlternateGui = self.getWidget('eAlternateGUI').get_text()
        
        
    def saveData(self):
        sSect = 'Client'
        self.cpParser.set(sSect,'DESCRIPTION',self.Description)
        self.cpParser.set(sSect,'WORKINGDIR',self.WorkingDir)
        self.cpParser.set(sSect,'HOST',self.Host)
        self.cpParser.set(sSect,'PORT',self.Port)
        self.cpParser.set(sSect,'PROTOCOL',self.Proto)
        self.cpParser.set(sSect,'TYPE',self.Type)
        self.cpParser.set(sSect,'LOCALE',self.Locale)
        self.cpParser.set(sSect,'DEBUG',self.Debug.upper())
        self.cpParser.set(sSect,'AlternateGui',self.AlternateGui)
        
              
        f = open(self.sFile,'w')
        self.cpParser.write(f)
        f.close()            
                          
                          
                          
    def main(self, args):
        
        print "start_glade"
        try:
            self.xml = gtk.glade.XML('GUI/cuon_config_wizard.glade2')
        except: 
            self.xml = gtk.glade.XML('../glade_cuon_config_wizard.xml')
        self.setXmlAutoconnect()
        print "end_glade"
        self.setDataFromFile()
        gtk.main()

print "starting"
ccf = CuonConfigWizard()
print "main starting"
ccf.main(None)
        
    
