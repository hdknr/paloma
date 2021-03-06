# -*- coding: utf-8 -*-
''' Django Backend Implementation
    - https://docs.djangoproject.com/en/dev/topics/email/
'''
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.backends.smtp import EmailBackend as DjangoEmailBackend
from django.core.mail.message import sanitize_address
from django.utils.translation import ugettext_lazy as _

from email.utils import parseaddr

from utils import class_path

import traceback
import logging
logger = logging.getLogger("paloma")


class PalomaEmailBackend(BaseEmailBackend):
    ''' A Django Email Backend to send emails thru Celery Task queue.
    '''
    def send_messages(self, email_messages, **kwargs):
        ''' Django Email Backend API - send_messages

            :param email_messages:
                list of django.core.mail.messages.EmailMessage instance

            - This implementation delegates STMP task to Celery worker.
        '''
        logger.debug(_('PalomaEmailBackend is used to send a message.'))
        from tasks import send_email
        results = []
        for msg in email_messages:
            results.append(send_email.delay(msg, **kwargs))
            # asynchronous send_email
        return results


class JournalEmailBackend(BaseEmailBackend):
    ''' A Django Email Backend to save email
        directly  to :ref:`paloma.models.Journal` model
    '''

    def send_messages(self, email_messages, **kwargs):
        ''' Django Email Backend API - send_messages

            :param email_messages:
                list of django.core.mail.messages.EmailMessage instance

            - https://github.com/django
              /django/blob/master/django/core/mail/message.py

        .. todo::
            - DO ERROR CHECK!!!!
            - DO ERROR TRACE!!!!
        '''
        logger.debug(_('JournalEmailBackend is used to send a message.'))
        from tasks import journalize
        try:
            sender = parseaddr(email_messages[0].from_email)[1]
            recipient = parseaddr(email_messages[0].to[0])[1]
            journalize(sender, recipient,
                       email_messages[0].message().as_string(), True)
            return 1
        except Exception:
            for err in traceback.format_exc().split('\n'):
                logger.error(err)
            return 0


class SmtpEmailBackend(DjangoEmailBackend):
    ''' handling SMTP
        (Basically django.core.mail.backends.smtp.EmailBackend)

            - return_path
            - message_id
    '''
    def _send(self, email_message):
        """A helper method that does the actual sending.

            :param email_message: EmaiMesage instance
            :type  email_message: django.core.mail.message.EmailMessage
        """

        if not email_message.recipients():
            return False

        #:Extended parameters for SMTP
        extended = getattr(email_message, "extended", {})

        from_address = sanitize_address(
            extended.get('return_path', None) or email_message.from_email,
            email_message.encoding)

        recipients = [sanitize_address(addr, email_message.encoding)
                      for addr in email_message.recipients()]

        #: Python standard email.message.Message
        mail_obj = email_message.message()

        return self.send_message_object(from_address, recipients,
                                        mail_obj, **extended)

    def send_message_object(self, from_address, recipients,
                            mail_obj, **extended):
        ''' directly send mail in Python standnard Mail instance
        '''
        logger.debug(_('SmtpEmailBackend is used to send a message.'))
        #: message_id ->Message-ID
        if extended.has_key('message_id'):
            if mail_obj.has_key('Message-ID'):
                mail_obj.replace_header('Message-ID', extended['message_id'])
            else:
                mail_obj.add_header('Message-ID', extended['message_id'])

        return self.send_message_string(
            from_address, recipients,
            mail_obj.as_string(), **extended)

    def send_message_string(self, from_address, recipients,
                            message_string, **extended):
        ''' directly send mail in string format of Python standnard Mail
        '''
        from tasks import smtp_status
        try:
            #: connection: smtplib.SMTP
            self.connection.sendmail(
                from_address, recipients, message_string)
            smtp_status.delay(class_path(self), 'OK', **extended)

        except Exception, e:
            for err in traceback.format_exc().split('\n'):
                logger.error(err)
            smtp_status.delay(class_path(self), class_path(e), **extended)
            if not self.fail_silently:
                raise
            return False
        return True
