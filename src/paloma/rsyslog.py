'''
This is an auto-generated Django model module
with using rsyslog-mysql provided MySQL tables Schema.
 
For Debian, install rsyslog-mysql package::

   $ sudo aptitude install rsyslog-mysql

Then, edit /etc/rsyslog.d/mysql.conf::

   $ModLoad ommysql
   mail.* :ommysql:localhost,project_db_name,project_db_user,project_db_name

Would be used mainly for debugging.
'''

from __future__ import unicode_literals

from django.db import models
from django.contrib import admin

# Models
class Systemevents(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    customerid = models.BigIntegerField(null=True, db_column='CustomerID', blank=True) # Field name made lowercase.
    receivedat = models.DateTimeField(null=True, db_column='ReceivedAt', blank=True) # Field name made lowercase.
    devicereportedtime = models.DateTimeField(null=True, db_column='DeviceReportedTime', blank=True) # Field name made lowercase.
    facility = models.IntegerField(null=True, db_column='Facility', blank=True) # Field name made lowercase.
    priority = models.IntegerField(null=True, db_column='Priority', blank=True) # Field name made lowercase.
    fromhost = models.CharField(max_length=60L, db_column='FromHost', blank=True) # Field name made lowercase.
    message = models.TextField(db_column='Message', blank=True) # Field name made lowercase.
    ntseverity = models.IntegerField(null=True, db_column='NTSeverity', blank=True) # Field name made lowercase.
    importance = models.IntegerField(null=True, db_column='Importance', blank=True) # Field name made lowercase.
    eventsource = models.CharField(max_length=60L, db_column='EventSource', blank=True) # Field name made lowercase.
    eventuser = models.CharField(max_length=60L, db_column='EventUser', blank=True) # Field name made lowercase.
    eventcategory = models.IntegerField(null=True, db_column='EventCategory', blank=True) # Field name made lowercase.
    eventid = models.IntegerField(null=True, db_column='EventID', blank=True) # Field name made lowercase.
    eventbinarydata = models.TextField(db_column='EventBinaryData', blank=True) # Field name made lowercase.
    maxavailable = models.IntegerField(null=True, db_column='MaxAvailable', blank=True) # Field name made lowercase.
    currusage = models.IntegerField(null=True, db_column='CurrUsage', blank=True) # Field name made lowercase.
    minusage = models.IntegerField(null=True, db_column='MinUsage', blank=True) # Field name made lowercase.
    maxusage = models.IntegerField(null=True, db_column='MaxUsage', blank=True) # Field name made lowercase.
    infounitid = models.IntegerField(null=True, db_column='InfoUnitID', blank=True) # Field name made lowercase.
    syslogtag = models.CharField(max_length=60L, db_column='SysLogTag', blank=True) # Field name made lowercase.
    eventlogtype = models.CharField(max_length=60L, db_column='EventLogType', blank=True) # Field name made lowercase.
    genericfilename = models.CharField(max_length=60L, db_column='GenericFileName', blank=True) # Field name made lowercase.
    systemid = models.IntegerField(null=True, db_column='SystemID', blank=True) # Field name made lowercase.
    class Meta:
        db_table = 'SystemEvents'

class Systemeventsproperties(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    systemeventid = models.IntegerField(null=True, db_column='SystemEventID', blank=True) # Field name made lowercase.
    paramname = models.CharField(max_length=255L, db_column='ParamName', blank=True) # Field name made lowercase.
    paramvalue = models.TextField(db_column='ParamValue', blank=True) # Field name made lowercase.
    class Meta:
        db_table = 'SystemEventsProperties'


# Systemevents Systemeventsproperties Admin

class SystemeventsAdmin(admin.ModelAdmin):
    list_display=tuple([f.name for f in Systemevents._meta.fields ])
admin.site.register(Systemevents,SystemeventsAdmin)

class SystemeventspropertiesAdmin(admin.ModelAdmin):
    list_display=tuple([f.name for f in Systemeventsproperties._meta.fields ])
admin.site.register(Systemeventsproperties,SystemeventspropertiesAdmin)
