class constants:
    def __init__(self):
        self.MN = {}
        self.MN['Mainwindow'] = 10
        self.MN['Client'] = 1000
        
        self.MN['Address'] = 2000
        self.MN['Address_info'] = 2001
        self.MN['Address_stat_caller'] = 2002
        self.MN['Address_stat_rep'] = 2003
        self.MN['Address_stat_salesman'] = 2004
        self.MN['Address_stat_schedul'] = 2005
        
        self.MN['Partner'] = 2100
        self.MN['Partner_info'] = 2101
        
        self.MN['Partner_Schedul'] = 2200
        self.MN['Partner_Schedul_info'] = 2201

        self.MN['Articles'] = 3000
        self.MN['Articles_stat_misc1'] = 3001
        
        self.MN['MaterialGroups'] = 23000



        self.MN['Order'] = 4000
        
        self.MN['Order_stat_misc1'] = 4001
        self.MN['Order_stat_global1'] = 4002
        self.MN['Order_stat_caller1'] = 4003
        self.MN['Order_stat_rep1'] = 4004
        self.MN['Order_stat_salesman1'] = 4005
        self.MN['PROPOSAL'] = 4500
         
        self.MN['Stock'] = 5000
        self.MN['Staff'] = 6000
        self.MN['StaffFee'] = 6100
        
        self.MN['Invoice'] = 7000
        self.MN['Invoice_info'] = 7001
        self.MN['Invoice_stat_taxvat1'] = 7101
        
        
        self.MN['DMS'] = 11000
        self.MN['Forms_Address_Notes_Misc'] = 11010
        self.MN['Forms_Address_Notes_Contacter'] = 11011
        self.MN['Forms_Address_Notes_Rep'] = 11012
        self.MN['Forms_Address_Notes_Salesman'] = 11013
        self.MN['Newsletter'] = 11100
        
        self.MN['Biblio'] = 12000
        self.MN['AI'] = 13000
        
        self.MN['Project'] = 14000
        self.MN['Project_info'] = 14001
        self.MN['Project_stat_misc1'] = 14011
        self.MN['Project_phase'] = 14100
        self.MN['Project_task'] = 14200
        self.MN['Project_staff_resources'] = 14300
        self.MN['Project_material_resources'] = 14400
        self.MN['Project_programming'] = 14500
        
        self.MN['SupportTicket']  = 17000


        self.MN['Web2'] = 20000
        self.MN['Stats'] = 22000
        self.MN['Calendar'] = 28000
        self.MN['Think'] = 29000
        
        self.MN['Leasing'] = 30001
        
        self.MN['Grave'] = 40000
        self.MN['Graveyard'] = 41000
        
        self.MimeType = {}
        
        self.MimeType['image/gif'] =  ['gif']
        self.MimeType['text/plain'] = [ 'txt']
        self.MimeType['text/html'] =  ['html']
        self.MimeType['image/jpeg'] =  ['jpg']
        self.MimeType['application/pdf'] =  ['pdf']
        
        self.MimeType['application/msword'] =  ['doc']
        self.MimeType['application/vnd.oasis.opendocument.text'] =  ['odt']
        self.MimeType['application/vnd.oasis.opendocument.spreadsheet'] = [ 'ods']
        self.MimeType['application/vnd.oasis.opendocument.graphics'] = [ 'odg']
        self.MimeType['application/vnd.oasis.opendocument.presentation'] = [ 'odp']
        self.MimeType['application/x-bzip'] =  ['bz']
        self.MimeType['application/x-bzip2'] = [ 'bz2']
        self.MimeType['application/x-compressed'] =  ['zip']
        self.MimeType['application/x-zip-compressed'] =  ['zip']
        self.MimeType['application/zip'] = [ 'zip']
        self.MimeType['multipart/x-zip'] =  ['zip']
        self.MimeType['application/excel'] =  ['xls']
        self.MimeType['application/vnd.ms-excel'] =  ['xls']
        self.MimeType['application/x-excel'] = [ 'xls']
        self.MimeType['application/x-msexcel'] =  ['xls']
        self.MimeType['image/png'] =  ['png']
        self.MimeType['image/tiff'] =  ['tiff']
        self.MimeType['image/bmp'] =  ['bmp']
        self.MimeType['image/x-windows-bmp'] =  ['bmp']
        self.MimeType['text/x-python'] =  ['py']
        self.MimeType['application/x-php'] =  ['php']
        self.MimeType['text/x-ini-file'] = ['ini', 'cfg']
        self.MimeType['application/xml'] = ['xml']
        
        
        
