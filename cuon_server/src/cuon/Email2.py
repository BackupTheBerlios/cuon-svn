#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
"""
******************************************************************************
* Description:  SimpleMail ist ein Modul zum Versenden von Emails 
*               mit und ohne Anhaengen.
* Filename:     simplemail.py
* Created:      2004-10-06 Gerold
* License:      LGPL: http://www.opensource.org/licenses/lgpl-license.php
* Requirements: Python 2.3:  http://www.python.org
*
* Änderungen 2007 von Juergen Hamel, siehe Hinweise in der Datei
*
* Einfaches Beispiel:
*
*   from simplemail import Email
*   Email(
*       from_address = "absender@domain.at",
*       to_address = "empfaenger@domain.at",
*       subject = "Betreff",
*       message = "Das ist der Nachrichtentext"
*   ).send()
*
* 2004-03-13 Gerold
*   - Umlaute in den Beschreibungen ausgebessert
*   - Schreibweise der Kommentare wurde so umgesetzt dass auf einfache
*     Art und Weise eine Uebersetzung stattfinden kann.
*     Erklaerung: "de" steht fuer "deutsch"
*                 "en" steht fuer "englisch"
*
* 2004-04-25 Gerold
*   - Kleine Ausbesserungen in den Beschreibungen vorgenommen
*   - Einfaches Beispiel in den Beschreibungstext integriert
*
* 2005-08-20 Gerold
*   - Das Versenden von Anhaengen ermoeglicht
*
* 2005-09-28 Gerold
*   - Die Rückgabe des Befehls "sendmail()" wird in das Attribut "statusdict"
*     der Instanz der Klasse "Email" geschrieben. So ist es jetzt auch moeglich,
*     beim Versenden an mehrere Emailadressen, eine exakte Rueckmeldung ueber
*     den Versandstatus zu erhalten. Das Format der Rueckgabe wird unter
*     der Url http://www.python.org/doc/current/lib/SMTP-objects.html#l2h-3493
*     genau erklaert.
*
*     Hier ein Auszug aus dieser Erklaerung:
*     This method will return normally if the mail is accepted for at least 
*     one recipient. Otherwise it will throw an exception. That is, if this 
*     method does not throw an exception, then someone should get your mail. 
*     If this method does not throw an exception, it returns a dictionary, 
*     with one entry for each recipient that was refused. Each entry contains 
*     a tuple of the SMTP error code and the accompanying error message sent 
*     by the server.
*
* 2005-09-29 Gerold
*   - Das Format der Hilfe geaendert.
*   - Ab jetzt wird auch der "User-Agent" im Header mitgesendet.
*     Jens, danke für die Idee.
*
* 2005-11-11 Gerold
*   - Fixed: Das Versenden von Emails funktioniert jetzt auch wenn man
*     sich am SMTP-Server mit Benutzername und Passwort anmelden muss.
*     ChrisSek, danke für den Hinweis.
*   - Es war, glaube ich, recht lästig, dass Testemails gesendet wurden, 
*     wenn man dieses Modul ausführte. Ich habe es so geändert, dass die
*     Testemails nur mehr dann gesendet werden, wenn man dieses Modul mit
*     dem Parameter "test" aufruft. Z.B. ``python simplemail.py test``
*
* 2005-12-10 Gerold
*   - Schlampigkeitsfehler ausgebessert. Es wurde ein Fehler gemeldet, wenn
*     man beim Initialisieren der Klasse Email auch den Dateinamen eines
*     Attachments übergeben hatte. Es war ein Unterstrich zu viel, der 
*     Entfernt wurde.
*
* 2006-03-22 Gerold
*   - Klassen fuer CC-Empfaenger und BCC-Empfaenger hinzugefuegt.
*     Ab jetzt können Emails auch an CC und BCC gesendet werden.
*     Wie das funktioniert sieht man in der Funktion ``testen()``
*
* 2006-03-30 Gerold
*   - Reply-to (Antwort an) kann jetzt auch angegeben werden.
*
* 2006-05-28 Gerold
*   - Wortlaut des Headers "User-Agent" geändert.
*   - Da nicht jeder SMTP-Server das Datum automatisch zum Header hinzufügt, 
*     wird ab jetzt das Datum beim Senden hinzugefügt. 
*     (Karl, danke für den wichtigen Hinweis.)
* 2005-06-08 Gerold
*   - Fehlerklassen von **SimpleMail_Exception** abgeleitet. Damit wird
*     bei einem Fehler jetzt auch eine aussagekräftigere Fehlermeldung 
*     ausgegeben. Dabei habe ich auch die vertauschten Fehlermeldungen
*     ausgetauscht. (Rebecca, danke für die Meldung.)
*   - Da die Klassen **CCRecipients** und **BCCRecipients** sowiso von
*     **Recipients** abgeleitet wurden, kann ich mir das Überschreiben
*     der Initialisierung (__init__) und die Angabe der Slots sparen.
*
******************************************************************************
"""

