# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string
from django.conf import settings 

from optparse import make_option
from datetime import datetime
import commands
import os
import sys

from . import GenericCommand
from ...models import Domain


DEFAULT_TRANSPORT ='jail'
DOMAIN_TRANSPORT=getattr(settings,"PALOMA_NAME","paloma")
POSTFIX_PATH='/etc/postfix'
POSTFIX_VIRTUAL_PATH= '/etc/postfix/virtual'
POSTFIX_CONF=['main.cf','master.cf',]
POSTFIX_VIRTUAL_MYSQL_PATH=os.path.join(POSTFIX_VIRTUAL_PATH,'mysql',)
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
            default= POSTFIX_VIRTUAL_PATH,
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
            default= DEFAULT_TRANSPORT,
            help=u'Postfix Default Transport'),

            make_option('--domain-transport',
            action='store',
            dest='domain-transport',
            default= DOMAIN_TRANSPORT,
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


    def handle_makeconfig(self,*args,**options):
        ''' create postfix configration files : /etc/postfix
        '''
        context = self.provide_context(*args,**options)
        
        for c in POSTFIX_VIRTUAL_MYSQL_CONF:
            #: Generate Virtual Configuration
            path = os.path.join( context['VIRTUAL_MYSQL_PATH'], c)
            print "\n"*3,"*" * (len(path)+20)
            print "providing:",path 
            print "*" * (len(path)+20) ,"\n" * 3
            conf_file = sys.stdout if options['dryrun'] else  open( path, "w")
            conf_file.write(  
                render_to_string("paloma/conf%s/mysql/%s" % (options['virtual-path'],c),context)
            )
            if not options['dryrun']:
                conf_file.close()

        for c in POSTFIX_CONF:
            #: Generate Virtual Configuration
            path = os.path.join( context['POSTFIX_PATH'] , c)
            print "\n"*3,"*" * (len(path)+20)
            print "Generating:",c
            print "*" * (len(path)+20) ,"\n" * 3
            conf_file = sys.stdout if options['dryrun'] else  open( path  , "w")
            conf_file.write(  
                render_to_string("paloma/conf/%s/%s" % (options['postfix-path'],c),context)
            )
            if not options['dryrun']:
                conf_file.close()

    def handle_print_transport(self,*args,**options):
        ''' print transport configuration for master.cf
        '''
        context = self.provide_context(*args,**options)
        
        print render_to_string("conf/%s/transport.cf" % (options['postfix-path'],),context)

    def handle_setconfig(self,*args,**options):
        context = self.provide_context(*args,**options)

        import commands 
        for c in POSTFIX_CONF:
            #: Generate Virtual Configuration
            print commands.getoutput("sudo ln -s %s %s --force" % ( os.path.join( context['POSTFIX_PATH'] , c), 
                                    os.path.join( POSTFIX_PATH ,c)
                                  ) )
        print commands.getoutput("sudo mkdir -p %s" % POSTFIX_VIRTUAL_PATH ) 
    
        print commands.getoutput("sudo ln -s %s %s --force" % (context['VIRTUAL_MYSQL_PATH'] , POSTFIX_VIRTUAL_MYSQL_PATH ))

    def provide_context (self,*args,**options):
        ''' create context dict
        '''
        context ={}
        context['POSTFIX_PATH'] = os.path.join( os.path.abspath(options['conf-path']), 
                        options['postfix-path'].replace('/','',1) )

        context['VIRTUAL_PATH'] = os.path.join( os.path.abspath(options['conf-path']), 
                        options['virtual-path'].replace('/','',1) )
        context['VIRTUAL_MYSQL_PATH'] =os.path.join( context['VIRTUAL_PATH'],'mysql' )

        if os.path.isdir( context['VIRTUAL_MYSQL_PATH'] ) ==False:
            os.makedirs( context['VIRTUAL_MYSQL_PATH'] )

        context['SETTINGS_MODULE'] = SETTINGS_MODULE 
        context['PROJECT_DIR'] = PROJECT_DIR
        context['DEFAULT_TRANSPORT'] = options['default-transport']
        context['DOMAIN_TRANSPORT'] = options['domain-transport']
        context['BOUNCER'] = BOUNCER
        context['USER'] = options['user']

        #:MySQL database configuration
        for k,v in settings.DATABASES[options['postfix-database']].items():
            context['DB%s' % k] = v

        if context['DBHOST'] == '':
            context['DBHOST'] ='localhost'
        
        for c in POSTFIX_VIRTUAL_MYSQL_CONF:
            #: Postfix Virtula Path
            context['MYSQL_%s' % c.split('.')[0].upper()] = os.path.join( POSTFIX_VIRTUAL_MYSQL_PATH,c)

        return context

    def handle_add_domain(self,*args,**options):
        ''' add hosted domain

            - args[0] : domain name
        '''
        if len(args) <1:
            print "Syntax for adding hosted domain"
            print "manage.py postfix ",self.command, " [[hosted domain]] "
            return

        (new_domain ,created)= Domain.objects.get_or_create(
                        domain=args[0], transport=options['domain-transport'])
        print new_domain,created
