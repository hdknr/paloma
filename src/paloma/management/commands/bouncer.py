# -*- coding: utf-8 -*-

from paloma.management.commands import GenericCommand
from optparse import make_option
from datetime import datetime

from django.conf import settings

from ...tasks import journalize,process_journal
class Command(GenericCommand):
    ''' bouncer
    '''

    option_list = GenericCommand.option_list + ( 

        make_option('--async',
            action='store',
            dest='async',
            default=True,
            help=u'Process asynchronously with message queue'),

        )   

    def handle_main(self,*args,**options):
        ''' main '''
        from paloma import report 
        import sys
        if sys.stdin.isatty():
            #: no stdin
            report('no stdin')
            return

        is_jailed = options.get('is_jailed',False)

        jid = journalize(args[0],args[1],''.join(sys.stdin.read()),is_jailed ) #:message queuing
        process_journal.delay(jid)
        #: defualt is async

    def handle_jail(self,*args,**options):
        ''' jail'''
        from paloma import report 
        report('jailed')
        options['is_jailed'] = True
        self.handle_main(*args,**options)
