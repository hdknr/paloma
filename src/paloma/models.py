# -*- coding: utf-8 -*-
from django.db.models import Q
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now
from django.conf import settings
from django import template  # import Template,Context
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.deconstruct import deconstructible

from email import message_from_string
from celery.result import AsyncResult
from bs4 import BeautifulSoup as Soup

import traceback
import re

from utils import (
    create_auto_secret,
    create_auto_short_secret,
    expire,
    get_template_source,
)
import json

import logging
logger = logging.getLogger('paloma')

DEFAULT_RETURN_PATH_RE = r"bcmsg-(?P<message_id>\d+)@(?P<domain>.+)"
DEFAULT_RETURN_PATH_FORMAT = "bcmsg-%(message_id)s@%(domain)s"

RETURN_PATH_RE = r"^(?P<commnad>.+)-(?P<message_id>\d+)@(?P<domain>.+)"
RETURN_PATH_FORMAT = "%(command)s-%(message_id)s@%(domain)s"


def return_path_from_address(address):
    return re.search(
        DEFAULT_RETURN_PATH_RE,
        address).groupdict()


def default_return_path(param):
    return DEFAULT_RETURN_PATH_FORMAT % param


def read_return_path(address):
    return re.search(
        RETURN_PATH_RE,
        address).groupdict()


def make_return_path(param):
    return RETURN_PATH_FORMAT % param


def MDT(t=None):
    return (t or now()).strftime('%m%d%H%M%S')


@deconstructible
class Domain(models.Model):
    ''' Domain

        -  virtual_transport_maps.cf
    '''
    domain = models.CharField(
        _(u'Domain'),
        unique=True, max_length=100, db_index=True, )
    ''' Domain

        -  key for virtual_transport_maps.cf
        -  key and return value for  virtual_domains_maps.cf
    '''
    description = models.CharField(
        _(u'Description'),
        max_length=200, default='')

    maxquota = models.BigIntegerField(null=True, blank=True, default=None)
    quota = models.BigIntegerField(null=True, blank=True, default=None)
    transport = models.CharField(max_length=765)
    '''
        - virtual_transport_maps.cf   looks this for specified **domain**.
    '''

    backupmx = models.IntegerField(null=True, blank=True, default=None)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _(u'Domain')
        verbose_name_plural = _(u'Domains')


@deconstructible
class Alias(models.Model):
    ''' Alias
        - local user - maildir
        - remote user - alias

        - for  virtual_alias_maps.cf
    '''
    address = models.CharField(
        _('Alias Address'), max_length=100)
    '''
        - key for virtual_alias_maps.cf
    '''
    alias = models.CharField(
        _('Alias Forward'), max_length=100)
    '''
        - value for virtual_alias_maps.cf
    '''
    mailbox = models.CharField(
        _(u'Mailbox'),
        max_length=100, null=True, default=None, blank=True,
        help_text=u'specify Maildir path if address is local user ')
    '''
        - for local usr
        - value for virtual_alias_maps.cf
    '''
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Alias')
        verbose_name_plural = _('Alias')
        unique_together = (('address', 'alias', ), )

##


class AbstractProfile(models.Model):
    ''' Profile meta class'''

    def target_context(self, member):
        """ override this to return context dict for template rendering  """
        raise NotImplementedError

    @classmethod
    def target(cls, obj, *args, **kwargs):
        context = {}
        subclasses = cls.__subclasses__()
        for ref in obj._meta.get_all_related_objects():
            if ref.model in subclasses:
                try:
                    context.update(
                        getattr(obj, ref.var_name
                                ).target_context(*args, **kwargs)
                    )
                except Exception:
                    pass
        return context

    class Meta:
        abstract = True


