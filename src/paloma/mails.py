# -*- coding: utf-8 -*-

#from django.core.mail import send_mail
from email import message_from_file
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
#
from django.core.mail import get_connection
from django.core.mail.message import (
    EmailMessage, SafeMIMEText,
)
from email import Charset
import uuid


import logging
logger = logging.getLogger('paloma')


def send_mail_simple(subject, text, addr_from,  addr_to):
    ''' Send simple email '''
    addr_to = addr_to if type(addr_to) == list else [addr_to]
    send_mail(subject, text, addr_from, addr_to)


def send_mail_from_file(stream, **kwargs):
    ''' Send an email from file
    '''
    if type(stream) == str:
        stream = open(stream)
    msg = message_from_file(stream)
    send_mail(msg['Subject'], str(msg),
              msg['From'], msg['To'].split(', '), **kwargs)


def send_mail(subject, message, from_email, recipient_list,
              fail_silently=False,
              auth_user=None, auth_password=None,
              connection=None, **kwargs):
    """Extended Django Sending Email Wrapper

        :param kwargs: dict extended parameter

        - return_path
        - message_id
    """
    connection = connection or get_connection(username=auth_user,
                                              password=auth_password,
                                              fail_silently=fail_silently)
    msg = EmailMessage(subject, message,
                       from_email, recipient_list,
                       connection=connection)

    msg.extended = kwargs

    msg.send()
    logger.debug(
        _('mails.send_mail:%(backend)s: sent to %(to)s from %(from)s') % {
            "backend": settings.EMAIL_BACKEND,
            "to": str(recipient_list),
            "from": str(from_email)}
    )


def create_message(
        addr_from='me@hoo.com',
        addr_to='you@bar.com',
        message_id=None,
        subject='subject',
        body='body',
        subtype='plain', encoding="utf-8"
):
    ''' Creating Message

    :rtype: SafeMIMTExt(MIMEMixin, email.mime.text.MIMETex)

    - `as_string()` method serializes into string
    '''

    message_id = message_id or uuid.uuid1().hex
    if encoding == "shift_jis":
        #: DoCoMo
        #: TODO chekck message encoding and convert it
        Charset.add_charset(
            'shift_jis', Charset.QP, Charset.BASE64, 'shift_jis')
        Charset.add_codec('shift_jis', 'cp932')

    message = SafeMIMEText(body, subtype, encoding)
    message['Subject'] = subject
    message['From'] = addr_from
    message['To'] = addr_to
    message['Message-ID'] = message_id

    return message
