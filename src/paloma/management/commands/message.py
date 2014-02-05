# -*- coding: utf-8 -*-

from paloma.management.commands import GenericCommand
from paloma.models import Message
from paloma.tasks import enqueue_mail
from paloma.utils import make_eta
from optparse import make_option
from django.utils.timezone import datetime, make_aware
from datetime import timedelta
import re

_opt_time = make_option('--time',
                        action='store',
                        dest='time',
                        default=None,
                        help=u'Time to send a mail message')


class Command(GenericCommand):
    ''' paloma maile management
    '''
    args = ''
    help = ''
    model = Message

    option_list = GenericCommand.option_list + (_opt_time, )

    ''' Command Option '''

    def handle_remove(self, *args, **options):
        '''　remove messages

        '''
        if options['id'] and options['id'].isdigit():
            try:
                Message.objects.get(id=options['id']).delete()
            except Exception, e:
                print "*** Cant remove message for ", options['id']
                print e
        else:
            Message.objects.all().delete()

    def handle_create_from_template(self, address, name, *args, **options):
        msg = Message.objects.create_from_template(address,
                                                   name, params=options)
        print "create message id=", msg.id

    def handle_enqueue(self, id, time, async=True, *args, **options):
        print "@@@ enqueuing message id=", id, time
        msg = Message.objects.get(id=id)

        if async in ['False', False]:
            async = False

        if time is None:
            enqueue_mail(mail_obj=msg, async=async)
            return

        if type(time) == str:
            m = re.search(r"^(?P<number>\d+)(?P<unit>[smh])$", time)
            if m:
                p = m.groupdict()
                d = {{'s': 'seconds',
                      'm': 'minutes',
                      'h': 'hours', }[p['unit']]: int(p['number'])}
                time = datetime.now() + timedelta(**d)
            else:
                time = make_aware(datetime.strptime(time, "%Y-%m-%d %H:%M:%S"))

        enqueue_mail.apply_async((), {'mail_obj': msg},
                                 eta_time=make_eta(time))
