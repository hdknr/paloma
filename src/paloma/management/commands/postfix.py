# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string
from django.conf import settings 

from optparse import make_option
from datetime import datetime
import commands
import os

from . import GenericCommand

JAIL='jail'
MAIN=getattr(settings,"PALOMA_NAME","paloma")
POSTFIX_PATH='/etc/postfix'
POSTFIX_CONF=['main.cf','master.cf',]
POSTFIX_VIRTUAL_MYSQL_PATH=os.path.join(POSTFIX_PATH,'virtual/mysql',)
POSTFIX_VIRTUAL_MYSQL_CONF=[ 'alias.cf','domain.cf','mailbox.cf','transport.cf', ]

BOUNCER=os.path.join( os.environ.get('VIRTUAL_ENV','') ,"bin/paloma_bouncer.py" )
# TODO:  Should think of the case of virtualenv is not available

SETTINGS_MODULE= os.environ['DJANGO_SETTINGS_MODULE']
PROJECT_DIR = os.path.dirname( __import__( SETTINGS_MODULE).__file__ )

class Command(GenericCommand):
    ''' paloma postfix management
    '''
    args = ''
    help = ''

    option_list = GenericCommand.option_list + (
            make_option('--virtual-path',
            action='store',
            dest='virtual-path',
            default= POSTFIX_VIRTUAL_MYSQL_PATH,
            help=u'Postfix Virtual Path'),

            make_option('--postfix-database',
            action='store',
            dest='postfix-database',
            default='default',
            help=u'Postfix Virtual Database Configuration Name in settings.py'),

            make_option('--postfix-path',
            action='store',
            dest='postfix-path',
            default= POSTFIX_PATH,
            help=u'Linux Postfix setting path '),

            make_option('--conf-path',
            action='store',
            dest='conf-path',
            default= ".",
            help=u'Generated Configuration Path'),

            make_option('--user',
            action='store',
            dest='user',
            default= "system",
            help=u'Unix User who runs BOUNCER script'),

            make_option('--bouncer',
            action='store',
            dest='bouncer',
            default= "system",
            help=u'Full Path of Bouncer Script'),

            make_option('--default-transport',
            action='store',
            dest='default-transport',
            default= JAIL,
            help=u'Postfix Default Transport'),

            make_option('--doamin-transport',
            action='store',
            dest='domain-transport',
            default= MAIN,
            help=u'Postfix Acceptable Domains Transport'),
        )
    ''' Command Option '''

    def handle_qlist(self,*args,**options):
        '''　qlist
'''
        import commands
        import re
        item = [ 
                r'^(?P<id>.+)',
                r'(?P<size>\d+)',
                r'(?P<day>.+)',
                r'(?P<month>.+)',
                r'(?P<date>\d+)',
                r'(?P<time>\d{2}:\d{2}:\d{2})',
                r'(?P<from>.+)$',
            ]
        pat = re.compile('\\s' .join(item))

        for l in commands.getoutput('mailq').split('\n'):
            s = pat.search(l)  
            if s : 
                print l

    def handle_delete(self,*args,**options):
        ''' delete message from queue '''
        options['id']= options['id'].replace('*','')
        print commands.getoutput('sudo  postsuper -d %(id)s' % options )
        
        '''  help
        '''
        import re
        for i in dir(self):
            m = re.search('^handle_(.*)$',i)
            if m == None:
                continue
            print m.group(1)

    def handle_config(self,*args,**options):

        context ={}
        context['POSTFIX_PATH'] = os.path.join( os.path.abspath(options['conf-path']), 
                        options['postfix-path'].replace('/','',1) )

        context['VIRTUAL_PATH'] = os.path.join( os.path.abspath(options['conf-path']), 
                        options['virtual-path'].replace('/','',1) )

        if os.path.isdir( context['VIRTUAL_PATH'] ) ==False:
            os.makedirs( context['VIRTUAL_PATH'] )

        context['SETTINGS_MODULE'] = SETTINGS_MODULE 
        context['PROJECT_DIR'] = PROJECT_DIR
        context['DEFAULT_TRANSPORT'] = options['default-transport']
        context['DOMAIN_TRANSPORT'] = options['domain-transport']
        context['BOUNCER'] = BOUNCER

        #:MySQL database configuration
        for k,v in settings.DATABASES[options['postfix-database']].items():
            context['DB%s' % k] = v
        
        for c in POSTFIX_VIRTUAL_MYSQL_CONF:
            #: Postfix Virtula Path
            context['MYSQL_%s' % c.split('.')[0].upper()] = os.path.join( options['virtual-path'],c)

            #: Generate Virtual Configuration
            conf_file = open( os.path.join( context['VIRTUAL_PATH'], c), "w")
            conf_file.write(  
                render_to_string("conf/%s/%s" % (options['virtual-path'],c),context)
            )
            conf_file.close()

        for c in POSTFIX_CONF:
            #: Generate Virtual Configuration
            print "Generating:",c
            conf_file = open( os.path.join( context['POSTFIX_PATH'] , c), "w")
            conf_file.write(  
                render_to_string("conf/%s/%s" % (options['postfix-path'],c),context)
            )
            conf_file.close()

    def handle_setconfig(self,*args,**options):
        pass

    def provide_context (self,*args,**options):

        context ={}
        context['POSTFIX_PATH'] = os.path.join( os.path.abspath(options['conf-path']), 
                        options['postfix-path'].replace('/','',1) )

        context['VIRTUAL_PATH'] = os.path.join( os.path.abspath(options['conf-path']), 
                        options['virtual-path'].replace('/','',1) )

        if os.path.isdir( context['VIRTUAL_PATH'] ) ==False:
            os.makedirs( context['VIRTUAL_PATH'] )

        context['SETTINGS_MODULE'] = SETTINGS_MODULE 
        context['PROJECT_DIR'] = PROJECT_DIR
        context['DEFAULT_TRANSPORT'] = options['default-transport']
        context['DOMAIN_TRANSPORT'] = options['domain-transport']
        context['BOUNCER'] = BOUNCER

        #:MySQL database configuration
        for k,v in settings.DATABASES[options['postfix-database']].items():
            context['DB%s' % k] = v
        
        for c in POSTFIX_VIRTUAL_MYSQL_CONF:
            #: Postfix Virtula Path
            context['MYSQL_%s' % c.split('.')[0].upper()] = os.path.join( options['virtual-path'],c)


        return context
