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


class Command(GenericCommand):
    ''' paloma postfix management
    '''
    args = ''
    help = ''

    option_list = GenericCommand.option_list + (
        )
    ''' Command Option '''

    def handle_add(self,name,domain,*args,**options):
        '''　add Site
        '''
         
        obj ,created= Site.objects.get_or_create(name=name,domain=domain )
        print obj,created

        map( lambda u : obj.operators.add(u), User.objects.filter(is_superuser=True))
