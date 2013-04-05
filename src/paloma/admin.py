# -*- coding: utf-8 -*- 
from django.contrib import admin
from django.conf import settings
from django.utils.timezone import now

from celery import app

from models import *
from tasks import apply_publish

if settings.DEBUG:
    try:
        from kombu.transport.django.models import Queue as KombuQueue,Message as KombuMessage
        from djcelery.models import TaskMeta,TaskSetMeta

        ### KombuQueue
        class KombuQueueAdmin(admin.ModelAdmin):
            list_display=tuple([f.name for f in KombuQueue._meta.fields ])
        admin.site.register(KombuQueue,KombuQueueAdmin)
        
        ### define __unicode__ to Queue class
        #
        #def __unicode__(self):
        #
        #   return self.name

        ### KombuMessage
        class KombuMessageAdmin(admin.ModelAdmin):
            list_display=tuple([f.name for f in KombuMessage._meta.fields])
        admin.site.register(KombuMessage,KombuMessageAdmin)

        ### TaskMeta
        class TaskMetaAdmin(admin.ModelAdmin):
            list_display=tuple([f.name for f in TaskMeta._meta.fields])
            list_filter = ('status',)
            date_hierarchy = 'date_done'
        admin.site.register(TaskMeta,TaskMetaAdmin)
        
        ### TaskSetMeta
        class TaskSetMetaAdmin(admin.ModelAdmin):
            list_display=tuple([f.name for f in TaskSetMeta._meta.fields])
        admin.site.register(TaskSetMeta,TaskSetMetaAdmin)
        
        
    except Exception,e:
        print e
        pass

### Domain 
class DomainAdmin(admin.ModelAdmin):
    list_display=tuple([f.name for f in Domain._meta.fields ])
admin.site.register(Domain,DomainAdmin)

### Alias 
class AliasAdmin(admin.ModelAdmin):
    list_display=tuple([f.name for f in Alias._meta.fields ])
admin.site.register(Alias,AliasAdmin)


#################################################

### Site 
class SiteAdmin(admin.ModelAdmin):
    list_display=tuple([f.name for f in Site._meta.fields ])
admin.site.register(Site,SiteAdmin)

### Text 
class TextAdmin(admin.ModelAdmin):
    list_display=tuple([f.name for f in Text._meta.fields ])
admin.site.register(Text,TextAdmin)

### Circle 
class CircleAdmin(admin.ModelAdmin):
    list_display=tuple([f.name for f in Circle._meta.fields ])
admin.site.register(Circle,CircleAdmin)

### Member 
class MemberAdmin(admin.ModelAdmin):
    list_display=tuple([f.name for f in Member._meta.fields ])
admin.site.register(Member,MemberAdmin)

### Publish 
class PublishAdmin(admin.ModelAdmin):
    list_display=tuple([f.name for f in Publish._meta.fields ])

    def save_model(self, request, obj, form, change):
        ''' Saving... 

            :param request: request object to view
            :param obj: Publish instance
            :param form: Form instance
            :param change: bool
        ''' 
        if all(['status' in form.changed_data,
               obj.status == 'scheduled',
               obj.dt_start < now() or  ( obj.task != None and obj.task !="") ]):
            #: do nothing
            return 

        super(PublishAdmin,self).save_model(request,obj,form,change)
        apply_publish(obj)

admin.site.register(Publish,PublishAdmin)

### Mail 
class MailAdmin(admin.ModelAdmin):
    list_display=tuple([f.name for f in Mail._meta.fields ])
admin.site.register(Mail,MailAdmin)


### Provision
class ProvisionAdmin(admin.ModelAdmin):
    list_display=tuple([f.name for f in Provision._meta.fields ])
admin.site.register(Provision,ProvisionAdmin)

### ActionMail 
class ActionMailAdmin(admin.ModelAdmin):
    list_display=tuple([f.name for f in ActionMail._meta.fields ])
admin.site.register(ActionMail,ActionMailAdmin)

### Journal 
class JournalAdmin(admin.ModelAdmin):
    list_display=tuple([f.name for f in Journal._meta.fields ])
admin.site.register(Journal,JournalAdmin)

#################
# rsyslog
try:
    from rsyslog import SystemeventsAdmin,SystemeventspropertiesAdmin
except:
    pass
