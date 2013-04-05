# -*- coding: utf-8 -*-
from django.conf import settings 
from django.contrib.auth.models import User 

from optparse import make_option
from datetime import datetime
import commands
import os

from . import GenericCommand
from ...models import Journal
from ...tasks import process_journal


class Command(GenericCommand):
    ''' paloma postfix management
    '''

    option_list = GenericCommand.option_list + (
        )
    ''' Command Option '''

    def handle_process(self,journal_id,*args,**options):
        '''　process journals
        '''
        
        try:
            process_journal(journal_id)
        except Journal.DoesNotExist,e:
            print journal_id , "was not found"

        except Exception,e:
            print "Error:",e

    def handle_list(self,count=10,*args,**options):
        for j in Journal.objects.order_by('-id'): 
            print j.id ,j.dt_created,j.sender, j.recipient, "Jailed" if j.is_jailed else ""
