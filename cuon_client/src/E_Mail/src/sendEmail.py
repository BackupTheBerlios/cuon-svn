# -*- coding: utf-8 -*-

##Copyright (C) [2003]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 


# Import smtplib for the actual sending function
import smtplib, sys
 
# Here are the email pacakge modules we'll need
from email.MIMEImage import MIMEImage
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText



class sendEmail:

    def __init__(self):
    
 
        COMMASPACE = ', '
 
        # Create the container (outer) email message.
        self.msg = MIMEMultipart()
        self.msg.preamble = ''
        
        # Guarantees the message ends in a newline
        self.msg.epilogue = ''

        self.mFiles = []

    def setSubject(self, s):
        self.msg['Subject'] = s

    def setFrom(self,s):
        self.msg['From'] = s
        

    def setTo(self,s):
        self.msg['To'] = s
        
 
    def addAttachments(self, *maFiles):
        for j in range(0, len(mFiles)):
            self.mFiles.append( maFiles[j])

                                                                                
    def sendTheEmail(self):
 

        # Assume we know that the txt files are all in ascii format
        for file in self.mFiles:
            # Open the files in binary mode.  Let the MIMEText class automatically
            # guess the specific image type.
            fp = open(file, 'rb')
            txt = MIMEText(fp.read())
            fp.close()
            self.msg.attach(txt)
 
            # Send the email via our own SMTP server.
            s = smtplib.SMTP()
            s.connect()
            s.sendmail(self.msg['From'], self.msg['To'], self.msg.as_string())
