# -*- coding: utf-8 -*-
#
import os

VERSION = (0, 1, 1, 'alpha', 0)

def get_version():
    version = '%d.%d.%d' % (VERSION[0], VERSION[1], VERSION[2])
    return version

def get_logger(name='paloma'): 
    # - Python logging api 
    import logging
    return  logging.getLogger(name)

def report(msg='',exception=None,level='error',name='paloma'):
    ''' error reporting
    '''
    import traceback
    if exception:
        msg = str(exception) + "\n" + str(traceback.format_exc() )
    getattr( get_logger(name) ,level,get_logger().error)( msg )


def run(project_dir):
    import sys,os

    sys.path.append(os.path.dirname( project_dir ) )
    sys.path.append( project_dir )

    #: argv[1] is manage.py command 
    sys.argv[1] = 'bouncer'

    from django.core.management import execute_manager
    import imp
    try:
        imp.find_module('settings') # Assumed to be in the same directory.
    except ImportError:
        import sys
        sys.stderr.write(str(sys.path))
        sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n" % __file__)
        sys.exit(1)
    
    import settings
    
    execute_manager(settings)
