
import os
import sys
sys.path.append(os.environ['CUON_PATH'])
import uno
import letter

aLetter = letter.letter()
aLetter.createAddress(sys.argv[1])



