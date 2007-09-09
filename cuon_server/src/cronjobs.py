# first Job, all new schedules update iCal
from xmlrpclib import ServerProxy


sv = ServerProxy('http://localhost:7080',allow_none = 1)

test1 =  sv.Web.cron_create_iCal('zope')
print test1

# second Job, only new Schedules update iCal

from xmlrpclib import ServerProxy


sv = ServerProxy('http://localhost:7080',allow_none = 1)

test1 =  sv.Web.cron_create_iCal2('zope')
print test1