import os.path
import sys
import time
import smtplib
import mimetypes
from email import Encoders
from email.Header import Header
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.Utils import formataddr
from email.Utils import formatdate
from email.Message import Message
from email.MIMEAudio import MIMEAudio
from email.MIMEBase import MIMEBase
from email.MIMEImage import MIMEImage
import StringIO
import base64
import bz2


# Exceptions
#----------------------------------------------------------------------
class SimpleMail_Exception(Exception):
    """
    SimpleMail Base-Exception
    """
    def __str__(self):
        return self.__doc__

class NoFromAddress_Exception(SimpleMail_Exception):
    """
    en: No sender address
    de: Es wurde keine Absenderadresse angegeben
    """
    pass

class NoToAddress_Exception(SimpleMail_Exception):
    """
    en: No recipient address
    de: Es wurde keine Empfaengeradresse angegeben
    """
    pass

class NoSubject_Exception(SimpleMail_Exception):
    """
    en: No subject
    de: Es wurde kein Betreff angegeben
    """
    pass

class AttachmentNotFound_Exception(SimpleMail_Exception):
    """
    en: Attachment not found
    de: Das uebergebene Attachment wurde nicht gefunden
    """
    pass



# Email-Anhaenge
#----------------------------------------------------------------------
class Attachments(object):
    """
    de: Dieses Objekt stellt die Anhaenge einer Email dar
    """

    __slots__ = ('_attachments')


    #----------------------------------------------------------------------
    def __init__(self):
        """
        de: Initialisiert die Anhaenge
        """
        
        self._attachments = []


    #----------------------------------------------------------------------
    def add_filename(self, dicFile = ''):
        """
        en: Adds an attachment
        de: Fuegt einen neuen Anhang hinzu
        """
        
        self._attachments.append(dicFile)


    #----------------------------------------------------------------------
    def count(self):
        """
        en: Returns the number of attachments
        de: Gibt die Anzahl der Anhaenge zurueck
        """

        return len(self._attachments)


    #----------------------------------------------------------------------
    def get_list(self):
        """
        en: Returns the attachments, as list
        de: Gibt die Anhaenge als Liste zurueck
        """

        return self._attachments



# Empfaenger-Klasse
#----------------------------------------------------------------------
class Recipients(object):
    """
    en: This object stands for all recipients from the email
    de: Dieses Objekt stellt die Empfaenger einer Email dar
    """

    __slots__ = ('_recipients')


    #----------------------------------------------------------------------
    def __init__(self):
        """
        en: Initializes the recipients
        de: Initialisiert die Empfaenger
        """

        self._recipients = []


    #----------------------------------------------------------------------
    def add(self, address, caption = ''):
        """
        en: Adds a new address to the list of recipients
            address = email address of the recipient
            caption = caption (name) of the recipient
        de: Fuegt der Empfaengerliste eine neue Adresse hinzu.
            address = Emailadresse des Empfaengrs
            caption = Bezeichnung (Name) des Empfaengers
        """

        self._recipients.append(formataddr((caption, address)))


    #----------------------------------------------------------------------
    def count(self):
        """
        en: Returns the number of recipients
        de: Gibt die Anzahl der Empfaenger zurueck
        """

        return len(self._recipients)


    #----------------------------------------------------------------------
    def __repr__(self):
        """
        en: Returns the list of recipients, as string
        de: Gibt die Empfengerliste als String zurueck
        """

        return str(self._recipients)


    #----------------------------------------------------------------------
    def get_list(self):
        """
        en: Returns the list of recipients, as list
        de: Gibt die Empfaengerliste als Liste zurueck
        """

        return self._recipients



# Empfaenger-Klasse fuer CC-Empfaenger (Carbon Copy)
#----------------------------------------------------------------------
class CCRecipients(Recipients):
    """
    en: This object stands for all CC-recipients from the email
    de: Dieses Objekt stellt die CC-Empfaenger einer Email dar
    """
    pass



