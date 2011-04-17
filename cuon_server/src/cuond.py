import cuon.basics
import sys
import shlex, subprocess
import time


baseSettings = cuon.basics.basics()



iXMLRPC = baseSettings.XMLRPC_INSTANCES 
iREPORT = baseSettings.REPORT_INSTANCES 

iPort = baseSettings.ADD_PORT_INSTANCES
lb_path = '/var/cuon/LoadBalancer'



    
    
def startAll(addPort):
    startXmlRpc(addPort)
    startReport(addPort)
    startIcal(addPort)
    startAI(addPort)
    startJabber(addPort)
    startWeb2(addPort)
    startWeb3(addPort)
    
def startXmlRpc(addPort):
    shellcommand = shlex.split("nohup python /usr/share/cuon/cuon_server/src/server_xmlrpc.py " +`addPort` + " >> /var/log/cuon_allserver.log &" )
    liStatus = subprocess.Popen(shellcommand)
    print shellcommand, liStatus
    
def startReport(addPort):
    shellcommand = shlex.split("nohup python /usr/share/cuon/cuon_server/src/server_report.py " +`addPort` + " >> /var/log/cuon_allserver.log &" )
    liStatus = subprocess.Popen(shellcommand)
    print shellcommand, liStatus
    
def startIcal(addPort):
    shellcommand = shlex.split("nohup python /usr/share/cuon/cuon_server/src/server_ical.py " +`addPort` + " >> /var/log/cuon_allserver.log &" )
    liStatus = subprocess.Popen(shellcommand)
    print shellcommand, liStatus
   
def startAI(addPort):
    shellcommand = shlex.split("nohup python /usr/share/cuon/cuon_server/src/server_ai.py " +`addPort` + " >> /var/log/cuon_allserver.log &" )
    liStatus = subprocess.Popen(shellcommand)
    print shellcommand, liStatus
   
def startJabber(addPort):
    shellcommand = shlex.split("nohup python /usr/share/cuon/cuon_server/src/server_jabber.py " +`addPort` + " >> /var/log/cuon_allserver.log &" )
    liStatus = subprocess.Popen(shellcommand)
    print shellcommand, liStatus

def startWeb2(addPort):
    shellcommand = shlex.split("nohup python /usr/share/cuon/cuon_server/src/server_web2.py " +`addPort` + " >> /var/log/cuon_allserver.log &" )
    liStatus = subprocess.Popen(shellcommand)
    print shellcommand, liStatus

def startWeb3(addPort):
    shellcommand = shlex.split("nohup python /usr/share/cuon/cuon_server/src/server_web3.py " +`addPort` + " >> /var/log/cuon_allserver.log &" )
    liStatus = subprocess.Popen(shellcommand)
    print shellcommand, liStatus
     
def writeLog(sMessage):
    f = open('/var/log/cuond_processes.log','a')
    s = '%04d-%02d-%02d  %02d.%02d.%02d    ' % time.localtime()[0:6]
    f.write(s + sMessage + '\n' )
    f.close()

