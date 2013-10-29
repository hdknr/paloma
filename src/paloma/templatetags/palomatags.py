# -*- coding: utf-8 -*-
from django import template
from django.db.models import Model,Manager
from django.contrib.auth.models import User
from django.template.base import Node,token_kwargs
from django.utils import six        #: for Python 3
#
import re

from paloma.models import Site,Circle

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


##

class IfAdminNode(Node):
    def __init__(self, user,circle,nodelist, extra_context=None):
        self.nodelist = nodelist
        # var and name are legacy attributes, being left in case they are used
        # by third-party subclasses of this Node.
        self.extra_context = extra_context or {}
        self.user_var = user
        self.circle_var = circle

    def __repr__(self):
        return "<IfAdminNode>"

    def render(self, context):
        #:コンテキストに追加する変数を容姿
        values = dict([(key, val.resolve(context)) for key, val in
                       six.iteritems(self.extra_context)])
        #:コンテキストに反映
        context.update(values)

        user = self.user_var.resolve(context)
        circle = self.circle_var.resolve(context)

        assert isinstance(user,User)
        assert isinstance(circle,Circle)

        if circle.is_admin(user) :
            print "@@@@@@@ is admin"
            output =  self.nodelist.render(context)
        else :
            print "@@@@@@@ is not admin"
            output =  ""
        #:ブロックタグに挟まれているテンプレートをレンダリング
        #:権限があるときだけレンダリングする
        
        context.pop()
        #:抜く

        return  output

@register.tag(name='ifadmin')
def tag_ifadmin(parser, token,*args,**kwargs):
    try:
        bits = token.split_contents()
        remaining_bits = bits[1:]
        extra_context = token_kwargs(remaining_bits, parser, support_legacy=True)

        user   = template.Variable(remaining_bits[0] )
        circle = template.Variable(remaining_bits[1] ) 
        
        nodelist = parser.parse(('endifadmin',))
        #:終了ブロックまで読み込み

        parser.delete_first_token()      
        #:これを呼ばないと,{% endallowed%} が別のブロックタグとして解釈されてしまう

        return IfAdminNode(user,circle,nodelist,extra_context=extra_context)

    except:
        print traceback.format_exc()
        pass

