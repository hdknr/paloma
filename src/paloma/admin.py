# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.contenttypes import generic
from django.conf import settings
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm
from django.forms.models import BaseInlineFormSet
from django.core.urlresolvers import reverse

from models import (
    Domain,
    Alias,
    Site,
    Template,
    Targetting,
    Circle,
    Member,
    Membership,
    Publish,
    Journal,
    Message,
    Provision,
    Publication,
)
from tasks import apply_publish, deliver_mail


def link_to_relation(self, obj, field=""):
    ''' relation field link
        - self : Admin
        - obj  : Model Instance
        - filed : Field Name
    '''
    if obj is None:
        return ""

    fobj = getattr(obj, field, None)
    if fobj:
        url = reverse("admin:%s_change" % fobj._meta.db_table,
                      args=[fobj.id])
        return '<a href="%s">%s</a>' % (url, fobj.__unicode__())

user_link = lambda self, obj: link_to_relation(self, obj, "user")
user_link.short_description = _(u"System User")
user_link.allow_tags = True

member_link = lambda self, obj: link_to_relation(self, obj, "member")
member_link.short_description = _(u"Member")
member_link.allow_tags = True

circle_link = lambda self, obj: link_to_relation(self, obj, "circle")
circle_link.short_description = _(u"Circle")
circle_link.allow_tags = True

publish_link = lambda self, obj: link_to_relation(self, obj, "publish")
publish_link.short_description = _(u"Publish")
publish_link.allow_tags = True

message_link = lambda self, obj: link_to_relation(self, obj, "message")
message_link.short_description = _(u"Message")
message_link.allow_tags = True

###

if settings.DEBUG:
    try:
        from kombu.transport.django.models import (
            Queue as KombuQueue,
            Message as KombuMessage
        )
        from djcelery.models import TaskMeta, TaskSetMeta

        ### KombuQueue
        class KombuQueueAdmin(admin.ModelAdmin):
            list_display = tuple([f.name for f in KombuQueue._meta.fields])
        admin.site.register(KombuQueue, KombuQueueAdmin)

        ### define __unicode__ to Queue class
        #
        #def __unicode__(self):
        #
        #   return self.name

        ### KombuMessage
        class KombuMessageAdmin(admin.ModelAdmin):
            list_display = tuple([f.name for f in KombuMessage._meta.fields])
        admin.site.register(KombuMessage, KombuMessageAdmin)

        ### TaskMeta
        class TaskMetaAdmin(admin.ModelAdmin):
            list_display = tuple([f.name for f in TaskMeta._meta.fields])
            list_filter = ('status',)
            date_hierarchy = 'date_done'
        admin.site.register(TaskMeta, TaskMetaAdmin)

        ### TaskSetMeta
        class TaskSetMetaAdmin(admin.ModelAdmin):
            list_display = tuple([f.name for f in TaskSetMeta._meta.fields])
        admin.site.register(TaskSetMeta, TaskSetMetaAdmin)

    except Exception, e:
        print e
        pass

### Domain


class DomainAdmin(admin.ModelAdmin):
    list_display = tuple([f.name for f in Domain._meta.fields])
admin.site.register(Domain, DomainAdmin)

### Alias


class AliasAdmin(admin.ModelAdmin):
    list_display = tuple([f.name for f in Alias._meta.fields])
admin.site.register(Alias, AliasAdmin)


#################################################

class SiteAdminForm(ModelForm):
    class Meta:
        model = Site
        exclude = []


class SiteAdmin(admin.ModelAdmin):
    form = SiteAdminForm
    list_display = tuple([f.name for f in Site._meta.fields])


admin.site.register(Site, SiteAdmin)

### Targetting


class TargettingInline(generic.GenericTabularInline):
    model = Targetting
    ct_field = 'mediator_content_type'
    ct_fk_field = 'mediator_object_id'


class TargettingAdmin(admin.ModelAdmin):
    list_display = tuple([f.name for f in Targetting._meta.fields])
admin.site.register(Targetting, TargettingAdmin)

### Circle


class CirlceAdminMembershipFormset(BaseInlineFormSet):

    def get_queryset(self):
        return self.instance.membership_set.filter()


class CircleAdminMembershipInline(admin.TabularInline):
#class CircleAdminMembershipInline(admin.StackedInline):
    model = Membership
    formset = CirlceAdminMembershipFormset
    extra = 0
    raw_id_fields = ['member', ]
    verbose_name = _('Cicle Administrator')
    verbose_name_plural = _('Cicle Administrators')


