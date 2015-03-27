# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string
from django.conf import settings 
from django.contrib.auth.models import User 
from django.utils.timezone import datetime

from optparse import make_option
from datetime import datetime
import commands
import os

from . import GenericCommand
from ...models import Site
from ...tasks import enqueue_publish,enqueue_mails_for_publish
from ...utils import make_eta

class Command(GenericCommand):
    ''' paloma Publish controller
    '''

    def handle_enqueue(self,*args,**options):
        '''　enqueue messages from Publish

        '''
        if options['sync']:
            print "Enqueue a publish",args[0],"Synchronously"
            enqueue_publish('manage',args[0])
        else:
            print "Enqueue a publish",args[0],"Asynchronously"
            enqueue_publish.apply_async('manage',args[0])

    def handle_enqueue_mails(self,publish_id,*args,**options):
        '''　enqueue messages from Publish

        '''
        eta_format='%y-%m-%d  %H:%M'

        if options['sync']:
            print "Enqueue mails of a publish",publish_id,"Synchronously"
            enqueue_mails_for_publish('manage', publish_id,False)

        elif options['eta']:
            print "Enqueue mails of a publish",publish_id,"Asynchronously for ",options['eta']
            try:
                task=enqueue_mails_for_publish.apply_async(
                    ( 'manage',publish_id, ),
                    eta=  make_eta( datetime.strptime( options['eta'],eta_format ) )
                )
                print task
            except Exception,e:
                print e, eta_format

        else:
            print "Enqueue mails of a publish",publish_id,"Asynchronously"
            enqueue_mails_for_publish.delay('manage',publish_id )
