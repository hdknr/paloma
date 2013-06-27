# -*- coding: utf-8 -*-

from django.db.models import AutoField,Sum,Max ,Q
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now
from django.core.mail import send_mail

from django.template import Template,Context

from datetime import datetime,timedelta
import sys,traceback
import re

from utils import create_auto_secret,create_auto_short_secret

import logging
log = logging.getLogger(__name__)

def action(pattern,*dargs,**dkwargs):
    ''' Action Decorator 

        - all "action" function has "action" signature in "func_dict"
     '''
    def receive_func(func):
        import functools
        @functools.wraps(func)
        def wrapper(sender,recipient,journal,*args, **kwargs):
            try:
                kwargs.update( re.search(pattern,recipient).groupdict() )
            except Exception,e:
                log.debug('action execute:' + str(e))
                return False
            #:call action function
            result=func(sender,recipient,journal,*args, **kwargs)
            return result
        wrapper.func_dict['action']=True        #: "action" function signature
        return wrapper
    return receive_func

from django.conf import settings
def process_action(sender,recipient ,journal):
    ''' Execute all "action" until one of them return True

        - moduls specifind PALOMA_ACTIONS in settings.py
    '''
    processed = False #:default not processed
    for actions in getattr(settings,'PALOMA_ACTIONS',[]):
        try:
            processed = any(  getattr(v,'func_dict',{}).get('action',False) == True and v(sender,recipient,journal)
                        for k,v in __import__(actions,{},{},['*'] ).__dict__.items() )
        except Exception,e:
            log.debug('process_action:'+str(e) )
            log.debug( str(e) +  traceback.format_exc().replace('\n','/') )
    #: return action status( True : processed )
    return processed