class CircleAdmin(admin.ModelAdmin):
    list_display = tuple([f.name for f in Circle._meta.fields])
    # inlines = [CircleAdminMembershipInline]
admin.site.register(Circle, CircleAdmin)


# Membership


class MembershipAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'circle_link', 'member_link', 'user', 'is_admin',
        'is_member_active', 'is_user_active', 'is_admitted', )
    list_filter = ('circle', 'is_admin', 'is_admitted', )
    raw_id_fields = ['member', ]
    search_fields = ('member__address', 'member__user__username',)

MembershipAdmin.member_link = member_link
MembershipAdmin.circle_link = circle_link
admin.site.register(Membership, MembershipAdmin)


class MembershipInline(admin.StackedInline):
    model = Membership
    extra = 0

### Member


class MemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_link', 'address', 'is_active', 'bounces', )
    inlines = [MembershipInline, ]
    raw_id_fields = ['user', ]
    search_fields = ('address', 'user__username',)
    list_filter = ('is_active', )
MemberAdmin.user_link = user_link
admin.site.register(Member, MemberAdmin)

### Publish


class PublishAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'site', 'publisher', 'subject', 'text',
        'task_id', 'status', 'dt_start', 'activated_at', )

    inlines = [
        TargettingInline,
    ]
    date_hierarchy = 'dt_start'

    def save_model(self, request, obj, form, change):
        ''' Saving...

            :param request: request object to view
            :param obj: Publish instance
            :param form: Form instance
            :param change: bool
        '''
        if all(['status' in form.changed_data,
               obj.status == 'scheduled',
               any([obj.dt_start and obj.dt_start < now(),
                    obj.task_id not in [None, ""], ]),
                ]):
            #: do nothing
            return

        super(PublishAdmin, self).save_model(request, obj, form, change)
        apply_publish(obj)
admin.site.register(Publish, PublishAdmin)


### Provision
class ProvisionAdmin(admin.ModelAdmin):
    list_display = tuple([f.name for f in Provision._meta.fields])
    search_fields = ('prospect',)
    raw_id_fields = ('member', )
admin.site.register(Provision, ProvisionAdmin)

### Journal


import traceback

class JournalAdmin(admin.ModelAdmin):
    list_display = tuple([f.name for f in Journal._meta.fields])
    date_hierarchy = 'dt_created'
    readonly_fields = ('body_text', )

    def body_text(self, obj):

        def _body(po):
            payload = po.get_payload()
            if isinstance(payload, list):
                # po.is_multipart() == True
                return "<hr/>".join([_body(p) for p in payload])
            if isinstance(payload, basestring):
                cs = po.get_content_charset() or po.get_charset()
                if cs:
                    return unicode(
                        po.get_payload(decode=True), cs, "replace")

                return payload
            return ''

        return _body(obj.mailobject())

    body_text.short_description = _('Body Text')
    body_text.allow_tags = True

admin.site.register(Journal, JournalAdmin)

##############

### Template


class TemplateAdmin(admin.ModelAdmin):
    list_display = tuple([f.name for f in Template._meta.fields])
admin.site.register(Template, TemplateAdmin)

### Message


def send_message(modeladmin, request, queryset):
    if queryset.model is not Message:
        return

    for message in queryset.filter():
        deliver_mail(mail_obj=message)  # Sync

send_message.short_description = _('Send Message')


class MessageAdmin(admin.ModelAdmin):
    list_display = tuple([f.name for f in Message._meta.fields])
    date_hierarchy = 'created'
    search_fields = ('mail_message_id',)
    actions = [send_message, ]
    raw_id_fields = ['member', ]
admin.site.register(Message, MessageAdmin)

### Publication


class PublicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'publish_link', 'message_link', 'message_created')
    list_filter = ('publish',)

PublicationAdmin.publish_link = publish_link
PublicationAdmin.message_link = message_link
message_created = lambda self, obj: obj.message.created
message_created.short_description = _(u"Created At")
message_created.allow_tags = True
PublicationAdmin.message_created = message_created

admin.site.register(Publication, PublicationAdmin)

#################
# rsyslog
try:
    from rsyslog import SystemeventsAdmin, SystemeventspropertiesAdmin
except:
    pass
