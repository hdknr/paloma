# -*- coding: utf-8 -*-
from django import VERSION
from django.db.models.base import ModelBase
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now, get_current_timezone, make_aware
from django.conf import settings
from django.template import TemplateDoesNotExist

if VERSION < (1, 8):
    from django.template.loader import find_template_loader
else:
    from django.template import engine
    find_template_loader = engine.Engine.get_default().template_loaders


import random
import os
import string
from datetime import datetime, timedelta

expire = lambda i=None: now() + \
    timedelta(seconds=getattr(settings, 'PALOMA_EXPIRE', 120))
class_path = lambda obj: ".".join([obj.__class__.__module__,
                                   obj.__class__.__name__])
make_eta = lambda dt: dt if dt.tzinfo \
    else make_aware(dt, get_current_timezone())


def gen_random_string(length, chrs=None):
    ''' generate random string

        :param length: length of generated string
        :param chrs:  character restriction
    '''

    if chrs is None:
        return os.urandom(length)
    else:
        return ''.join([chrs[random.SystemRandom().randrange(len(chrs))]
                        for _ in xrange(length)])


def gen_nonce(when=None):
    ''' generate nonce

        :param when: datetime
    '''
    NONCE_CHARS = string.ascii_letters + string.digits
    salt = gen_random_string(6, NONCE_CHARS)

    when = when if when else datetime.now()
    return when.strftime('%Y%m%d%H%M%S%f' + salt)


def create_auto_secret():
    ''' create auto secret '''
    SECRET_CHARS = string.ascii_letters + string.digits
    return gen_random_string(32, SECRET_CHARS)


def create_auto_short_secret():
    ''' create auto short secret '''
    SECRET_CHARS = string.ascii_letters + string.digits
    return gen_random_string(8, SECRET_CHARS)


def is_model(obj):
    ''' check if obj is Django model instance or not '''
    return getattr(obj, '__metaclass__', None) == ModelBase


def to_model_signature(obj):
    ''' Convert model instance into string signature '''
    if is_model(obj):
        return "_model:%s:%s:%d" % (
            obj._meta.app_label, obj._meta.module_name, obj.id)
    return obj


def from_model_signature(signature):
    ''' Conver model signature into model instance '''
    if type(signature) != str:
        return signature

    token = signature.split(':')
    if token[0] != "_model":
        return signature

    ct = ContentType.objects.get(app_label=token[1], model=token[2])
    return ct.get_object_for_this_type(id=token[3])

_template_source_loaders = ()  # Cache


def get_template_loaders(dir=None):
    global _template_source_loaders
    if _template_source_loaders is ():
        loaders = []
        for loader_name in settings.TEMPLATE_LOADERS:
            loader = find_template_loader(loader_name)
            if loader is not None:
                loaders.append(loader)
        _template_source_loaders = tuple(loaders)

    return _template_source_loaders


def get_template_source(name, dirs=None):

    for loader in get_template_loaders(dirs):
        try:
            return loader.load_template_source(name, dirs)[0]
        except TemplateDoesNotExist:
            pass
    raise TemplateDoesNotExist(name)
