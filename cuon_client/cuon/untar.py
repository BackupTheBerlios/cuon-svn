import sys
import tarfile
tar = tarfile.open('newclient','r:bz2')
for tarinfo in tar:
    tar.extract(tarinfo)
tar.close()
