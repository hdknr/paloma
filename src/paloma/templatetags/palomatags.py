# -*- coding: utf-8 -*-
from django import template
from django.db.models import Model,Manager
import re

from paloma.models import Site

# - logging
import logging,traceback
log = logging.getLogger(__name__)
warn = lambda : log.warn(traceback.format_exc() )
#
register = template.Library()

@register.assignment_tag
def membership_for_user(circle,user):
    try:
        return circle.membership_for_user(user)
    except Exception,e:
        return None     

@register.assignment_tag
def app_site():
    ''' application site '''
    return Site.app_site()

@register.assignment_tag
def app_circles(user=None):
    ''' application circles'''
    if user:
        return Site.app_site().circle_set.filter(  
                    membership__member__user = user ).order_by('-is_default')
    return Site.app_site().circle_set.all().order_by('-is_default')