@deconstructible
class Site(models.Model):
    ''' Site
    '''
    name = models.CharField(_(u'Owner Site Name'),
                            max_length=100, db_index=True, unique=True)
    ''' Site Name '''

    domain = models.CharField(_(u'@Domain'),
                              max_length=100, default='localhost',
                              db_index=True, unique=True,
                              null=False, blank=False, )
    ''' @Domain'''

    url = models.CharField(_(u'URL'),
                           max_length=150, db_index=True,
                           unique=True, default="/",)
    ''' URL path '''

    operators = models.ManyToManyField(User, verbose_name=_(u'Site Operators'))
    ''' Site Operators '''

    @property
    def authority_address(self):
        return "%s@%s" % (self.name, self.domain)

    @property
    def default_circle(self):
        try:
            return self.circle_set.get(is_default=True,)
        except:
            #: if no, get default:
            name = getattr(settings, 'PALOMA_NAME', 'all')
            return self.circle_set.get_or_create(
                site=self,
                name=name,
                symbol=name,
            )[0]

    def __unicode__(self):
        return self.domain

    @classmethod
    def app_site(cls):
        return Site.objects.get_or_create(
            name=getattr(settings, 'PALOMA_NAME', 'paloma'),
            domain=getattr(settings, 'PALOMA_DEFAULT_DOMAIN', 'example.com'),
        )[0]

# Mesage Tempalte


class TemplateManager(models.Manager):
    def get_template(self, name, site=None):
        site = site or Site.app_site()
        ret, created = self.get_or_create(site=site, name=name)
        if created or not ret.subject or not ret.text:
            try:
                path = 'paloma/mails/default_%s.html' % name.lower()
                source = Soup(get_template_source(path))
                ret.subject = source.select('subject')[0].text
                ret.subject = ret.subject.replace('\n', '').replace('\r', '')
                ret.text = source.select('text')[0].text
                ret.save()
            except Exception:
                logger.debug(traceback.format_exc())

        return ret


@deconstructible
class Template(models.Model):
    ''' Site Notice Text '''

    site = models.ForeignKey(Site, verbose_name=_(u'Owner Site'))
    ''' Owner Site'''

    name = models.CharField(
        _(u'Template Name'),
        max_length=100, db_index=True,)
    ''' Notice Name'''

    subject = models.CharField(
        _(u'Template Subject'),
        max_length=100, default='',)
    ''' Subject '''

    text = models.TextField(
        _(u'Template Text'),
        max_length=100, default='',)
    ''' Text '''

    objects = TemplateManager()

    @classmethod
    def get_default_template(cls, name='DEFAULT_TEMPLATE', site=None):
        site = site or Site.app_site()
        return Template.objects.get_or_create(site=site, name=name,)[0]

    def render(self, *args, **kwargs):
        '''
            :param kwargs: Context dictionary
        '''
        return tuple([template.Template(t).render(template.Context(kwargs))
                      for t in [self.subject, self.text]])

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = (('site', 'name'),)
        verbose_name = _(u'Template')
        verbose_name_plural = _(u'Templates')


@deconstructible
class Targetting(models.Model):
    '''  '''
    site = models.ForeignKey(Site, verbose_name=_(u'Owner Site'))
    ''' Owner Site'''

    targetter_content_type = models.ForeignKey(
        ContentType,
        related_name="targetter")
    ''' targetter model class'''

    targetter_object_id = models.PositiveIntegerField()
    ''' tragetter object id '''

    targetter = generic.GenericForeignKey(
        'targetter_content_type',
        'targetter_object_id')
    ''' targgetter instance '''

    mediator_content_type = models.ForeignKey(
        ContentType,
        related_name="mediator")
    ''' mediator model class'''

    mediator_object_id = models.PositiveIntegerField()
    ''' mediator object id '''

    mediator = generic.GenericForeignKey('mediator_content_type',
                                         'mediator_object_id')
    ''' mediator instance '''

    def __unicode__(self):
        return self.targetter.__unicode__()


class CircleManager(models.Manager):

    def find_for_domain(self, domain, symbol=None):
        q = {'site__domain': domain}
        if symbol is None or symbol == '':
            q['is_default'] = True
        else:
            q['symbol'] = symbol
        return self.get(**q)

    def accessible_list(self, user):
        return self.filter(
            Q(membership__member__user=user) | Q(is_secret=False)
        ).distinct()

    def of_user(self, user):
        return self.filter(membership__member__user=user)

    def of_user_exclusive(self, user):
        return self.exclude(membership__member__user=user)

    def of_admin(self, user):
        return self.filter(membership__member__user=user,
                           membership__is_admin=True)