# Empfaenger-Klasse fuer BCC-Empfaenger (Blind Carbon Copy)
#----------------------------------------------------------------------
class BCCRecipients(Recipients):
    """
    en: This object stands for all BCC-recipients from the email
    de: Dieses Objekt stellt die BCC-Empfaenger einer Email dar
    """
    pass



# Email-Klasse
#----------------------------------------------------------------------
class Email(object):
    """
    en: This Object stands for one email, which can sent with
        the method 'send'.
    de: Dieses Objekt stellt eine Email dar, welche mit der
        Methode 'send' verschickt werden kann.
    """

    __slots__ = (
        'from_address',
        'from_caption',
        'recipients',
        'cc_recipients',
        'bcc_recipients',
        'subject',
        'message',
        'smtp_server',
        'smtp_user',
        'smtp_password',
        'smtp_crypt',
        'attachments',
        'content_subtype',
        'content_charset',
        'header_charset',
        'statusdict',
        'user_agent',
        'reply_to_address',
        'reply_to_caption',
    )


    #----------------------------------------------------------------------
    def __init__(
        self,
        from_address = "",
        from_caption = "",
        to_address = "",
        to_caption = "",
        subject = "",
        message = "",
        smtp_server = "localhost",
        smtp_user = "",
        smtp_password = "",
        attachment_file = "",
        user_agent = "",
        reply_to_address = "",
        reply_to_caption = "",
        
    ):
        """
        en: Initialize the email object
            from_address     = the email address of the sender
            from_caption     = the caption (name) of the sender
            to_address       = the email address of the recipient
            to_caption       = the caption (name) of the recipient
            subject          = the subject of the email message
            message          = the body text of the email message
            smtp_server      = the ip-address or the name of the SMTP-server
            smtp_user        = (optional) Login name for the SMTP-Server
            smtp_passwort    = (optional) Password for the SMTP-Server
            user_agent       = (optional) program identification
            reply_to_address = (optional) Reply-to email address
            reply_to_caption = (optional) Reply-to caption (name)
        
        de: Initialisiert das Email-Objekt
            from_address     = die Emailadresse des Absenders
            from_caption     = die Beschrifung (der Name) des Absenders
            to_address       = die Emailadresse des Empfaengers
            to_caption       = die Beschriftung (der Name) des Empfaengers
            subject          = der Betreff der Emailnachricht
            message          = der Nachrichtentext
            smtp_server      = IP-Adresse oder Name des SMTP-Servers.
                               Es kann auch der Port mit ``:`` vom Server getrennt 
                               angehaengt werden. (z.B. ``localhost:25``)
            smtp_user        = (optional) Benutzername zum Anmelden an den SMTP-Server
            smtp_passwort    = (optional) das Passwort zum Anmelden an den SMTP-Server
            user_agent       = (optional) Programm-Identifikation
            reply_to_address = (optional) Antwort-an Emailadresse
            reply_to_caption = (optional) Antwort-an Beschriftung (Name)
        """

        self.from_address = from_address
        self.from_caption = from_caption
        self.recipients = Recipients()
        self.cc_recipients = CCRecipients()
        self.bcc_recipients = BCCRecipients()
        if to_address:
            self.recipients.add(to_address, to_caption)
        self.subject = subject
        self.message = message
        self.smtp_server = smtp_server
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.smtp_crypt = None
        self.attachments = Attachments()
        if attachment_file:
            self.attachments.add_filename(attachment_file)
        self.content_subtype = "plain"
        self.content_charset = "iso-8859-1"
        self.header_charset = "us-ascii"
        self.statusdict = None
        if user_agent:
            self.user_agent = user_agent
        else:
            self.user_agent = (
                "SimpleMail (http://www.python-forum.de/post-18144.html) " 
                "Python v%s"
            ) % sys.version.split()[0]
        self.reply_to_address = reply_to_address
        self.reply_to_caption = reply_to_caption


    #----------------------------------------------------------------------
    def send(self):
        """
        de: Sendet die Email an den Empfaenger.
            Wird das Email nur an einen Empfaenger gesendet, dann wird bei
            Erfolg <True> zurueck gegeben. Wird das Email an mehrere Empfaenger
            gesendet und wurde an mindestens einen der Empfaenger erfolgreich
            ausgeliefert, dann wird ebenfalls <True> zurueck gegeben.
            
            Wird das Email nur an einen Empfaenger gesendet, dann wird bei
            Misserfolg <False> zurueck gegeben. Wird das Email an mehrere 
            Empfaenger gesendet und wurde an keinen der Empfaenger erfolgreich
            ausgeliefert, dann wird <False> zurueck gegeben.
        """

        #
        # pruefen ob alle notwendigen Informationen angegeben wurden
        #
        if len(self.from_address.strip()) == 0:
            raise NoFromAddress_Exception
        if self.recipients.count() == 0:
            if (
                (self.cc_recipients.count() == 0) and 
                (self.bcc_recipients.count() == 0)
            ):
                raise NoToAddress_Exception
        if len(self.subject.strip()) == 0:
            raise NoSubject_Exception

        #
        # Email zusammensetzen
        #
        if len(self.attachments) == 0:
            # Nur Text
            msg = MIMEText(
                _text = self.message,
                _subtype = self.content_subtype,
                _charset = self.content_charset
            )
        else:
            # Multipart
            msg = MIMEMultipart()
            if self.message:
                att = MIMEText(
                    _text = self.message,
                    _subtype = self.content_subtype,
                    _charset = self.content_charset
                )
                msg.attach(att)

        # Empfänger, CC, BCC, Absender, User-Agent, Antwort-an 
        # und Betreff hinzufügen
        from_str = formataddr((self.from_caption, self.from_address))
        msg["From"] = from_str
        if self.reply_to_address:
            reply_to_str = formataddr((self.reply_to_caption, self.reply_to_address))
            msg["Reply-To"] = reply_to_str
        if self.recipients.count() > 0:
            msg["To"] = ", ".join(self.recipients.get_list())
        if self.cc_recipients.count() > 0:
            msg["Cc"] = ", ".join(self.cc_recipients.get_list())
        msg["Date"] = formatdate(time.time())
        msg["User-Agent"] = self.user_agent
        try:
            msg["Subject"] = Header(
                self.subject, self.header_charset
            )
        except(UnicodeDecodeError):
            msg["Subject"] = Header(
                self.subject, self.content_charset
            )
        msg.preamble = "You will not see this in a MIME-aware mail reader.\n"
        msg.epilogue = ""

        # Falls MULTIPART --> zusammensetzen
        if len(self.attachments) > 0:
            for dicFile in self.attachments:
                # Pruefen ob Datei existiert
                filename = dicFile['filename']
                # Datentyp herausfinden
                ctype, encoding = mimetypes.guess_type(filename)
                print ctype, encoding
                
                if ctype is None or encoding is not None:
                    ctype = 'application/octet-stream'
                maintype, subtype = ctype.split('/', 1)
                s = base64.decodestring(dicFile['data'])
                s = bz2.decompress(s)
                fp = StringIO.StringIO(s)
                if maintype == 'text':
                    # Note: we should handle calculating the charset
                    att = MIMEText(fp.read(), _subtype=subtype)
                elif maintype == 'image':
                    att = MIMEImage(fp.read(), _subtype=subtype)
                elif maintype == 'audio':
                    att = MIMEAudio(fp.read(), _subtype=subtype)
                else:
                    att = MIMEBase(maintype, subtype)
                    att.set_payload(fp.read())
                    # Encode the payload using Base64
                    Encoders.encode_base64(att)
                
                fp.close()

                # Set the filename parameter
                
                att.add_header(
                    'Content-Disposition', 
                    'attachment', 
                    filename = os.path.split(filename)[1].strip()
                )
                msg.attach(att)

        #
        # Am SMTP-Server anmelden und evt. authentifizieren
        #
        smtp = smtplib.SMTP()
        if self.smtp_crypt == 'TLS':
            print 'TLS found'
            try:
                smtp.starttls()
            except Exception, param:
                print Exception, param
                
            
        if self.smtp_server:
            smtp.connect(self.smtp_server)
        else:
            smtp.connect()
        if self.smtp_user:
            smtp.login(user = self.smtp_user, password = self.smtp_password)

        #
        # Email versenden
        #
        self.statusdict = smtp.sendmail(
            from_str, 
            (
                self.recipients.get_list() + 
                self.cc_recipients.get_list() + 
                self.bcc_recipients.get_list()
            ), 
            msg.as_string()
        )
        smtp.close()
        
        # Rueckmeldung
        return True

    # Juergen Hamel
    # Löschen der Testroutinen
    
