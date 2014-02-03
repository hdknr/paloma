# -*- coding: utf-8 -*-
from . import GenericCommand
from ...models import Journal
from ...tasks import process_journal


class Command(GenericCommand):
    ''' paloma postfix management
    '''

    option_list = GenericCommand.option_list + ()
    ''' Command Option '''

    def handle_process(self, id, *args, **options):
        '''　process journals
        '''

        try:
            process_journal(id)

        except Journal.DoesNotExist:
            print "Journal id=", id, "was not found"

        except Exception, e:
            print "Error:", e

    def handle_list(self, count=10, *args, **options):
        for j in Journal.objects.order_by('-id'):
            if j.is_jailed:
                print j.id, j.dt_created, j.sender, j.recipient, "Jailed"
