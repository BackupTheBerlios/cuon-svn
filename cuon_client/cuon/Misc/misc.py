

import os
import sys
import time
import random	


class misc:
    def __init__(self):
        pass


    def getRandomFilename(self, sPrefix='.tmp'):
    
    
        s = ''
        
        n = random.randint(0,1000000000)
        for i in range(13):
            ok = 1
            while ok:
                r = random.randint(65,122)
                if r < 91 or r > 96:
                    ok = 0
                    s = s + chr(r)
                    
        s = s + `n` + sPrefix

        return s