@deconstructible
class Circle(models.Model):
    ''' Circle
    '''
    site = models.ForeignKey(
        Site, verbose_name=_(u'Owner Site'))
    ''' Owner Site'''

    name = models.CharField(
        _(u'Circle Name'), max_length=100, db_index=True)
    ''' Circle Name '''

    description = models.TextField(
        _(u'Circle Description'), null=True, default=None, blank=True)

    symbol = models.CharField(
        _(u'Circle Symbol'), max_length=100, db_index=True,
        help_text=_(u'Circle Symbol Help Text'), )
    ''' Symbol '''

    is_default = models.BooleanField(
        _(u'Is Default Circle'), default=False,
        help_text=_('Is Default Circle Help'),)
    ''' Site's Default Circle or not '''

    is_moderated = models.BooleanField(
        _(u'Is Moderated Circle'),
        default=True, help_text=_('Is Moderated Circle Help'), )
    ''' True: Only operators(Membership.is_admin True)
    can circulate their message.'''

    is_secret = models.BooleanField(
        _(u'Is Secret Circle'),
        default=False, help_text=_('Is Secret Circle Help'), )
    ''' True: only membership users know its existence '''

    objects = CircleManager()

    def __unicode__(self):
        return "%s of %s" % (self.name, self.site.__unicode__())

    @property
    def main_address(self):
        return "%s@%s" % (self.symbol, self.site.domain)

    @property
    def domain(self):
        return self.site.domain

    def save(self, **kwargs):
        if self.is_default:
            self.site.circle_set.update(is_default=False)
        else:
            query = () if self.id is None else (~Q(id=self.id), )
            if self.site.circle_set.filter(
                    is_default=True, *query).count() < 1:
                self.is_default = True

        super(Circle, self).save(**kwargs)

    def is_admin_user(self, user):
        return user.is_superuser or self.membership_set.filter(
            member__user=user, is_admin=True).exists()

    def is_admin(self, user):
        return user.is_superuser or self.membership_set.filter(
            member__user=user, is_admin=True).exists()

    def is_operator(self, user):
        return user.is_superuser or self.membership_set.filter(
            member__user=user, is_admin=True).exists()

    def is_member(self, user):
        return self.membership_set.filter(
            member__user=user, is_admitted=True).exists()

    @property
    def memberships(self):
        return self.membership_set.all()

    def membership_for_user(self, user):
        try:
            return self.membership_set.get(member__user=user)
        except:
            return None

    @property
    def memberships_unadmitted(self):
        return self.membership_set.filter(is_admitted=False)

    def are_member(self, users):
        ''' all users are member of this Circle '''
        return all(
            map(lambda u: self.membership_set.filter(member__user=u).exists(),
                users))
        pass

    def any_admin(self):
        try:
            admin_list = self.membership_set.filter(is_admin=True)
            if admin_list.count() > 0:
                return admin_list[0]

            return User.objects.filter(is_superuser=True)[0]
        except Exception:
            logger.debug(traceback.format_exc())

        return None

    def add_member(self, member, is_admin=False, is_admitted=False):
        membership, created = Membership.objects.get_or_create(circle=self,
                                                               member=member)
        membership.is_admin = is_admin
        membership.is_admitted = is_admitted
        membership.save()
        return membership

    class Meta:
        unique_together = (
            ('site', 'name'),
            ('site', 'symbol'),)
        verbose_name = _(u'Circle')
        verbose_name_plural = _(u'Circles')


@deconstructible
class Member(models.Model):
    ''' Member

        - a system user can have multiple personality
    '''
    user = models.ForeignKey(User, verbose_name=_(u'System User'))
    ''' System User '''

    address = models.CharField(_(u'Forward address'),
                               max_length=100, unique=True)
    ''' Email Address
    '''
    is_active = models.BooleanField(_(u'Actaive status'), default=False)
    ''' Active Status '''

    bounces = models.IntegerField(_(u'Bounce counts'), default=0)
    ''' Bounce count'''

    circles = models.ManyToManyField(Circle,
                                     through='Membership',
                                     verbose_name=_(u'Opt-in Circle'))
    ''' Opt-In Circles'''

    def __unicode__(self):
        return "%s(%s)" % (
            self.user.__unicode__() if self.user else "unbound user",
            self.address if self.address else "not registered",
        )

    def reset_password(self, active=False):
        ''' reset password '''
        newpass = User.objects.make_random_password()
        self.user.set_password(newpass)
        self.user.is_active = active
        self.user.save()
        return newpass

    def get_absolute_url(self):
        ''' Django API '''
        return None
        # return self.user.get_absolute_url() if self.user else None

    class Meta:
        verbose_name = _(u'Member')
        verbose_name_plural = _(u'Members')