def writeConfigfile():
#    print 'write'
#    <config>
#    <service name="cuon">
#        <listen ip="192.168.17.12:7680"/>
#        <group name="servers" scheduler="roundr" enable="true">
#          <host name="server1" ip="192.168.17.12:7580"/>
#          <host name="server2" ip="192.168.17.12:7600"/>
#        </group>
#     </service>
#   
# 	<admin>
# 	   <web listen="localhost:7001" enable="true"/>
#	<ssh listen="localhost:7002" enable="true"/>
# 	   <user name="admin" password="..xpoEyRReGzk" access="full"/>
#		
# 	 </admin>
# </config>

    print 'write'
    s = '<config> ' 
    
    if baseSettings.XMLRPC_ALLOW_HTTP:
        s += '\n\t<service name="cuon_http">\n\t\t<listen ip="' + baseSettings.XMLRPC_HOST + ':7000"/>\n\t\t\t<group name="server_xmlrpc" scheduler="roundr" enable="true">'
        for i in range (0, iXMLRPC):
            addPort = iPort *i
        
            s += '\n\t\t\t\t<host name="server_http_' + `i` + '" ip="' +  baseSettings.XMLRPC_HOST + ':' + `baseSettings.XMLRPC_HTTP_PORT + addPort`+ '"/>'
        
        s+= '\n\t\t\t</group>\n\t\t</service>'

    if baseSettings.XMLRPC_PROTO.upper() == 'HTTPS':

        s += '\n\t<service name="cuon_https">\n\t\t<listen ip="' + baseSettings.XMLRPC_HOST + ':7500"/>\n\t\t\t<group name="server_xmlrpc_https" scheduler="roundr" enable="true">'
        for i in range (0, iXMLRPC):
            addPort = iPort *i
            s += '\n\t\t\t\t<host name="server_https_' + `i` + '" ip="' +  baseSettings.XMLRPC_HOST + ':' + `baseSettings.XMLRPC_HTTPS_PORT + addPort`+ '"/>'
            
        s+= '\n\t\t\t</group>\n\t\t</service>'       
   
    s += '\n\n\t<service name="cuon_report">\n\t\t<listen ip="localhost:' + `baseSettings.REPORT_PORT ` + '"/>\n\t\t\t<group name="server_report" scheduler="roundr" enable="true">'
    for i in range (1, iREPORT +1):
        addPort = iPort *i
    
        s += '\n\t\t\t\t<host name="server_report_' + `i` + '" ip="' +  baseSettings.XMLRPC_HOST + ':' + `baseSettings.REPORT_PORT + addPort` + '"/>'
    
    s+= '\n\t\t\t</group>\n\t\t</service>'
    
    s+= '	\n\t<admin>  \n\t\t<web listen="localhost:7001" enable="true"/> \n\t\t<ssh listen="localhost:7002" enable="true"/> \n\t\t<user name="admin" password="' + baseSettings.INSTANCES_PASSWORD + '" access="full"/>\n\t</admin> \n</config>'
    
        
    f = open(lb_path + '/etc/config.xml', 'w')
    f.write(s)
    f.close()

def startLoadBalancing():
    # kill old process
    killProcess("/bin/txlb.tac")
    writeConfigfile()
    shellcommand = 'cd ' + lb_path + ' ; twistd -noy ./bin/txlb.tac ' 
    oStatus = subprocess.Popen(shellcommand, stdout=subprocess.PIPE,   shell = True)
    #oStatus.wait()
def killAll():
    liProcesses = ['server_ai', 'server_ical',  'server_jabber',  'server_report',  'server_web2',  'server_web3',  'server_xmlrpc', '/bin/txlb.tac']
    for sName in liProcesses:
        killProcess(sName)
        
    
def killProcess(sName):
    
    #shellcommand = shlex.split('ps ax | grep server | grep -v grep | sed  -e "s/^[[:space:]]*//g" | cut -d" " -f 1 ')
    shellcommand = 'ps ax | grep ' + sName + ' | grep -v grep | sed  -e "s/^[[:space:]]*//g" | cut -d" " -f 1 '
    oStatus = subprocess.Popen(shellcommand, stdout=subprocess.PIPE,   shell = True)
    oStatus.wait()
    poll = oStatus.poll()
    values = oStatus.stdout.read()
        
    print 'values, poll = ', values,  poll
    if poll == 0:
        liValues = values.split()
        print 'li values = ',  liValues
        for iKill in liValues:
            shellcommand = shlex.split('kill ' + iKill)
            oStatus = subprocess.Popen(shellcommand)
            oStatus.wait()
            poll = oStatus.poll()
            if poll != 0:
                shellcommand = shlex.split('kill -9' + iKill)
                oStatus = subprocess.Popen(shellcommand)
                oStatus.wait()
            
try:    
    sStart = sys.argv[1].upper()
except:
    sStart = 'START'
writeLog(sStart)
writeLog('xmlrpc + report = ' + `iXMLRPC` +',  ' + `iREPORT`)

if sStart in ['START', 'RESTART', 'RELOAD']:
    if sStart == 'RESTART':
        killAll()
        
    print 'iXMLRPC,  iREPORT = ',  iXMLRPC,  iREPORT
    if iXMLRPC > 1 or iREPORT > 1:
        print 'load balance starting'
        for i in range(0, iXMLRPC):
            startXmlRpc(iPort *i)
        for i in range(1, iREPORT + 1 ):    
            startReport(iPort *i)
        
        addPort = 0
        
        startIcal(addPort)
        startAI(addPort)
        startJabber(addPort)
        startWeb2(addPort)
        startWeb3(addPort)
        startLoadBalancing()
    else:
        
        startAll(0)
        
elif sStart == 'STOP':
    
    killAll()
    
    
   
            
            
        
