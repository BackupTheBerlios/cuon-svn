import sys
from types import *
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import string
class dataEntry:

    def __init__(self):
        self.nameOfEntry="EMPTY"
        self.typeOfEntry="EMPTY"
        


    def setName(self,s):
        self.nameOfEntry = s

    def getName(self):
        return self.nameOfEntry



    def setType(self,s):
        self.typeOfEntry = s

    def getType(self):
        return self.typeOfEntry


    def setSizeOfEntry(self,s):
        self.sizeOfEntryOfEntry = s

    def getSizeOfEntry(self):
        return self.sizeOfEntryOfEntry


    def setVerifyType(self,s):
        self.verifyType = s

    def getVerifyType(self):
        return self.verifyType


    def setCreateSql(self,s):
        self.createSql = s

    def getCreateSql(self):
        return self.createSql


    def setSqlField(self,s):
        self.sqlFieldOfEntry = s

    def getSqlField(self):
        return self.sqlFieldOfEntry.encode("utf-8")


    def setBgColor(self,sColor):
        self.bgColor = sColor

      
    def getBgColor(self):
        return self.bgColor

    def setFgColor(self,sColor):
        self.fgColor = sColor

      
    def getFgColor(self):
        return self.fgColor