@deconstructible
class Membership(models.Model):
    member = models.ForeignKey(Member, verbose_name=_(u'Member'))
    ''' Member ( :ref:`paloma.models.Member` ) '''
    circle = models.ForeignKey(Circle, verbose_name=_(u'Circle'))
    ''' Circle ( :ref:`paloma.models.Circle` )'''

    is_admin = models.BooleanField(_(u'Is Circle Admin'), default=False)

    is_admitted = models.BooleanField(
        _(u'Is Membership Admitted'),
        default=False,
        help_text=_(u'Is Membership Admitted Help'))
    ''' Member must be admitted by a Circle Admin to has a Membership '''

    def is_member_active(self):
        return self.member.is_active

    is_member_active.short_description = _(u"Is Member Active")

    def is_user_active(self):
        return self.member.user.is_active

    is_user_active.short_description = _(u"Is User Active")

    def user(self):
        return self.member.user

    def __unicode__(self):
        return "%s -> %s(%s)" % (
            self.member.__unicode__() if self.member else "N/A",
            self.circle.__unicode__() if self.circle else "N/A",
            _(u"Circle Admin") if self.is_admin else _(u"General Member"),)

    def get_absolute_url(self):
        ''' Django API '''
        # if self.member and self.member.user:
        #     return self.member.user.get_absolute_url()

        return None

    class Meta:
        unique_together = (('member', 'circle', ), )
        verbose_name = _(u'Membership')
        verbose_name_plural = _(u'Memberships')

PUBLISH_STATUS = (
    ('pending', _('Pending')),
    ('scheduled', _('Scheduled')),
    ('active', _('Active')),
    ('finished', _('Finished')),
    ('canceled', _('Canceled')),)


@deconstructible
class Publish(models.Model):
    ''' Message Delivery Publish'''

    site = models.ForeignKey(Site, verbose_name=_(u'Site'),)
    ''' Site '''

    publisher = models.ForeignKey(User, verbose_name=_(u'Publisher'))
    ''' publisher '''

    messages = models.ManyToManyField('Message',
                                      through="Publication",
                                      verbose_name=_("Messages"),
                                      related_name="message_set",)

    subject = models.CharField(_(u'Subject'), max_length=101,)
    ''' Subject '''

    text = models.TextField(_(u'Text'), )
    ''' Text '''

    circles = models.ManyToManyField(Circle, verbose_name=_(u'Target Circles'))
    ''' Circle'''

    task_id = models.CharField(_(u'Task ID'),
                               max_length=40, default=None,
                               null=True, blank=True,)
    ''' Task ID  '''

    status = models.CharField(_(u"Publish Status"), max_length=24,
                              db_index=True,
                              help_text=_('Publish Status Help'),
                              default="pending", choices=PUBLISH_STATUS)

    dt_start = models.DateTimeField(
        _(u'Time to Send'),
        help_text=_(u'Time to Send Help'),
        null=True, blank=True, default=now)
    ''' Stat datetime to send'''

    activated_at = models.DateTimeField(
        _(u'Task Activated Time'),
        help_text=_(u'Task Activated Time Help'),
        null=True, blank=True, default=None)
    ''' Task Activated Time '''

    forward_to = models.CharField(
        _(u'Forward address'),
        max_length=100, default=None, null=True, blank=True)
    ''' Forward address for incomming email '''

    targettings = generic.GenericRelation(
        Targetting,
        verbose_name=_('Optional Targetting'),
        object_id_field="mediator_object_id",
        content_type_field="mediator_content_type")

    def __unicode__(self):
        if self.dt_start:
            return self.subject + self.dt_start.strftime(
                "(%Y-%m-%d %H:%M:%S) by " + self.publisher.__unicode__())
        else:
            return self.subject + "(now)"

    def get_context(self, circle, user):
        context = {}
        for ref in self._meta.get_all_related_objects():
            if ref.model in AbstractProfile.__subclasses__():
                try:
                    context.update(
                        getattr(self,
                                ref.var_name).target_context(circle, user)
                    )
                except Exception:
                    pass
        return context

    def target_members_for_user(self, user):
        return Member.objects.filter(
            membership__circle__in=self.circles.all(),
            user=user)

    @property
    def is_timeup(self):
        return self.dt_start is None or self.dt_start <= now()

    @property
    def task(self):
        try:
            return AsyncResult(self.task_id)
        except:
            return None

    class Meta:
        verbose_name = _(u'Publish')
        verbose_name_plural = _(u'Publish')