#Perl   application/x-perl
#Ada    text/x-ada
#C  text/x-csrc;text/x-chdr
#ChangeLog  text/x-changelog
#C++    text/x-c++src;text/x-c++hdr
#C# text/x-csharp
#CSS    text/css
#.desktop   application/x-desktop
#Diff   text/x-patch
#Fortran 95 text/x-fortran
#GtkRC  text/x-gtkrc
#Haskell    text/x-haskell
#IDL    text/x-idl
#.ini   text/x-ini-file
#Java   text/x-java
#JavaScript application/x-javascript
#LaTeX  text/x-tex
#Lua    text/x-lua
#Makefile   text/x-makefile
#MSIL   text/x-msil
#Nemerle    text/x-nemerle
#Octave text/x-octave;text/x-matlab
#Pascal text/x-pascal
#gettext translation    text/x-gettext-translation
#Python text/x-python
#R  text/x-R
#Ruby   application/x-ruby
#Scheme text/x-scheme
#sh application/x-shellscript
#SQL    text/x-sql
#Tcl    text/x-tcl
#Texinfo    text/x-texinfo
#VB.NET text/x-vbnet;text/x-vb
#Verilog    text/x-verilog-src
#VHDL   text/x-vhdl
#XML    application/xml
 #      self.MimeType['multipart/signed'] = 'txt'
#        self.MimeType[''] = ''
#        self.MimeType[''] = ''
#        self.MimeType[''] = ''
#        self.MimeType[''] = ''
#        self.MimeType[''] = ''
#        self.MimeType[''] = ''
#        self.MimeType[''] = ''
#        self.MimeType[''] = ''
#        self.MimeType[''] = ''
#        self.MimeType[''] = ''
#        self.MimeType[''] = ''
#        self.MimeType[''] = ''
#        self.MimeType[''] = ''
#        self.MimeType[''] = ''
#        self.MimeType[''] = ''
#        self.MimeType[''] = ''
#        self.MimeType[''] = ''
#        self.MimeType[''] = ''
#        self.MimeType[''] = ''
#        self.MimeType[''] = ''
#        self.MimeType[''] = ''
#        self.MimeType[''] = ''
#        self.MimeType[''] = ''
#        self.MimeType[''] = ''
#        self.MimeType[''] = ''
#        self.MimeType[''] = ''
#        self.MimeType[''] = ''
#        self.MimeType[''] = ''
#        self.MimeType[''] = ''
#        self.MimeType[''] = ''
#        self.MimeType[''] = ''
#        self.MimeType[''] = ''
#        self.MimeType[''] = ''
#        self.MimeType[''] = ''
#        self.MimeType[''] = ''
#        self.MimeType[''] = ''
#        self.MimeType[''] = ''
#        self.MimeType[''] = ''
#        self.MimeType[''] = ''
#        self.MimeType[''] = ''
#        self.MimeType[''] = ''
#        self.MimeType[''] = ''
#        self.MimeType[''] = ''
#        self.MimeType[''] = ''
#        self.MimeType[''] = ''
#        self.MimeType[''] = ''
#        self.MimeType[''] = ''
#        self.MimeType[''] = ''
#        self.MimeType[''] = ''
#        self.MimeType[''] = ''
        


