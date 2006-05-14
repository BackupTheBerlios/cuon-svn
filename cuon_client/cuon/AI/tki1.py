import aiml
from ai_main import ai_main

class tki1(ai_main):
    def __init__(self):
        ai_main.__init__(self)
        
    def startAI(self):
        ok = True
        while ok:
            question = raw_input('>')
    
            question = self.checkQ(question)
            
            answer = self.k.respond(question)
            #print 'answer = ', answer
            if answer == "ENDPROGRAM":
                ok = False
                answer = self.k.respond('ENDPROGRAM')
        
            print answer.decode('utf-7').encode('latin-1')


tk1 = tki1()
tk1.startAI()


