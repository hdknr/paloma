# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string
from django.conf import settings 
from django.contrib.auth.models import User 


from optparse import make_option
from datetime import datetime
import commands
import os

from . import GenericCommand
from ...models import Site
from ...tasks import enqueue_publish,enqueue_mails_for_publish

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
        if options['sync']:
            print "Enqueue mails of a publish",publish_id,"Synchronously"
            enqueue_mails_for_publish('manage', publish_id,False)
        else:
            print "Enqueue mails of a publish",publish_id,"Asynchronously"
            enqueue_mails_for_publish.apply_async('manage',publish_id )
