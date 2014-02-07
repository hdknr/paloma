# -*- coding: utf-8 -*-

from paloma.management.commands import GenericCommand

from ...tasks import journalize, process_journal

import logging
import traceback
log = logging.getLogger('paloma')


class Command(GenericCommand):
    ''' bouncer
    '''
    option_list = GenericCommand.option_list + ()

    def handle_test(self, *args, **options):
        ''' simple testing '''
        import uuid
        msg = "running bouncer:signature=%s" % uuid.uuid1().hex
        print "logging as:\n", msg
        log.debug(msg)

    def handle_main(self, *args, **options):
        ''' main '''

        import sys
        if sys.stdin.isatty():
            #: no stdin
            log.warn('no stdin')
            return

        is_jailed = options.get('is_jailed', False)

        jid = journalize(args[0], args[1],
                         ''.join(sys.stdin.read()), is_jailed)
        #:message journalized

        try:
            log.debug("bouncer.handle_main:process journal =%d" % jid)
            process_journal.delay(jid)      #: defualt is async
        except:
            for err in traceback.format_exc().split('\n'):
                log.error("bouncer.handle_main:%s" % err)

    def handle_jail(self, *args, **options):
        ''' jail'''
        from paloma import report
        report('jailed')
        options['is_jailed'] = True
        self.handle_main(*args, **options)
