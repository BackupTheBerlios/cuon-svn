import xmlrpclib
# connection-Data
#CUON_SERVER="http://84.244.7.139:9673/Cuon"
CUON_SERVER="http://localhost:8080/Cuon"
Username = 'jhamel'
Password = 'barner'
# connect to Server
Server = xmlrpclib.ServerProxy(CUON_SERVER)
# Authorized
sid = Server.src.Databases.py_createSessionID( Username, Password)

print sid
# Set Information for cuon
dicUser={'Name':Username,'SessionID':sid,'userType':'cuon'}

# start show
ok = True
while ok:
    q1 = raw_input('> ')
    if q1 == 'Ciao' or q1 == 'Ende':
        ok = False
    answer =  Server.src.AI.py_getAI(q1.decode('iso-8859-1').encode('utf-7'),dicUser)
    print answer.decode('utf-7').encode('iso-8859-1')
