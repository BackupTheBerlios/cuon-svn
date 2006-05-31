#! /usr/bin/python

try:
    import aiml
except:
    print 'No AI'
import SimpleXMLRPCServer
from ai_main import ai_main


class ai(ai_main):

    def __init__(self):
        ai_main.__init__(self)


    def getAnswer(self, question):
        answer = 'NO DATA FOUND'
        question = self.checkQ(question)
        f = open('/root/cuonai.log','a')
        f.write(`question` + '\n')
        try:
            answer = self.k.respond(question.decode('utf-7'))
            f.write(`answer` + '\n')

        except:
            pass
        
        f.write('\n')
        f.close()
        #return  answer.decode('latin-1').encode('utf-7')
        return  answer
    



oAI = ai()

if __name__ == '__main__':
    server = SimpleXMLRPCServer.SimpleXMLRPCServer(("localhost",8765))
    server.register_instance(oAI)


#Go into the main listener loop
print "Listening on port 8765"
server.serve_forever()