####
class JournalManager(models.Manager):
    ''' Message Manager'''
    def handle_incomming_mail(self, sender, is_jailed, recipient, mssage):
        '''
            :param mesage: :py:class:`email.Message`
        '''
        pass


@deconstructible
class Journal(models.Model):
    ''' Raw Message

    '''
    dt_created = models.DateTimeField(
        _(u'Journaled Datetime'),
        help_text=_(u'Journaled datetime'), auto_now_add=True)
    ''' Journaled Datetime '''

    sender = models.CharField(u'Sender', max_length=100)
    ''' sender '''

    recipient = models.CharField(u'Receipient', max_length=100)
    ''' recipient '''

    text = models.TextField(
        _(u'Message Text'), default=None, blank=True, null=True)
    ''' Message text '''

    is_jailed = models.BooleanField(_(u'Jailed Message'), default=False)
    ''' Jailed(Reciepient missing emails have been journaled) if true '''

    def mailobject(self):
        ''' return mail object

            :rtype: email.message.Message
        '''
        return message_from_string(self.text)

    class Meta:
        verbose_name = _(u'Journal')
        verbose_name_plural = _(u'Journals')

    def forwards(self):
        return Alias.objects.filter(address=self.recipient)

    def forward_from(self):
        return "jfwd-{0}@{1}".format(
            self.id,
            self.recipient.split('@')[1],
        )


try:
    from rsyslog import Systemevents, Systemeventsproperties
    Systemevents()
    Systemeventsproperties()
except:
    pass


@deconstructible
class MessageManager(models.Manager):

    def create_from_template(self,
                             member_or_recepient,
                             template_name,
                             params={},
                             message_id=None,
                             circle=None):
        ''' Create Message from specified Template '''

        template_name = template_name.lower()
        msg = {
            'circle': circle,
        }

        member = None
        recipient = None
        if type(member_or_recepient) == Member:
            member = member_or_recepient

        elif type(member_or_recepient) == Membership:
            member = member_or_recepient.member
            circle = member_or_recepient.circle
        else:   # str
            recipient = member_or_recepient

        site = msg['circle'].site if msg['circle'] else Site.app_site()

        # load tempalte from storage
        template = Template.objects.get_template(site=site,
                                                 name=template_name)
        message_id = message_id or \
            "msg-%s-%s@%s" % (template_name, MDT(), site.domain)

        #  create
        try:
            mail, created = self.get_or_create(mail_message_id=message_id)
            mail.cirlce = circle
            mail.template = template
            mail.member = member
            mail.recipient = recipient
            mail.render(**params)
            mail.save()

            return mail
        except Exception, e:
            for err in traceback.format_exc().split('\n'):
                logger.debug('send_template_mail:error:%s:%s' % (str(e), err))

        return None


