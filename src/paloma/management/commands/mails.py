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
from ...models import Mail
#from ...tasks import enqueue_publish,enqueue_mails_for_publish

class Command(GenericCommand):
    ''' paloma Mail controller
    '''

    def handle_reset(self,mail_id,*args,**options):
        '''　   reset mail

        '''
        Mail.objects.get(id=mail_id).set_status()

    def handle_send(self,mail_id,*args,**options):
        mail = Mail.objects.get(id=mail_id)
