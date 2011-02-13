# -*- coding: utf-8 -*-

##Copyright (C) [2003]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 

import os
import sys
#sys.path.append(os.environ['CUON_PATH'])
import uno
from unohelper import Base,systemPathToFileUrl, absolutize
from com.sun.star.beans import PropertyValue
from com.sun.star.beans.PropertyState import DIRECT_VALUE
from com.sun.star.uno import Exception as UnoException
from com.sun.star.io import IOException,XInputStream, XOutputStream


from ooconnect import ooconnect 

class letter(ooconnect):

    def __init__(self):
        ooconnect.__init__(self)

    def createAddress(self, id):
        # get the central desktop object
        desktop = self.smgr.createInstanceWithContext( "com.sun.star.frame.Desktop",self.ctx)
        path = os.environ['CUON_OO_DOC']
        inProps = PropertyValue( "Hidden" , 0 , True, 0 ),
        fileUrl = uno.absolutize('test.sxc' , systemPathToFileUrl(path) )
        model = desktop.loadComponentFromURL( fileUrl , "_blank", 0, inProps)


        # access the current writer document
        #model = desktop.getCurrentComponent()

        # access the document's text property
        text = model.Text

        # create a cursor
        cursor = text.createTextCursor()

        liAddress = self.unpickleObject(id)
        for i in range(0,len(liAddress)):
            # insert the text into the document
            text.insertString( cursor, `liAddress[i]`, 0 )


        # Do a nasty thing before exiting the python process. In case the
        # last call is a oneway call (e.g. see idl-spec of insertString),
        # it must be forced out of the remote-bridge caches before python
        # exits the process. Otherwise, the oneway call may or may not reach
        # the target object.
        # I do this here by calling a cheap synchronous call (getPropertyValue).
        self.ctx.ServiceManager