@deconstructible
class Message(models.Model):
    ''' Message '''

    mail_message_id = models.CharField(u'Message ID', max_length=100,
                                       db_index=True, unique=True)
    ''' Mesage-ID header - 'Message-ID: <local-part "@" domain>' '''

    template = models.ForeignKey(Template, verbose_name=u'Template',
                                 null=True, on_delete=models.SET_NULL)
    ''' Message Template '''

    member = models.ForeignKey(Member, verbose_name=u'Member',
                               null=True, default=None, blank=True,
                               on_delete=models.SET_NULL)
    ''' Recipient Member (member.circle is Sender)'''

    circle = models.ForeignKey(Circle, verbose_name=u'Circle',
                               null=True, default=None,
                               on_delete=models.SET_NULL)
    ''' Target Circle ( if None, Site's default circle is used.)'''

    recipient = models.EmailField(u'recipient', max_length=50,
                                  default=None, blank=True, null=True)
    ''' Recipient  (for non-Member )'''

    subject = models.TextField(u'Message Subject', default=None,
                               blank=True, null=True)
    ''' Message Subject '''

    text = models.TextField(_(u'Message Text'), default=None,
                            blank=True, null=True)
    ''' Message text '''

    status = models.CharField(u'Status', max_length=50,
                              default=None, blank=True, null=True)
    ''' SMTP Status '''

    task_id = models.CharField(u'Task ID', max_length=40,
                               default=None, null=True, blank=True, )
    ''' Task ID  '''

    checked = models.BooleanField(_(u'Mail Checked'), default=False, )

    created = models.DateTimeField(_(u'Created'), auto_now_add=True)
    updated = models.DateTimeField(_(u'Updated'), auto_now=True)
    smtped = models.DateTimeField(_(u'SMTP Time'),
                                  default=None, blank=True, null=True)

    parameters = models.TextField(
        blank=True, null=True, )
    ''' extra parameters '''

    _context_cache = None
    ''' Base Text'''

    objects = MessageManager()

    def __init__(self, *args, **kwargs):
        super(Message, self).__init__(*args, **kwargs)
        if self.template is None:
            self.template = Template.get_default_template()

    def __unicode__(self):
        try:
            return self.template.__unicode__() + str(self.recipients)
        except:
            return unicode(self.id)

    @property
    def task(self):
        try:
            return AsyncResult(self.task_id)
        except:
            return None

    @property
    def recipients(self):       # plural!!!!
        return [self.recipient] if self.recipient else [self.member.address]

    def context(self, **kwargs):
        '''  "text" and "subject" are rendered with this context

            - member    : paloma.models.Member
            - template  : paloma.models.Template
            - kwargs    : extra parameters
            - [any]     : JSON serialized dict save in "parameters"
        '''
        ret = {"member": self.member, "template": self.template, }
        ret.update(kwargs)
        try:
            ret.update(json.loads(self.parameters))
        except:
            pass
        return ret

    def render(self, do_save=True, **kwargs):
        ''' render for member in circle'''
        if self.template:
            self.text = template.Template(
                self.template.text
            ).render(template.Context(self.context(**kwargs)))

            self.subject = template.Template(
                self.template.subject
            ).render(template.Context(self.context(**kwargs)))

            if do_save:
                self.save()

    @property
    def from_address(self):
        circle = self.circle or self.template.site.default_circle
        return circle.main_address

    @property
    def return_path(self):
        ''' default return path '''
        return make_return_path({"command": "msg", "message_id": self.id,
                                 "domain": self.template.site.domain})

    def set_status(self, status=None, smtped=None, do_save=True):
        self.smtped = smtped
        self.status = status
        if do_save:
            self.save()

    @classmethod
    def update_status(cls, msg, **kwargs):
        for m in cls.objects.filter(
                mail_message_id=kwargs.get('message_id', '')):
            m.set_status(msg, now())

    class Meta:
        verbose_name = _(u'Message')
        verbose_name_plural = _(u'Messages')


@deconstructible
class Provision(models.Model):
    ''' Account Provision management
    '''

    member = models.OneToOneField(Member, verbose_name=_(u'Member'),
                                  on_delete=models.SET_NULL,
                                  null=True, default=None, blank=True)
    ''' Member'''

    status = models.CharField(_(u"Provision Status"),
                              max_length=24, db_index=True,)
    ''' Provisioning  Status'''

    circle = models.ForeignKey(Circle, verbose_name=_(u'Circle'),
                               null=True, default=None, blank=True,
                               on_delete=models.SET_NULL)
    ''' Circle'''

    inviter = models.ForeignKey(User, verbose_name=_(u'Inviter'),
                                null=True, default=None, blank=True,
                                on_delete=models.SET_NULL)
    ''' Inviter'''

    prospect = models.CharField(_(u'Provision Prospect'),
                                max_length=100, default=None,
                                null=True, blank=True)
    ''' Prospect Email Address'''

    secret = models.CharField(
        _(u'Provision Secret'),
        max_length=100,
        default='',
        unique=True)
    ''' Secret
    '''
    short_secret = models.CharField(
        _(u'Provision Short Secret'),
        max_length=10, unique=True,
        default='')
    ''' Short Secret
    '''

    url = models.CharField(_(u'URL for Notice'),
                           max_length=200, default=None, null=True, blank=True)
    ''' URL for notice '''

    dt_expire = models.DateTimeField(
        _(u'Provision Secret Expired'),
        null=True, blank=True,
        default=None,
        help_text=u'Secrete Expired', )
    ''' Secrete Expired'''

    dt_try = models.DateTimeField(_(u'Provision Try Datetime'),
                                  null=True, blank=True, default=None,
                                  help_text=u'Try Datetime', )
    ''' Try Datetime'''

    dt_commit = models.DateTimeField(_(u'Commit Datetime'),
                                     null=True, blank=True, default=None,
                                     help_text=u'Commit Datetime', )
    ''' Commit Datetime'''

    def __init__(self, *args, **kwargs):
        super(Provision, self).__init__(*args, **kwargs)

        self.dt_expire = self.dt_expire or expire()
        self.secret = self.secret or create_auto_secret()
        self.short_secret = self.short_secret or create_auto_short_secret()

    def is_open(self, dt_now=None):
        ''' check if this is open status or not
        '''
        dt_now = dt_now if dt_now else now()

        return (self.dt_commit is None) and \
               (self.dt_expire > dt_now) and  \
               (self.mailbox is not None) and  \
               (self.group is not None)

    def close(self):
        ''' close this enroll management
        '''
        self.dt_commit = now()
        self.save()

    def provided(self, user, address, is_active=True):
        self.member = Member.objects.get_or_create(
            user=user, address=address)[0]
        self.member.is_active = is_active
        self.member.save()
        if self.circle:
            membership, created = Membership.objects.get_or_create(
                circle=self.circle, member=self.member)
            membership.is_admitted = is_active
            membership.save()

        self.dt_commit = now()
        self.save()
        return membership

    def reset(self, save=False):
        self.secret = create_auto_secret()
        self.short_secret = create_auto_short_secret()
        self.dt_commit = None
        self.dt_expire = expire()
        if save:
            self.save()

    def send_response(self):
        '''  send response mail
        '''
        from paloma.tasks import send_templated_message

        mail_message_id = u"%s-up-%d@%s" % (self.circle.symbol,
                                            self.id,
                                            self.circle.site.domain)
        name = "provision_%s" % self.status
        recipient = self.member and self.member.address or self.prospect
        send_templated_message(
            recipient,
            name,
            params={'provision': self},
            message_id=mail_message_id,
        )
        logger.debug(_('Provision %(provision)s is sent for %(to)s') % {
            "provision": name,
            "to": str(recipient)})

    class Meta:
        verbose_name = _('Provision')
        verbose_name_plural = _('Provisions')


class PublicationManager(models.Manager):

    def publish(self, publish, circle, member, signature='pub'):
        assert all([publish, circle, member])
        msgid = "<%s-%d-%d-%d@%s>" % (
            signature, publish.id,
            circle.id, member.id, circle.domain)

        ret, created = self.get_or_create(
            publish=publish,
            message=Message.objects.get_or_create(
                mail_message_id=msgid,
                template=Template.get_default_template('PUBLICATION'),
                circle=circle,
                member=member,)[0]  # (object,created )
        )

        ret.render()
        ret.save()
        return ret


@deconstructible
class Publication(models.Model):
    ''' Each Published Item

    '''
    publish = models.ForeignKey(Publish, verbose_name=_(u'Publish'))
    ''' Mail Schedule'''

    message = models.ForeignKey(Message, verbose_name=_(u'Mail Message'))
    ''' Message '''

    objects = PublicationManager()

    def context(self, **kwargs):
        ret = self.message.context(**kwargs)
        ret['publish'] = self.publish

        #: Circle & Member Targetting
        ret.update(
            AbstractProfile.target(self.message.circle, self.message.member)
        )

        #:AdHoc Targetting
        for t in self.publish.targettings.all():
            try:
                ret.update(t.target(self))
            except:
                pass
        return ret

    def render(self, **kwargs):
        ''' render for member in circle'''
        self.message.text = template.Template(
            self.publish.text
        ).render(template.Context(self.context(**kwargs)))

        self.message.subject = template.Template(
            self.publish.subject
        ).render(template.Context(self.context(**kwargs)))

        self.message.save()
